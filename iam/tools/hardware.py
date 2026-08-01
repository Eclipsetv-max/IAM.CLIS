# -*- coding: utf-8 -*-
"""
IAM Hardware - Informacion completa del hardware
CPU, RAM, disco, red, bateria, temperatura, sensores
"""

import subprocess
import platform
import os
import socket
from typing import Tuple, List, Dict, Any


class Hardware:
    """
    Informacion completa del hardware del sistema
    """
    
    def __init__(self):
        self.is_windows = platform.system() == "Windows"
        self.is_linux = platform.system() == "Linux"
        self.is_mac = platform.system() == "Darwin"
    
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
    
    def _run_wmic(self, args: List[str], timeout: int = 30) -> Tuple[bool, str]:
        """Ejecutar comando wmic"""
        try:
            result = subprocess.run(
                ['wmic'] + args,
                capture_output=True, text=True, timeout=timeout,
                encoding='utf-8', errors='replace'
            )
            return True, result.stdout if result.stdout else result.stderr
        except Exception as e:
            return False, str(e)
    
    # === CPU ===
    
    def get_cpu_info(self) -> Tuple[bool, Dict]:
        """Obtener informacion detallada del CPU"""
        try:
            info = {
                'cores_physical': os.cpu_count(),
                'architecture': platform.machine(),
                'processor': platform.processor()
            }
            
            if self.is_windows:
                cmd = '''
                $cpu = Get-CimInstance -ClassName Win32_Processor | Select-Object -First 1
                [PSCustomObject]@{
                    Name = $cpu.Name
                    Manufacturer = $cpu.Manufacturer
                    MaxClockSpeed = $cpu.MaxClockSpeed
                    CurrentClockSpeed = $cpu.CurrentClockSpeed
                    NumberOfCores = $cpu.NumberOfCores
                    NumberOfLogicalProcessors = $cpu.NumberOfLogicalProcessors
                    L2CacheSize = $cpu.L2CacheSize
                    L3CacheSize = $cpu.L3CacheSize
                    LoadPercentage = $cpu.LoadPercentage
                } | Format-List | Out-String
                '''
                success, output = self._run_powershell(cmd)
                if success:
                    info['details'] = output.strip()
            
            return True, info
        except Exception as e:
            return False, {'error': str(e)}
    
    def get_cpu_load(self) -> Tuple[bool, Dict]:
        """Obtener carga del CPU"""
        try:
            if self.is_windows:
                cmd = '''
                $cpu = Get-CimInstance -ClassName Win32_Processor | Select-Object -First 1
                [PSCustomObject]@{
                    Load = $cpu.LoadPercentage
                    Status = $cpu.CpuStatus
                } | Format-List | Out-String
                '''
                success, output = self._run_powershell(cmd)
                return success, output.strip() if success else output
            return False, "No disponible"
        except Exception as e:
            return False, str(e)
    
    # === MEMORIA RAM ===
    
    def get_ram_info(self) -> Tuple[bool, Dict]:
        """Obtener informacion de memoria RAM"""
        try:
            info = {}
            
            if self.is_windows:
                cmd = '''
                $ram = Get-CimInstance -ClassName Win32_PhysicalMemory | Measure-Object -Property Capacity -Sum
                $total = $ram.Sum / 1MB
                $os = Get-CimInstance -ClassName Win32_OperatingSystem
                $free = $os.FreePhysicalMemory / 1KB
                $used = $total - $free
                [PSCustomObject]@{
                    TotalGB = [math]::Round($total/1024, 2)
                    UsedGB = [math]::Round($used/1024, 2)
                    FreeGB = [math]::Round($free/1024, 2)
                    PercentUsed = [math]::Round(($used/$total)*100, 1)
                } | Format-List | Out-String
                '''
                success, output = self._run_powershell(cmd)
                if success:
                    info['details'] = output.strip()
                
                # Slots de memoria
                cmd_slots = '''
                Get-CimInstance -ClassName Win32_PhysicalMemory | 
                Select-Object DeviceLocator, Capacity, Speed, Manufacturer |
                Format-Table -AutoSize | Out-String
                '''
                success2, output2 = self._run_powershell(cmd_slots)
                if success2:
                    info['slots'] = output2.strip()
            
            return True, info
        except Exception as e:
            return False, {'error': str(e)}
    
    # === DISCO DURO ===
    
    def get_disk_info(self) -> Tuple[bool, List[Dict]]:
        """Obtener informacion de discos"""
        try:
            disks = []
            
            if self.is_windows:
                cmd = '''
                Get-PhysicalDisk | 
                Select-Object DeviceId, FriendlyName, MediaType, Size, HealthStatus |
                Format-Table -AutoSize | Out-String
                '''
                success, output = self._run_powershell(cmd)
                if success:
                    disks.append({'physical': output.strip()})
                
                cmd2 = '''
                Get-Volume | Where-Object { $_.DriveLetter } |
                Select-Object DriveLetter, FileSystemLabel, FileSystem, 
                @{N='SizeGB';E={[math]::Round($_.Size/1GB,2)}},
                @{N='FreeGB';E={[math]::Round($_.SizeRemaining/1GB,2)}},
                @{N='UsedPercent';E={[math]::Round(($_.Size-$_.SizeRemaining)/$_.Size*100,1)}},
                HealthStatus |
                Format-Table -AutoSize | Out-String
                '''
                success2, output2 = self._run_powershell(cmd2)
                if success2:
                    disks.append({'volumes': output2.strip()})
            
            return True, disks
        except Exception as e:
            return False, [{'error': str(e)}]
    
    def get_disk_health(self) -> Tuple[bool, str]:
        """Obtener salud de los discos"""
        try:
            if self.is_windows:
                cmd = '''
                Get-PhysicalDisk | 
                Select-Object FriendlyName, HealthStatus, OperationalStatus |
                Format-Table -AutoSize | Out-String
                '''
                success, output = self._run_powershell(cmd)
                return success, output.strip() if success else output
            return False, "No disponible"
        except Exception as e:
            return False, str(e)
    
    # === TARJETA GRAFICA ===
    
    def get_gpu_info(self) -> Tuple[bool, List[Dict]]:
        """Obtener informacion de GPU"""
        try:
            gpus = []
            
            if self.is_windows:
                cmd = '''
                Get-CimInstance -ClassName Win32_VideoController | 
                Select-Object Name, AdapterRAM, DriverVersion, VideoProcessor, CurrentHorizontalResolution, CurrentVerticalResolution |
                Format-List | Out-String
                '''
                success, output = self._run_powershell(cmd)
                if success:
                    gpus.append(output.strip())
            
            return True, gpus
        except Exception as e:
            return False, [{'error': str(e)}]
    
    # === TARJETA MADRE ===
    
    def get_motherboard_info(self) -> Tuple[bool, Dict]:
        """Obtener informacion de la tarjeta madre"""
        try:
            info = {}
            
            if self.is_windows:
                cmd = '''
                $mb = Get-CimInstance -ClassName Win32_BaseBoard
                $bios = Get-CimInstance -ClassName Win32_BIOS
                [PSCustomObject]@{
                    Manufacturer = $mb.Manufacturer
                    Product = $mb.Product
                    SerialNumber = $mb.SerialNumber
                    BIOSManufacturer = $bios.Manufacturer
                    BIOSVersion = $bios.SMBIOSBIOSVersion
                    BIOSDate = $bios.ReleaseDate
                } | Format-List | Out-String
                '''
                success, output = self._run_powershell(cmd)
                if success:
                    info['details'] = output.strip()
            
            return True, info
        except Exception as e:
            return False, {'error': str(e)}
    
    def get_bios_info(self) -> Tuple[bool, Dict]:
        """Obtener informacion del BIOS"""
        return self.get_motherboard_info()
    
    # === BATERIA ===
    
    def get_battery_info(self) -> Tuple[bool, Dict]:
        """Obtener informacion de bateria (laptops)"""
        try:
            if self.is_windows:
                cmd = '''
                $battery = Get-CimInstance -ClassName Win32_Battery -ErrorAction SilentlyContinue
                if ($battery) {
                    [PSCustomObject]@{
                        ChargeLevel = $battery.EstimatedChargeRemaining
                        Status = $battery.BatteryStatus
                        Chemistry = $battery.BatteryChemistry
                        TimeRemaining = $battery.EstimatedRunTime
                    } | Format-List | Out-String
                } else {
                    "No se detecto bateria"
                }
                '''
                success, output = self._run_powershell(cmd)
                return success, output.strip() if success else output
            return False, "No disponible"
        except Exception as e:
            return False, str(e)
    
    # === TEMPERATURA ===
    
    def get_temperature(self) -> Tuple[bool, Dict]:
        """Obtener temperatura del sistema"""
        try:
            temps = {}
            
            if self.is_windows:
                # Intentar via WMI
                cmd = '''
                $thermal = Get-CimInstance -Namespace "root/WMI" -ClassName MSAcpi_ThermalZoneTemperature -ErrorAction SilentlyContinue
                if ($thermal) {
                    $thermal | ForEach-Object {
                        [PSCustomObject]@{
                            Zone = $_.InstanceName
                            Temperature = [math]::Round(($_.CurrentTemperature - 2732) / 10, 1)
                        }
                    } | Format-Table -AutoSize | Out-String
                } else {
                    "Sensores de temperatura no disponibles"
                }
                '''
                success, output = self._run_powershell(cmd)
                if success:
                    temps['thermal_zones'] = output.strip()
            
            return True, temps
        except Exception as e:
            return False, {'error': str(e)}
    
    # === RED ===
    
    def get_network_adapters(self) -> Tuple[bool, List[Dict]]:
        """Obtener adaptadores de red"""
        try:
            adapters = []
            
            if self.is_windows:
                cmd = '''
                Get-NetAdapter | 
                Select-Object Name, InterfaceDescription, Status, MacAddress, LinkSpeed, 
                @{N='IPAddress';E={(Get-NetIPAddress -InterfaceIndex $_.ifIndex -ErrorAction SilentlyContinue).IPAddress -join ', '}} |
                Format-Table -AutoSize | Out-String
                '''
                success, output = self._run_powershell(cmd)
                if success:
                    adapters.append(output.strip())
            
            return True, adapters
        except Exception as e:
            return False, [{'error': str(e)}]
    
    def get_wifi_info(self) -> Tuple[bool, Dict]:
        """Obtener informacion WiFi"""
        try:
            if self.is_windows:
                cmd = '''
                $wifi = netsh wlan show interfaces
                $wifi | Out-String
                '''
                success, output = self._run_powershell(cmd)
                return success, output.strip() if success else output
            return False, "No disponible"
        except Exception as e:
            return False, str(e)
    
    # === USB ===
    
    def get_usb_devices(self) -> Tuple[bool, List[Dict]]:
        """Obtener dispositivos USB conectados"""
        try:
            devices = []
            
            if self.is_windows:
                cmd = '''
                Get-PnpDevice -Class USB -ErrorAction SilentlyContinue |
                Select-Object FriendlyName, Status, InstanceId |
                Format-Table -AutoSize | Out-String
                '''
                success, output = self._run_powershell(cmd)
                if success:
                    devices.append(output.strip())
            
            return True, devices
        except Exception as e:
            return False, [{'error': str(e)}]
    
    # === SISTEMA COMPLETO ===
    
    def get_full_system_info(self) -> Tuple[bool, Dict]:
        """Obtener informacion completa del sistema"""
        try:
            info = {
                'os': platform.system(),
                'os_version': platform.version(),
                'hostname': platform.node(),
                'username': os.getenv("USERNAME", os.getenv("USER", "unknown")),
                'python': platform.python_version()
            }
            
            if self.is_windows:
                cmd = '''
                $os = Get-CimInstance -ClassName Win32_OperatingSystem
                $cs = Get-CimInstance -ClassName Win32_ComputerSystem
                [PSCustomObject]@{
                    Manufacturer = $cs.Manufacturer
                    Model = $cs.Model
                    TotalPhysicalMemory = [math]::Round($cs.TotalPhysicalMemory/1GB, 2)
                    NumberOfProcessors = $cs.NumberOfProcessors
                    NumberOfLogicalProcessors = $cs.NumberOfLogicalProcessors
                    OSName = $os.Caption
                    OSVersion = $os.Version
                    LastBoot = $os.LastBootUpTime
                    CurrentUser = $os.UserName
                } | Format-List | Out-String
                '''
                success, output = self._run_powershell(cmd)
                if success:
                    info['system'] = output.strip()
            
            return True, info
        except Exception as e:
            return False, {'error': str(e)}


# Instancia global
hardware = Hardware()
