# -*- coding: utf-8 -*-
"""
IAM System - Informacion completa del sistema
Procesos, red, servicios, hardware, clipboard
"""

import os
import platform
import datetime
import subprocess
import socket
from typing import Dict, Any, List, Tuple, Optional


class SystemInfo:
    """
    Informacion completa del sistema
    """
    
    @staticmethod
    def get_basic_info() -> Dict[str, Any]:
        """Obtener informacion basica del sistema"""
        return {
            "os": platform.system(),
            "os_version": platform.version(),
            "platform": platform.platform(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "python_version": platform.python_version(),
            "hostname": platform.node(),
            "username": os.getenv("USERNAME", os.getenv("USER", "unknown")),
        }
    
    @staticmethod
    def get_time() -> str:
        """Obtener hora actual"""
        now = datetime.datetime.now()
        return now.strftime('%H:%M:%S')
    
    @staticmethod
    def get_date() -> str:
        """Obtener fecha actual"""
        now = datetime.datetime.now()
        return now.strftime('%d/%m/%Y')
    
    @staticmethod
    def get_datetime() -> str:
        """Obtener fecha y hora"""
        now = datetime.datetime.now()
        return now.strftime('%d/%m/%Y %H:%M:%S')
    
    @staticmethod
    def get_working_directory() -> str:
        """Obtener directorio de trabajo"""
        return os.getcwd()
    
    @staticmethod
    def get_env_info() -> Dict[str, str]:
        """Obtener variables de entorno relevantes"""
        relevant = ["PATH", "HOME", "USER", "PYTHONPATH", "VIRTUAL_ENV", 
                    "TEMP", "USERNAME", "COMPUTERNAME", "SYSTEMROOT"]
        return {k: os.environ.get(k, "No definida") for k in relevant}
    
    # === PROCESOS ===
    
    @staticmethod
    def list_processes() -> Tuple[bool, List[Dict]]:
        """Listar procesos en ejecucion"""
        try:
            if platform.system() == "Windows":
                result = subprocess.run(
                    "tasklist /FO CSV /NH",
                    shell=True, capture_output=True, text=True, timeout=10
                )
                processes = []
                for line in result.stdout.strip().split('\n'):
                    parts = line.split('","')
                    if len(parts) >= 5:
                        processes.append({
                            'name': parts[0].strip('"'),
                            'pid': parts[1].strip('"'),
                            'memory': parts[4].strip('"')
                        })
                return True, processes[:50]
            else:
                result = subprocess.run(
                    ["ps", "aux", "--sort=-pcpu"],
                    capture_output=True, text=True, timeout=10
                )
                processes = []
                for line in result.stdout.strip().split('\n')[1:21]:
                    parts = line.split()
                    processes.append({
                        'name': parts[10] if len(parts) > 10 else '?',
                        'pid': parts[1],
                        'cpu': parts[2],
                        'memory': parts[3]
                    })
                return True, processes
        except Exception as e:
            return False, [{'error': str(e)}]
    
    @staticmethod
    def kill_process(pid: str) -> Tuple[bool, str]:
        """Matar un proceso"""
        try:
            if platform.system() == "Windows":
                subprocess.run(f"taskkill /PID {pid} /F", shell=True, 
                             capture_output=True, timeout=10)
            else:
                subprocess.run(["kill", "-9", pid], capture_output=True, timeout=10)
            return True, f"[OK] Proceso {pid} terminado"
        except Exception as e:
            return False, f"[ERROR] Error: {e}"
    
    @staticmethod
    def search_process(name: str) -> Tuple[bool, List[Dict]]:
        """Buscar procesos por nombre"""
        try:
            success, processes = SystemInfo.list_processes()
            if not success:
                return False, processes
            
            found = [p for p in processes if name.lower() in p.get('name', '').lower()]
            return True, found
        except Exception as e:
            return False, [{'error': str(e)}]
    
    # === RED ===
    
    @staticmethod
    def get_network_info() -> Dict[str, Any]:
        """Obtener informacion de red"""
        info = {
            'hostname': socket.gethostname(),
            'ip_local': '',
            'ip_public': '',
            'interfaces': []
        }
        
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            info['ip_local'] = s.getsockname()[0]
            s.close()
        except:
            pass
        
        try:
            import requests
            response = requests.get('https://api.ipify.org', timeout=5)
            info['ip_public'] = response.text
        except:
            pass
        
        return info
    
    @staticmethod
    def ping(host: str, count: int = 4) -> Tuple[bool, str]:
        """Hacer ping a un host"""
        try:
            param = "-n" if platform.system() == "Windows" else "-c"
            result = subprocess.run(
                ["ping", param, str(count), host],
                capture_output=True, text=True, timeout=30
            )
            return True, result.stdout
        except Exception as e:
            return False, f"[ERROR] Error: {e}"
    
    @staticmethod
    def get_open_ports() -> Tuple[bool, List[Dict]]:
        """Obtener puertos abiertos"""
        try:
            if platform.system() == "Windows":
                result = subprocess.run(
                    "netstat -ano | findstr LISTENING",
                    shell=True, capture_output=True, text=True, timeout=10
                )
            else:
                result = subprocess.run(
                    ["netstat", "-tlnp"],
                    capture_output=True, text=True, timeout=10
                )
            
            ports = []
            for line in result.stdout.strip().split('\n')[:20]:
                if line.strip():
                    ports.append({'info': line.strip()})
            
            return True, ports
        except Exception as e:
            return False, [{'error': str(e)}]
    
    @staticmethod
    def check_port(port: int) -> Tuple[bool, bool]:
        """Verificar si un puerto esta en uso"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex(('localhost', port))
            sock.close()
            return True, result == 0
        except Exception as e:
            return False, False
    
    # === SERVICIOS ===
    
    @staticmethod
    def list_services() -> Tuple[bool, List[Dict]]:
        """Listar servicios del sistema"""
        try:
            if platform.system() == "Windows":
                result = subprocess.run(
                    "net start",
                    shell=True, capture_output=True, text=True, timeout=10
                )
                services = []
                for line in result.stdout.strip().split('\n')[1:]:
                    if line.strip():
                        services.append({'name': line.strip()})
                return True, services[:30]
            else:
                result = subprocess.run(
                    ["systemctl", "list-units", "--type=service", "--state=running"],
                    capture_output=True, text=True, timeout=10
                )
                services = []
                for line in result.stdout.strip().split('\n')[1:31]:
                    if line.strip():
                        services.append({'name': line.strip()[:60]})
                return True, services
        except Exception as e:
            return False, [{'error': str(e)}]
    
    @staticmethod
    def start_service(name: str) -> Tuple[bool, str]:
        """Iniciar un servicio"""
        try:
            if platform.system() == "Windows":
                result = subprocess.run(
                    f'net start "{name}"',
                    shell=True, capture_output=True, text=True, timeout=15
                )
                if result.returncode == 0:
                    return True, f"Servicio '{name}' iniciado"
                return False, result.stdout.strip() or result.stderr.strip()
            else:
                result = subprocess.run(
                    ["systemctl", "start", name],
                    capture_output=True, text=True, timeout=15
                )
                if result.returncode == 0:
                    return True, f"Servicio '{name}' iniciado"
                return False, result.stderr.strip()
        except Exception as e:
            return False, str(e)
    
    @staticmethod
    def stop_service(name: str) -> Tuple[bool, str]:
        """Detener un servicio"""
        try:
            if platform.system() == "Windows":
                result = subprocess.run(
                    f'net stop "{name}"',
                    shell=True, capture_output=True, text=True, timeout=15
                )
                if result.returncode == 0:
                    return True, f"Servicio '{name}' detenido"
                return False, result.stdout.strip() or result.stderr.strip()
            else:
                result = subprocess.run(
                    ["systemctl", "stop", name],
                    capture_output=True, text=True, timeout=15
                )
                if result.returncode == 0:
                    return True, f"Servicio '{name}' detenido"
                return False, result.stderr.strip()
        except Exception as e:
            return False, str(e)
    
    # === CLIPBOARD ===
    
    @staticmethod
    def get_clipboard() -> Tuple[bool, str]:
        """Obtener contenido del clipboard"""
        try:
            if platform.system() == "Windows":
                result = subprocess.run(
                    "powershell Get-Clipboard",
                    shell=True, capture_output=True, text=True, timeout=5
                )
                return True, result.stdout.strip()
            else:
                result = subprocess.run(
                    ["xclip", "-selection", "clipboard", "-o"],
                    capture_output=True, text=True, timeout=5
                )
                return True, result.stdout.strip()
        except Exception as e:
            return False, f"[ERROR] Error: {e}"
    
    @staticmethod
    def set_clipboard(text: str) -> Tuple[bool, str]:
        """Establecer contenido del clipboard"""
        try:
            if platform.system() == "Windows":
                subprocess.run(
                    f'echo {text} | clip',
                    shell=True, capture_output=True, timeout=5
                )
                return True, "[OK] Copiado al clipboard"
            else:
                subprocess.run(
                    ["xclip", "-selection", "clipboard"],
                    input=text.encode(), timeout=5
                )
                return True, "[OK] Copiado al clipboard"
        except Exception as e:
            return False, f"[ERROR] Error: {e}"
    
    # === DISCO ===
    
    @staticmethod
    def list_drives() -> Tuple[bool, List[Dict]]:
        """Listar unidades de disco"""
        try:
            if platform.system() == "Windows":
                result = subprocess.run(
                    "wmic logicaldisk get caption,size,freespace,volumename",
                    shell=True, capture_output=True, text=True, timeout=10
                )
                drives = []
                for line in result.stdout.strip().split('\n')[1:]:
                    parts = line.split()
                    if len(parts) >= 2:
                        drives.append({
                            'letter': parts[0],
                            'name': parts[-1] if len(parts) > 3 else '',
                            'free': parts[1] if len(parts) > 1 else '?',
                            'total': parts[2] if len(parts) > 2 else '?'
                        })
                return True, drives
            else:
                result = subprocess.run(
                    ["df", "-h"],
                    capture_output=True, text=True, timeout=10
                )
                drives = []
                for line in result.stdout.strip().split('\n')[1:]:
                    parts = line.split()
                    if len(parts) >= 6:
                        drives.append({
                            'device': parts[0],
                            'size': parts[1],
                            'used': parts[2],
                            'free': parts[3],
                            'mount': parts[5]
                        })
                return True, drives
        except Exception as e:
            return False, [{'error': str(e)}]
    
    # === HARDWARE ===
    
    @staticmethod
    def get_cpu_info() -> Dict[str, Any]:
        """Obtener info del CPU"""
        info = {
            'processor': platform.processor(),
            'cores': os.cpu_count(),
            'architecture': platform.machine()
        }
        
        try:
            if platform.system() == "Windows":
                result = subprocess.run(
                    "wmic cpu get name,numberofcores,maxclockspeed",
                    shell=True, capture_output=True, text=True, timeout=10
                )
                lines = result.stdout.strip().split('\n')
                if len(lines) > 1:
                    parts = lines[1].split()
                    info['name'] = ' '.join(parts[:-2]) if len(parts) > 2 else parts[0] if parts else ''
        except:
            pass
        
        return info
    
    @staticmethod
    def get_memory_info() -> Dict[str, Any]:
        """Obtener info de memoria"""
        try:
            if platform.system() == "Windows":
                result = subprocess.run(
                    "wmic OS get TotalVisibleMemorySize,FreePhysicalMemory",
                    shell=True, capture_output=True, text=True, timeout=10
                )
                lines = [l for l in result.stdout.strip().split('\n') if l.strip()]
                if len(lines) >= 2:
                    # Parse header to find column order
                    header = lines[0].strip()
                    parts = lines[1].split()
                    if len(parts) >= 2:
                        # Determine which column is which based on header
                        if header.index('TotalVisibleMemorySize') < header.index('FreePhysicalMemory'):
                            total_kb = int(parts[0])
                            free_kb = int(parts[1])
                        else:
                            free_kb = int(parts[0])
                            total_kb = int(parts[1])
                        return {
                            'total': f"{total_kb / 1024 / 1024:.1f} GB",
                            'free': f"{free_kb / 1024 / 1024:.1f} GB",
                            'used': f"{(total_kb - free_kb) / 1024 / 1024:.1f} GB",
                            'percent': round((1 - free_kb / total_kb) * 100, 1)
                        }
        except:
            pass
        
        return {'total': 'N/A', 'free': 'N/A', 'used': 'N/A', 'percent': 0}
    
    # === BROWSER HISTORY (simplificado) ===
    
    @staticmethod
    def get_installed_programs() -> Tuple[bool, List[str]]:
        """Obtener programas instalados"""
        try:
            if platform.system() == "Windows":
                result = subprocess.run(
                    'reg query "HKLM\\Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall" /s /v DisplayName',
                    shell=True, capture_output=True, text=True, timeout=15
                )
                programs = []
                for line in result.stdout.split('\n'):
                    if 'DisplayName' in line:
                        name = line.split('REG_SZ')[-1].strip()
                        if name:
                            programs.append(name)
                return True, sorted(programs)[:50]
            else:
                return True, []
        except Exception as e:
            return False, [f"[ERROR] Error: {e}"]
    
    # === SCREENSHOT ===
    
    @staticmethod
    def take_screenshot(output_path: str = None) -> Tuple[bool, str]:
        """Tomar screenshot"""
        try:
            if not output_path:
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                output_path = os.path.join(os.path.expanduser("~"), "Desktop", f"screenshot_{timestamp}.png")
            
            if platform.system() == "Windows":
                try:
                    import mss
                    with mss.mss() as sct:
                        sct.shot(output=output_path)
                        return True, f"[OK] Screenshot guardado: {output_path}"
                except ImportError:
                    subprocess.run(
                        f'snippingtool /clip',
                        shell=True, timeout=10
                    )
                    return True, "[OK] Snipping Tool abierto"
            else:
                subprocess.run(["screencapture", output_path], timeout=10)
                return True, f"[OK] Screenshot guardado: {output_path}"
        except Exception as e:
            return False, f"[ERROR] Error: {e}"


# Instancia global
system_info = SystemInfo()
