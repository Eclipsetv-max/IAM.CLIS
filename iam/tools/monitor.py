# -*- coding: utf-8 -*-
"""
IAM Monitor - Monitoreo en tiempo real del sistema
CPU, memoria, disco, red, procesos, alertas
"""

import subprocess
import platform
import time
import threading
import json
from typing import Tuple, List, Dict, Any, Callable
from datetime import datetime


class Monitor:
    """
    Monitoreo en tiempo real del sistema
    """
    
    def __init__(self):
        self.is_windows = platform.system() == "Windows"
        self._alerts = []
        self._callbacks = {}
    
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
    
    # === CPU MONITORING ===
    
    def get_cpu_usage(self) -> Tuple[bool, float]:
        """Obtener uso actual del CPU"""
        try:
            if self.is_windows:
                cmd = '''
                $cpu = (Get-CimInstance -ClassName Win32_Processor | Measure-Object -Property LoadPercentage -Average).Average
                $cpu
                '''
                success, output = self._run_powershell(cmd)
                if success:
                    return True, float(output.strip())
            else:
                import psutil
                return True, psutil.cpu_percent(interval=1)
            return False, 0.0
        except Exception as e:
            return False, 0.0
    
    def get_cpu_details(self) -> Tuple[bool, Dict]:
        """Detalles del CPU"""
        try:
            if self.is_windows:
                cmd = '''
                $cpu = Get-CimInstance -ClassName Win32_Processor | Select-Object -First 1
                [PSCustomObject]@{
                    Name = $cpu.Name
                    Load = $cpu.LoadPercentage
                    Cores = $cpu.NumberOfCores
                    LogicalProcessors = $cpu.NumberOfLogicalProcessors
                    ClockSpeed = $cpu.CurrentClockSpeed
                } | ConvertTo-Json
                '''
                success, output = self._run_powershell(cmd)
                if success:
                    return True, json.loads(output)
            return False, {}
        except Exception as e:
            return False, {}
    
    # === MEMORY MONITORING ===
    
    def get_memory_usage(self) -> Tuple[bool, Dict]:
        """Obtener uso de memoria"""
        try:
            if self.is_windows:
                cmd = '''
                $os = Get-CimInstance -ClassName Win32_OperatingSystem
                $total = $os.TotalVisibleMemorySize / 1KB
                $free = $os.FreePhysicalMemory / 1KB
                $used = $total - $free
                [PSCustomObject]@{
                    TotalGB = [math]::Round($total/1024, 2)
                    UsedGB = [math]::Round($used/1024, 2)
                    FreeGB = [math]::Round($free/1024, 2)
                    PercentUsed = [math]::Round(($used/$total)*100, 1)
                } | ConvertTo-Json
                '''
                success, output = self._run_powershell(cmd)
                if success:
                    return True, json.loads(output)
            return False, {}
        except Exception as e:
            return False, {}
    
    # === DISK MONITORING ===
    
    def get_disk_usage(self) -> Tuple[bool, List[Dict]]:
        """Obtener uso de disco"""
        try:
            if self.is_windows:
                cmd = '''
                Get-Volume | Where-Object { $_.DriveLetter } |
                Select-Object DriveLetter, FileSystemLabel,
                @{N='SizeGB';E={[math]::Round($_.Size/1GB,2)}},
                @{N='FreeGB';E={[math]::Round($_.SizeRemaining/1GB,2)}},
                @{N='UsedPercent';E={[math]::Round(($_.Size-$_.SizeRemaining)/$_.Size*100,1)}} |
                ConvertTo-Json
                '''
                success, output = self._run_powershell(cmd)
                if success:
                    data = json.loads(output)
                    return True, data if isinstance(data, list) else [data]
            return False, []
        except Exception as e:
            return False, []
    
    def get_disk_activity(self) -> Tuple[bool, Dict]:
        """Actividad de disco"""
        try:
            if self.is_windows:
                cmd = '''
                $disk = Get-CimInstance -ClassName Win32_PerfFormattedData_PerfDisk_PhysicalDisk |
                Where-Object { $_.Name -eq "_Total" }
                [PSCustomObject]@{
                    ReadBytesPerSec = $disk.DiskReadBytesPerSec
                    WriteBytesPerSec = $disk.DiskWriteBytesPerSec
                    QueueLength = $disk.CurrentDiskQueueLength
                } | ConvertTo-Json
                '''
                success, output = self._run_powershell(cmd)
                if success:
                    return True, json.loads(output)
            return False, {}
        except Exception as e:
            return False, {}
    
    # === NETWORK MONITORING ===
    
    def get_network_activity(self) -> Tuple[bool, List[Dict]]:
        """Actividad de red"""
        try:
            if self.is_windows:
                cmd = '''
                Get-NetAdapter | Where-Object { $_.Status -eq "Up" } |
                Select-Object Name, @{N='ReceivedMB';E={[math]::Round($_.ReceivedBytes/1MB,2)}},
                @{N='SentMB';E={[math]::Round($_.SentBytes/1MB,2)}}, LinkSpeed |
                ConvertTo-Json
                '''
                success, output = self._run_powershell(cmd)
                if success:
                    data = json.loads(output)
                    return True, data if isinstance(data, list) else [data]
            return False, []
        except Exception as e:
            return False, []
    
    # === PROCESS MONITORING ===
    
    def get_top_processes(self, metric: str = "cpu", count: int = 10) -> Tuple[bool, List[Dict]]:
        """Top procesos por metrica"""
        try:
            if self.is_windows:
                if metric == "cpu":
                    sort = "CPU"
                elif metric == "memory":
                    sort = "WorkingSet64"
                else:
                    sort = "CPU"
                
                cmd = f'''
                Get-Process | Sort-Object -Property {sort} -Descending |
                Select-Object -First {count} Id, ProcessName, CPU,
                @{{"N='MemoryMB';E={{[math]::Round($_.WorkingSet64/1MB,1)}}}} |
                ConvertTo-Json
                '''
                success, output = self._run_powershell(cmd)
                if success:
                    data = json.loads(output)
                    return True, data if isinstance(data, list) else [data]
            return False, []
        except Exception as e:
            return False, []
    
    # === ALERTAS ===
    
    def add_alert(self, name: str, condition: Callable, action: Callable, 
                  interval: int = 60):
        """Agregar alerta"""
        self._alerts.append({
            'name': name,
            'condition': condition,
            'action': action,
            'interval': interval,
            'last_check': 0
        })
    
    def check_alerts(self):
        """Verificar alertas"""
        now = time.time()
        for alert in self._alerts:
            if now - alert['last_check'] >= alert['interval']:
                if alert['condition']():
                    alert['action']()
                alert['last_check'] = now
    
    def remove_alert(self, name: str):
        """Eliminar alerta"""
        self._alerts = [a for a in self._alerts if a['name'] != name]
    
    # === DASHBOARD ===
    
    def get_system_dashboard(self) -> Tuple[bool, Dict]:
        """Obtener dashboard completo del sistema"""
        try:
            dashboard = {
                'timestamp': datetime.now().isoformat(),
                'cpu': {},
                'memory': {},
                'disk': [],
                'network': [],
                'top_processes': []
            }
            
            success, cpu = self.get_cpu_usage()
            if success:
                dashboard['cpu']['usage'] = cpu
            
            success, mem = self.get_memory_usage()
            if success:
                dashboard['memory'] = mem
            
            success, disk = self.get_disk_usage()
            if success:
                dashboard['disk'] = disk
            
            success, net = self.get_network_activity()
            if success:
                dashboard['network'] = net
            
            success, procs = self.get_top_processes("cpu", 5)
            if success:
                dashboard['top_processes'] = procs
            
            return True, dashboard
        except Exception as e:
            return False, {}
    
    # === CONTINUOUS MONITORING ===
    
    def start_continuous_monitor(self, callback: Callable, interval: int = 5):
        """Iniciar monitoreo continuo"""
        def monitor_loop():
            while True:
                dashboard = self.get_system_dashboard()
                callback(dashboard)
                time.sleep(interval)
        
        thread = threading.Thread(target=monitor_loop, daemon=True)
        thread.start()
        return thread
    
    # === UTILIDADES ===
    
    def get_system_uptime(self) -> Tuple[bool, str]:
        """Obtener tiempo de actividad"""
        try:
            if self.is_windows:
                # Usar formato ISO para evitar problemas de localizacion
                cmd = '''
                $boot = (Get-CimInstance -ClassName Win32_OperatingSystem).LastBootUpTime
                $boot.ToString('yyyy-MM-ddTHH:mm:ss')
                '''
                success, output = self._run_powershell(cmd)
                if success:
                    boot_str = output.strip()
                    # Intentar parsear formato ISO
                    try:
                        boot_time = datetime.fromisoformat(boot_str)
                    except:
                        # Fallback: intentar formato con timezone
                        boot_time = datetime.fromisoformat(boot_str.replace('Z', '+00:00'))
                    uptime = datetime.now() - boot_time
                    days = uptime.days
                    hours, remainder = divmod(uptime.seconds, 3600)
                    minutes, seconds = divmod(remainder, 60)
                    return True, f"{days}d {hours}h {minutes}m {seconds}s"
            return False, "N/A"
        except Exception as e:
            return False, str(e)
    
    def get_temperature(self) -> Tuple[bool, Dict]:
        """Obtener temperatura"""
        try:
            if self.is_windows:
                cmd = '''
                $thermal = Get-CimInstance -Namespace "root/WMI" -ClassName MSAcpi_ThermalZoneTemperature -ErrorAction SilentlyContinue
                if ($thermal) {
                    $thermal | ForEach-Object {
                        [PSCustomObject]@{
                            Zone = $_.InstanceName
                            TempC = [math]::Round(($_.CurrentTemperature - 2732) / 10, 1)
                        }
                    } | ConvertTo-Json
                } else { "[]" }
                '''
                success, output = self._run_powershell(cmd)
                if success:
                    data = json.loads(output)
                    return True, data if isinstance(data, list) else [data]
            return False, []
        except Exception as e:
            return False, []


# Instancia global
monitor = Monitor()
