# -*- coding: utf-8 -*-
"""
IAM Automation - Automatizacion de teclado y mouse
Escribir, clicks, atajos, mover mouse, etc.
"""

import subprocess
import platform
import time
from typing import Tuple, List, Optional


class Automation:
    """
    Automatizacion de teclado y mouse
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
    
    # === TECLADO ===
    
    def type_text(self, text: str) -> Tuple[bool, str]:
        """Escribir texto"""
        try:
            if self.is_windows:
                # Escapar caracteres especiales para PowerShell
                escaped = text.replace("'", "''").replace('"', '`"')
                cmd = f'''
                Add-Type -AssemblyName System.Windows.Forms
                [System.Windows.Forms.SendKeys]::SendWait("{escaped}")
                '''
                success, output = self._run_powershell(cmd)
                return True, f"[OK] Texto enviado" if success else output
            elif self.is_linux:
                cmd = ['xdotool', 'type', text]
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
                return True, "[OK] Texto enviado" if result.returncode == 0 else result.stderr
            return False, "No disponible"
        except Exception as e:
            return False, str(e)
    
    def press_key(self, key: str) -> Tuple[bool, str]:
        """Presionar una tecla"""
        try:
            key_map = {
                "enter": "{ENTER}",
                "tab": "{TAB}",
                "escape": "{ESC}",
                "esc": "{ESC}",
                "backspace": "{BACKSPACE}",
                "delete": "{DELETE}",
                "del": "{DELETE}",
                "space": " ",
                "up": "{UP}",
                "down": "{DOWN}",
                "left": "{LEFT}",
                "right": "{RIGHT}",
                "home": "{HOME}",
                "end": "{END}",
                "pageup": "{PGUP}",
                "pagedown": "{PGDN}",
                "f1": "{F1}", "f2": "{F2}", "f3": "{F3}", "f4": "{F4}",
                "f5": "{F5}", "f6": "{F6}", "f7": "{F7}", "f8": "{F8}",
                "f9": "{F9}", "f10": "{F10}", "f11": "{F11}", "f12": "{F12}",
                "ctrl": "^",
                "alt": "%",
                "shift": "+",
                "win": "^{ESC}"
            }
            
            ps_key = key_map.get(key.lower(), key)
            
            if self.is_windows:
                cmd = f'''
                Add-Type -AssemblyName System.Windows.Forms
                [System.Windows.Forms.SendKeys]::SendWait("{ps_key}")
                '''
                success, output = self._run_powershell(cmd)
                return True, f"[OK] Tecla '{key}' presionada" if success else output
            return False, "No disponible"
        except Exception as e:
            return False, str(e)
    
    def hotkey(self, *keys) -> Tuple[bool, str]:
        """Presionar combinacion de teclas"""
        try:
            if self.is_windows:
                # Convertir a formato PowerShell
                key_map = {
                    "ctrl": "^", "alt": "%", "shift": "+",
                    "enter": "{ENTER}", "tab": "{TAB}", "escape": "{ESC}",
                    "delete": "{DELETE}", "backspace": "{BACKSPACE}",
                    "home": "{HOME}", "end": "{END}",
                    "f1": "{F1}", "f2": "{F2}", "f3": "{F3}", "f4": "{F4}",
                    "f5": "{F5}", "f6": "{F6}", "f7": "{F7}", "f8": "{F8}",
                    "f9": "{F9}", "f10": "{F10}", "f11": "{F11}", "f12": "{F12}",
                    "a": "a", "b": "b", "c": "c", "d": "d", "e": "e", "f": "f",
                    "g": "g", "h": "h", "i": "i", "j": "j", "k": "k", "l": "l",
                    "m": "m", "n": "n", "o": "o", "p": "p", "q": "q", "r": "r",
                    "s": "s", "t": "t", "u": "u", "v": "v", "w": "w", "x": "x",
                    "y": "y", "z": "z", "0": "0", "1": "1", "2": "2", "3": "3",
                    "4": "4", "5": "5", "6": "6", "7": "7", "8": "8", "9": "9"
                }
                
                combo = "".join([key_map.get(k.lower(), k) for k in keys])
                cmd = f'''
                Add-Type -AssemblyName System.Windows.Forms
                [System.Windows.Forms.SendKeys]::SendWait("{combo}")
                '''
                success, output = self._run_powershell(cmd)
                return True, f"[OK] Combinacion '{'+'.join(keys)}' enviada" if success else output
            return False, "No disponible"
        except Exception as e:
            return False, str(e)
    
    # === MOUSE ===
    
    def move_mouse(self, x: int, y: int) -> Tuple[bool, str]:
        """Mover mouse a posicion"""
        try:
            if self.is_windows:
                cmd = f'''
                Add-Type -AssemblyName System.Windows.Forms
                [System.Windows.Forms.Cursor]::Position = New-Object System.Drawing.Point({x}, {y})
                '''
                success, output = self._run_powershell(cmd)
                return True, f"[OK] Mouse movido a ({x}, {y})" if success else output
            return False, "No disponible"
        except Exception as e:
            return False, str(e)
    
    def get_mouse_position(self) -> Tuple[bool, tuple]:
        """Obtener posicion actual del mouse"""
        try:
            if self.is_windows:
                cmd = '''
                Add-Type -AssemblyName System.Windows.Forms
                $pos = [System.Windows.Forms.Cursor]::Position
                "$($pos.X),$($pos.Y)"
                '''
                success, output = self._run_powershell(cmd)
                if success:
                    parts = output.strip().split(',')
                    return True, (int(parts[0]), int(parts[1]))
            return False, (0, 0)
        except Exception as e:
            return False, (0, 0)
    
    def click_mouse(self, button: str = "left", x: int = None, y: int = None) -> Tuple[bool, str]:
        """Hacer click"""
        try:
            if x and y:
                self.move_mouse(x, y)
                time.sleep(0.1)
            
            if self.is_windows:
                if button.lower() == "left":
                    click = "LEFT"
                elif button.lower() == "right":
                    click = "RIGHT"
                elif button.lower() == "middle":
                    click = "MIDDLE"
                else:
                    click = "LEFT"
                
                cmd = f'''
                Add-Type -AssemblyName System.Windows.Forms
                [System.Windows.Forms.SendKeys]::SendWait("{{{click}}}")
                '''
                success, output = self._run_powershell(cmd)
                return True, f"[OK] Click {button}" if success else output
            return False, "No disponible"
        except Exception as e:
            return False, str(e)
    
    def double_click(self, x: int = None, y: int = None) -> Tuple[bool, str]:
        """Hacer doble click"""
        try:
            if x and y:
                self.move_mouse(x, y)
                time.sleep(0.1)
            
            if self.is_windows:
                cmd = '''
                Add-Type -AssemblyName System.Windows.Forms
                [System.Windows.Forms.SendKeys]::SendWait("{LEFT}{LEFT}")
                '''
                success, output = self._run_powershell(cmd)
                return True, "[OK] Doble click" if success else output
            return False, "No disponible"
        except Exception as e:
            return False, str(e)
    
    def right_click(self, x: int = None, y: int = None) -> Tuple[bool, str]:
        """Hacer click derecho"""
        return self.click_mouse("right", x, y)
    
    def drag_mouse(self, start_x: int, start_y: int, end_x: int, end_y: int) -> Tuple[bool, str]:
        """Arrastrar mouse"""
        try:
            if self.is_windows:
                cmd = f'''
                Add-Type -AssemblyName System.Windows.Forms
                [System.Windows.Forms.Cursor]::Position = New-Object System.Drawing.Point({start_x}, {start_y})
                Start-Sleep -Milliseconds 100
                [System.Windows.Forms.SendKeys]::SendWait("{{LEFTDOWN}}")
                Start-Sleep -Milliseconds 100
                [System.Windows.Forms.Cursor]::Position = New-Object System.Drawing.Point({end_x}, {end_y})
                Start-Sleep -Milliseconds 100
                [System.Windows.Forms.SendKeys]::SendWait("{{LEFTUP}}")
                '''
                success, output = self._run_powershell(cmd)
                return True, "[OK] Arrastrado" if success else output
            return False, "No disponible"
        except Exception as e:
            return False, str(e)
    
    def scroll_mouse(self, clicks: int = 3) -> Tuple[bool, str]:
        """Scroll del mouse"""
        try:
            if self.is_windows:
                direction = "UP" if clicks > 0 else "DOWN"
                amount = abs(clicks)
                
                cmd = f'''
                Add-Type -AssemblyName System.Windows.Forms
                for ($i = 0; $i -lt {amount}; $i++) {{
                    [System.Windows.Forms.SendKeys]::SendWait("{{{direction}}}")
                    Start-Sleep -Milliseconds 50
                }}
                '''
                success, output = self._run_powershell(cmd)
                return True, f"[OK] Scroll {direction}" if success else output
            return False, "No disponible"
        except Exception as e:
            return False, str(e)
    
    # === SCREEN ===
    
    def get_screen_size(self) -> Tuple[bool, tuple]:
        """Obtener tamano de pantalla"""
        try:
            if self.is_windows:
                cmd = '''
                Add-Type -AssemblyName System.Windows.Forms
                $screen = [System.Windows.Forms.Screen]::PrimaryScreen
                "$($screen.Bounds.Width),$($screen.Bounds.Height)"
                '''
                success, output = self._run_powershell(cmd)
                if success:
                    parts = output.strip().split(',')
                    return True, (int(parts[0]), int(parts[1]))
            return False, (0, 0)
        except Exception as e:
            return False, (0, 0)
    
    # === CLIPBOARD ===
    
    def get_clipboard(self) -> Tuple[bool, str]:
        """Obtener contenido del clipboard"""
        try:
            if self.is_windows:
                cmd = 'Get-Clipboard'
                success, output = self._run_powershell(cmd)
                return success, output.strip() if success else output
            return False, "No disponible"
        except Exception as e:
            return False, str(e)
    
    def set_clipboard(self, text: str) -> Tuple[bool, str]:
        """Establecer contenido del clipboard"""
        try:
            if self.is_windows:
                escaped = text.replace("'", "''")
                cmd = f'Set-Clipboard -Value "{escaped}"'
                success, output = self._run_powershell(cmd)
                return True, "[OK] Clipboard actualizado" if success else output
            return False, "No disponible"
        except Exception as e:
            return False, str(e)
    
    def clear_clipboard(self) -> Tuple[bool, str]:
        """Limpiar clipboard"""
        try:
            if self.is_windows:
                cmd = 'Set-Clipboard -Value $null'
                success, output = self._run_powershell(cmd)
                return True, "[OK] Clipboard limpiado" if success else output
            return False, "No disponible"
        except Exception as e:
            return False, str(e)
    
    # === VENTANAS ===
    
    def get_active_window(self) -> Tuple[bool, str]:
        """Obtener ventana activa"""
        try:
            if self.is_windows:
                cmd = '''
                Add-Type @"
                using System;
                using System.Runtime.InteropServices;
                public class Win32 {{
                    [DllImport("user32.dll")]
                    public static extern IntPtr GetForegroundWindow();
                    [DllImport("user32.dll")]
                    public static extern int GetWindowText(IntPtr hWnd, System.Text.StringBuilder text, int count);
                }}
                "@
                $hwnd = [Win32]::GetForegroundWindow()
                $sb = New-Object System.Text.StringBuilder 256
                [Win32]::GetWindowText($hwnd, $sb, 256)
                $sb.ToString()
                '''
                success, output = self._run_powershell(cmd)
                return success, output.strip() if success else output
            return False, "No disponible"
        except Exception as e:
            return False, str(e)
    
    def minimize_window(self) -> Tuple[bool, str]:
        """Minimizar ventana activa"""
        return self.hotkey("win", "down")
    
    def maximize_window(self) -> Tuple[bool, str]:
        """Maximizar ventana activa"""
        return self.hotkey("win", "up")
    
    def close_window(self) -> Tuple[bool, str]:
        """Cerrar ventana activa"""
        return self.hotkey("alt", "f4")
    
    def switch_window(self) -> Tuple[bool, str]:
        """Cambiar ventana"""
        return self.hotkey("alt", "tab")
    
    # === APLICACIONES ===
    
    def open_app(self, app: str) -> Tuple[bool, str]:
        """Abrir aplicacion"""
        try:
            if self.is_windows:
                cmd = f'Start-Process "{app}"'
                success, output = self._run_powershell(cmd)
                return True, f"[OK] {app} abierto" if success else output
            return False, "No disponible"
        except Exception as e:
            return False, str(e)
    
    def open_file(self, filepath: str) -> Tuple[bool, str]:
        """Abrir archivo con aplicacion predeterminada"""
        try:
            if self.is_windows:
                cmd = f'Start-Process "{filepath}"'
                success, output = self._run_powershell(cmd)
                return True, f"[OK] Archivo abierto" if success else output
            return False, "No disponible"
        except Exception as e:
            return False, str(e)
    
    def open_url(self, url: str) -> Tuple[bool, str]:
        """Abrir URL en navegador"""
        try:
            if self.is_windows:
                cmd = f'Start-Process "{url}"'
                success, output = self._run_powershell(cmd)
                return True, f"[OK] URL abierta" if success else output
            return False, "No disponible"
        except Exception as e:
            return False, str(e)


# Instancia global
automation = Automation()
