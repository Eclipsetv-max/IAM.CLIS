# -*- coding: utf-8 -*-
"""
IAM Enhanced CLI v3.0 - Claude Code-like Experience
Streaming, Multi-line, Diff Editor, Permissions, Context Window
"""

import os
import re
import sys
import json
import time
import hashlib
import threading
from pathlib import Path
from typing import List, Optional, Dict, Tuple, Callable, Generator
from difflib import get_close_matches, unified_diff
from datetime import datetime
from dataclasses import dataclass, field

try:
    from prompt_toolkit import PromptSession
    from prompt_toolkit.completion import Completer, Completion, PathCompleter
    from prompt_toolkit.history import FileHistory
    from prompt_toolkit.styles import Style
    from prompt_toolkit.formatted_text import HTML
    from prompt_toolkit.key_binding import KeyBindings
    from prompt_toolkit.buffer import Buffer
    from prompt_toolkit.layout import Window, BufferControl
    from prompt_toolkit.layout.containers import HSplit, VSplit
    HAS_PROMPT_TOOLKIT = True
except ImportError:
    HAS_PROMPT_TOOLKIT = False

from rich.console import Console
from rich.markdown import Markdown
from rich.syntax import Syntax
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.live import Live
from rich import box

from ..config.settings import settings, COLORS


# ============================================================================
# CONSTANTS
# ============================================================================

MAX_CONTEXT_TOKENS = 200000
TOKENS_PER_CHAR = 0.25

THEMES = {
    "claude": {
        "name": "Claude",
        "primary": "\033[38;2;189;147;249m",
        "accent": "\033[38;2;255;121;198m",
        "success": "\033[38;2;80;250;123m",
        "error": "\033[38;2;255;85;85m",
        "warning": "\033[38;2;241;250;140m",
        "dim": "\033[2m",
        "reset": "\033[0m",
        "prompt_char": "\033[38;2;189;147;249m>\033[0m",
    },
    "cyberpunk": {
        "name": "Cyberpunk",
        "primary": "\033[38;2;0;255;255m",
        "accent": "\033[38;2;255;0;255m",
        "success": "\033[38;2;0;255;128m",
        "error": "\033[38;2;255;0;64m",
        "warning": "\033[38;2;255;255;0m",
        "dim": "\033[2m",
        "reset": "\033[0m",
        "prompt_char": "\033[38;2;0;255;255m>\033[0m",
    },
    "dracula": {
        "name": "Dracula",
        "primary": "\033[38;2;189;147;249m",
        "accent": "\033[38;2;255;121;198m",
        "success": "\033[38;2;80;250;123m",
        "error": "\033[38;2;255;85;85m",
        "warning": "\033[38;2;241;250;140m",
        "dim": "\033[2m",
        "reset": "\033[0m",
        "prompt_char": "\033[38;2;189;147;249m>\033[0m",
    },
    "nord": {
        "name": "Nord",
        "primary": "\033[38;2;136;192;208m",
        "accent": "\033[38;2;143;188;187m",
        "success": "\033[38;2;163;190;140m",
        "error": "\033[38;2;191;97;106m",
        "warning": "\033[38;2;235;203;139m",
        "dim": "\033[2m",
        "reset": "\033[0m",
        "prompt_char": "\033[38;2;136;192;208m>\033[0m",
    },
    "monokai": {
        "name": "Monokai",
        "primary": "\033[38;2;166;226;46m",
        "accent": "\033[38;2;249;38;114m",
        "success": "\033[38;2;166;226;46m",
        "error": "\033[38;2;249;38;114m",
        "warning": "\033[38;2;253;151;31m",
        "dim": "\033[2m",
        "reset": "\033[0m",
        "prompt_char": "\033[38;2;166;226;46m>\033[0m",
    },
    "default": {
        "name": "Default",
        "primary": "\033[36m",
        "accent": "\033[38;2;0;212;170m",
        "success": "\033[32m",
        "error": "\033[31m",
        "warning": "\033[33m",
        "dim": "\033[2m",
        "reset": "\033[0m",
        "prompt_char": "\033[36m>\033[0m",
    },
}


# ============================================================================
# CONTEXT WINDOW DISPLAY
# ============================================================================

class ContextWindow:
    """Muestra el uso del contexto estilo Claude"""

    def __init__(self, max_tokens: int = MAX_CONTEXT_TOKENS):
        self.max_tokens = max_tokens
        self.messages: List[Dict] = []
        self.total_tokens = 0

    def add_message(self, role: str, content: str):
        tokens = int(len(content) * TOKENS_PER_CHAR)
        self.messages.append({
            "role": role,
            "content": content[:500],
            "tokens": tokens,
            "timestamp": datetime.now(),
        })
        self.total_tokens += tokens

        while self.total_tokens > self.max_tokens and len(self.messages) > 1:
            removed = self.messages.pop(0)
            self.total_tokens -= removed["tokens"]

    def get_usage_bar(self) -> str:
        usage = self.total_tokens / self.max_tokens
        bar_len = 30
        filled = int(bar_len * usage)

        if usage < 0.5:
            color = "\033[32m"
        elif usage < 0.8:
            color = "\033[33m"
        else:
            color = "\033[31m"

        bar = "#" * filled + "-" * (bar_len - filled)
        return f"{color}{bar} {usage*100:.1f}% ({self.total_tokens}/{self.max_tokens} tokens)\033[0m"

    def get_usage_panel(self) -> Panel:
        usage = self.total_tokens / self.max_tokens
        color = "green" if usage < 0.5 else "yellow" if usage < 0.8 else "red"

        table = Table(show_header=False, box=None, padding=(0, 1))
        table.add_column("Key", style="dim")
        table.add_column("Value")

        table.add_row("Contexto", self.get_usage_bar())
        table.add_row("Mensajes", str(len(self.messages)))
        table.add_row("Restante", f"{self.max_tokens - self.total_tokens:,} tokens")

        return Panel(table, title="Context Window", border_style=color, padding=(0, 1))


# ============================================================================
# SMART SUGGESTIONS
# ============================================================================

class SmartSuggestions:
    """Sugiere acciones siguientes como Claude"""

    def __init__(self):
        self.suggestion_patterns = {
            "create_file": [
                "Abrir el archivo creado",
                "Ejecutar el archivo",
                "/folder Vincular proyecto",
            ],
            "error": [
                "Revisar el error",
                "Buscar solucion",
                "Reintentar",
            ],
            "code": [
                "Analizar el codigo",
                "Ejecutar pruebas",
                "Formatear codigo",
            ],
            "git": [
                "Ver estado",
                "Hacer commit",
                "Subir cambios",
            ],
            "question": [
                "Buscar mas informacion",
                "Ver documentacion",
                "Probar ejemplo",
            ],
        }

    def get_suggestions(self, response: str, query: str) -> List[str]:
        response_lower = response.lower()
        query_lower = query.lower()

        suggestions = []

        if any(w in response_lower for w in ["creado", "archivo creado", "new file"]):
            suggestions.extend(self.suggestion_patterns["create_file"][:2])

        if any(w in response_lower for w in ["error", "fallo", "failed"]):
            suggestions.extend(self.suggestion_patterns["error"][:2])

        if any(w in response_lower for w in ["def ", "class ", "function"]):
            suggestions.extend(self.suggestion_patterns["code"][:2])

        if "?" in query:
            suggestions.extend(self.suggestion_patterns["question"][:1])

        if not suggestions:
            suggestions = ["Continuar", "Ver ayuda"]

        return suggestions[:3]

    def format_suggestions(self, suggestions: List[str]) -> Text:
        text = Text("  \u2192 Sugerencias: ", style="dim italic")
        for i, s in enumerate(suggestions):
            text.append(f"[{i+1}]", style="cyan bold")
            text.append(f" {s}", style="white")
            if i < len(suggestions) - 1:
                text.append("  ", style="dim")
        return text


# ============================================================================
# SESSION MANAGER UI
# ============================================================================

class SessionManagerUI:
    """UI para gestionar sesiones estilo Claude"""

    def __init__(self, console: Console):
        self.console = console
        self.sessions_dir = settings.DATA_DIR / "sessions"
        self.sessions_dir.mkdir(exist_ok=True)
        self.current_session_id = None

    def create_session(self, name: str = None) -> str:
        session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        if name:
            session_id = f"{name}_{session_id}"

        session_file = self.sessions_dir / f"{session_id}.json"
        session_data = {
            "id": session_id,
            "name": name or "Session",
            "created_at": datetime.now().isoformat(),
            "messages": [],
            "metadata": {},
        }

        with open(session_file, "w", encoding="utf-8") as f:
            json.dump(session_data, f, indent=2, ensure_ascii=False)

        self.current_session_id = session_id
        return session_id

    def list_sessions(self) -> List[Dict]:
        sessions = []
        for f in sorted(self.sessions_dir.glob("*.json"), reverse=True):
            try:
                with open(f, "r", encoding="utf-8") as fp:
                    data = json.load(fp)
                    sessions.append(data)
            except Exception:
                pass
        return sessions

    def show_sessions(self):
        sessions = self.list_sessions()

        if not sessions:
            self.console.print("  [dim]No hay sesiones previas[/dim]")
            return

        table = Table(title="Sesiones", box=box.ROUNDED, border_style="cyan")
        table.add_column("ID", style="cyan", width=20)
        table.add_column("Nombre", style="white")
        table.add_column("Fecha", style="dim")
        table.add_column("Mensajes", style="green")

        for s in sessions[:10]:
            msg_count = len(s.get("messages", []))
            created = s.get("created_at", "")[:16]
            current = " <<<" if s.get("id") == self.current_session_id else ""
            table.add_row(
                s.get("id", "?"),
                s.get("name", "?"),
                created,
                str(msg_count),
            )

        self.console.print(table)

    def load_session(self, session_id: str) -> Optional[Dict]:
        session_file = self.sessions_dir / f"{session_id}.json"
        if session_file.exists():
            with open(session_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.current_session_id = session_id
                return data
        return None

    def save_message(self, role: str, content: str):
        if not self.current_session_id:
            return

        session_file = self.sessions_dir / f"{self.current_session_id}.json"
        if session_file.exists():
            with open(session_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            data["messages"].append({
                "role": role,
                "content": content[:1000],
                "timestamp": datetime.now().isoformat(),
            })

            with open(session_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)


# ============================================================================
# STATS TRACKER
# ============================================================================

class StatsTracker:
    """Trackea estadisticas de la sesion"""

    def __init__(self):
        self.session_start = datetime.now()
        self.commands_run = 0
        self.queries_to_ai = 0
        self.total_response_time = 0.0
        self.errors = 0
        self.responses_saved = 0

    def track_command(self):
        self.commands_run += 1

    def track_ai_query(self, response_time: float):
        self.queries_to_ai += 1
        self.total_response_time += response_time

    def track_error(self):
        self.errors += 1

    def track_save(self):
        self.responses_saved += 1

    @property
    def avg_response_time(self) -> float:
        if self.queries_to_ai == 0:
            return 0.0
        return self.total_response_time / self.queries_to_ai

    @property
    def session_duration(self) -> str:
        delta = datetime.now() - self.session_start
        minutes = int(delta.total_seconds() / 60)
        seconds = int(delta.total_seconds() % 60)
        return f"{minutes}m {seconds}s"


# ============================================================================
# ALIASES
# ============================================================================

DEFAULT_ALIASES = {
    "ll": "/ls -la",
    "..": "/ls ..",
    "cls": "clear",
    "h": "help",
    "?": "help",
    "q": "exit",
    "x": "exit",
    "ip": "/ip",
    "cpu": "/cpu",
    "ram": "/mem",
    "gpu": "/gpu",
    "disk": "/disk",
    "proc": "/proc",
    "ps": "/proc",
    "net": "/net",
    "wifi": "/wifi",
    "hw": "/hardware",
    "git": "/git status",
    "gs": "/git status",
    "ga": "/git add .",
    "gc": "/git commit",
    "gp": "/git push",
    "gl": "/git log",
    "status": "/status",
    "sys": "/hardware",
    "bash": "/run",
    "python": "/py",
    "pip": "/pip-list",
    "htop": "/top",
    "ping": "/ping",
    "scan": "/scan",
    "ports": "/ports",
    "firewall": "/firewall",
    "users": "/usuarios",
    "logs": "/logs",
    "backup": "/backup",
    "encrypt": "/encrypt",
    "decrypt": "/decrypt",
    "hash": "/hash",
    "db": "/sqlite-query",
    "sql": "/sqlite-query",
    "api": "/get",
    "curl": "/get",
    "wget": "/download",
    "dl": "/download",
    "install": "/pip-install",
    "uninstall": "/pip-uninstall",
}


class AliasManager:
    def __init__(self):
        self.aliases_file = settings.DATA_DIR / "aliases.json"
        self.aliases: Dict[str, str] = dict(DEFAULT_ALIASES)
        self._load_custom()

    def _load_custom(self):
        if self.aliases_file.exists():
            try:
                with open(self.aliases_file, "r", encoding="utf-8") as f:
                    self.aliases.update(json.load(f))
            except Exception:
                pass

    def save(self):
        custom = {k: v for k, v in self.aliases.items() if k not in DEFAULT_ALIASES}
        with open(self.aliases_file, "w", encoding="utf-8") as f:
            json.dump(custom, f, indent=2, ensure_ascii=False)

    def resolve(self, text: str) -> str:
        parts = text.strip().split(None, 1)
        if not parts:
            return text
        cmd = parts[0].lower()
        if cmd in self.aliases:
            rest = parts[1] if len(parts) > 1 else ""
            return f"{self.aliases[cmd]} {rest}".strip()
        return text

    def add(self, name: str, command: str):
        self.aliases[name.lower()] = command
        self.save()

    def remove(self, name: str) -> bool:
        if name.lower() in self.aliases and name.lower() not in DEFAULT_ALIASES:
            del self.aliases[name.lower()]
            self.save()
            return True
        return False


# ============================================================================
# COMMANDS
# ============================================================================

COMMANDS = [
    "/help", "/status", "/mode", "/engine", "/model", "/think", "/level",
    "/memory", "/recall", "/forget", "/sessions", "/new", "/switch", "/clear",
    "/mkdir", "/touch", "/ls", "/cat", "/edit", "/rm", "/mv", "/cp",
    "/find", "/grep", "/disk", "/info", "/tree", "/hash", "/diff",
    "/zip", "/unzip", "/lines", "/perm", "/owner", "/backup",
    "/proc", "/kill", "/top", "/net", "/ping", "/ports", "/clip", "/clipset",
    "/drives", "/cpu", "/mem", "/services", "/screenshot", "/programs",
    "/analyze", "/format", "/lang", "/run", "/py",
    "/ip", "/dns", "/traceroute", "/scan", "/wifi", "/conexiones", "/arp", "/rutas",
    "/hardware", "/gpu", "/disco", "/bateria", "/temp", "/usb",
    "/firewall", "/firewall-on", "/firewall-off", "/usuarios", "/crear-user",
    "/logs", "/logs-seguridad",
    "/tareas", "/tarea-crear", "/tarea-ejecutar",
    "/registro", "/buscar-registro",
    "/escribe", "/abre", "/click", "/minimizar", "/maximizar", "/cerrar",
    "/git init", "/git status", "/git commit", "/git push", "/git pull",
    "/git log", "/git branches", "/git checkout",
    "/get", "/post", "/scrape", "/test-api", "/download",
    "/pip-install", "/pip-list", "/pip-uninstall",
    "/npm-install", "/npm-list", "/requirements",
    "/dashboard", "/monitor", "/uptime",
    "/encrypt", "/decrypt", "/hash-text", "/generate-key", "/generate-password",
    "/sqlite-create", "/sqlite-query", "/sqlite-tables", "/sqlite-export",
    "/compact", "/think", "/context", "/cost", "/folder", "/project",
    "exit", "quit", "salir", "help", "clear",
    "general", "builder", "plan", "frontend", "backend", "debug", "security",
]

COMMAND_DESCRIPTIONS = {
    "/help": "Ver ayuda completa",
    "/status": "Estado del sistema",
    "/mode": "Cambiar modo/agente",
    "/engine": "Cambiar motor de IA",
    "/model": "Cambiar modelo",
    "/think": "Activar/desactivar modo pensamiento",
    "/level": "Nivel de analisis",
    "/memory": "Ver memoria a largo plazo",
    "/recall": "Recallar memoria",
    "/forget": "Olvidar memoria",
    "/sessions": "Listar sesiones",
    "/new": "Nueva sesion",
    "/switch": "Cambiar sesion",
    "/clear": "Limpiar pantalla",
    "/mkdir": "Crear carpeta",
    "/touch": "Crear archivo",
    "/ls": "Listar directorio",
    "/cat": "Leer archivo",
    "/edit": "Editar archivo",
    "/rm": "Eliminar archivo",
    "/mv": "Mover archivo",
    "/cp": "Copiar archivo",
    "/find": "Buscar archivos",
    "/grep": "Buscar texto en archivos",
    "/disk": "Uso de disco",
    "/info": "Info de archivo",
    "/tree": "Arbol de carpetas",
    "/hash": "Hash MD5/SHA256",
    "/diff": "Comparar archivos",
    "/zip": "Comprimir ZIP",
    "/unzip": "Descomprimir ZIP",
    "/lines": "Contar lineas",
    "/perm": "Ver permisos",
    "/owner": "Ver propietario",
    "/backup": "Crear backup",
    "/proc": "Listar procesos",
    "/kill": "Matar proceso",
    "/top": "Top procesos",
    "/net": "Info de red",
    "/ping": "Ping a host",
    "/ports": "Puertos abiertos",
    "/clip": "Ver clipboard",
    "/clipset": "Copiar al clipboard",
    "/drives": "Unidades de disco",
    "/cpu": "Info del CPU",
    "/mem": "Info de memoria",
    "/services": "Servicios activos",
    "/screenshot": "Tomar screenshot",
    "/programs": "Programas instalados",
    "/analyze": "Analizar codigo",
    "/format": "Formatear codigo",
    "/lang": "Detectar lenguaje",
    "/run": "Ejecutar comando",
    "/py": "Ejecutar Python",
    "/ip": "Mi IP publica",
    "/dns": "Lookup DNS",
    "/traceroute": "Ruta de red",
    "/scan": "Escanear puertos",
    "/wifi": "Redes WiFi",
    "/conexiones": "Conexiones activas",
    "/arp": "Tabla ARP",
    "/rutas": "Tabla de rutas",
    "/hardware": "Info completa del PC",
    "/gpu": "Info tarjeta grafica",
    "/disco": "Info discos",
    "/bateria": "Info bateria",
    "/temp": "Temperatura",
    "/usb": "Dispositivos USB",
    "/firewall": "Estado del firewall",
    "/firewall-on": "Activar firewall",
    "/firewall-off": "Desactivar firewall",
    "/usuarios": "Lista de usuarios",
    "/crear-user": "Crear usuario",
    "/logs": "Logs del sistema",
    "/logs-seguridad": "Logs de seguridad",
    "/tareas": "Listar tareas programadas",
    "/tarea-crear": "Crear tarea programada",
    "/tarea-ejecutar": "Ejecutar tarea",
    "/registro": "Leer registro de Windows",
    "/buscar-registro": "Buscar en registro",
    "/escribe": "Escribir texto (auto-type)",
    "/abre": "Abrir aplicacion/URL",
    "/click": "Hacer click",
    "/minimizar": "Minimizar ventana",
    "/maximizar": "Maximizar ventana",
    "/cerrar": "Cerrar ventana",
    "/git init": "Inicializar repositorio git",
    "/git status": "Ver estado de git",
    "/git commit": "Commitear cambios",
    "/git push": "Subir cambios",
    "/git pull": "Bajar cambios",
    "/git log": "Ver historial git",
    "/git branches": "Ver ramas",
    "/git checkout": "Cambiar rama",
    "/get": "HTTP GET request",
    "/post": "HTTP POST request",
    "/scrape": "Scraping web",
    "/test-api": "Testear API",
    "/download": "Descargar archivo",
    "/pip-install": "Instalar paquete Python",
    "/pip-list": "Listar paquetes Python",
    "/pip-uninstall": "Desinstalar paquete Python",
    "/npm-install": "Instalar paquete npm",
    "/npm-list": "Listar paquetes npm",
    "/requirements": "Crear requirements.txt",
    "/dashboard": "Panel de monitoreo",
    "/monitor": "Monitoreo realtime",
    "/uptime": "Tiempo activo del sistema",
    "/encrypt": "Cifrar archivo",
    "/decrypt": "Descifrar archivo",
    "/hash-text": "Hash de texto",
    "/generate-key": "Generar clave",
    "/generate-password": "Generar password",
    "/sqlite-create": "Crear base SQLite",
    "/sqlite-query": "Ejecutar SQL",
    "/sqlite-tables": "Listar tablas SQLite",
    "/sqlite-export": "Exportar SQLite a JSON",
    "/compact": "Modo compacto de respuesta",
    "/think": "Modo pensamiento profundo",
    "/context": "Ver uso de contexto",
    "/cost": "Ver costo estimado",
    "/folder": "Vincular proyecto a carpeta",
    "/project": "Seleccionar carpeta del proyecto (abre navegador)",
    "exit": "Salir de IAM",
    "quit": "Salir de IAM",
    "salir": "Salir de IAM",
    "help": "Ver ayuda",
    "clear": "Limpiar pantalla",
    "general": "Cambiar a modo General",
    "builder": "Cambiar a modo Builder",
    "plan": "Cambiar a modo Plan",
    "frontend": "Cambiar a modo Frontend",
    "backend": "Cambiar a modo Backend",
    "debug": "Cambiar a modo Debug",
    "security": "Cambiar a modo Security",
}


# ============================================================================
# ENHANCED CLI MAIN CLASS
# ============================================================================

class EnhancedCLI:
    """CLI profesional v3.0 - Experiencia Claude Code"""

    def __init__(self, history_file: str = None, theme: str = "claude"):
        if history_file is None:
            data_dir = settings.DATA_DIR
            data_dir.mkdir(exist_ok=True)
            history_file = str(data_dir / "cli_history")

        self.history_file = history_file
        self.console = Console()
        self.theme = THEMES.get(theme, THEMES["claude"])
        self.theme_name = theme
        self.aliases = AliasManager()
        self.context_window = ContextWindow()
        self.suggestions = SmartSuggestions()
        self.session_ui = SessionManagerUI(self.console)
        self.use_prompt_toolkit = False
        self.session = None

        self.compact_mode = False
        self.think_mode = False
        self.total_tokens_used = 0
        self.total_cost = 0.0
        self.stats = StatsTracker()

        self._last_response = ""
        self._last_query = ""
        self._last_tool_calls = []
        self.active_project = None  # Proyecto activo para mostrar en prompt
        self.mode_switch_callback = None  # Callback para cambiar modo con Tab
        self._last_tab_time = 0  # Debounce para Tab

        self._init_prompt_toolkit()

    def _init_prompt_toolkit(self):
        if not HAS_PROMPT_TOOLKIT:
            return

        try:
            self.history = FileHistory(self.history_file)
            self.style = Style.from_dict({
                "prompt": "ansicyan bold",
                "completion-menu.completion": "bg:#1e1e2e fg:#89b4fa",
                "completion-menu.completion.current": "bg:#313244 fg:#89b4fa bold",
            })

            self.bindings = KeyBindings()

            @self.bindings.add("c-k")
            def _(event):
                self._show_palette(event)

            @self.bindings.add("c-s")
            def _(event):
                event.app.current_buffer.insert_text("=")

            @self.bindings.add("c-r")
            def _(event):
                self._reverse_search(event)

            self._last_tab_time = 0

            @self.bindings.add("tab")
            def _(event):
                import time, sys
                now = time.time()
                if now - self._last_tab_time < 0.5:
                    return
                self._last_tab_time = now
                try:
                    sys.stderr.write("TAB PRESSED\n")
                    sys.stderr.flush()
                except:
                    pass
                if self.mode_switch_callback:
                    new_mode = self.mode_switch_callback()
                    if new_mode:
                        buf = event.app.current_buffer
                        buf.text = buf.text
                        buf.cursor_position = len(buf.text)

            self.session = PromptSession(
                history=self.history,
                complete_while_typing=False,
                style=self.style,
                key_bindings=self.bindings,
            )
            self.use_prompt_toolkit = True
        except Exception as e:
            self.use_prompt_toolkit = False
            self.session = None

    def _show_palette(self, event):
        """Command palette Ctrl+K"""
        self.console.print("\n  [cyan bold]Command Palette[/cyan bold]")
        table = Table(show_header=True, header_style="bold", box=box.SIMPLE, padding=(0, 2))
        table.add_column("#", style="dim", width=3)
        table.add_column("Cmd", style="cyan", min_width=15)
        table.add_column("Desc", style="white")

        cmds_with_desc = [(c, COMMAND_DESCRIPTIONS.get(c, "")) for c in COMMANDS[:40]]
        for i, (cmd, desc) in enumerate(cmds_with_desc, 1):
            table.add_row(str(i), cmd, desc)

        self.console.print(table)

        try:
            choice = input("\n  Selecciona: ").strip()
            if choice.isdigit() and 1 <= int(choice) <= len(cmds_with_desc):
                event.app.current_buffer.text = cmds_with_desc[int(choice)-1][0]
        except Exception:
            pass

    def _reverse_search(self, event):
        """Historial inverso Ctrl+R"""
        try:
            query = input("\n  [cyan]reverse-i-search:[/cyan] ").strip()
            if not query:
                return

            matches = []
            with open(self.history_file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if query.lower() in line.lower():
                        matches.append(line)

            if matches:
                self.console.print(f"  [green]Encontradas {len(matches)} coincidencias[/green]")
                event.app.current_buffer.text = matches[-1]
        except Exception:
            pass

    def set_theme(self, theme_name: str) -> bool:
        if theme_name in THEMES:
            self.theme = THEMES[theme_name]
            self.theme_name = theme_name
            return True
        return False

    # Colores por modo
    MODE_COLORS = {
        "general": "#89b4fa",   # azul claro
        "builder": "#a6e3a1",  # verde
        "debug": "#f38ba8",    # rojo
        "security": "#f9e2af", # amarillo
        "reader": "#cba6f7",   # morado
    }

    def get_input(self, mode: str) -> Optional[str]:
        import msvcrt, sys

        project_tag = ""
        if self.active_project:
            project_name = os.path.basename(self.active_project)
            project_tag = f" [{project_name}]"

        mode_color = self.MODE_COLORS.get(mode, "#89b4fa")

        # Mostrar prompt
        try:
            sys.stdout.write(f"\r\033[38;2;189;147;249m  >\033[0m \033[38;2;{int(mode_color[1:3],16)};{int(mode_color[3:5],16)};{int(mode_color[5:7],16)}miam/{mode}\033[0m\033[2m{project_tag}\033[0m ")
            sys.stdout.flush()
        except:
            try:
                print(f"  > iam/{mode}{project_tag} ", end='', flush=True)
            except:
                pass

        # Leer input char por char para detectar Tab
        chars = []
        while True:
            if msvcrt.kbhit():
                ch = msvcrt.getch()

                # Tab = 0x09
                if ch == b'\t':
                    if self.mode_switch_callback:
                        new_mode = self.mode_switch_callback()
                        if new_mode:
                            # Limpiar linea y redibujar
                            sys.stdout.write(f"\r\033[2K")
                            try:
                                mc = self.MODE_COLORS.get(new_mode, "#89b4fa")
                                r, g, b = int(mc[1:3],16), int(mc[3:5],16), int(mc[5:7],16)
                                sys.stdout.write(f"\033[38;2;189;147;249m  >\033[0m \033[38;2;{r};{g};{b}miam/{new_mode}\033[0m\033[2m{project_tag}\033[0m ")
                            except:
                                sys.stdout.write(f"  > iam/{new_mode}{project_tag} ")
                            sys.stdout.flush()
                            # Restaurar texto escrito
                            if chars:
                                sys.stdout.write(''.join(chars))
                                sys.stdout.flush()
                    continue

                # Enter
                if ch in (b'\r', b'\n'):
                    sys.stdout.write('\n')
                    sys.stdout.flush()
                    text = ''.join(chars).strip()
                    if text and not text.startswith("/"):
                        text = self.aliases.resolve(text)
                    return text

                # Backspace
                if ch == b'\x08':
                    if chars:
                        chars.pop()
                        sys.stdout.write('\b \b')
                        sys.stdout.flush()
                    continue

                # Escape sequences (arrow keys etc)
                if ch == b'\xe0' or ch == b'\x00':
                    msvcrt.getch()
                    continue

                # Ctrl+C
                if ch == b'\x03':
                    return None

                # Caracter normal
                try:
                    char = ch.decode('cp1252')
                    chars.append(char)
                    sys.stdout.write(char)
                    sys.stdout.flush()
                except:
                    pass

    def render_response(self, response: str):
        if not response:
            return

        if self.compact_mode:
            self._render_compact(response)
            return

        # Separar resultados de TOOL_CALLs del texto de la IA
        lines = response.split("\n")
        tool_results = []
        text_lines = []

        for line in lines:
            stripped = line.strip()
            if stripped.startswith("[OK]") or stripped.startswith("[ERROR]") or stripped.startswith("[WARN]"):
                tool_results.append(stripped)
            else:
                text_lines.append(line)

        # Mostrar resultados de TOOL_CALLs de forma visual
        if tool_results:
            self._render_tool_results(tool_results)

        # Mostrar texto de la IA
        text = "\n".join(text_lines).strip()
        if text:
            if "```" in text or ("    " in text and any(
                kw in text for kw in ["def ", "class ", "import ", "if ", "for "]
            )):
                self._render_mixed(text)
            else:
                try:
                    md = Markdown(text)
                    self.console.print(md)
                except Exception:
                    self.console.print(text)

    def _render_tool_results(self, results: list):
        """Mostrar resultados de TOOL_CALLs con iconos visuales mejorados"""
        ok_count = sum(1 for r in results if r.startswith("[OK]"))
        error_count = sum(1 for r in results if r.startswith("[ERROR]"))
        warn_count = sum(1 for r in results if r.startswith("[WARN]"))
        skip_count = sum(1 for r in results if r.startswith("[SKIP]"))

        # Resumen visual con iconos Unicode
        icons = []
        if ok_count:
            icons.append(f"[green]{ok_count} OK[/green]")
        if error_count:
            icons.append(f"[red]{error_count} ERROR[/red]")
        if warn_count:
            icons.append(f"[yellow]{warn_count} WARN[/yellow]")
        if skip_count:
            icons.append(f"[dim]{skip_count} skip[/dim]")

        if not icons:
            return

        summary = "  ".join(icons)
        self.console.print(f"\n  {summary}")

        # Detalles de archivos creados (solo nombres y tamaños)
        created_files = []
        for r in results:
            if r.startswith("[OK]") and "Archivo" in r:
                # Extraer nombre y tamaño
                try:
                    parts = r.split(": ", 1)
                    if len(parts) > 1:
                        detail = parts[1]
                        # Limpiar path para mostrar solo nombre
                        import os
                        basename = os.path.basename(detail.split("(")[0].strip())
                        size_match = re.search(r'\(([\d,]+)\s*bytes\)', r)
                        size_str = f" ({size_match.group(1)} bytes)" if size_match else ""
                        created_files.append(f"    [green]+[/green] [cyan]{basename}[/cyan]{size_str}")
                except:
                    pass

        if created_files:
            self.console.print("\n  [bold]Archivos:[/bold]")
            for f in created_files:
                self.console.print(f)

        # Errores y warnings
        for r in results:
            if r.startswith("[ERROR]"):
                self.console.print(f"  [red]  ! {r}[/red]")
            elif r.startswith("[WARN]"):
                self.console.print(f"  [yellow]  ! {r}[/yellow]")

    def _render_compact(self, response: str):
        lines = response.strip().split("\n")
        if len(lines) > 10:
            self.console.print("\n".join(lines[:5]))
            self.console.print(f"  [dim]... {len(lines)-5} lineas mas[/dim]")
        else:
            self.console.print(response)

    def _render_mixed(self, text: str):
        parts = re.split(r'(```[\s\S]*?```)', text)
        for part in parts:
            if part.startswith("```") and part.endswith("```"):
                lines = part.split("\n")
                lang = lines[0].replace("```", "").strip() or "python"
                code = "\n".join(lines[1:-1])
                try:
                    syntax = Syntax(code, lang, theme="monokai", line_numbers=True)
                    self.console.print(Panel(syntax, border_style="cyan", padding=(0, 1)))
                except Exception:
                    self.console.print(Panel(code, border_style="cyan", padding=(0, 1)))
            elif part.strip():
                try:
                    md = Markdown(part)
                    self.console.print(md)
                except Exception:
                    self.console.print(part)

    def show_thinking(self, query: str):
        """Muestra animacion de pensamiento"""
        if not self.think_mode:
            return

        print(f"\n  [dim]\u25cf Pensando...[/dim]")
        print(f"  [dim]  \u2514 Query: {query[:80]}{'...' if len(query) > 80 else ''}[/dim]")

    def show_suggestions(self, response: str, query: str):
        """Muestra sugerencias inteligentes"""
        suggs = self.suggestions.get_suggestions(response, query)
        if suggs:
            self.console.print(self.suggestions.format_suggestions(suggs))

    def show_context_usage(self):
        """Muestra panel de contexto"""
        self.console.print(self.context_window.get_usage_panel())

    def show_cost(self):
        """Muestra costo estimado"""
        table = Table(title="Costo Estimado", box=box.ROUNDED, border_style="cyan")
        table.add_column("Metrica", style="cyan")
        table.add_column("Valor", style="green")

        table.add_row("Tokens totales", f"{self.total_tokens_used:,}")
        table.add_row("Costo estimado", f"${self.total_cost:.4f}")
        table.add_row("Mensajes en contexto", str(len(self.context_window.messages)))

        self.console.print(table)

    def print_banner(self):
        t = self.theme["accent"]
        d = self.theme["dim"]
        r = self.theme["reset"]
        s = self.theme["success"]
        p = self.theme["primary"]

        print()
        print(f"{t}\033[1m")
        print(" _____          __  __ ")
        print("|_   _|   /\\   |  \\/  |")
        print("  | |    /  \\  | \\  / |")
        print("  | |   / /\\ \\ | |\\/| |")
        print(" _| |_ / ____ \\| |  | |")
        print("|_____/_/    \\_\\_|  |_|")
        print(f"{r}")
        print(f"{s}\033[1m    IAM Core V3.1{r}")
        print(f"{d}")
        print("    Ctrl+K  Command Palette    Ctrl+R  Reverse Search")
        print("    TAB     Cambiar modo       /help   Ayuda")
        print("    /think  Modo pensamiento   /compact Respuestas cortas")
        print("    /context Ver contexto       /cost   Ver costo")
        print("    /folder Vincular proyecto   /save   Guardar respuesta" + r)
        print()

    def print_help_table(self):
        table = Table(
            title=f"IAM v3.2.0 | Tema: {self.theme_name}",
            box=box.ROUNDED,
            show_header=True,
            header_style="bold cyan",
        )
        table.add_column("Comando", style="green", width=20)
        table.add_column("Descripcion", style="white", width=40)

        categories = {
            "IA": ["/help", "/status", "/mode", "/engine", "/model", "/think", "/compact", "/context", "/cost"],
            "Sesion": ["/sessions", "/new", "/switch", "/clear"],
            "Archivos": ["/ls", "/cat", "/edit", "/rm", "/mv", "/cp", "/find", "/grep", "/tree"],
            "Sistema": ["/proc", "/kill", "/top", "/cpu", "/mem", "/hardware"],
            "Red": ["/ip", "/dns", "/ping", "/ports", "/scan", "/wifi"],
            "Git": ["/git init", "/git status", "/git commit", "/git push", "/git pull"],
            "Nuevo": ["/compact", "/think", "/context", "/cost", "/save", "/project"],
        }

        for cat, cmds in categories.items():
            table.add_row(f"[bold]{cat}[/bold]", "", style="on grey11")
            for cmd in cmds:
                desc = COMMAND_DESCRIPTIONS.get(cmd, "")
                table.add_row(f"  {cmd}", f"  {desc}")

        self.console.print(table)

    def print_aliases(self):
        table = Table(title="Aliases", box=box.ROUNDED, border_style="cyan")
        table.add_column("Alias", style="cyan", width=15)
        table.add_column("Expansion", style="green")
        table.add_column("Tipo", style="dim")

        for name, cmd in sorted(self.aliases.aliases.items()):
            tipo = "built-in" if name in DEFAULT_ALIASES else "custom"
            table.add_row(name, cmd, tipo)

        self.console.print(table)

    def print_sessions(self):
        self.session_ui.show_sessions()

    def print_stats(self):
        table = Table(title="Estadisticas", box=box.ROUNDED, border_style="cyan")
        table.add_column("Metrica", style="cyan")
        table.add_column("Valor", style="green")

        table.add_row("Tema", self.theme_name)
        table.add_row("Modo compacto", "ON" if self.compact_mode else "OFF")
        table.add_row("Modo pensamiento", "ON" if self.think_mode else "OFF")
        table.add_row("Tokens usados", f"{self.total_tokens_used:,}")
        table.add_row("Costo estimado", f"${self.total_cost:.4f}")
        table.add_row("Aliases activos", str(len(self.aliases.aliases)))
        table.add_row("Sesiones", str(len(self.session_ui.list_sessions())))

        self.console.print(table)

    def print_themes(self):
        table = Table(title="Temas", box=box.ROUNDED, border_style="cyan")
        table.add_column("Nombre", style="cyan")
        table.add_column("Estado", style="green")

        for name in THEMES:
            status = " <<< ACTUAL" if name == self.theme_name else ""
            table.add_row(name, status)

        self.console.print(table)

    def toggle_compact(self) -> bool:
        self.compact_mode = not self.compact_mode
        return self.compact_mode

    def toggle_think(self) -> bool:
        self.think_mode = not self.think_mode
        return self.think_mode

    def print_success(self, message: str):
        self.console.print(Panel(f"[bold green]{message}[/bold green]", border_style="green", title="OK"))

    def print_error(self, message: str):
        self.console.print(Panel(f"[bold red]{message}[/bold red]", border_style="red", title="Error"))

    def print_warning(self, message: str):
        self.console.print(Panel(f"[bold yellow]{message}[/bold yellow]", border_style="yellow", title="Advertencia"))

    def print_info(self, message: str):
        self.console.print(Panel(f"[bold cyan]{message}[/bold cyan]", border_style="cyan", title="Info"))

    def save_response(self, query: str, response: str, mode: str) -> str:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_query = re.sub(r'[^\w\s-]', '', query[:50]).strip().replace(' ', '_')
        filename = f"{timestamp}_{safe_query}.md"
        filepath = settings.DATA_DIR / "responses" / filename
        filepath.parent.mkdir(exist_ok=True)

        content = f"""# IAM Response

**Fecha:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Modo:** {mode}
**Query:** {query}

---

{response}

---

*IAM v3.2.0*
"""
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

        return str(filepath)
