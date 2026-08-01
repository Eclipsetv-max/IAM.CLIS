# -*- coding: utf-8 -*-
"""
IAM Loading - Animaciones de carga y estado de pensamiento
"""

import sys
import os
import time
import threading
from typing import Optional


class LoadingIndicator:
    """Indicador de carga con animaciones - compatible con Windows"""
    
    # Caracteres ASCII seguros para Windows (cp1252)
    SPINNERS = {
        'dots': ['.', '..', '...', '....', '...'],
        'line': ['-', '\\', '|', '/'],
        'clock': ['o', 'O', '0', 'O'],
        'arrow': ['>', '>>', '>>>', '>>>>', '>>>'],
        'bounce': ['*', '**', '***', '****', '***', '**'],
        'pulse': ['[ ]', '[.]', '[o]', '[O]', '[o]', '[.]', '[ ]'],
        'brain': ['*', '**', '***', '[OK]', '*'],
        'build': ['[ ]', '[*]', '[+]', '[#]', '[+]', '[*]', '[ ]'],
    }
    
    def __init__(self):
        self._stop_event = threading.Event()
        self._thread: Optional[threading.Thread] = None
        self._message: str = ""
        self._spinner_type: str = 'dots'
        self._is_running: bool = False
        self._lock = threading.Lock()
    
    def _animate(self):
        """Animacion en thread separado"""
        spinner = self.SPINNERS.get(self._spinner_type, self.SPINNERS['dots'])
        idx = 0
        dots = 0
        
        while not self._stop_event.is_set():
            with self._lock:
                char = spinner[idx % len(spinner)]
                dots_str = '.' * (dots % 4)
                
                try:
                    # Usar print con flush para forzar actualizacion
                    line = f'\r  {char} {self._message}{dots_str}   '
                    sys.stdout.buffer.write(line.encode('utf-8', errors='replace'))
                    sys.stdout.buffer.flush()
                except Exception:
                    try:
                        # Fallback a print
                        print(f'\r  {char} {self._message}{dots_str}   ', end='', flush=True)
                    except Exception:
                        pass
            
            idx += 1
            dots += 1
            
            # Esperar
            self._stop_event.wait(0.12)
        
        # Limpiar linea al terminar
        try:
            with self._lock:
                clean = '\r' + ' ' * 70 + '\r'
                sys.stdout.buffer.write(clean.encode('utf-8', errors='replace'))
                sys.stdout.buffer.flush()
        except Exception:
            try:
                print('\r' + ' ' * 70 + '\r', end='', flush=True)
            except:
                pass
    
    def start(self, message: str = "Procesando", spinner: str = 'dots'):
        """Iniciar animacion de carga"""
        self.stop()
        self._message = message
        self._spinner_type = spinner
        self._stop_event.clear()
        self._is_running = True
        
        self._thread = threading.Thread(target=self._animate, daemon=True)
        self._thread.start()
    
    def update_message(self, message: str):
        """Actualizar mensaje sin reiniciar animacion"""
        with self._lock:
            self._message = message
    
    def stop(self):
        """Detener animacion"""
        if self._is_running:
            self._stop_event.set()
            if self._thread:
                self._thread.join(timeout=1.0)
            self._is_running = False
            try:
                with self._lock:
                    clean = '\r' + ' ' * 70 + '\r'
                    sys.stdout.buffer.write(clean.encode('utf-8', errors='replace'))
                    sys.stdout.buffer.flush()
            except Exception:
                try:
                    print('\r' + ' ' * 70 + '\r', end='', flush=True)
                except:
                    pass
    
    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        self.stop()


class ThinkingAnimation:
    """Animacion de pensamiento profundo"""
    
    STAGES = [
        ('[*]', 'Analizando consulta', 'dots'),
        ('[>]', 'Identificando patrones', 'pulse'),
        ('[#]', 'Evaluando opciones', 'clock'),
        ('[+]', 'Generando solucion', 'brain'),
        ('[OK]', 'Verificando resultado', 'line'),
    ]
    
    def __init__(self, show_details: bool = False):
        self.indicator = LoadingIndicator()
        self.show_details = show_details
        self._current_stage = 0
    
    def start(self, query: str = ""):
        """Iniciar animacion de pensamiento"""
        self._current_stage = 0
        emoji, msg, spinner = self.STAGES[0]
        self.indicator.start(f'{emoji} {msg}', spinner)
    
    def next_stage(self):
        """Avanzar al siguiente stage"""
        self._current_stage += 1
        if self._current_stage < len(self.STAGES):
            emoji, msg, spinner = self.STAGES[self._current_stage]
            self.indicator.update_message(f'{emoji} {msg}')
    
    def stage(self, stage_num: int, message: str = ""):
        """Ir a un stage especifico"""
        if 0 <= stage_num < len(self.STAGES):
            self._current_stage = stage_num
            emoji, default_msg, spinner = self.STAGES[stage_num]
            msg = message or default_msg
            self.indicator.update_message(f'{emoji} {msg}')
    
    def stop(self):
        """Detener animacion"""
        self.indicator.stop()
    
    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        self.stop()
