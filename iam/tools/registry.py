# -*- coding: utf-8 -*-
"""
IAM Registry - Acceso completo al registro de Windows
Permite leer, escribir, exportar, importar y administrar el registro
"""

import subprocess
import platform
import os
from typing import Tuple, List, Dict, Any


class Registry:
    """
    Acceso completo al registro de Windows
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
    
    def _run_reg(self, args: List[str], timeout: int = 30) -> Tuple[bool, str]:
        """Ejecutar comando reg.exe"""
        try:
            result = subprocess.run(
                ['reg'] + args,
                capture_output=True, text=True, timeout=timeout,
                encoding='utf-8', errors='replace'
            )
            return True, result.stdout if result.stdout else result.stderr
        except Exception as e:
            return False, str(e)
    
    # === LEER REGISTRO ===
    
    def read_key(self, key_path: str, value_name: str = None) -> Tuple[bool, Any]:
        """Leer clave del registro"""
        if not self.is_windows:
            return False, "Solo disponible en Windows"
        
        try:
            if value_name:
                cmd = f'(Get-ItemProperty -Path "{key_path}" -Name "{value_name}" -ErrorAction SilentlyContinue).{value_name}'
            else:
                cmd = f'Get-ItemProperty -Path "{key_path}" | Select-Object * | Out-String'
            
            success, output = self._run_powershell(cmd)
            return success, output.strip() if success else output
        except Exception as e:
            return False, str(e)
    
    def get_value(self, key_path: str, value_name: str) -> Tuple[bool, str]:
        """Obtener valor especifico"""
        if not self.is_windows:
            return False, "Solo disponible en Windows"
        
        try:
            cmd = f'(Get-ItemProperty -Path "{key_path}" -Name "{value_name}" -ErrorAction SilentlyContinue).{value_name}'
            success, output = self._run_powershell(cmd)
            return success, output.strip() if success else output
        except Exception as e:
            return False, str(e)
    
    def list_values(self, key_path: str) -> Tuple[bool, List[Dict]]:
        """Listar valores de una clave"""
        if not self.is_windows:
            return False, []
        
        try:
            cmd = f'''
            $props = Get-ItemProperty -Path "{key_path}" -ErrorAction SilentlyContinue
            if ($props) {{
                $props.PSObject.Properties | Where-Object {{ $_.Name -notlike "PS*" }} | ForEach-Object {{
                    [PSCustomObject]@{{ Name=$_.Name; Value=$_.Value; Type=$_.MemberType }}
                }} | Format-Table -AutoSize | Out-String
            }}
            '''
            success, output = self._run_powershell(cmd)
            return success, output.strip() if success else output
        except Exception as e:
            return False, str(e)
    
    def list_subkeys(self, key_path: str) -> Tuple[bool, List[str]]:
        """Listar subclaves"""
        if not self.is_windows:
            return False, []
        
        try:
            cmd = f'(Get-ChildItem -Path "{key_path}" -ErrorAction SilentlyContinue).PSChildName | Out-String'
            success, output = self._run_powershell(cmd)
            if success:
                keys = [k.strip() for k in output.strip().split('\n') if k.strip()]
                return True, keys
            return False, output
        except Exception as e:
            return False, str(e)
    
    # === ESCRIBIR REGISTRO ===
    
    def create_key(self, key_path: str) -> Tuple[bool, str]:
        """Crear clave del registro"""
        if not self.is_windows:
            return False, "Solo disponible en Windows"
        
        try:
            cmd = f'New-Item -Path "{key_path}" -Force | Out-Null; "OK"'
            success, output = self._run_powershell(cmd)
            return True, f"[OK] Clave creada: {key_path}" if success else output
        except Exception as e:
            return False, str(e)
    
    def set_value(self, key_path: str, value_name: str, value: Any, 
                  value_type: str = "String") -> Tuple[bool, str]:
        """Establecer valor en el registro"""
        if not self.is_windows:
            return False, "Solo disponible en Windows"
        
        try:
            type_map = {
                "string": "String",
                "dword": "DWord",
                "qword": "QWord",
                "binary": "Binary",
                "expandstring": "ExpandString",
                "multistring": "MultiString"
            }
            
            ps_type = type_map.get(value_type.lower(), "String")
            
            if ps_type == "DWord":
                cmd = f'Set-ItemProperty -Path "{key_path}" -Name "{value_name}" -Value {int(value)} -Type DWord'
            elif ps_type == "QWord":
                cmd = f'Set-ItemProperty -Path "{key_path}" -Name "{value_name}" -Value {int(value)} -Type QWord'
            else:
                cmd = f'Set-ItemProperty -Path "{key_path}" -Name "{value_name}" -Value "{value}" -Type {ps_type}'
            
            success, output = self._run_powershell(cmd)
            return True, f"[OK] Valor '{value_name}' establecido" if success else output
        except Exception as e:
            return False, str(e)
    
    def delete_value(self, key_path: str, value_name: str) -> Tuple[bool, str]:
        """Eliminar valor del registro"""
        if not self.is_windows:
            return False, "Solo disponible en Windows"
        
        try:
            cmd = f'Remove-ItemProperty -Path "{key_path}" -Name "{value_name}" -Force'
            success, output = self._run_powershell(cmd)
            return True, f"[OK] Valor '{value_name}' eliminado" if success else output
        except Exception as e:
            return False, str(e)
    
    def delete_key(self, key_path: str) -> Tuple[bool, str]:
        """Eliminar clave del registro"""
        if not self.is_windows:
            return False, "Solo disponible en Windows"
        
        try:
            cmd = f'Remove-Item -Path "{key_path}" -Recurse -Force'
            success, output = self._run_powershell(cmd)
            return True, f"[OK] Clave eliminada: {key_path}" if success else output
        except Exception as e:
            return False, str(e)
    
    # === EXPORTAR/IMPORTAR ===
    
    def export_key(self, key_path: str, output_file: str) -> Tuple[bool, str]:
        """Exportar clave a archivo .reg"""
        if not self.is_windows:
            return False, "Solo disponible en Windows"
        
        try:
            cmd = f'reg export "{key_path}" "{output_file}" /y'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
            return True, f"[OK] Exportado a: {output_file}" if result.returncode == 0 else result.stderr
        except Exception as e:
            return False, str(e)
    
    def import_key(self, reg_file: str) -> Tuple[bool, str]:
        """Importar desde archivo .reg"""
        if not self.is_windows:
            return False, "Solo disponible en Windows"
        
        try:
            cmd = f'reg import "{reg_file}"'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
            return True, f"[OK] Importado desde: {reg_file}" if result.returncode == 0 else result.stderr
        except Exception as e:
            return False, str(e)
    
    # === BUSCAR ===
    
    def search(self, term: str, root: str = "HKLM") -> Tuple[bool, List[Dict]]:
        """Buscar en el registro"""
        if not self.is_windows:
            return False, []
        
        try:
            cmd = f'''
            $results = @()
            Get-ChildItem -Path "{root}" -Recurse -ErrorAction SilentlyContinue | ForEach-Object {{
                $key = $_.PSPath
                $props = Get-ItemProperty -Path $key -ErrorAction SilentlyContinue
                if ($props) {{
                    $props.PSObject.Properties | Where-Object {{ $_.Name -notlike "PS*" -and $_.Value -like "*{term}*" }} | ForEach-Object {{
                        $results += [PSCustomObject]@{{ Key=$key; Name=$_.Name; Value=$_.Value }}
                    }}
                }}
            }}
            $results | Select-Object -First 20 | Format-Table -AutoSize | Out-String
            '''
            success, output = self._run_powershell(cmd, timeout=60)
            return success, output.strip() if success else output
        except Exception as e:
            return False, str(e)
    
    # === CLAVES COMUNES ===
    
    def get_common_paths(self) -> Dict[str, str]:
        """Obtener rutas comunes del registro"""
        return {
            "HKLM_SOFTWARE": "HKLM:\\SOFTWARE",
            "HKLM_SYSTEM": "HKLM:\\SYSTEM",
            "HKLM_RUN": "HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run",
            "HKCU_RUN": "HKCU:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run",
            "HKLM_UNINSTALL": "HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall",
            "HKLM_FIREWALL": "HKLM:\\SYSTEM\\CurrentControlSet\\Services\\SharedAccess\\Parameters\\FirewallPolicy",
            "HKLM_STARTUP": "HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\StartupApproved\\Run",
            "HKCU_STARTUP": "HKCU:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\StartupApproved\\Run",
            "HKLM_NETWORK": "HKLM:\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters\\Interfaces",
            "HKLM_ENVIRONMENT": "HKLM:\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Environment",
            "HKCU_ENVIRONMENT": "HKCU:\\Environment"
        }
    
    def get_startup_programs(self) -> Tuple[bool, List[Dict]]:
        """Obtener programas de inicio"""
        try:
            programs = []
            
            # HKLM Run
            success, output = self.get_value(
                "HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run", ""
            )
            
            # HKCU Run  
            success2, output2 = self.get_value(
                "HKCU:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run", ""
            )
            
            return True, {"HKLM": output, "HKCU": output2}
        except Exception as e:
            return False, str(e)
    
    # === INSTALACIONES ===
    
    def get_installed_programs(self) -> Tuple[bool, List[Dict]]:
        """Obtener programas instalados via registro"""
        try:
            cmd = '''
            $programs = @()
            $paths = @(
                "HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\*",
                "HKLM:\\SOFTWARE\\WOW6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\*",
                "HKCU:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\*"
            )
            foreach ($path in $paths) {
                Get-ItemProperty $path -ErrorAction SilentlyContinue | ForEach-Object {
                    if ($_.DisplayName) {
                        $programs += [PSCustomObject]@{
                            Name = $_.DisplayName
                            Version = $_.DisplayVersion
                            Publisher = $_.Publisher
                            InstallDate = $_.InstallDate
                            Size = $_.EstimatedSize
                        }
                    }
                }
            }
            $programs | Sort-Object Name | Format-Table -AutoSize | Out-String
            '''
            success, output = self._run_powershell(cmd, timeout=60)
            return success, output.strip() if success else output
        except Exception as e:
            return False, str(e)


# Instancia global
registry = Registry()
