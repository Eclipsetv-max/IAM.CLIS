# -*- coding: utf-8 -*-
"""
IAM Process - Gestion completa de procesos
Crear, eliminar, monitorear, priorizar, inyectar, etc.
"""

import subprocess
import platform
import os
import signal
import time
from typing import Tuple, List, Dict, Any


class ProcessManager:
    """
    Gestion completa de procesos del sistema
    """
    
    def __init__(self):
        self.is_windows = platform.system() == "Windows"
        self.is_linux = platform.system() == "Linux"
    
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
    
    def _run_command(self, cmd: List[str], timeout: int = 30) -> Tuple[bool, str]:
        """Ejecutar comando del sistema"""
        try:
            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=timeout,
                encoding='utf-8', errors='replace'
            )
            return True, result.stdout if result.stdout else result.stderr
        except Exception as e:
            return False, str(e)
    
    # === LISTAR PROCESOS ===
    
    def list_processes(self, sort_by: str = "cpu", count: int = 50) -> Tuple[bool, List[Dict]]:
        """Listar procesos en ejecucion"""
        try:
            if self.is_windows:
                cmd = f'tasklist /FO CSV /NH'
                success, output = self._run_command(['tasklist', '/FO', 'CSV', '/NH'], timeout=30)
                if success:
                    # Parse CSV output
                    processes = []
                    for line in output.strip().split('\n'):
                        parts = line.strip().split('","')
                        if len(parts) >= 5:
                            name = parts[0].strip('"')
                            pid = parts[1].strip('"')
                            mem = parts[4].strip('"')
                            processes.append({'name': name, 'pid': pid, 'memory': mem})
                    return True, processes[:count]
                return success, output
            else:
                cmd = ['ps', 'aux', '--sort=-pcpu']
                success, output = self._run_command(cmd)
                return success, output if success else output
        except Exception as e:
            return False, str(e)
    
    def get_process_info(self, pid: int = None, name: str = None) -> Tuple[bool, Dict]:
        """Obtener informacion detallada de un proceso"""
        try:
            if self.is_windows:
                if pid:
                    cmd = f'''
                    Get-Process -Id {pid} | 
                    Select-Object Id, ProcessName, Path, CPU, WorkingSet64, HandleCount,
                    Threads, StartTime, Responding, PriorityClass |
                    Format-List | Out-String
                    '''
                elif name:
                    cmd = f'''
                    Get-Process -Name "{name}" | 
                    Select-Object Id, ProcessName, Path, CPU, WorkingSet64, HandleCount,
                    Threads, StartTime, Responding, PriorityClass |
                    Format-List | Out-String
                    '''
                else:
                    return False, "Se requiere PID o nombre"
                
                success, output = self._run_powershell(cmd)
                return success, output.strip() if success else output
            return False, "No disponible"
        except Exception as e:
            return False, str(e)
    
    # === BUSCAR PROCESOS ===
    
    def search_process(self, query: str) -> Tuple[bool, List[Dict]]:
        """Buscar procesos por nombre"""
        try:
            if self.is_windows:
                cmd = f'''
                Get-Process | Where-Object {{ $_.ProcessName -like "*{query}*" }} |
                Select-Object Id, ProcessName, CPU,
                @{{"N='MemoryMB';E={{[math]::Round($_.WorkingSet64/1MB,1)}}}} |
                Format-Table -AutoSize | Out-String
                '''
                success, output = self._run_powershell(cmd)
                return success, output.strip() if success else output
            else:
                cmd = ['pgrep', '-f', query]
                success, output = self._run_command(cmd)
                return success, output if success else output
        except Exception as e:
            return False, str(e)
    
    def find_process_by_port(self, port: int) -> Tuple[bool, Dict]:
        """Encontrar proceso que usa un puerto"""
        try:
            if self.is_windows:
                cmd = f'''
                $net = netstat -ano | Select-String ":{port} "
                $net | ForEach-Object {{
                    $pid = ($_ -split '\\s+')[-1]
                    $process = Get-Process -Id $pid -ErrorAction SilentlyContinue
                    if ($process) {{
                        [PSCustomObject]@{{
                            Port = {port}
                            PID = $pid
                            Name = $process.ProcessName
                            Path = $process.Path
                        }}
                    }}
                }} | Format-Table -AutoSize | Out-String
                '''
                success, output = self._run_powershell(cmd)
                return success, output.strip() if success else output
            return False, "No disponible"
        except Exception as e:
            return False, str(e)
    
    # === MATAR PROCESOS ===
    
    def kill_process(self, pid: int = None, name: str = None, force: bool = False) -> Tuple[bool, str]:
        """Matar un proceso"""
        try:
            if self.is_windows:
                if pid:
                    cmd = f'taskkill /PID {pid} {"/F" if force else ""}'
                elif name:
                    cmd = f'taskkill /IM {name}.exe {"/F" if force else ""}'
                else:
                    return False, "Se requiere PID o nombre"
                
                success, output = self._run_command(cmd.split())
                return True, f"[OK] Proceso terminado" if success else output
            else:
                if pid:
                    if force:
                        os.kill(pid, signal.SIGKILL)
                    else:
                        os.kill(pid, signal.SIGTERM)
                    return True, f"[OK] Proceso {pid} terminado"
                return False, "Se requiere PID"
        except Exception as e:
            return False, str(e)
    
    def kill_all_by_name(self, name: str) -> Tuple[bool, str]:
        """Matar todos los procesos con un nombre"""
        try:
            if self.is_windows:
                cmd = f'taskkill /IM {name}.exe /F'
                success, output = self._run_command(cmd.split())
                return True, f"[OK] Todos los procesos {name} terminados" if success else output
            return False, "No disponible"
        except Exception as e:
            return False, str(e)
    
    # === CREAR PROCESOS ===
    
    def start_process(self, command: str, wait: bool = False) -> Tuple[bool, str]:
        """Iniciar un proceso"""
        try:
            if wait:
                success, output = self._run_command(command.split(), timeout=300)
                return success, output
            else:
                proc = subprocess.Popen(
                    command, shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                return True, f"[OK] Proceso iniciado PID: {proc.pid}"
        except Exception as e:
            return False, str(e)
    
    def start_background(self, command: str) -> Tuple[bool, str]:
        """Iniciar proceso en background"""
        try:
            if self.is_windows:
                cmd = f'Start-Process -WindowStyle Hidden -FilePath "{command}"'
                success, output = self._run_powershell(cmd)
                return True, f"[OK] Proceso iniciado en background" if success else output
            else:
                proc = subprocess.Popen(
                    command, shell=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    start_new_session=True
                )
                return True, f"[OK] Proceso iniciado en background PID: {proc.pid}"
        except Exception as e:
            return False, str(e)
    
    # === MONITOREAR ===
    
    def monitor_process(self, pid: int, duration: int = 10) -> Tuple[bool, Dict]:
        """Monitorear un proceso por un tiempo"""
        try:
            samples = []
            start_time = time.time()
            
            while time.time() - start_time < duration:
                if self.is_windows:
                    cmd = f'''
                    $proc = Get-Process -Id {pid} -ErrorAction SilentlyContinue
                    if ($proc) {{
                        [PSCustomObject]@{{
                            Time = Get-Date -Format "HH:mm:ss"
                            CPU = $proc.CPU
                            MemoryMB = [math]::Round($proc.WorkingSet64/1MB,1)
                            Handles = $proc.HandleCount
                            Threads = $proc.Threads.Count
                        }}
                    }}
                    '''
                    success, output = self._run_powershell(cmd)
                    if success and output.strip():
                        samples.append(output.strip())
                
                time.sleep(1)
            
            return True, samples
        except Exception as e:
            return False, str(e)
    
    def get_top_processes(self, metric: str = "cpu", count: int = 10) -> Tuple[bool, str]:
        """Obtener top procesos por metrica"""
        try:
            if self.is_windows:
                if metric == "cpu":
                    sort = "CPU"
                elif metric == "memory":
                    sort = "WorkingSet64"
                elif metric == "handles":
                    sort = "HandleCount"
                else:
                    sort = "CPU"
                
                cmd = f'''
                Get-Process | 
                Sort-Object -Property {sort} -Descending |
                Select-Object -First {count} Id, ProcessName, CPU,
                @{{"N='MemoryMB';E={{[math]::Round($_.WorkingSet64/1MB,1)}}}},
                HandleCount |
                Format-Table -AutoSize | Out-String
                '''
                success, output = self._run_powershell(cmd)
                return success, output.strip() if success else output
            return False, "No disponible"
        except Exception as e:
            return False, str(e)
    
    # === SERVICIOS COMO PROCESOS ===
    
    def get_services_running(self) -> Tuple[bool, str]:
        """Obtener servicios que estan corriendo como procesos"""
        try:
            if self.is_windows:
                cmd = '''
                Get-Service | Where-Object { $_.Status -eq "Running" } |
                Select-Object Name, DisplayName, Status |
                Format-Table -AutoSize | Out-String
                '''
                success, output = self._run_powershell(cmd, timeout=60)
                return success, output.strip() if success else output
            return False, "No disponible"
        except Exception as e:
            return False, str(e)
    
    # === PROCESOS POR USUARIO ===
    
    def get_processes_by_user(self, username: str = None) -> Tuple[bool, str]:
        """Obtener procesos de un usuario - usa el usuario actual si no se especifica"""
        try:
            if username is None:
                import os
                username = os.getenv("USERNAME", os.getenv("USER", ""))
            
            if self.is_windows:
                cmd = f'''
                Get-Process | Where-Object {{ $_.Path -and (Get-ProcessOwner $_.Id) -eq "{username}" }} |
                Select-Object Id, ProcessName, CPU |
                Format-Table -AutoSize | Out-String
                '''
                success, output = self._run_powershell(cmd)
                return success, output.strip() if success else output
            return False, "No disponible"
        except Exception as e:
            return False, str(e)
    
    # === DEPENDENCIAS ===
    
    def get_process_dependencies(self, pid: int) -> Tuple[bool, str]:
        """Obtener dependencias DLL de un proceso"""
        try:
            if self.is_windows:
                cmd = f'''
                (Get-Process -Id {pid}).Modules | 
                Select-Object ModuleName, FileName |
                Format-Table -AutoSize | Out-String
                '''
                success, output = self._run_powershell(cmd)
                return success, output.strip() if success else output
            return False, "No disponible"
        except Exception as e:
            return False, str(e)
    
    # === PRIORIDAD ===
    
    def set_process_priority(self, pid: int, priority: str = "normal") -> Tuple[bool, str]:
        """Cambiar prioridad de un proceso"""
        try:
            priority_map = {
                "low": "BelowNormal",
                "normal": "Normal",
                "high": "High",
                "realtime": "RealTime",
                "above": "AboveNormal",
                "below": "BelowNormal"
            }
            
            ps_priority = priority_map.get(priority.lower(), "Normal")
            
            if self.is_windows:
                cmd = f'(Get-Process -Id {pid}).PriorityClass = "{ps_priority}"'
                success, output = self._run_powershell(cmd)
                return True, f"[OK] Prioridad cambiada a {ps_priority}" if success else output
            return False, "No disponible"
        except Exception as e:
            return False, str(e)
    
    # === AFINIDAD ===
    
    def get_process_affinity(self, pid: int) -> Tuple[bool, str]:
        """Obtener afinidad de CPU de un proceso"""
        try:
            if self.is_windows:
                cmd = f'''
                (Get-Process -Id {pid}).ProcessorAffinity | Out-String
                '''
                success, output = self._run_powershell(cmd)
                return success, output.strip() if success else output
            return False, "No disponible"
        except Exception as e:
            return False, str(e)
    
    def set_process_affinity(self, pid: int, mask: int) -> Tuple[bool, str]:
        """Establecer afinidad de CPU"""
        try:
            if self.is_windows:
                cmd = f'(Get-Process -Id {pid}).ProcessorAffinity = {mask}'
                success, output = self._run_powershell(cmd)
                return True, f"[OK] Afinidad cambiada" if success else output
            return False, "No disponible"
        except Exception as e:
            return False, str(e)
    
    # === MEMORIA ===
    
    def get_process_memory(self, pid: int) -> Tuple[bool, Dict]:
        """Obtener uso de memoria de un proceso"""
        try:
            if self.is_windows:
                cmd = f'''
                $proc = Get-Process -Id {pid}
                [PSCustomObject]@{{
                    WorkingSet = [math]::Round($proc.WorkingSet64/1MB,2)
                    PrivateMemory = [math]::Round($proc.PrivateMemorySize64/1MB,2)
                    VirtualMemory = [math]::Round($proc.VirtualMemorySize64/1MB,2)
                    PagedMemory = [math]::Round($proc.PagedMemorySize64/1MB,2)
                }} | Format-List | Out-String
                '''
                success, output = self._run_powershell(cmd)
                return success, output.strip() if success else output
            return False, "No disponible"
        except Exception as e:
            return False, str(e)


# Instancia global
process_manager = ProcessManager()
