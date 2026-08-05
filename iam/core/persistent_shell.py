# -*- coding: utf-8 -*-
"""
IAM Persistent Shell - Shell que mantiene estado entre comandos
IAM: shell persistente con command queue
"""

import os
import subprocess
import threading
import tempfile
import time
from typing import Optional, Tuple, Dict, Any
from dataclasses import dataclass, field
from pathlib import Path
import queue


@dataclass
class CommandResult:
    """Resultado de un comando"""
    stdout: str
    stderr: str
    exit_code: int
    interrupted: bool = False
    duration_ms: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "stdout": self.stdout,
            "stderr": self.stderr,
            "exit_code": self.exit_code,
            "interrupted": self.interrupted,
            "duration_ms": self.duration_ms
        }


class PersistentShell:
    """
    Shell persistente que mantiene estado entre comandos
    IAM: mantiene directorio de trabajo y variables de entorno
    """
    
    _instances: Dict[str, 'PersistentShell'] = {}
    _lock = threading.Lock()
    
    def __new__(cls, working_dir: str = None):
        """Singleton por directorio de trabajo"""
        working_dir = working_dir or os.getcwd()
        
        with cls._lock:
            if working_dir not in cls._instances:
                instance = super().__new__(cls)
                instance._initialized = False
                cls._instances[working_dir] = instance
            return cls._instances[working_dir]
    
    def __init__(self, working_dir: str = None):
        if self._initialized:
            return
        
        self._initialized = True
        self.working_dir = working_dir or os.getcwd()
        self._env = os.environ.copy()
        self._command_history: list = []
        self._lock = threading.RLock()
        self._last_command_time = 0
        self._command_count = 0
    
    @classmethod
    def get_instance(cls, working_dir: str = None) -> 'PersistentShell':
        """Obtener instancia del shell"""
        return cls(working_dir)
    
    def exec(self, command: str,         timeout: int = 30, 
             cwd: str = None) -> CommandResult:
        """
        Ejecutar comando en el shell persistente
        
        Args:
            command: Comando a ejecutar
            timeout: Timeout en segundos
            cwd: Directorio de trabajo (override)
        
        Returns:
            CommandResult con stdout, stderr, exit_code
        """
        start_time = time.time()
        exec_dir = cwd or self.working_dir
        
        with self._lock:
            self._command_history.append({
                "command": command,
                "cwd": exec_dir,
                "timestamp": time.time()
            })
            self._command_count += 1
        
        try:
            # Detectar shell apropiado
            if os.name == 'nt':  # Windows
                shell_cmd = ['cmd', '/c', command]
            else:
                shell_cmd = ['bash', '-c', command]
            
            # Ejecutar con timeout
            result = subprocess.run(
                shell_cmd,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=exec_dir,
                env=self._env,
                encoding='utf-8',
                errors='replace'
            )
            
            duration_ms = int((time.time() - start_time) * 1000)
            
            # Actualizar directorio de trabajo si es cd
            if command.strip().startswith('cd '):
                new_dir = command.strip()[3:].strip().strip('"').strip("'")
                if os.path.isdir(new_dir):
                    self.working_dir = os.path.abspath(new_dir)
            
            return CommandResult(
                stdout=result.stdout,
                stderr=result.stderr,
                exit_code=result.returncode,
                duration_ms=duration_ms
            )
            
        except subprocess.TimeoutExpired:
            duration_ms = int((time.time() - start_time) * 1000)
            return CommandResult(
                stdout="",
                stderr=f"Command timed out after {timeout}s",
                exit_code=-1,
                interrupted=True,
                duration_ms=duration_ms
            )
        except Exception as e:
            duration_ms = int((time.time() - start_time) * 1000)
            return CommandResult(
                stdout="",
                stderr=str(e),
                exit_code=-1,
                duration_ms=duration_ms
            )
    
    def exec_background(self, command: str, cwd: str = None) -> subprocess.Popen:
        """
        Ejecutar comando en background
        Retorna el proceso para monitorear
        """
        exec_dir = cwd or self.working_dir
        
        if os.name == 'nt':
            shell_cmd = ['cmd', '/c', command]
        else:
            shell_cmd = ['bash', '-c', command]
        
        return subprocess.Popen(
            shell_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=exec_dir,
            env=self._env
        )
    
    def set_env(self, key: str, value: str):
        """Establecer variable de entorno"""
        with self._lock:
            self._env[key] = value
    
    def get_env(self, key: str, default: str = None) -> Optional[str]:
        """Obtener variable de entorno"""
        return self._env.get(key, default)
    
    def get_cwd(self) -> str:
        """Obtener directorio de trabajo actual"""
        return self.working_dir
    
    def get_history(self, limit: int = 50) -> list:
        """Obtener historial de comandos"""
        return self._command_history[-limit:]
    
    def get_stats(self) -> Dict[str, Any]:
        """Obtener estadisticas del shell"""
        return {
            "working_dir": self.working_dir,
            "command_count": self._command_count,
            "history_size": len(self._command_history),
            "last_command": self._command_history[-1] if self._command_history else None
        }
    
    def clear_history(self):
        """Limpiar historial"""
        self._command_history.clear()
    
    def reset(self):
        """Resetear shell a estado inicial"""
        self.working_dir = os.getcwd()
        self._env = os.environ.copy()
        self._command_history.clear()
        self._command_count = 0


# ==================== FUNCIONES DE UTILIDAD ====================

def get_shell(working_dir: str = None) -> PersistentShell:
    """Obtener shell persistente"""
    return PersistentShell.get_instance(working_dir)


def run_command(command: str,         timeout: int = 30, cwd: str = None) -> CommandResult:
    """Ejecutar comando rapidamente"""
    shell = get_shell(cwd)
    return shell.exec(command, timeout=timeout)


def run_command_safe(command: str,         timeout: int = 30, cwd: str = None) -> Tuple[bool, str]:
    """
    Ejecutar comando de forma segura
    Retorna: (exito, salida)
    """
    result = run_command(command, timeout=timeout, cwd=cwd)
    
    if result.exit_code == 0:
        return True, result.stdout
    else:
        error = result.stderr or result.stdout
        return False, error


# ==================== SHELL PERSISTENTE WINDOWS ====================

class WindowsPersistentShell(PersistentShell):
    """Shell persistente para Windows que mantiene estado"""
    
    def __init__(self, working_dir: str = None):
        super().__init__(working_dir)
        if os.name == 'nt':
            # Windows: usar PowerShell para mejor compatibilidad
            self._shell_type = 'powershell'
        else:
            self._shell_type = 'bash'
    
    def exec(self, command: str,         timeout: int = 30, 
             cwd: str = None) -> CommandResult:
        """Ejecutar comando con soporte Windows"""
        start_time = time.time()
        exec_dir = cwd or self.working_dir
        
        try:
            if os.name == 'nt':
                # PowerShell para Windows
                result = subprocess.run(
                    ['powershell', '-Command', command],
                    capture_output=True,
                    text=True,
                    timeout=timeout,
                    cwd=exec_dir,
                    env=self._env,
                    encoding='utf-8',
                    errors='replace'
                )
            else:
                result = subprocess.run(
                    ['bash', '-c', command],
                    capture_output=True,
                    text=True,
                    timeout=timeout,
                    cwd=exec_dir,
                    env=self._env,
                    encoding='utf-8',
                    errors='replace'
                )
            
            duration_ms = int((time.time() - start_time) * 1000)
            
            # Actualizar directorio de trabajo
            if command.strip().startswith('cd '):
                new_dir = command.strip()[3:].strip().strip('"').strip("'")
                full_path = os.path.join(exec_dir, new_dir) if not os.path.isabs(new_dir) else new_dir
                if os.path.isdir(full_path):
                    self.working_dir = os.path.abspath(full_path)
            
            return CommandResult(
                stdout=result.stdout,
                stderr=result.stderr,
                exit_code=result.returncode,
                duration_ms=duration_ms
            )
            
        except subprocess.TimeoutExpired:
            return CommandResult(
                stdout="",
                stderr=f"Timeout after {timeout}s",
                exit_code=-1,
                interrupted=True
            )
        except Exception as e:
            return CommandResult(
                stdout="",
                stderr=str(e),
                exit_code=-1
            )


# Instancia global
_shell: Optional[PersistentShell] = None


def get_global_shell() -> PersistentShell:
    """Obtener shell global"""
    global _shell
    if _shell is None:
        if os.name == 'nt':
            _shell = WindowsPersistentShell()
        else:
            _shell = PersistentShell()
    return _shell
