# -*- coding: utf-8 -*-
"""
IAM Network - Herramientas completas de red
Escaneo, DNS, traceroute, puertos,-speedtest, ping, etc.
"""

import subprocess
import platform
import socket
import struct
import time
from typing import Tuple, List, Dict, Any


class Network:
    """
    Herramientas completas de red
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
    
    # === INFORMACION DE RED ===
    
    def get_ip_info(self) -> Tuple[bool, Dict]:
        """Obtener informacion IP completa"""
        try:
            info = {
                'hostname': socket.gethostname(),
                'local_ip': '',
                'public_ip': '',
                'interfaces': []
            }
            
            # IP local
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.connect(("8.8.8.8", 80))
                info['local_ip'] = s.getsockname()[0]
                s.close()
            except:
                pass
            
            # IP publica
            try:
                result = subprocess.run(
                    ['curl', '-s', 'https://api.ipify.org'],
                    capture_output=True, text=True, timeout=10
                )
                info['public_ip'] = result.stdout.strip()
            except:
                pass
            
            # Interfaces
            if self.is_windows:
                cmd = '''
                Get-NetIPAddress -AddressFamily IPv4 | 
                Select-Object InterfaceAlias, IPAddress, PrefixLength |
                Format-Table -AutoSize | Out-String
                '''
                success, output = self._run_powershell(cmd)
                if success:
                    info['interfaces'] = output.strip()
            
            return True, info
        except Exception as e:
            return False, {'error': str(e)}
    
    def get_network_interfaces(self) -> Tuple[bool, List[Dict]]:
        """Obtener todas las interfaces de red"""
        try:
            if self.is_windows:
                cmd = '''
                Get-NetAdapter | 
                Select-Object Name, InterfaceDescription, Status, MacAddress, LinkSpeed, 
                @{N='IPAddress';E={(Get-NetIPAddress -InterfaceIndex $_.ifIndex -ErrorAction SilentlyContinue).IPAddress -join ', '}} |
                Format-Table -AutoSize | Out-String
                '''
                success, output = self._run_powershell(cmd)
                return success, output.strip() if success else output
            else:
                success, output = self._run_command(['ifconfig', '-a'])
                return success, output if success else output
        except Exception as e:
            return False, str(e)
    
    # === PING ===
    
    def ping(self, host: str, count: int = 4, timeout: int = 5) -> Tuple[bool, str]:
        """Hacer ping a un host"""
        try:
            if self.is_windows:
                cmd = ['ping', '-n', str(count), '-w', str(timeout * 1000), host]
            else:
                cmd = ['ping', '-c', str(count), '-W', str(timeout), host]
            
            success, output = self._run_command(cmd, timeout=timeout * count + 5)
            return success, output if success else output
        except Exception as e:
            return False, str(e)
    
    def ping_sweep(self, network: str = "192.168.1", start: int = 1, end: int = 254) -> Tuple[bool, List[str]]:
        """Escaneo de red - encontrar dispositivos activos"""
        try:
            active = []
            
            for i in range(start, end + 1):
                ip = f"{network}.{i}"
                param = "-n" if self.is_windows else "-c"
                cmd = ['ping', param, '1', '-W', '1', ip]
                
                try:
                    result = subprocess.run(
                        cmd, capture_output=True, text=True, timeout=2
                    )
                    if result.returncode == 0:
                        active.append(ip)
                except:
                    pass
            
            return True, active
        except Exception as e:
            return False, [str(e)]
    
    # === DNS ===
    
    def dns_lookup(self, domain: str) -> Tuple[bool, Dict]:
        """Lookup DNS completo"""
        try:
            info = {
                'domain': domain,
                'ips': [],
                'reverse': []
            }
            
            # Resolver IPs
            try:
                ips = socket.getaddrinfo(domain, None)
                info['ips'] = list(set([ip[4][0] for ip in ips]))
            except:
                pass
            
            # Reverse DNS
            for ip in info['ips']:
                try:
                    hostname = socket.gethostbyaddr(ip)
                    info['reverse'].append({'ip': ip, 'hostname': hostname[0]})
                except:
                    info['reverse'].append({'ip': ip, 'hostname': 'N/A'})
            
            # MX, NS records via nslookup
            cmd = ['nslookup', '-type=MX', domain]
            success, output = self._run_command(cmd, timeout=10)
            if success:
                info['mx_records'] = output
            
            cmd_ns = ['nslookup', '-type=NS', domain]
            success_ns, output_ns = self._run_command(cmd_ns, timeout=10)
            if success_ns:
                info['ns_records'] = output_ns
            
            return True, info
        except Exception as e:
            return False, {'error': str(e)}
    
    def reverse_dns(self, ip: str) -> Tuple[bool, str]:
        """DNS inverso"""
        try:
            hostname = socket.gethostbyaddr(ip)
            return True, hostname[0]
        except:
            return False, "No se pudo resolver"
    
    # === TRACEROUTE ===
    
    def traceroute(self, host: str, max_hops: int = 30) -> Tuple[bool, str]:
        """Ruta hacia un host"""
        try:
            if self.is_windows:
                cmd = ['tracert', '-d', '-h', str(max_hops), host]
            else:
                cmd = ['traceroute', '-m', str(max_hops), host]
            
            success, output = self._run_command(cmd, timeout=max_hops * 5)
            return success, output if success else output
        except Exception as e:
            return False, str(e)
    
    # === ESCANEO DE PUERTOS ===
    
    def scan_ports(self, host: str, start_port: int = 1, end_port: int = 1024,
                   timeout: float = 0.1) -> Tuple[bool, List[Dict]]:
        """Escanear puertos"""
        try:
            open_ports = []
            
            for port in range(start_port, end_port + 1):
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(timeout)
                    result = sock.connect_ex((host, port))
                    
                    if result == 0:
                        try:
                            service = socket.getservbyport(port)
                        except:
                            service = "unknown"
                        
                        open_ports.append({
                            'port': port,
                            'state': 'open',
                            'service': service
                        })
                    
                    sock.close()
                except:
                    pass
            
            return True, open_ports
        except Exception as e:
            return False, [{'error': str(e)}]
    
    def check_port(self, host: str, port: int) -> Tuple[bool, bool]:
        """Verificar si un puerto esta abierto"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex((host, port))
            sock.close()
            return True, result == 0
        except:
            return False, False
    
    # === SPEEDTEST ===
    
    def speed_test(self) -> Tuple[bool, Dict]:
        """Test de velocidad de internet"""
        try:
            cmd = '''
            $download = (Invoke-WebRequest -Uri "http://speedtest.tele2.net/10MB.zip" -OutFile $null -UseBasicParsing).Content.Length
            [PSCustomObject]@{ Download = "$([math]::Round($download/1MB, 2)) MB" } | Out-String
            '''
            
            # Alternativa: usar speedtest-cli si esta disponible
            success, output = self._run_powershell(cmd, timeout=60)
            if success:
                return True, {'result': output.strip()}
            
            return False, "Speedtest no disponible"
        except Exception as e:
            return False, str(e)
    
    # === CONEXIONES ===
    
    def get_connections(self) -> Tuple[bool, List[Dict]]:
        """Obtener conexiones de red activas"""
        try:
            if self.is_windows:
                cmd = '''
                Get-NetTCPConnection -State Established |
                Select-Object LocalAddress, LocalPort, RemoteAddress, RemotePort, State |
                Format-Table -AutoSize | Out-String
                '''
                success, output = self._run_powershell(cmd)
                return success, output.strip() if success else output
            else:
                success, output = self._run_command(['netstat', '-tunap'])
                return success, output if success else output
        except Exception as e:
            return False, str(e)
    
    def get_listening_ports(self) -> Tuple[bool, List[Dict]]:
        """Obtener puertos en escucha"""
        try:
            if self.is_windows:
                cmd = '''
                Get-NetTCPConnection -State Listen |
                Select-Object LocalAddress, LocalPort, OwningProcess |
                Sort-Object LocalPort |
                Format-Table -AutoSize | Out-String
                '''
                success, output = self._run_powershell(cmd)
                return success, output.strip() if success else output
            else:
                success, output = self._run_command(['netstat', '-tlnp'])
                return success, output if success else output
        except Exception as e:
            return False, str(e)
    
    # === WIFI ===
    
    def get_wifi_networks(self) -> Tuple[bool, List[Dict]]:
        """Escanear redes WiFi disponibles"""
        try:
            if self.is_windows:
                cmd = '''
                netsh wlan show networks mode=bssid | 
                Select-String -Pattern "SSID|Signal|Authentication|Encryption" |
                Out-String
                '''
                success, output = self._run_powershell(cmd)
                return success, output.strip() if success else output
            return False, "No disponible"
        except Exception as e:
            return False, str(e)
    
    def get_wifi_profiles(self) -> Tuple[bool, List[str]]:
        """Obtener perfiles WiFi guardados"""
        try:
            if self.is_windows:
                cmd = '''
                netsh wlan show profiles | 
                Select-String -Pattern "All User Profile" |
                ForEach-Object { ($_ -split ":")[-1].Trim() }
                '''
                success, output = self._run_powershell(cmd)
                if success:
                    profiles = [p.strip() for p in output.strip().split('\n') if p.strip()]
                    return True, profiles
                return False, output
            return False, "No disponible"
        except Exception as e:
            return False, str(e)
    
    def connect_wifi(self, ssid: str, password: str = None) -> Tuple[bool, str]:
        """Conectar a red WiFi"""
        try:
            if self.is_windows:
                if password:
                    cmd = f'''
                    netsh wlan connect name="{ssid}" 
                    netsh wlan set profileparameter name="{ssid}" keyMaterial="{password}"
                    '''
                else:
                    cmd = f'netsh wlan connect name="{ssid}"'
                
                success, output = self._run_powershell(cmd)
                return True, f"[OK] Conectando a {ssid}" if success else output
            return False, "No disponible"
        except Exception as e:
            return False, str(e)
    
    # === WHOIS ===
    
    def whois(self, domain: str) -> Tuple[bool, str]:
        """Consulta WHOIS"""
        try:
            success, output = self._run_command(['whois', domain], timeout=15)
            return success, output if success else output
        except:
            return False, "whois no disponible"
    
    # === HTTP HEADERS ===
    
    def http_headers(self, url: str) -> Tuple[bool, Dict]:
        """Obtener headers HTTP"""
        try:
            cmd = f'''
            $response = Invoke-WebRequest -Uri "{url}" -Method Head -UseBasicParsing
            $response.Headers | Format-List | Out-String
            '''
            success, output = self._run_powershell(cmd, timeout=15)
            return success, output.strip() if success else output
        except Exception as e:
            return False, str(e)
    
    # === NETSTAT COMPLETO ===
    
    def get_all_connections(self) -> Tuple[bool, str]:
        """Obtener todas las conexiones de red"""
        try:
            if self.is_windows:
                cmd = 'netstat -ano'
            else:
                cmd = 'netstat -tunap'
            
            success, output = self._run_command(cmd)
            return success, output if success else output
        except Exception as e:
            return False, str(e)
    
    # === RUTAS ===
    
    def get_routes(self) -> Tuple[bool, str]:
        """Obtener tabla de rutas"""
        try:
            if self.is_windows:
                cmd = 'route print'
            else:
                cmd = 'netstat -rn'
            
            success, output = self._run_command(cmd)
            return success, output if success else output
        except Exception as e:
            return False, str(e)
    
    def add_route(self, destination: str, gateway: str, mask: str = "255.255.255.0") -> Tuple[bool, str]:
        """Agregar ruta"""
        try:
            if self.is_windows:
                cmd = f'route add {destination} mask {mask} {gateway}'
            else:
                cmd = f'sudo route add -net {destination} netmask {mask} gw {gateway}'
            
            success, output = self._run_command(cmd)
            return True, f"[OK] Ruta agregada" if success else output
        except Exception as e:
            return False, str(e)
    
    def delete_route(self, destination: str) -> Tuple[bool, str]:
        """Eliminar ruta"""
        try:
            if self.is_windows:
                cmd = f'route delete {destination}'
            else:
                cmd = f'sudo route del -net {destination}'
            
            success, output = self._run_command(cmd)
            return True, f"[OK] Ruta eliminada" if success else output
        except Exception as e:
            return False, str(e)
    
    # === ARP ===
    
    def get_arp_table(self) -> Tuple[bool, str]:
        """Obtener tabla ARP"""
        try:
            success, output = self._run_command(['arp', '-a'])
            return success, output if success else output
        except Exception as e:
            return False, str(e)
    
    # === HOSTNAME ===
    
    def resolve_hostname(self, hostname: str) -> Tuple[bool, str]:
        """Resolver hostname a IP"""
        try:
            ip = socket.gethostbyname(hostname)
            return True, ip
        except:
            return False, "No se pudo resolver"


# Instancia global
network = Network()
