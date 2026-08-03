# -*- coding: utf-8 -*-
"""
IAM Permissions - Sistema de permisos para acciones sensibles
Pide confirmación antes de ejecutar comandos, modificar archivos, etc.
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass, asdict
from enum import Enum


class PermissionAction(Enum):
    """Acciones que requieren permiso"""
    EXECUTE_COMMAND = "execute_command"
    MODIFY_FILE = "modify_file"
    DELETE_FILE = "delete_file"
    NETWORK_ACCESS = "network_access"
    INSTALL_PACKAGE = "install_package"
    SYSTEM_CHANGE = "system_change"
    READ_SENSITIVE = "read_sensitive"


class PermissionLevel(Enum):
    """Niveles de permiso"""
    ASK = "ask"           # Siempre preguntar
    ALLOW = "allow"       # Permitir esta vez
    DENY = "deny"         # Denegar esta vez
    ALWAYS_ALLOW = "always_allow"  # Siempre permitir (guardado)
    ALWAYS_DENY = "always_deny"    # Siempre denegar (guardado)


@dataclass
class PermissionRequest:
    """Solicitud de permiso"""
    action: PermissionAction
    target: str
    description: str
    risk_level: str = "low"  # low, medium, high, critical
    details: Dict[str, Any] = None


@dataclass
class PermissionRule:
    """Regla de permiso guardada"""
    action: str
    pattern: str  # patron o nombre del recurso
    level: str    # always_allow, always_deny
    created_at: str = None
    expires_at: str = None  # opcional: expiracion
    
    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()


class PermissionSystem:
    """
    Sistema de permisos para IAM
    Controla el acceso a acciones sensibles
    Inspirado en opencode: banned commands, safe commands, read-before-edit
    """
    
    def __init__(self):
        self.rules_file = Path(__file__).parent.parent / "data" / "permission_rules.json"
        self.rules: Dict[str, PermissionRule] = {}
        self._load_rules()
        
        # Tracking de archivos leidos (para read-before-edit)
        self.read_files: Dict[str, str] = {}  # path -> checksum
        self.file_checksums: Dict[str, str] = {}  # path -> last checksum
        
        # Comandos prohibidos (inspirado en opencode) - NUNCA se ejecutan
        self.banned_commands = [
            "curl", "wget", "nc", "netcat", "telnet", "ssh", "scp", "rsync",
            "firefox", "chrome", "edge", "iexplore", "opera",
            "rm -rf /", "rm -rf /*", "rmdir /s /q", "format c:",
            "dd if=", "mkfs", "> /dev/sda",
            "chmod 777", "chown root",
            "sudo rm", "sudo chmod", "sudo chown",
            ":(){ :|:& };:", "fork bomb",
            "reg delete HKLM", "reg delete HKCU",
        ]
        
        # Comandos seguros de solo lectura (no requieren permiso)
        self.safe_read_commands = [
            "ls", "dir", "pwd", "cd", "echo", "cat", "type",
            "git status", "git log", "git diff", "git show",
            "git branch", "git remote", "git stash list",
            "python --version", "node --version", "npm --version",
            "pip list", "npm list",
            "whoami", "hostname", "date", "time",
            "tree", "find", "where", "which",
            "head", "tail", "wc", "grep", "findstr",
        ]
        
        # Patrones de alto riesgo
        self.high_risk_commands = [
            "rm -rf", "rmdir /s", "format", "del /f", "del /q",
            "shutdown", "restart", "taskkill", "net user", "net localgroup",
            "reg delete", "reg add", "icacls", "takeown", "cipher",
            "diskpart", "bcdedit", "gpupdate", "secedit"
        ]
        
        self.medium_risk_commands = [
            "pip install", "npm install", "apt install", "yum install",
            "git push", "git commit", "git merge",
            "python", "node", "npm run", "yarn"
        ]
        
        # Patrones de archivos sensibles
        self.sensitive_patterns = [
            ".env", ".env.local", ".env.production",
            "id_rsa", "id_ed25519", "*.pem", "*.key",
            "password", "secret", "token", "credential",
            "config.json", "settings.json", "database.yml"
        ]
    
    def _load_rules(self):
        """Cargar reglas guardadas"""
        if self.rules_file.exists():
            try:
                with open(self.rules_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                for key, value in data.get("rules", {}).items():
                    self.rules[key] = PermissionRule(**value)
            except Exception:
                self.rules = {}
    
    def _save_rules(self):
        """Guardar reglas"""
        self.rules_file.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "rules": {k: asdict(v) for k, v in self.rules.items()},
            "last_updated": datetime.now().isoformat()
        }
        try:
            with open(self.rules_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception:
            pass
    
    def _get_rule_key(self, action: PermissionAction, target: str) -> str:
        """Generar clave para regla"""
        return f"{action.value}:{target}"
    
    def check_permission(self, request: PermissionRequest) -> Tuple[bool, str]:
        """
        Verificar si ya existe permiso guardado
        Retorna: (tiene_permiso, nivel_permiso)
        """
        # Buscar regla exacta
        key = self._get_rule_key(request.action, request.target)
        if key in self.rules:
            rule = self.rules[key]
            if rule.level == "always_allow":
                return True, "always_allow"
            elif rule.level == "always_deny":
                return False, "always_deny"
        
        # Buscar regla por patron
        for rule_key, rule in self.rules.items():
            if rule.action == request.action.value:
                if self._match_pattern(request.target, rule.pattern):
                    if rule.level == "always_allow":
                        return True, "always_allow"
                    elif rule.level == "always_deny":
                        return False, "always_deny"
        
        # No hay regla, hay que preguntar
        return None, "ask"
    
    def _match_pattern(self, target: str, pattern: str) -> bool:
        """Verificar si target coincide con patron"""
        if "*" in pattern:
            import fnmatch
            return fnmatch.fnmatch(target.lower(), pattern.lower())
        return target.lower() == pattern.lower()
    
    def save_permission(self, action: PermissionAction, target: str, level: str):
        """Guardar permiso"""
        key = self._get_rule_key(action, target)
        self.rules[key] = PermissionRule(
            action=action.value,
            pattern=target,
            level=level
        )
        self._save_rules()
    
    def remove_permission(self, action: PermissionAction, target: str):
        """Eliminar permiso"""
        key = self._get_rule_key(action, target)
        if key in self.rules:
            del self.rules[key]
            self._save_rules()
    
    def clear_all_permissions(self):
        """Eliminar todas las reglas"""
        self.rules.clear()
        self._save_rules()
    
    def get_saved_permissions(self) -> list:
        """Obtener permisos guardados"""
        return [
            {
                "action": r.action,
                "pattern": r.pattern,
                "level": r.level,
                "created": r.created_at
            }
            for r in self.rules.values()
        ]
    
    def assess_risk(self, command: str) -> str:
        """Evaluar riesgo de un comando"""
        cmd_lower = command.lower()
        
        # Alto riesgo
        for risk_cmd in self.high_risk_commands:
            if risk_cmd in cmd_lower:
                return "high"
        
        # Riesgo medio
        for risk_cmd in self.medium_risk_commands:
            if risk_cmd in cmd_lower:
                return "medium"
        
        # Verificar si es comando del sistema
        system_cmds = ["cmd", "powershell", "bash", "sh", "wsl"]
        if any(cmd_lower.startswith(sys) for sys in system_cmds):
            return "medium"
        
        return "low"
    
    def is_sensitive_file(self, filepath: str) -> bool:
        """Verificar si es archivo sensible"""
        filename = os.path.basename(filepath).lower()
        
        for pattern in self.sensitive_patterns:
            if "*" in pattern:
                import fnmatch
                if fnmatch.fnmatch(filename, pattern):
                    return True
            elif pattern in filename:
                return True
        
        return False
    
    def format_permission_dialog(self, request: PermissionRequest) -> str:
        """Formatear diálogo de permiso con estilo recuadro"""
        risk_icons = {
            "low": "🔒",
            "medium": "⚠️",
            "high": "🚨",
            "critical": "💀"
        }
        
        risk_colors = {
            "low": "36",      # Cyan
            "medium": "33",   # Yellow
            "high": "31",     # Red
            "critical": "35"  # Magenta
        }
        
        icon = risk_icons.get(request.risk_level, "❓")
        color = risk_colors.get(request.risk_level, "37")
        
        # Truncar target si es muy largo
        target_display = request.target[:40] + "..." if len(request.target) > 40 else request.target
        
        dialog = f"""
  ╭────────────────────────────────────────────────────────────╮
  │  {icon}  \033[{color}mSOLICITUD DE PERMISO\033[0m                                    
  ├────────────────────────────────────────────────────────────┤
  │                                                            │
  │  \033[90mAccion:\033[0m     {request.action.value:<20}                
  │  \033[90mObjetivo:\033[0m   {target_display:<20}                
  │  \033[90mRiesgo:\033[0m     \033[{color}m{request.risk_level.upper()}\033[0m                          
  │                                                            │
  ├────────────────────────────────────────────────────────────┤
  │                                                            │
  │    \033[32m[1]\033[0m Si         Permitir una vez                      
  │    \033[31m[2]\033[0m No         Denegar esta vez                      
  │    \033[33m[3]\033[0m Siempre    Guardar permiso                       
  │    \033[90m[4]\033[0m Cancelar   Cancelar operacion                   
  │                                                            │
  ╰────────────────────────────────────────────────────────────╯"""
        return dialog
    
    def format_permissions_list(self) -> str:
        """Formatear lista de permisos guardados"""
        if not self.rules:
            return "No hay permisos guardados."
        
        output = ["PERMISOS GUARDADOS:\n"]
        
        for key, rule in self.rules.items():
            icon = "[OK]" if rule.level == "always_allow" else "[X]"
            output.append(f"  {icon} {rule.action}: {rule.pattern}")
            output.append(f"      Nivel: {rule.level}")
        
        return "\n".join(output)
    
    # ==================== NUEVOS METODOS (inspirados en opencode) ====================
    
    def is_banned_command(self, command: str) -> bool:
        """Verificar si un comando esta prohibido (NUNCA se ejecuta)"""
        cmd_lower = command.lower().strip()
        
        for banned in self.banned_commands:
            if cmd_lower.startswith(banned) or banned in cmd_lower:
                return True
        
        return False
    
    def is_safe_read_command(self, command: str) -> bool:
        """Verificar si un comando es seguro de solo lectura (no requiere permiso)"""
        cmd_lower = command.lower().strip()
        
        for safe in self.safe_read_commands:
            if cmd_lower.startswith(safe):
                return True
        
        return False
    
    def track_file_read(self, filepath: str, checksum: str = None):
        """Registrar que un archivo fue leido (para read-before-edit)"""
        abs_path = os.path.abspath(filepath)
        self.read_files[abs_path] = checksum or datetime.now().isoformat()
    
    def track_file_write(self, filepath: str, checksum: str = None):
        """Registrar que un archivo fue escrito/modificado"""
        abs_path = os.path.abspath(filepath)
        self.file_checksums[abs_path] = checksum or datetime.now().isoformat()
    
    def was_file_read(self, filepath: str) -> bool:
        """Verificar si un archivo fue leido antes de editarlo"""
        abs_path = os.path.abspath(filepath)
        return abs_path in self.read_files
    
    def has_file_changed(self, filepath: str, current_checksum: str) -> bool:
        """Verificar si un archivo cambio desde la ultima lectura"""
        abs_path = os.path.abspath(filepath)
        
        if abs_path not in self.file_checksums:
            return False  # No tenemos registro, asumir que no cambio
        
        return self.file_checksums[abs_path] != current_checksum
    
    def check_edit_permission(self, filepath: str) -> Tuple[bool, str]:
        """
        Verificar permiso para editar archivo (read-before-edit)
        Retorna: (puede_editar, razon)
        """
        abs_path = os.path.abspath(filepath)
        
        # Verificar si es archivo sensible
        if self.is_sensitive_file(abs_path):
            return False, "Archivo sensible - requiere permiso especial"
        
        # Verificar si fue leido
        if not self.was_file_read(abs_path):
            return False, "El archivo no ha sido leido - lee el archivo primero"
        
        return True, "Permiso concedido"
    
    def get_security_report(self) -> str:
        """Obtener reporte de seguridad"""
        lines = [
            "REPORTE DE SEGURIDAD",
            "=" * 50,
            "",
            f"Comandos prohibidos: {len(self.banned_commands)}",
            f"Comandos seguros: {len(self.safe_read_commands)}",
            f"Archivos sensibles: {len(self.sensitive_patterns)}",
            f"Permisos guardados: {len(self.rules)}",
            f"Archivos trackeados: {len(self.read_files)}",
            "",
            "COMANDOS PROHIBIDOS (no se ejecutan nunca):",
        ]
        
        for cmd in self.banned_commands[:10]:
            lines.append(f"  - {cmd}")
        
        lines.append("")
        lines.append("COMANDOS SEGUROS (sin permiso):")
        for cmd in self.safe_read_commands[:10]:
            lines.append(f"  - {cmd}")
        
        return "\n".join(lines)


# Instancia global
permission_system = PermissionSystem()


def request_permission(action: PermissionAction, target: str, 
                      description: str, risk_level: str = "low") -> bool:
    """
    Funcion principal para solicitar permiso
    Retorna True si se permite, False si se deniega
    """
    request = PermissionRequest(
        action=action,
        target=target,
        description=description,
        risk_level=risk_level
    )
    
    # Verificar si ya hay permiso guardado
    has_permission, level = permission_system.check_permission(request)
    
    if has_permission is not None:
        return has_permission
    
    # No hay permiso guardado, mostrar dialogo
    print(permission_system.format_permission_dialog(request))
    
    # Leer input del usuario
    while True:
        try:
            response = input("\n  Tu respuesta: ").strip().lower()
            
            if response in ["1", "si", "s", "yes", "y"]:
                print("  \033[32m✓ Permiso otorgado\033[0m")
                return True
            elif response in ["2", "no", "n"]:
                print("  \033[31m✗ Permiso denegado\033[0m")
                return False
            elif response in ["3", "siempre", "always", "all"]:
                permission_system.save_permission(action, target, "always_allow")
                print(f"  \033[33m✓ Permiso guardado para siempre\033[0m")
                return True
            elif response in ["4", "cancelar", "cancel", "c"]:
                print("  \033[90m✗ Operacion cancelada\033[0m")
                return False
            else:
                print("  \033[31mRespuesta invalida. Usa: 1, 2, 3 o 4\033[0m")
        except (EOFError, KeyboardInterrupt):
            return False


def require_permission(action: PermissionAction, target: str,
                      description: str, risk_level: str = "low",
                      fallback: bool = False) -> Tuple[bool, str]:
    """
    Requiere permiso y retorna resultado con mensaje
    """
    request = PermissionRequest(
        action=action,
        target=target,
        description=description,
        risk_level=risk_level
    )
    
    # Verificar si ya hay permiso guardado
    has_permission, level = permission_system.check_permission(request)
    
    if has_permission is not None:
        return has_permission, f"Permiso {level}"
    
    # Mostrar dialogo
    print(permission_system.format_permission_dialog(request))
    
    while True:
        try:
            response = input("\n  Tu respuesta: ").strip().lower()
            
            if response in ["1", "si", "s", "yes", "y"]:
                print("  \033[32m✓ Permiso otorgado\033[0m")
                return True, "Permiso otorgado"
            elif response in ["2", "no", "n"]:
                print("  \033[31m✗ Permiso denegado\033[0m")
                return False, "Permiso denegado"
            elif response in ["3", "siempre", "always", "all"]:
                permission_system.save_permission(action, target, "always_allow")
                print("  \033[33m✓ Permiso guardado para siempre\033[0m")
                return True, "Permiso guardado para siempre"
            elif response in ["4", "cancelar", "cancel", "c"]:
                print("  \033[90m✗ Operacion cancelada\033[0m")
                return False, "Operacion cancelada"
            else:
                print("  \033[31mRespuesta invalida. Usa: 1, 2, 3 o 4\033[0m")
        except (EOFError, KeyboardInterrupt):
            return fallback, "Permiso por defecto"
