# -*- coding: utf-8 -*-
"""
IAM Security - Administracion de seguridad del sistema
Firewall, usuarios, permisos, auditoria
"""

import subprocess
import platform
import os
from typing import Tuple, List, Dict, Any


class Security:
    """
    Administrador de seguridad del sistema
    """
    
    def __init__(self):
        self.is_windows = platform.system() == "Windows"
    
    def _run_powershell(self, command: str, timeout: int = 30) -> Tuple[bool, str]:
        """Ejecutar comando de PowerShell"""
        try:
            result = subprocess.run(
                ['powershell', '-Command', command],
                capture_output=True, text=True, timeout=timeout,
                encoding='utf-8', errors='replace'
            )
            return True, result.stdout if result.stdout else result.stderr
        except Exception as e:
            return False, str(e)
    
    # === FIREWALL ===
    
    def get_firewall_status(self) -> Tuple[bool, Dict]:
        """Obtener estado del firewall"""
        try:
            if self.is_windows:
                cmd = '''
                $fw = Get-NetFirewallProfile
                $fw | Select-Object Name, Enabled, DefaultInboundAction, DefaultOutboundAction |
                Format-Table -AutoSize | Out-String
                '''
                success, output = self._run_powershell(cmd)
                return success, output.strip() if success else output
            return False, "No disponible"
        except Exception as e:
            return False, str(e)
    
    def enable_firewall(self, profile: str = "all") -> Tuple[bool, str]:
        """Habilitar firewall"""
        try:
            if self.is_windows:
                if profile == "all":
                    cmd = 'Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled True'
                else:
                    cmd = f'Set-NetFirewallProfile -Profile {profile} -Enabled True'
                success, output = self._run_powershell(cmd)
                return True, f"[OK] Firewall habilitado" if success else output
            return False, "No disponible"
        except Exception as e:
            return False, str(e)
    
    def disable_firewall(self, profile: str = "all") -> Tuple[bool, str]:
        """Deshabilitar firewall"""
        try:
            if self.is_windows:
                if profile == "all":
                    cmd = 'Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled False'
                else:
                    cmd = f'Set-NetFirewallProfile -Profile {profile} -Enabled False'
                success, output = self._run_powershell(cmd)
                return True, f"[OK] Firewall deshabilitado" if success else output
            return False, "No disponible"
        except Exception as e:
            return False, str(e)
    
    def get_firewall_rules(self, direction: str = "inbound", count: int = 20) -> Tuple[bool, str]:
        """Obtener reglas del firewall"""
        try:
            if self.is_windows:
                cmd = f'''
                Get-NetFirewallRule -Direction {direction.capitalize()} -Enabled True |
                Select-Object -First {count} |
                Select-Object DisplayName, Action, Profile |
                Format-Table -AutoSize | Out-String
                '''
                success, output = self._run_powershell(cmd, timeout=60)
                return success, output.strip() if success else output
            return False, "No disponible"
        except Exception as e:
            return False, str(e)
    
    def add_firewall_rule(self, name: str, port: int, action: str = "allow",
                         direction: str = "inbound", protocol: str = "TCP") -> Tuple[bool, str]:
        """Agregar regla al firewall"""
        try:
            if self.is_windows:
                cmd = f'''
                New-NetFirewallRule -DisplayName "{name}" `
                    -Direction {direction.capitalize()} `
                    -Action {action.capitalize()} `
                    -Protocol {protocol} `
                    -LocalPort {port} `
                    -Enabled True
                '''
                success, output = self._run_powershell(cmd)
                return True, f"[OK] Regla '{name}' creada" if success else output
            return False, "No disponible"
        except Exception as e:
            return False, str(e)
    
    def remove_firewall_rule(self, name: str) -> Tuple[bool, str]:
        """Eliminar regla del firewall"""
        try:
            if self.is_windows:
                cmd = f'Remove-NetFirewallRule -DisplayName "{name}"'
                success, output = self._run_powershell(cmd)
                return True, f"[OK] Regla '{name}' eliminada" if success else output
            return False, "No disponible"
        except Exception as e:
            return False, str(e)
    
    # === USUARIOS ===
    
    def list_users(self) -> Tuple[bool, List[Dict]]:
        """Listar usuarios del sistema"""
        try:
            if self.is_windows:
                cmd = '''
                Get-LocalUser | 
                Select-Object Name, Enabled, LastLogon, PasswordRequired, PasswordLastSet |
                Format-Table -AutoSize | Out-String
                '''
                success, output = self._run_powershell(cmd)
                return success, output.strip() if success else output
            else:
                import pwd
                users = []
                for u in pwd.getpwall():
                    if u.pw_uid >= 1000:
                        users.append({
                            'name': u.pw_name,
                            'uid': u.pw_uid,
                            'home': u.pw_dir
                        })
                return True, users
        except Exception as e:
            return False, str(e)
    
    def create_user(self, username: str, password: str) -> Tuple[bool, str]:
        """Crear usuario"""
        try:
            if self.is_windows:
                cmd = f'''
                New-LocalUser -Name "{username}" `
                    -Password (ConvertTo-SecureString "{password}" -AsPlainText -Force) `
                    -FullName "{username}" `
                    -Description "Creado por IAM"
                '''
                success, output = self._run_powershell(cmd)
                return True, f"[OK] Usuario '{username}' creado" if success else output
            else:
                result = subprocess.run(
                    ['sudo', 'useradd', '-m', username],
                    capture_output=True, text=True, timeout=10
                )
                if result.returncode == 0:
                    subprocess.run(
                        ['sudo', 'passwd', username],
                        input=f"{password}\n{password}\n",
                        capture_output=True, text=True, timeout=10
                    )
                    return True, f"[OK] Usuario '{username}' creado"
                return False, result.stderr
        except Exception as e:
            return False, str(e)
    
    def delete_user(self, username: str) -> Tuple[bool, str]:
        """Eliminar usuario"""
        try:
            if self.is_windows:
                cmd = f'Remove-LocalUser -Name "{username}"'
                success, output = self._run_powershell(cmd)
                return True, f"[OK] Usuario '{username}' eliminado" if success else output
            else:
                result = subprocess.run(
                    ['sudo', 'userdel', '-r', username],
                    capture_output=True, text=True, timeout=10
                )
                return True, f"[OK] Usuario '{username}' eliminado" if result.returncode == 0 else result.stderr
        except Exception as e:
            return False, str(e)
    
    def change_password(self, username: str, new_password: str) -> Tuple[bool, str]:
        """Cambiar contrasena"""
        try:
            if self.is_windows:
                cmd = f'''
                Set-LocalUser -Name "{username}" `
                    -Password (ConvertTo-SecureString "{new_password}" -AsPlainText -Force)
                '''
                success, output = self._run_powershell(cmd)
                return True, f"[OK] Contrasena de '{username}' cambiada" if success else output
            return False, "No disponible"
        except Exception as e:
            return False, str(e)
    
    def get_user_groups(self, username: str = None) -> Tuple[bool, List[str]]:
        """Obtener grupos de un usuario - usa el usuario actual si no se especifica"""
        try:
            if username is None:
                import os
                username = os.getenv("USERNAME", os.getenv("USER", ""))
            
            if self.is_windows:
                cmd = f'''
                (Get-LocalUser -Name "{username}").PrincipalContext |
                Get-PrincipalGroup | 
                Select-Object -ExpandProperty Name
                '''
                success, output = self._run_powershell(cmd)
                if success:
                    groups = [g.strip() for g in output.strip().split('\n') if g.strip()]
                    return True, groups
                return False, output
            return False, "No disponible"
        except Exception as e:
            return False, str(e)
    
    # === GRUPOS ===
    
    def list_groups(self) -> Tuple[bool, List[str]]:
        """Listar grupos del sistema"""
        try:
            if self.is_windows:
                cmd = '''
                Get-LocalGroup | Select-Object -ExpandProperty Name
                '''
                success, output = self._run_powershell(cmd)
                if success:
                    groups = [g.strip() for g in output.strip().split('\n') if g.strip()]
                    return True, groups
                return False, output
            else:
                import grp
                return True, [g.gr_name for g in grp.getgrall() if g.gr_gid >= 1000]
        except Exception as e:
            return False, str(e)
    
    # === AUDITORIA ===
    
    def get_security_logs(self, count: int = 20) -> Tuple[bool, str]:
        """Obtener logs de seguridad"""
        try:
            if self.is_windows:
                cmd = f'''
                Get-WinEvent -LogName Security -MaxEvents {count} -ErrorAction SilentlyContinue |
                Select-Object TimeCreated, Id, LevelDisplayName, Message |
                Format-Table -AutoSize | Out-String
                '''
                success, output = self._run_powershell(cmd, timeout=60)
                return success, output.strip() if success else output
            return False, "No disponible"
        except Exception as e:
            return False, str(e)
    
    def get_system_logs(self, count: int = 20) -> Tuple[bool, str]:
        """Obtener logs del sistema"""
        try:
            if self.is_windows:
                cmd = f'''
                Get-WinEvent -LogName System -MaxEvents {count} -ErrorAction SilentlyContinue |
                Select-Object TimeCreated, Id, LevelDisplayName, Message |
                Format-Table -AutoSize | Out-String
                '''
                success, output = self._run_powershell(cmd, timeout=60)
                return success, output.strip() if success else output
            return False, "No disponible"
        except Exception as e:
            return False, str(e)
    
    def get_application_logs(self, count: int = 20) -> Tuple[bool, str]:
        """Obtener logs de aplicaciones"""
        try:
            if self.is_windows:
                cmd = f'''
                Get-WinEvent -LogName Application -MaxEvents {count} -ErrorAction SilentlyContinue |
                Select-Object TimeCreated, Id, LevelDisplayName, Message |
                Format-Table -AutoSize | Out-String
                '''
                success, output = self._run_powershell(cmd, timeout=60)
                return success, output.strip() if success else output
            return False, "No disponible"
        except Exception as e:
            return False, str(e)
    
    # === CONTRASENAS ===
    
    def check_password_policy(self) -> Tuple[bool, Dict]:
        """Verificar politica de contrasenas"""
        try:
            if self.is_windows:
                cmd = '''
                net accounts | Out-String
                '''
                success, output = self._run_powershell(cmd)
                return success, output.strip() if success else output
            return False, "No disponible"
        except Exception as e:
            return False, str(e)
    
    # === SERVICES ===
    
    def get_privileged_services(self) -> Tuple[bool, str]:
        """Obtener servicios con privilegios elevados"""
        try:
            if self.is_windows:
                cmd = '''
                Get-CimInstance -ClassName Win32_Service |
                Where-Object { $_.StartMode -eq "Auto" -and $_.State -eq "Running" } |
                Select-Object Name, DisplayName, StartName, State |
                Format-Table -AutoSize | Out-String
                '''
                success, output = self._run_powershell(cmd, timeout=60)
                return success, output.strip() if success else output
            return False, "No disponible"
        except Exception as e:
            return False, str(e)
    
    # === CERTIFICADOS ===
    
    def get_certificates(self, store: str = "LocalMachine") -> Tuple[bool, str]:
        """Obtener certificados SSL"""
        try:
            if self.is_windows:
                cmd = f'''
                Get-ChildItem -Path "Cert:\\{store}\\My" -ErrorAction SilentlyContinue |
                Select-Object Subject, Issuer, NotAfter, Thumbprint |
                Format-Table -AutoSize | Out-String
                '''
                success, output = self._run_powershell(cmd)
                return success, output.strip() if success else output
            return False, "No disponible"
        except Exception as e:
            return False, str(e)


# Instancia global
security = Security()
