# -*- coding: utf-8 -*-
"""
IAM Loading v2.0 - Animaciones de carga espectaculares
Spinners fluidos, barras de progreso, animaciones por fase y modo
"""

import sys
import os
import time
import threading
from typing import Optional, List, Callable


class LoadingIndicator:
    """Indicador de carga con animaciones fluidas y modernas"""

    # ── Spinners Unicode de alta calidad ──────────────────────────────────
    SPINNERS = {
        # Puntos arriados (general) - el clásico mejorado
        'dots': ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'],

        # Barra de progreso (builder) - efecto de carga
        'build': [
            '⣾  ', '⣽  ', '⣻  ', '⢿  ', '⡿  ', '⣟  ', '⣯  ', '⣷  ',
        ],

        # Línea giratoria (debug) - estilo radar
        'line': [' ◐ ', ' ◓ ', ' ◑ ', ' ◒ '],

        # Pulso de seguridad (security) - escudo animado
        'pulse': [
            '\033[38;2;74;222;128m━\033[0m━━━━━━━━━',
            '━\033[38;2;74;222;128m━\033[0m━━━━━━━━',
            '━━\033[38;2;74;222;128m━\033[0m━━━━━━━',
            '━━━\033[38;2;74;222;128m━\033[0m━━━━━━',
            '━━━━\033[38;2;74;222;128m━\033[0m━━━━━',
            '━━━━━\033[38;2;74;222;128m━\033[0m━━━━',
            '━━━━━━\033[38;2;74;222;128m━\033[0m━━━',
            '━━━━━━━\033[38;2;74;222;128m━\033[0m━━',
            '━━━━━━━━\033[38;2;74;222;128m━\033[0m━',
            '━━━━━━━━━\033[38;2;74;222;128m━\033[0m',
            '━━━━━━━━\033[38;2;74;222;128m━\033[0m━',
            '━━━━━━━\033[38;2;74;222;128m━\033[0m━━',
            '━━━━━━\033[38;2;74;222;128m━\033[0m━━━',
            '━━━━━\033[38;2;74;222;128m━\033[0m━━━━',
            '━━━━\033[38;2;74;222;128m━\033[0m━━━━━',
            '━━━\033[38;2;74;222;128m━\033[0m━━━━━━',
            '━━\033[38;2;74;222;128m━\033[0m━━━━━━━',
            '━\033[38;2;74;222;128m━\033[0m━━━━━━━━',
        ],

        # Reloj giratorio (reader) - barra rotativa
        'clock': [' ▰▱▱▱▱▱▱', ' ▰▰▱▱▱▱▱', ' ▰▰▰▱▱▱▱', ' ▰▰▰▰▱▱▱',
                  ' ▰▰▰▰▰▱▱', ' ▰▰▰▰▰▰▱', ' ▰▰▰▰▰▰▰', ' ▱▰▰▰▰▰▰',
                  ' ▱▱▰▰▰▰▰', ' ▱▱▱▰▰▰▰', ' ▱▱▱▱▰▰▰', ' ▱▱▱▱▱▰▰',
                  ' ▱▱▱▱▱▱▰'],

        # Cerebro pensante (think) - con efecto de brillo
        'brain': [
            '\033[38;2;168;85;247m●\033[0m○○○○',
            '○\033[38;2;168;85;247m●\033[0m○○○',
            '○○\033[38;2;168;85;247m●\033[0m○○',
            '○○○\033[38;2;168;85;247m●\033[0m○',
            '○○○○\033[38;2;168;85;247m●\033[0m',
            '○○○\033[38;2;168;85;247m●\033[0m○',
            '○○\033[38;2;168;85;247m●\033[0m○○',
            '○\033[38;2;168;85;247m●\033[0m○○○',
        ],

        # Flechas (arrow) - directional
        'arrow': [' ➜    ', '  ➜   ', '   ➜  ', '    ➜ ', '     ➜', '    ➜ ',
                  '   ➜  ', '  ➜   '],

        # Cyberpunk (cyber) - matrix style
        'cyber': [' ▁▂▃▄▅▆▇█', ' ▂▃▄▅▆▇█▁', ' ▃▄▅▆▇█▁▂', ' ▄▅▆▇█▁▂▃',
                  ' ▅▆▇█▁▂▃▄', ' ▆▇█▁▂▃▄▅', ' ▇█▁▂▃▄▅▆', ' █▁▂▃▄▅▆▇',
                  ' ▇█▁▂▃▄▅▆', ' ▆▇█▁▂▃▄▅', ' ▅▆▇█▁▂▃▄', ' ▄▅▆▇█▁▂▃',
                  ' ▃▄▅▆▇█▁▂', ' ▂▃▄▅▆▇█▁'],

        # Dots bouncing (bounce) - energetic
        'bounce': [
            '    ●   ', '   ●    ', '  ●     ', ' ●      ',
            '●       ', ' ●      ', '  ●     ', '   ●    ',
        ],

        # Spinner clásico suave (smooth) - para operaciones largas
        'smooth': [
            '\033[38;2;99;102;241m◜\033[0m', '\033[38;2;99;102;241m◜\033[0m',
            '\033[38;2;120;120;250m◜\033[0m', '\033[38;2;140;140;255m◜\033[0m',
            '\033[38;2;160;160;255m◝\033[0m', '\033[38;2;140;140;255m◝\033[0m',
            '\033[38;2;120;120;250m◞\033[0m', '\033[38;2;99;102;241m◞\033[0m',
            '\033[38;2;80;80;230m◟\033[0m', '\033[38;2;99;102;241m◟\033[0m',
        ],

        # Wave (wave) - onda sinusoidal
        'wave': [
            '▁▂▃▄▃▂', '▂▃▄▅▄▃', '▃▄▅▆▅▄', '▄▅▆▇▆▅',
            '▅▆▇█▇▆', '▆▇█▉█▇', '▇█▉▉▉█', '█▉▉▉▉▉',
            '▇█▉▉▉█', '▆▇█▉█▇', '▅▆▇▆▅▆', '▄▅▆▅▄▅',
            '▃▄▃▂▃▄', '▂▃▂▁▂▃', '▁▂▁▁▁▂',
        ],

        # Typewriter (type) - para texto
        'type': [' ⣾ ', ' ⣽ ', ' ⣻ ', ' ⢿ ', ' ⡿ ', ' ⣟ ', ' ⣯ ', ' ⣷ '],

        # Orbit (orbit) - para análisis
        'orbit': [
            '◉───────', '─◉──────', '──◉─────', '───◉────',
            '────◉───', '─────◉──', '──────◉─', '───────◉',
            '──────◉─', '─────◉──', '────◉───', '───◉────',
            '──◉─────', '─◉──────',
        ],

        # Bars loading (bars) - para descargas
        'bars': [
            '░░░░░░░░░░', '█░░░░░░░░░', '██░░░░░░░░', '███░░░░░░░',
            '████░░░░░░', '█████░░░░░', '██████░░░░', '███████░░░',
            '████████░░', '█████████░', '██████████', '░█████████',
            '░░████████', '░░░███████', '░░░░██████', '░░░░░█████',
            '░░░░░░████', '░░░░░░░░██', '░░░░░░░░░█',
        ],

        # Dots vertical (dots_v) - para compilación
        'dots_v': [' ', ' ▁ ', ' ▂ ', ' ▃ ', ' ▄ ', ' ▅ ', ' ▆ ', ' ▇ ', ' █ ',
                   ' ▇ ', ' ▆ ', ' ▅ ', ' ▄ ', ' ▃ ', ' ▂ ', ' ▁ '],

        # Moon phases (moon) - para operaciones nocturnas
        'moon': ['🌑', '🌒', '🌓', '🌔', '🌕', '🌖', '🌗', '🌘'],
    }

    # ── Colores ANSI por spinner / modo ──────────────────────────────────
    SPINNER_COLORS = {
        'dots':    '\033[38;2;34;211;238m',   # CYAN
        'build':   '\033[38;2;249;115;22m',   # ORANGE
        'line':    '\033[38;2;239;68;68m',    # RED
        'pulse':   '\033[38;2;74;222;128m',   # GREEN
        'clock':   '\033[38;2;250;204;21m',   # YELLOW
        'brain':   '\033[38;2;168;85;247m',   # PURPLE
        'arrow':   '\033[38;2;59;130;246m',   # BLUE
        'cyber':   '\033[38;2;236;72;153m',   # PINK
        'bounce':  '\033[38;2;251;146;60m',   # ORANGE-BRIGHT
        'smooth':  '\033[38;2;99;102;241m',   # INDIGO
        'wave':    '\033[38;2;56;189;248m',   # SKY
        'type':    '\033[38;2;248;113;113m',  # ROSE
        'orbit':   '\033[38;2;132;204;22m',   # LIME
        'bars':    '\033[38;2;251;191;36m',   # AMBER
        'dots_v':  '\033[38;2;147;197;253m',  # BLUE-LIGHT
        'moon':    '\033[38;2;253;224;71m',   # YELLOW-BRIGHT
    }

    # ── Animaciones por contexto de acción ───────────────────────────────
    ACTION_ANIMATIONS = {
        'create_file':  {'spinner': 'build',  'prefix': 'creando',  'icon': '📄'},
        'edit_file':    {'spinner': 'smooth', 'prefix': 'editando', 'icon': '✏️'},
        'read_file':    {'spinner': 'type',   'prefix': 'leyendo',  'icon': '📖'},
        'execute':      {'spinner': 'wave',   'prefix': 'ejecutando', 'icon': '⚡'},
        'create_folder':{'spinner': 'orbit',  'prefix': 'creando',  'icon': '📁'},
        'delete':       {'spinner': 'line',   'prefix': 'eliminando', 'icon': '🗑️'},
        'search':       {'spinner': 'dots_v', 'prefix': 'buscando', 'icon': '🔍'},
        'thinking':     {'spinner': 'brain',  'prefix': 'pensando', 'icon': '🧠'},
        'analyzing':    {'spinner': 'orbit',  'prefix': 'analizando', 'icon': '🔬'},
        'validating':   {'spinner': 'pulse',  'prefix': 'validando', 'icon': '✅'},
        'compiling':    {'spinner': 'bars',   'prefix': 'compilando', 'icon': '⚙️'},
        'connecting':   {'spinner': 'dots',   'prefix': 'conectando', 'icon': '🌐'},
        'loading':      {'spinner': 'smooth', 'prefix': 'cargando', 'icon': '📦'},
    }

    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    
    def __init__(self):
        self._stop_event = threading.Event()
        self._thread: Optional[threading.Thread] = None
        self._message: str = ""
        self._spinner_type: str = 'dots'
        self._is_running: bool = False
        self._lock = threading.Lock()
        self._phase: int = 0
        self._start_time: float = 0
        self._context: str = ""
        self._progress: float = 0.0  # 0.0 a 1.0
        self._total_steps: int = 0
        self._current_step: int = 0
    
    def _build_spinner_line(self, char: str, color: str) -> str:
        """Construir la línea completa del spinner con formato"""
        elapsed = time.time() - self._start_time if self._start_time else 0
        elapsed_str = f"{elapsed:.1f}s" if elapsed > 0.1 else ""

        # Barra de progreso si hay steps
        progress_bar = ""
        if self._total_steps > 0 and self._current_step > 0:
            bar_width = 20
            filled = int(bar_width * (self._current_step / self._total_steps))
            bar = '█' * filled + '░' * (bar_width - filled)
            pct = int(100 * self._current_step / self._total_steps)
            progress_bar = f' [{bar}] {pct}%'

        # Formato final
        parts = [
            f'\r  {color}{self.BOLD}{char}{self.RESET}',
            f' {self.BOLD}{self._message}{self.RESET}',
        ]
        if progress_bar:
            parts.append(f' {self.DIM}{progress_bar}{self.RESET}')
        if elapsed_str:
            parts.append(f' {self.DIM}{elapsed_str}{self.RESET}')
        parts.append('   ')

        return ''.join(parts)

    def _animate(self):
        """Animación fluida en thread separado"""
        spinner = self.SPINNERS.get(self._spinner_type, self.SPINNERS['dots'])
        color = self.SPINNER_COLORS.get(self._spinner_type, self.SPINNER_COLORS['dots'])
        idx = 0
        
        while not self._stop_event.is_set():
            with self._lock:
                char = spinner[idx % len(spinner)]
                
                try:
                    line = self._build_spinner_line(char, color)
                    sys.stdout.buffer.write(line.encode('utf-8', errors='replace'))
                    sys.stdout.buffer.flush()
                except Exception:
                    try:
                        print(f'\r  {char} {self._message}   ', end='', flush=True)
                    except Exception:
                        pass
            
            idx += 1
            # Velocidad adaptativa: más rápido al inicio, más lento después
            if idx < 10:
                self._stop_event.wait(0.06)
            else:
                self._stop_event.wait(0.08)
        
        # Limpiar línea al terminar
        self._clear_line()
    
    def _clear_line(self):
        """Limpiar la línea de la terminal"""
        try:
            with self._lock:
                clean = '\r' + ' ' * 100 + '\r'
                sys.stdout.buffer.write(clean.encode('utf-8', errors='replace'))
                sys.stdout.buffer.flush()
        except Exception:
            try:
                print('\r' + ' ' * 100 + '\r', end='', flush=True)
            except:
                pass

    def start(self, message: str = "Procesando", spinner: str = 'dots'):
        """Iniciar animación de carga"""
        self.stop()
        self._message = message
        self._spinner_type = spinner
        self._stop_event.clear()
        self._is_running = True
        self._start_time = time.time()
        self._phase = 0
        self._progress = 0.0
        self._current_step = 0
        self._total_steps = 0
        
        self._thread = threading.Thread(target=self._animate, daemon=True)
        self._thread.start()
    
    def start_action(self, action: str, filename: str = "", extra: str = ""):
        """Iniciar animación contextual por tipo de acción"""
        config = self.ACTION_ANIMATIONS.get(action, self.ACTION_ANIMATIONS['thinking'])
        spinner = config['spinner']
        icon = config['icon']
        prefix = config['prefix']

        msg = f"{icon} {prefix}"
        if filename:
            msg += f": {os.path.basename(filename)}"
        if extra:
            msg += f" {extra}"

        self.start(msg, spinner)
    
    def start_progress(self, message: str, total_steps: int, spinner: str = 'build'):
        """Iniciar animación con barra de progreso"""
        self.start(message, spinner)
        self._total_steps = total_steps
        self._current_step = 0
    
    def update_progress(self, step: int, message: str = ""):
        """Actualizar progreso"""
        with self._lock:
            self._current_step = step
            if message:
                self._message = message
    
    def advance_progress(self, message: str = ""):
        """Avanzar un paso en el progreso"""
        with self._lock:
            self._current_step += 1
            if message:
                self._message = message
    
    def update_message(self, message: str):
        """Actualizar mensaje dinámicamente"""
        with self._lock:
            self._message = message
    
    def next_phase(self, message: str = ""):
        """Avanzar a la siguiente fase con nuevo mensaje"""
        with self._lock:
            self._phase += 1
            if message:
                self._message = message
    
    def stop(self):
        """Detener animación"""
        if self._is_running:
            self._stop_event.set()
            if self._thread:
                self._thread.join(timeout=1.0)
            self._is_running = False
            self._clear_line()
    
    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        self.stop()


class ToolCallProgress:
    """Barra de progreso visual para ejecución de TOOL_CALLs"""

    COLORS = {
        'ok':     '\033[38;2;74;222;128m',   # GREEN
        'error':  '\033[38;2;239;68;68m',    # RED
        'warn':   '\033[38;2;251;191;36m',   # AMBER
        'info':   '\033[38;2;99;102;241m',   # INDIGO
        'dim':    '\033[2m',
        'bold':   '\033[1m',
        'reset':  '\033[0m',
    }

    def __init__(self, total: int):
        self.total = total
        self.current = 0
        self.results = []
        self.start_time = time.time()

    def _format_time(self, seconds: float) -> str:
        """Formatear tiempo de forma legible"""
        if seconds < 0.1:
            return ""
        if seconds < 60:
            return f"{seconds:.1f}s"
        mins = int(seconds // 60)
        secs = seconds % 60
        return f"{mins}m {secs:.0f}s"

    def _build_bar(self) -> str:
        """Construir barra de progreso visual"""
        c = self.COLORS
        bar_width = 25
        filled = int(bar_width * (self.current / self.total)) if self.total > 0 else 0
        empty = bar_width - filled

        bar = f"{c['ok']}{'█' * filled}{c['dim']}{'░' * empty}{c['reset']}"
        pct = int(100 * self.current / self.total) if self.total > 0 else 0
        elapsed = self._format_time(time.time() - self.start_time)

        line = f"\r  {c['info']}  {c['reset']} {bar} {c['bold']}{pct:3d}%{c['reset']}"
        if elapsed:
            line += f" {c['dim']}{elapsed}{c['reset']}"
        line += "   "
        return line

    def update(self, index: int, filename: str, success: bool, size_str: str = ""):
        """Actualizar progreso con resultado de archivo"""
        self.current = index
        c = self.COLORS

        icon = f"{c['ok']}✓{c['reset']}" if success else f"{c['error']}✗{c['reset']}"
        status = "OK" if success else "ERROR"

        try:
            bar_line = self._build_bar()
            sys.stdout.buffer.write(bar_line.encode('utf-8', errors='replace'))
            sys.stdout.buffer.flush()
        except:
            pass

        self.results.append({
            'file': filename,
            'success': success,
            'size': size_str,
            'status': status,
        })

    def finish(self) -> str:
        """Finalizar y generar reporte"""
        c = self.COLORS
        elapsed = time.time() - self.start_time

        ok_count = sum(1 for r in self.results if r['success'])
        err_count = sum(1 for r in self.results if not r['success'])

        # Limpiar barra
        try:
            clean = '\r' + ' ' * 80 + '\r'
            sys.stdout.buffer.write(clean.encode('utf-8', errors='replace'))
            sys.stdout.buffer.flush()
        except:
            pass

        # Generar reporte con caracteres ASCII seguros
        lines = []

        # Resumen visual
        if ok_count > 0:
            lines.append(f"  {c['ok']}{c['bold']}{ok_count} OK{c['reset']}")
        if err_count > 0:
            lines.append(f"  {c['error']}{c['bold']}{err_count} ERROR{c['reset']}")
        if elapsed > 0:
            lines.append(f"  {c['dim']}{self._format_time(elapsed)}{c['reset']}")

        return " ".join(lines)


class ThinkingAnimation:
    """Animación de pensamiento profundo por fases con transiciones suaves"""
    
    STAGES = [
        {
            'icon': '🔍',
            'message': 'Analizando consulta y estructura',
            'spinner': 'orbit',
            'color': '\033[38;2;56;189;248m',
            'duration': 0.8,
        },
        {
            'icon': '🧩',
            'message': 'Identificando patrones y componentes',
            'spinner': 'brain',
            'color': '\033[38;2;168;85;247m',
            'duration': 1.0,
        },
        {
            'icon': '🏗️',
            'message': 'Diseñando arquitectura del código',
            'spinner': 'build',
            'color': '\033[38;2;249;115;22m',
            'duration': 1.2,
        },
        {
            'icon': '⚡',
            'message': 'Generando código limpio y funcional',
            'spinner': 'wave',
            'color': '\033[38;2;56;189;248m',
            'duration': 1.5,
        },
        {
            'icon': '✅',
            'message': 'Validando calidad y sintaxis',
            'spinner': 'pulse',
            'color': '\033[38;2;74;222;128m',
            'duration': 0.6,
        },
        {
            'icon': '🎨',
            'message': 'Aplicando estilo y formato final',
            'spinner': 'smooth',
            'color': '\033[38;2;236;72;153m',
            'duration': 0.5,
        },
    ]

    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    
    def __init__(self, show_details: bool = False):
        self.indicator = LoadingIndicator()
        self.show_details = show_details
        self._current_stage = 0
        self._stage_start = 0
        self._completed_stages = []
    
    def _show_stage_transition(self):
        """Mostrar transición visual entre fases"""
        if self._completed_stages and self.show_details:
            try:
                last = self._completed_stages[-1]
                c = self.COLORS.get(last.get('spinner', ''), '\033[0m')
                transition = f"\r  {c}  ✓ {last['icon']} {last['message']}{self.RESET}\n"
                sys.stdout.buffer.write(transition.encode('utf-8', errors='replace'))
                sys.stdout.buffer.flush()
            except:
                pass
    
    @property
    def COLORS(self):
        return LoadingIndicator.SPINNER_COLORS
    
    def start(self, query: str = ""):
        """Iniciar animación de pensamiento"""
        self._current_stage = 0
        self._completed_stages = []
        self._stage_start = time.time()
        stage = self.STAGES[0]
        self.indicator.start(f"{stage['icon']} {stage['message']}", stage['spinner'])
    
    def next_stage(self):
        """Avanzar al siguiente stage con transición"""
        # Guardar stage completado
        if self._current_stage < len(self.STAGES):
            self._completed_stages.append(self.STAGES[self._current_stage])

        self._current_stage += 1
        self._stage_start = time.time()

        if self._current_stage < len(self.STAGES):
            stage = self.STAGES[self._current_stage]
            self.indicator.start(f"{stage['icon']} {stage['message']}", stage['spinner'])
    
    def stage(self, stage_num: int, message: str = ""):
        """Ir a un stage específico"""
        if 0 <= stage_num < len(self.STAGES):
            self._current_stage = stage_num
            self._stage_start = time.time()
            stage = self.STAGES[stage_num]
            msg = message or stage['message']
            self.indicator.start(f"{stage['icon']} {msg}", stage['spinner'])
    
    def stop(self):
        """Detener animación"""
        self.indicator.stop()
    
    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        self.stop()


class PhaseAnimation:
    """Animación con múltiples fases visuales progresivas"""

    def __init__(self, phases: List[dict] = None):
        """
        phases: lista de dicts con keys:
            - message: str
            - spinner: str (key del SPINNERS de LoadingIndicator)
            - icon: str (emoji)
        """
        self.phases = phases or []
        self.indicator = LoadingIndicator()
        self._current = 0
        self._completed = []

    def start(self):
        """Iniciar en la primera fase"""
        if self.phases:
            self._current = 0
            p = self.phases[0]
            self.indicator.start(f"{p.get('icon', '●')} {p['message']}", p.get('spinner', 'smooth'))

    def advance(self, message: str = ""):
        """Avanzar a la siguiente fase"""
        # Guardar la actual
        if self._current < len(self.phases):
            self._completed.append(self.phases[self._current])

        self._current += 1
        if self._current < len(self.phases):
            p = self.phases[self._current]
            msg = message or f"{p.get('icon', '●')} {p['message']}"
            self.indicator.start(msg, p.get('spinner', 'smooth'))

    def set_phase(self, index: int, message: str = ""):
        """Saltar a una fase específica"""
        if 0 <= index < len(self.phases):
            self._current = index
            p = self.phases[index]
            msg = message or f"{p.get('icon', '●')} {p['message']}"
            self.indicator.start(msg, p.get('spinner', 'smooth'))

    def stop(self):
        """Detener animación"""
        self.indicator.stop()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.stop()
