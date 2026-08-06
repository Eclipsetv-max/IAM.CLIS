# -*- coding: utf-8 -*-
"""
IAM Agent - Agente de IA avanzado con razonamiento profundo
Version 4.5 - CSS/JS premium, multi-language quality rules
"""

import json
import os
import requests
from typing import Dict, Any, Optional, List, Tuple
from datetime import datetime

from ..config.settings import settings, COLORS
from ..config.prompts import AGENT_PROMPTS, get_agent_prompt
from .session import Session, SessionManager
from .reasoning import ReasoningEngine, ThinkingLevel
from .memory import MemorySystem
from .gemini import gemini_client
from .freetheai import freetheai_client
from ..tools.filesystem import filesystem
from ..tools.system import system_info
from ..tools.code import code_manager
from ..tools.registry import registry
from ..tools.scheduler import scheduler
from ..tools.hardware import hardware
from ..tools.security import security
from ..tools.network import network
from ..tools.process import process_manager
from ..tools.automation import automation
from ..tools.database import database
from ..tools.encryption import encryption
from ..tools.git_tools import git
from ..tools.web import web
from ..tools.monitor import monitor
from ..tools.packages import packages
from ..tools.screen import ScreenMonitor
from .loading import LoadingIndicator, ToolCallProgress
from .permissions import (
    PermissionSystem, PermissionAction, PermissionLevel,
    permission_system, request_permission, require_permission
)

# Nuevos modulos v4.1
from ..tools.smart_templates import smart_templates
from ..tools.code_validator import validate_file
from ..tools.advanced_actions import advanced_actions, ALL_ACTIONS, TOTAL_ACTIONS

# Modulos IAM
from .file_history import FileHistory, file_history
from .cost_tracking import CostTracker, cost_tracker
from .auto_compact import AutoCompactor, auto_compactor
from .context_loader import ContextLoader, context_loader
from .sub_agent import SubAgent, SubAgentType, sub_agent
from .events import events, EventType
from .persistent_shell import get_shell


class Agent:
    """
    Agente de IA avanzado con capacidades de razonamiento
    Inspirado en Claude y otros modelos de ultima generacion
    """
    
    # Mensajes por modo - que aparece cuando la IA esta trabajando
    MODE_MESSAGES = {
        "general": "[analizando]",
        "builder": "[construyendo]",
        "debug": "[depurando]",
        "security": "[verificando]",
        "reader": "[leyendo]",
    }
    
    # Tipo de animacion por modo
    MODE_SPINNERS = {
        "general": "smooth",    # Indigo suave para análisis general
        "builder": "build",     # Barra de carga para construir
        "debug": "line",        # Radar para depurar
        "security": "pulse",    # Pulso verde para seguridad
        "reader": "clock",      # Reloj para leer
    }
    
    def _get_mode_message(self, extra: str = "") -> str:
        """Obtener mensaje segun el modo actual"""
        base = self.MODE_MESSAGES.get(self.current_mode, "[pensando]")
        if extra:
            return f"{base} {extra}"
        return base
    
    def _get_mode_spinner(self) -> str:
        """Obtener tipo de animacion segun el modo actual"""
        return self.MODE_SPINNERS.get(self.current_mode, "dots")
    
    def __init__(self, memory: MemorySystem = None):
        self.session_manager = SessionManager()
        self.current_mode: str = "general"
        self.engine: str = settings.DEFAULT_ENGINE
        self.reasoning = ReasoningEngine()
        self.show_thinking: bool = False
        self.thinking_level: ThinkingLevel = ThinkingLevel.DEEP
        self.memory = memory or MemorySystem()
        self.active_project: str = None  # Carpeta activa del proyecto
        self._local_model = None  # Modelo local fine-tuned
        
        # Modulos IAM
        self.file_history = file_history
        self.cost_tracker = cost_tracker
        self.auto_compactor = auto_compactor
        self.context_loader = context_loader
        self.sub_agent = sub_agent
        self.events = events
        self.shell = get_shell()
        
        # Tracking de archivos leidos (para read-before-edit)
        self._files_read_this_session: set = set()
        
        # File records para read-before-edit (IAM)
        self._file_records: Dict[str, Dict] = {}
    
    @property
    def current_session(self) -> Optional[Session]:
        return self.session_manager.current_session
    
    @property
    def system_prompt(self) -> str:
        return get_agent_prompt(self.current_mode)
    
    def set_active_project(self, path: str) -> bool:
        """Establecer la carpeta activa del proyecto"""
        if path and os.path.isdir(path):
            self.active_project = os.path.abspath(path)
            return True
        return False

    def clear_active_project(self):
        """Limpiar la carpeta activa"""
        self.active_project = None

    def resolve_project_path(self, path: str) -> str:
        """Resolver una ruta relativa contra el proyecto activo.
        Si active_project esta definido y la ruta es relativa, la resuelve ahi."""
        if not path:
            return path

        # Si es ruta absoluta, usar tal cual
        if os.path.isabs(path):
            return path

        # Si hay proyecto activo, resolver ahi
        if self.active_project:
            resolved = os.path.join(self.active_project, path)
            return os.path.abspath(resolved)

        return path

    def _build_enriched_prompt(self) -> str:
        """Construir prompt enriquecido con contexto del sistema y memoria"""
        base_prompt = self.system_prompt
        
        # Contexto del sistema (solo info esencial)
        system_context = self._get_system_context()
        
        # Memoria relevante (limitada)
        memory_context = self._get_memory_context()
        
        # Proyecto activo (solo nombre)
        project_info = ""
        if self.active_project:
            project_info = f"\n- PROYECTO: {os.path.basename(self.active_project)}"
        
        enriched = f"""{base_prompt}

## CONTEXTO
{system_context}
{project_info}

## MEMORIA
{memory_context}

## REGLAS
- SIEMPRE usa [TOOL_CALL] para crear/editar archivos
- NO describas, EJECUTA"""
        
        return enriched
    
    def _get_system_context(self) -> str:
        """Obtener contexto actual del sistema"""
        try:
            cwd = os.getcwd()
            home = os.path.expanduser("~")
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            import platform
            os_name = platform.system()
            os_version = platform.version()
            
            try:
                files = len([f for f in os.listdir(cwd) if os.path.isfile(os.path.join(cwd, f))])
                dirs = len([d for d in os.listdir(cwd) if os.path.isdir(os.path.join(cwd, d))])
            except:
                files = 0
                dirs = 0
            
            context = f"""- Directorio actual: {cwd}
- Directorio home: {home}
- Sistema operativo: {os_name} {os_version}
- Fecha/Hora: {now}
- Archivos en directorio actual: {files}
- Subdirectorios: {dirs}
- Modo activo: {self.current_mode}
- Motor de IA: {self.engine}"""
            
            # Agregar info del scan inicial si existe
            if hasattr(self, 'system_context') and self.system_context:
                sc = self.system_context
                context += f"""
- Usuario: {sc.get('user', 'N/A')}
- PC: {sc.get('pc_name', 'N/A')}
- Procesador: {sc.get('processor', 'N/A')}
- RAM: {sc.get('ram_gb', 'N/A')} GB
- Disco libre: {sc.get('disk_free_gb', 'N/A')} GB"""
                
                if sc.get('projects'):
                    projects = [p['name'] for p in sc['projects']]
                    context += f"\n- Proyectos en escritorio: {', '.join(projects)}"
                
                if sc.get('desktop_items'):
                    context += f"\n- Items en escritorio: {len(sc['desktop_items'])}"
            
            return context
        except Exception as e:
            return f"- Error obteniendo contexto: {str(e)}"
    
    def _get_memory_context(self) -> str:
        """Obtener contexto relevante de la memoria a largo plazo"""
        try:
            # Buscar memorias relevantes basadas en el ultimo mensaje
            if self.current_session:
                last_msg = self.current_session.get_last_user_message()
                if last_msg:
                    memories = self.memory.recall(last_msg, limit=5)
                    if memories:
                        memory_lines = []
                        for mem in memories:
                            memory_lines.append(f"- [{mem.category}] {mem.content[:100]}...")
                        return "\n".join(memory_lines)
            
            # Si no hay mensaje, obtener memorias recientes
            recent = self.memory.get_recent(limit=3)
            if recent:
                memory_lines = []
                for mem in recent:
                    memory_lines.append(f"- [{mem.category}] {mem.content[:100]}...")
                return "\n".join(memory_lines)
            
            return "- No hay memorias previas registradas"
        except Exception:
            return "- Error accediendo a la memoria"
    
    def set_mode(self, mode: str) -> bool:
        """Cambiar modo/agente"""
        if mode in AGENT_PROMPTS:
            self.current_mode = mode
            if self.current_session:
                self.current_session.mode = mode
                self.current_session.model = settings.MODELS.get(mode, settings.MODELS["general"])
            # Usar motor IAM en builder para mejor calidad de codigo
            if mode == "builder":
                self.engine = "iam"
            return True
        return False
    
    def set_engine(self, engine: str) -> bool:
        """Cambiar motor de IA"""
        if engine in settings.AVAILABLE_ENGINES:
            self.engine = engine
            # Si cambia a local, cargar modelo
            if engine == "local":
                self._load_local_model()
            return True
        return False
    
    def _load_local_model(self, model_path: str = None) -> bool:
        """Cargar modelo local fine-tuned"""
        try:
            from ..training.local_model import IAMLocalModel, find_local_models
            
            if self._local_model and self._local_model.is_available():
                return True
            
            # Buscar modelo disponible
            if model_path is None:
                models = find_local_models()
                if models:
                    model_path = models[0]["path"]
                else:
                    print("[IAM] No hay modelos locales. Entrena uno con: python iam/training/train.py")
                    return False
            
            self._local_model = IAMLocalModel()
            self._local_model.load(model_path)
            return True
        except Exception as e:
            print(f"[IAM] Error cargando modelo local: {e}")
            return False
    
    def _call_local_model(self, prompt: str) -> str:
        """Llamar al modelo local fine-tuned"""
        if not self._local_model or not self._local_model.is_available():
            return "[ERROR] Modelo local no disponible"
        
        system_prompt = self.system_prompt
        response = self._local_model.generate(
            prompt=prompt,
            system_prompt=system_prompt,
            max_new_tokens=1024,
            temperature=0.7,
        )
        return response or ""
    
    def set_thinking_level(self, level: str) -> bool:
        """Cambiar nivel de pensamiento"""
        try:
            self.thinking_level = ThinkingLevel(level)
            return True
        except ValueError:
            return False
    
    def toggle_thinking(self) -> bool:
        """Activar/desactivar muestra de pensamiento"""
        self.show_thinking = not self.show_thinking
        return self.show_thinking
    
    def _smart_analyze(self, user_message: str) -> dict:
        """
        Analisis inteligente pre-envio a la IA
        Piensa como un programador experto antes de actuar
        """
        msg_lower = user_message.lower()
        
        analysis = {
            "intent": "unknown",
            "complexity": "simple",
            "requires_files": False,
            "requires_execution": False,
            "requires_ui": False,
            "suggested_mode": self.current_mode,
            "keywords": [],
            "context_hints": [],
            "emotion": "neutral",
            "urgency": "normal",
            "topic": "general"
        }
        
        # Detectar intencion (expandido)
        create_words = ["crea", "crear", "haz", "hacer", "genera", "generar", "nuevo", "nueva", 
                       "construye", "construir", "desarrolla", "desarrollar", "implementa", "implementar",
                       "armar", "arma", "montar", "monta", "produci", "producir"]
        edit_words = ["edita", "editar", "modifica", "modificar", "cambia", "cambiar", 
                     "agrega", "agregar", "añade", "añadir", "actualiza", "actualizar",
                     "mejora", "mejorar", "ajusta", "ajustar", "corrije", "corregir",
                     "reescri", "reemplaza", "reemplazar", "sobreescri"]
        execute_words = ["ejecuta", "ejecutar", "corre", "correr", "run", "exec", 
                        "lanza", "lanzar", "inicia", "iniciar", "arranca", "arrancar",
                        "corre", "corriendo"]
        read_words = ["lee", "leer", "muestra", "mostrar", "que dice", "cat", 
                     "abre", "abrir", "visuali", "ver", "mirar", "observa"]
        search_words = ["busca", "buscar", "find", "encuentra", "encontrar", 
                       "locali", "detecta", "detectar", "identifica", "identificar"]
        delete_words = ["borra", "borrar", "eliminar", "elimina", "rm", "delete", 
                       "suprime", "suprimir", "destruye", "destruir", "limpia", "limpiar"]
        analyze_words = ["analiza", "analizar", "revisa", "revisar", "check", "verifica", 
                        "verificar", "evalua", "evaluar", "examina", "examinar", "inspecciona"]
        explain_words = ["explica", "explicar", "que es", "que hace", "como funciona", 
                        "describe", "describir", "detalla", "detallar", "describe"]
        config_words = ["configura", "configurar", "setup", "ajusta", "ajustar", 
                       "personaliza", "personalizar", "cambia", "cambiar"]
        
        if any(w in msg_lower for w in create_words):
            analysis["intent"] = "create"
            analysis["requires_files"] = True
        elif any(w in msg_lower for w in edit_words):
            analysis["intent"] = "edit"
            analysis["requires_files"] = True
        elif any(w in msg_lower for w in execute_words):
            analysis["intent"] = "execute"
            analysis["requires_execution"] = True
        elif any(w in msg_lower for w in read_words):
            analysis["intent"] = "read"
        elif any(w in msg_lower for w in search_words):
            analysis["intent"] = "search"
        elif any(w in msg_lower for w in delete_words):
            analysis["intent"] = "delete"
        elif any(w in msg_lower for w in analyze_words):
            analysis["intent"] = "analyze"
        elif any(w in msg_lower for w in explain_words):
            analysis["intent"] = "explain"
        elif any(w in msg_lower for w in config_words):
            analysis["intent"] = "config"
        
        # Detectar complejidad (expandido)
        complex_words = ["proyecto", "app", "aplicacion", "web", "api", "sistema", 
                        "plataforma", "dashboard", "panel", "interfaz completa",
                        "frontend y backend", "fullstack", "base de datos"]
        medium_words = ["funcion", "clase", "metodo", "script", "componente", "modulo",
                       "clase", "objeto", "endpoint", "ruta", "vista"]
        
        if any(w in msg_lower for w in complex_words):
            analysis["complexity"] = "complex"
        elif any(w in msg_lower for w in medium_words):
            analysis["complexity"] = "medium"
        
        # Detectar UI (expandido)
        ui_words = ["ui", "interfaz", "ventana", "grafico", "tkinter", "gui", 
                   "pantalla", "formulario", "dialogo", "modal", "popup",
                   "web", "html", "css", "frontend", "diseño", "layout"]
        if any(w in msg_lower for w in ui_words):
            analysis["requires_ui"] = True
        
        # Detectar keywords de tecnologia (expandido)
        tech_keywords = ["python", "javascript", "js", "html", "css", "java", "go", "rust", 
                        "react", "flask", "django", "fastapi", "express", "node", "vue",
                        "angular", "svelte", "typescript", "ts", "sql", "mongodb", "redis",
                        "docker", "kubernetes", "aws", "azure", "gcp", "git", "github",
                        "tailwind", "bootstrap", "sass", "less", "webpack", "vite"]
        for kw in tech_keywords:
            if kw in msg_lower:
                analysis["keywords"].append(kw)
        
        # Detectar contexto (expandido)
        if any(w in msg_lower for w in ["escritorio", "desktop"]):
            analysis["context_hints"].append("desktop")
        if any(w in msg_lower for w in ["dentro de", "en esa", "ahi", "aqui", "en ella", "dentro"]):
            analysis["context_hints"].append("existing_folder")
        if any(w in msg_lower for w in ["carpeta", "directorio", "ruta", "path"]):
            analysis["context_hints"].append("folder_context")
        
        # Detectar emoción/intención emocional
        if any(w in msg_lower for w in ["urgente", "rapido", "ya", "ahora", "necesito"]):
            analysis["urgency"] = "high"
        elif any(w in msg_lower for w in ["cuando puedas", "sin prisa", "tranquilo"]):
            analysis["urgency"] = "low"
        
        if any(w in msg_lower for w in ["no funciona", "error", "fallo", "bug", "problema"]):
            analysis["emotion"] = "frustrated"
        elif any(w in msg_lower for w in ["gracias", "genial", "perfecto", "excelente"]):
            analysis["emotion"] = "positive"
        
        # Detectar tema/tópico
        if any(w in msg_lower for w in ["seguridad", "hack", "vulnerabilidad", "firewall"]):
            analysis["topic"] = "security"
        elif any(w in msg_lower for w in ["red", "internet", "wifi", "conexion", "ip"]):
            analysis["topic"] = "network"
        elif any(w in msg_lower for w in ["hardware", "cpu", "ram", "disco", "gpu"]):
            analysis["topic"] = "hardware"
        elif any(w in msg_lower for w in ["base de datos", "sql", "mongo", "redis"]):
            analysis["topic"] = "database"
        elif any(w in msg_lower for w in ["git", "repositorio", "commit", "branch"]):
            analysis["topic"] = "git"
        elif any(w in msg_lower for w in ["deploy", "desplegar", "servidor", "hosting"]):
            analysis["topic"] = "devops"
        
        return analysis
    
    def _validate_tool_call(self, action: str, path: str = None, content: str = None, command: str = None) -> tuple:
        """
        Validar un TOOL_CALL antes de ejecutarlo
        Retorna: (is_valid, message)
        """
        if action == "create_file":
            if not path:
                # Intentar generar un path basado en el contenido
                if content:
                    if content.strip().startswith('<!DOCTYPE') or content.strip().startswith('<html'):
                        path = 'index.html'
                    elif 'function ' in content or 'const ' in content:
                        path = 'script.js'
                    elif '{' in content:
                        path = 'style.css'
                    else:
                        path = 'index.html'
                else:
                    return False, "Falta ruta del archivo"
            # Verificar que la ruta no tenga caracteres basura
            if '[' in path or ']' in path:
                path = path.replace('[', '').replace(']', '')
            if len(path) < 3:
                return False, f"Ruta demasiado corta: {path}"
            return True, "OK"
        
        elif action == "edit_file":
            if not path:
                return False, "Falta ruta del archivo"
            if not os.path.exists(path):
                return False, f"Archivo no existe: {path}"
            return True, "OK"
        
        elif action == "read_file":
            if not path:
                return False, "Falta ruta del archivo"
            if not os.path.exists(path):
                return False, f"Archivo no existe: {path}"
            return True, "OK"
        
        elif action == "create_folder":
            if not path:
                return False, "Falta ruta de la carpeta"
            if '[' in path or ']' in path:
                return False, f"Ruta contiene caracteres invalidos: {path}"
            return True, "OK"
        
        elif action == "delete_file":
            if not path:
                return False, "Falta ruta del archivo a eliminar"
            return True, "OK"
        
        elif action == "execute":
            if not command:
                return False, "Falta el comando a ejecutar"
            # No validar comandos peligrosos
            dangerous = ["rm -rf", "rmdir /s", "format", "del /f"]
            if any(d in command.lower() for d in dangerous):
                return False, "Comando peligroso detectado"
            return True, "OK"
        
        elif action is None:
            return False, "No se detecto ninguna accion en el TOOL_CALL"
        
        return False, f"Accion desconocida: {action}"
    
    def _verify_execution(self, action: str, path: str = None, success: bool = True) -> str:
        """
        Verificar que la ejecucion fue exitosa y dar feedback
        """
        if action == "create_file" and path:
            if os.path.exists(path):
                size = os.path.getsize(path)
                return f"[OK] Verificado: {path} ({size} bytes)"
            else:
                return f"[ERROR] {path} no se creo correctamente"
        
        elif action == "edit_file" and path:
            if os.path.exists(path):
                return f"[OK] Verificado: {path} editado correctamente"
            else:
                return f"[ERROR] {path} no existe despues de editar"
        
        return ""
    
    def _detect_project_folder(self, content: str) -> str:
        """Detectar la carpeta del proyecto basado en el contexto"""
        # Si hay proyecto activo, usarlo directamente
        if self.active_project and os.path.isdir(self.active_project):
            return self.active_project

        import re
        from datetime import datetime
        
        # Generar nombre basado en el mensaje del usuario
        words = re.findall(r'[a-zA-Záéíóúñ]+', content.lower())
        skip = {'crear', 'crea', 'hacer', 'haz', 'una', 'un', 'el', 'la', 'los', 'las',
                'con', 'por', 'para', 'que', 'se', 'sea', 'como', 'mas', 'más',
                'portfolio', 'landing', 'ecommerce', 'blog', 'dashboard', 'web', 'pagina',
                'html', 'css', 'javascript', 'js', 'personal', 'minimalista', 'moderno',
                'animaciones', 'suaves', 'modo', 'oscuro', 'archivo', 'archivos', 'carpeta'}
        key_words = [w for w in words if w not in skip and len(w) > 2][:3]
        name = '_'.join(key_words) if key_words else 'proyecto'
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        folder_name = f"{name}_{timestamp}"
        
        # Crear en la carpeta de tests si existe, si no en el escritorio
        test_dir = os.environ.get('TEST_OUTPUT_DIR', 
                                   os.path.join(os.path.expanduser("~"), "Desktop", "iam_real_tests"))
        os.makedirs(test_dir, exist_ok=True)
        
        project_path = os.path.join(test_dir, folder_name)
        os.makedirs(project_path, exist_ok=True)
        return project_path
    
    def _detect_and_create_raw_files(self, content: str, folder: str) -> list:
        """Detectar HTML/CSS/JS en contenido raw y crear archivos.
        Versión mejorada para manejar código largo correctamente."""
        import re
        results = []
        
        if not folder or not content:
            return results
        
        html_content = None
        css_content = None
        js_content = None
        
        # Detectar HTML: buscar <!DOCTYPE o <html
        if '<!DOCTYPE' in content or '<html' in content:
            # Buscar desde <!DOCTYPE hasta </html>
            html_match = re.search(r'(<!DOCTYPE[^>]*>.*?</html>)', content, re.DOTALL | re.IGNORECASE)
            if html_match:
                html_content = html_match.group(1).strip()
            else:
                # Intentar con <html> hasta </html>
                html_match = re.search(r'(<html[^>]*>.*?</html>)', content, re.DOTALL | re.IGNORECASE)
                if html_match:
                    html_content = html_match.group(1).strip()
        
        # Detectar CSS: primero intentar extraer de <style> tags
        if not html_content:
            # Buscar <style> tags (puede haber múltiples)
            style_matches = re.findall(r'<style[^>]*>(.*?)</style>', content, re.DOTALL | re.IGNORECASE)
            if style_matches:
                css_content = '\n\n'.join([m.strip() for m in style_matches])
        
        # Detectar CSS standalone: buscar patrón selector { propiedades }
        if not css_content:
            # Buscar bloques CSS más grandes
            css_patterns = [
                r'\*[\s\S]*?\{[^}]+\}',  # * { ... }
                r'\.[a-zA-Z][\w\-\s]*\{[^}]+\}',  # .class { ... }
                r'#[a-zA-Z][\w\-\s]*\{[^}]+\}',  # #id { ... }
                r'[a-zA-Z][\w\-\s]*\{[^}]+\}',  # element { ... }
            ]
            
            for pattern in css_patterns:
                css_matches = re.findall(pattern, content, re.DOTALL)
                if css_matches:
                    # Unir todos los bloques CSS encontrados
                    css_text = '\n\n'.join(css_matches)
                    if len(css_text) > 50:
                        css_content = css_text
                        break
        
        # Detectar JS: buscar bloques de código JavaScript
        js_indicators = [
            'function ', 'const ', 'let ', 'var ', 'document.', 'window.',
            'addEventListener', 'querySelector', 'querySelectorAll',
            'addEventListener', 'fetch(', 'async ', 'await ',
            'class ', 'export ', 'import ', 'require('
        ]
        
        js_lines = []
        in_js_block = False
        
        for line in content.split('\n'):
            stripped = line.strip()
            
            # Detectar inicio de bloque JS
            if any(ind in stripped for ind in js_indicators):
                in_js_block = True
                js_lines.append(line)
            elif in_js_block:
                # Continuar si estamos dentro de un bloque JS
                if stripped and not stripped.startswith('//') and not stripped.startswith('/*'):
                    js_lines.append(line)
                elif not stripped:
                    # Línea vacía puede ser parte del código
                    js_lines.append(line)
                else:
                    # Comentario o fin de bloque
                    if len(js_lines) > 3:
                        break
                    js_lines = []
                    in_js_block = False
        
        if len(js_lines) > 3:
            js_content = '\n'.join(js_lines)
        
        # Crear archivos
        if html_content and len(html_content) > 50:
            path = os.path.join(folder, 'index.html')
            try:
                os.makedirs(os.path.dirname(path) if os.path.dirname(path) else '.', exist_ok=True)
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                results.append(f"[OK] Archivo creado: {path}")
            except Exception as e:
                results.append(f"[ERROR] Error creando {path}: {e}")
        
        if css_content and len(css_content) > 20:
            path = os.path.join(folder, 'style.css')
            try:
                os.makedirs(os.path.dirname(path) if os.path.dirname(path) else '.', exist_ok=True)
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(css_content)
                results.append(f"[OK] Archivo creado: {path}")
            except Exception as e:
                results.append(f"[ERROR] Error creando {path}: {e}")
        
        if js_content and len(js_content) > 50:
            path = os.path.join(folder, 'main.js')
            try:
                os.makedirs(os.path.dirname(path) if os.path.dirname(path) else '.', exist_ok=True)
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(js_content)
                results.append(f"[OK] Archivo creado: {path}")
            except Exception as e:
                results.append(f"[ERROR] Error creando {path}: {e}")
        
        return results
    
    def chat(self, user_message: str, stream: bool = True) -> str:
        """
        Enviar mensaje y obtener respuesta con streaming
        Incluye analisis inteligente pre-envio
        """
        if not self.current_session:
            self.session_manager.create_session(mode=self.current_mode)
        
        # Detectar imagenes pegadas [IMAGE:path]
        import re
        import base64
        self._pending_images = []
        img_matches = re.findall(r'\[IMAGE:(.+?)\]', user_message)
        for img_path in img_matches:
            if os.path.exists(img_path):
                with open(img_path, 'rb') as f:
                    b64 = base64.b64encode(f.read()).decode()
                self._pending_images.append(b64)
        user_message = re.sub(r'\[IMAGE:.+?\]', '', user_message).strip()
        if not user_message and self._pending_images:
            user_message = "Analiza esta imagen"
        
        # FASE 1: ANALISIS INTELIGENTE (como yo pienso)
        smart = self._smart_analyze(user_message)
        
        # Si necesita archivos y estamos en modo general, sugerir builder
        if smart["requires_files"] and smart["complexity"] == "complex":
            if self.current_mode == "general":
                # Cambiar a builder automaticamente para proyectos complejos
                self.set_mode("builder")
        
        thinking_output = ""
        if self.show_thinking:
            analysis = self.reasoning.analyze(user_message)
            thinking_output = self.reasoning.format_thinking(analysis) + "\n\n"
        
        self.current_session.add_message("user", user_message)
        
        # AUTO-COMPACTION: Verificar si el contexto necesita compactarse
        if self.current_session:
            context_limit = self.cost_tracker.get_context_limit(
                settings.MODELS.get(self.current_mode, "mimo-v2.5-free")
            )
            if self.auto_compactor.should_compact(
                self.current_session.get_context(),
                context_limit
            ):
                # Compactar contexto
                compact_result = self.auto_compactor.compact(
                    self.current_session.get_context(),
                    context_limit
                )
                if compact_result.success:
                    # Reconstruir sesion con contexto compactado
                    self.current_session.messages = []
                    self.current_session.add_message(
                        "system",
                        f"[Contexto compactado]: {compact_result.summary}"
                    )
        
        # Construir prompt enriquecido
        enriched_prompt = self._build_enriched_prompt()
        
        # Streaming de respuesta
        if stream:
            response = self._chat_streaming(enriched_prompt)
        else:
            response = self._chat_normal(enriched_prompt)
        
        # Ejecutar TOOL_CALLs si la IA generó alguno
        if response:
            tool_result = self._execute_tool_calls(response)
            
            # Detectar si la IA dijo que NO puede crear archivos (respuesta inválida)
            no_creation_phrases = [
                "no tengo acceso", "no puedo crear", "no tengo herramientas",
                "no tengo tool_call", "no puedo ejecutar", "no tengo permisos",
                "no puedo generar", "no tengo capacidad", "no puedo hacer"
            ]
            ia_says_no = any(phrase in response.lower() for phrase in no_creation_phrases)
            
            # Si la IA dijo que no puede pero el usuario pidió crear algo
            user_wants_creation = any(word in user_message.lower() for word in 
                ["crea", "crear", "haz", "genera", "construye", "desarrolla", "web", "pagina", "app",
                 "portfolio", "landing", "tienda", "blog", "api", "formulario"])
            
            if ia_says_no and user_wants_creation and self.active_project:
                # Forzar reintento con instrucciones muy claras
                force_follow_up = self._chat_normal(
                    f"ERROR: La respuesta anterior no usó TOOL_CALL. "
                    f"El usuario pidió: {user_message}. "
                    f"DEBES crear archivos usando [TOOL_CALL]. "
                    f"NO respondas sin TOOL_CALLs. "
                    f"Usa este formato EXACTAMENTE: "
                    f"[TOOL_CALL] action: create_file name: \"index.html\" "
                    f"<!DOCTYPE html><html>...</html> [/TOOL_CALL] "
                    f"Crea TODOS los archivos necesarios ahora."
                )
                if force_follow_up:
                    force_result = self._execute_tool_calls(force_follow_up)
                    if force_result and '[OK]' in force_result:
                        tool_result = force_result
            
            # Verificar si el usuario quiere accion
            user_wants_action = any(word in user_message.lower() for word in 
                ["mejora", "mejorar", "edita", "editar", "arregla", "arreglar", "cambia", "cambiar", 
                 "modifica", "modificar", "actualiza", "actualizar", "fix", "corrije",
                 "crea", "crear", "haz", "genera", "construye", "desarrolla", "web", "pagina", "app"])
            
            # Auto-detectar proyecto si no hay uno activo
            if user_wants_action and not self.active_project:
                detected = self._detect_project_folder(user_message)
                if detected:
                    self.active_project = detected
            
            if user_wants_action and self.active_project:
                # Verificar que hizo la IA
                made_edit = 'edit_file' in response or 'editfile' in response.lower() or 'reescrito' in tool_result.lower() or 'editado' in tool_result.lower()
                made_create = 'create_file' in response or 'createfile' in response.lower() or 'creado' in tool_result.lower() or 'Verificado' in tool_result
                
                # Contar archivos creados
                created_files = []
                if made_create:
                    import re
                    created_matches = re.findall(r'\[OK\]\s*(?:Archivo (?:creado|reescrito)|Verificado):\s*(.+?)(?:\s*\(\d+.*?\))?$', tool_result, re.MULTILINE)
                    created_files = [os.path.basename(f) for f in created_matches]
                
                # Verificar si faltan archivos tipicos de web - verificacion fisica (debe tener contenido suficiente)
                def _file_ok(folder, name):
                    p = os.path.join(folder, name)
                    if not (os.path.isfile(p) and os.path.getsize(p) > 0):
                        return False
                    # Para CSS, verificar que tenga al menos 50 lineas (no solo variables)
                    if name.endswith('.css'):
                        try:
                            with open(p, 'r', encoding='utf-8') as f:
                                lines = len(f.readlines())
                            return lines >= 50
                        except:
                            return False
                    return True
                
                if self.active_project and os.path.isdir(self.active_project):
                    has_html = _file_ok(self.active_project, 'index.html')
                    has_css = any(f.endswith('.css') and _file_ok(self.active_project, f) 
                                  for f in os.listdir(self.active_project))
                    has_js = any(f.endswith('.js') and _file_ok(self.active_project, f) 
                                 for f in os.listdir(self.active_project))
                else:
                    has_html = any(f.endswith('.html') for f in created_files) or 'index.html' in str(created_files)
                    has_css = any(f.endswith('.css') for f in created_files)
                    has_js = any(f.endswith('.js') for f in created_files)
                
                needs_html = not has_html
                needs_css = not has_css
                needs_js = not has_js
                
                # Si no hizo nada util O faltan archivos - reintento con loop
                if (not made_edit and not made_create) or (made_create and (needs_html or needs_css or needs_js)):
                    for _retry in range(1):
                        missing = []
                        if needs_html:
                            missing.append("index.html")
                        if needs_css:
                            missing.append("style.css")
                        if needs_js:
                            missing.append("script.js")
                        if not missing:
                            break

                        # Construir contexto de archivos existentes
                        existing_context = ""
                        if self.active_project and os.path.isdir(self.active_project):
                            for fname in os.listdir(self.active_project):
                                fpath = os.path.join(self.active_project, fname)
                                if os.path.isfile(fpath) and os.path.getsize(fpath) > 0:
                                    try:
                                        with open(fpath, 'r', encoding='utf-8') as f:
                                            content = f.read()
                                        existing_context += f"\n--- {fname} (existente) ---\n{content[:1500]}\n"
                                    except:
                                        pass

                        next_file = missing[0]
                        
                        # Si falta CSS pero hay HTML, pedir HTML completo con CSS inline y luego separar
                        if next_file == "style.css" and has_html:
                            follow_up = self._chat_normal(
                                f"El usuario pidio: {user_message}. "
                                f"{existing_context}\n"
                                f"El HTML de arriba esta INCOMPLETO y le faltan estilos. "
                                f"Reescribe el HTML COMPLETO con TODOS los estilos CSS DENTRO de un tag <style>. "
                                f"Incluye: variables, layout, navbar, hero, secciones, cards, responsive, animaciones. "
                                f"MINIMO 300 lineas de CSS dentro del <style>. "
                                f"[TOOL_CALL] action: create_file name: \"index.html\" HTML completo con <style> [/TOOL_CALL]",
                                max_tokens=3072
                            )
                        elif next_file == "script.js":
                            follow_up = self._chat_normal(
                                f"El usuario pidio: {user_message}. "
                                f"{existing_context}\n"
                                f"Crea el archivo script.js con JavaScript funcional para el HTML de arriba. "
                                f"DEBE incluir: animaciones, interacciones, navegacion, efectos. "
                                f"[TOOL_CALL] action: create_file name: \"script.js\" tu JS aqui [/TOOL_CALL]",
                                max_tokens=3072
                            )
                        else:
                            follow_up = self._chat_normal(
                                f"El usuario pidio: {user_message}. "
                                f"Archivos creados: {created_files if created_files else 'ninguno'}. "
                                f"FALTA: {next_file}. "
                                f"Crea SOLO este archivo AHORA en un [TOOL_CALL]. "
                                f"El archivo debe estar en la RAIZ de la carpeta del proyecto, NO en subcarpetas. "
                                f"Formato: [TOOL_CALL] action: create_file name: \"{next_file}\" contenido aqui [/TOOL_CALL]",
                                max_tokens=3072
                            )
                        if follow_up:
                            follow_result = self._execute_tool_calls(follow_up)
                            if follow_result and '[OK]' in follow_result:
                                tool_result += "\n" + follow_result
                                
                                # Extraer CSS del HTML si tiene <style> inline
                                if self.active_project and os.path.isfile(os.path.join(self.active_project, 'index.html')):
                                    html_path = os.path.join(self.active_project, 'index.html')
                                    try:
                                        with open(html_path, 'r', encoding='utf-8') as f:
                                            html_content = f.read()
                                        # Buscar bloques <style>...</style>
                                        import re as _re
                                        style_matches = _re.findall(r'<style[^>]*>(.*?)</style>', html_content, _re.DOTALL | _re.IGNORECASE)
                                        if style_matches:
                                            css_content = '\n\n'.join(style_matches)
                                            # Guardar CSS en archivo separado
                                            css_path = os.path.join(self.active_project, 'style.css')
                                            with open(css_path, 'w', encoding='utf-8') as f:
                                                f.write(css_content)
                                            # Reemplazar <style>...</style> por link a CSS
                                            new_html = _re.sub(r'<style[^>]*>.*?</style>', '<link rel="stylesheet" href="style.css">', html_content, flags=_re.DOTALL | _re.IGNORECASE)
                                            with open(html_path, 'w', encoding='utf-8') as f:
                                                f.write(new_html)
                                            tool_result += f"\n[OK] CSS extraido de HTML: style.css ({len(css_content)} bytes)"
                                            has_css = True
                                            needs_css = False
                                        
                                        # Asegurar que el HTML tenga <script src="script.js">
                                        with open(html_path, 'r', encoding='utf-8') as f:
                                            html_content = f.read()
                                        if 'script.js' not in html_content:
                                            # Agregar script tag antes de </body> o al final
                                            if '</body>' in html_content:
                                                new_html = html_content.replace('</body>', '    <script src="script.js"></script>\n</body>')
                                            elif '</html>' in html_content:
                                                new_html = html_content.replace('</html>', '    <script src="script.js"></script>\n</html>')
                                            else:
                                                new_html = html_content + '\n<script src="script.js"></script>'
                                            with open(html_path, 'w', encoding='utf-8') as f:
                                                f.write(new_html)
                                            tool_result += f"\n[OK] script.js tag agregado al HTML"
                                    except:
                                        pass
                                
                                created_files = re.findall(r'\[OK\]\s+(?:Archivo|Reescrito|Verificado)\s+(?:creado|reescrito)?:\s+(\S+)', tool_result)
                                # Verificar existencia fisica en disco (con contenido suficiente)
                                if self.active_project:
                                    def _fok(name):
                                        p = os.path.join(self.active_project, name)
                                        if not (os.path.isfile(p) and os.path.getsize(p) > 0):
                                            return False
                                        if name.endswith('.css'):
                                            try:
                                                with open(p, 'r', encoding='utf-8') as f:
                                                    return len(f.readlines()) >= 50
                                            except:
                                                return False
                                        return True
                                    has_html = _fok('index.html')
                                    has_css = any(f.endswith('.css') and _fok(f) for f in os.listdir(self.active_project))
                                    has_js = any(f.endswith('.js') and _fok(f) for f in os.listdir(self.active_project))
                                else:
                                    has_html = any('index.html' in f for f in created_files)
                                    has_css = any('style.css' in f or f.endswith('.css') for f in created_files)
                                    has_js = any('script.js' in f or f.endswith('.js') for f in created_files)
                                needs_html = not has_html
                                needs_css = not has_css
                                needs_js = not has_js
                    
                    # Fallback: crear archivos placeholder si la IA no los creo
                    if self.active_project and (needs_html or needs_css or needs_js):
                        if needs_html:
                            placeholder = '<!DOCTYPE html>\n<html lang="es">\n<head>\n<meta charset="UTF-8">\n<meta name="viewport" content="width=device-width, initial-scale=1.0">\n<title>Proyecto</title>\n<link rel="stylesheet" href="style.css">\n</head>\n<body>\n<h1>Proyecto</h1>\n<script src="script.js"></script>\n</body>\n</html>'
                            path = os.path.join(self.active_project, 'index.html')
                            with open(path, 'w', encoding='utf-8') as f:
                                f.write(placeholder)
                            tool_result += f"\n[OK] Archivo creado (fallback): index.html ({len(placeholder)} bytes)"
                        if needs_css:
                            fallback_css = '''/* ================================================================
   IAM PREMIUM CSS v5.0 - Estilos automatizados de alta calidad
   Efectos: Glassmorphism, Gradientes complejos, Animaciones suaves
   ================================================================ */

/* === VARIABLES === */
:root {
  --primary: #6366f1;
  --primary-light: #818cf8;
  --primary-dark: #4f46e5;
  --secondary: #06b6d4;
  --secondary-light: #22d3ee;
  --accent: #f59e0b;
  --accent-light: #fbbf24;
  --success: #10b981;
  --danger: #ef4444;
  --warning: #f59e0b;
  --bg: #0f172a;
  --bg-alt: #1e293b;
  --bg-card: #1e293b;
  --bg-card-hover: #334155;
  --bg-glass: rgba(30, 41, 59, 0.7);
  --text: #f1f5f9;
  --text-light: #e2e8f0;
  --text-muted: #94a3b8;
  --text-dim: #64748b;
  --border: rgba(99, 102, 241, 0.15);
  --border-light: rgba(148, 163, 184, 0.1);
  --shadow-xs: 0 1px 2px rgba(0,0,0,0.3);
  --shadow-sm: 0 2px 8px rgba(0,0,0,0.3);
  --shadow-md: 0 8px 30px rgba(0,0,0,0.35);
  --shadow-lg: 0 20px 60px rgba(0,0,0,0.4);
  --shadow-glow: 0 0 40px rgba(99, 102, 241, 0.25);
  --shadow-glow-lg: 0 0 80px rgba(99, 102, 241, 0.35);
  --gradient-primary: linear-gradient(135deg, #6366f1 0%, #06b6d4 100%);
  --gradient-warm: linear-gradient(135deg, #f59e0b 0%, #ef4444 100%);
  --gradient-cool: linear-gradient(135deg, #06b6d4 0%, #10b981 100%);
  --gradient-dark: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
  --gradient-hero: linear-gradient(160deg, #0f172a 0%, #1a1040 35%, #312e81 65%, #1e293b 100%);
  --gradient-glass: linear-gradient(135deg, rgba(255,255,255,0.05) 0%, rgba(255,255,255,0.02) 100%);
  --radius-sm: 8px;
  --radius: 12px;
  --radius-md: 16px;
  --radius-lg: 24px;
  --radius-xl: 32px;
  --radius-full: 9999px;
  --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  --transition-slow: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
  --transition-bounce: all 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
}

/* === RESET === */
*, *::before, *::after { margin: 0; padding: 0; box-sizing: border-box; }
html { scroll-behavior: smooth; font-size: 16px; scrollbar-width: thin; scrollbar-color: var(--primary) var(--bg); }
body {
  font-family: 'Inter', 'Segoe UI', system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
  background: var(--bg); color: var(--text); line-height: 1.7; overflow-x: hidden;
  -webkit-font-smoothing: antialiased; -moz-osx-font-smoothing: grayscale;
}

/* === SCROLLBAR === */
::-webkit-scrollbar { width: 8px; height: 8px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--primary); border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: var(--primary-light); }
::selection { background: var(--primary); color: white; }

/* === TIPOGRAFIA === */
h1, h2, h3, h4, h5, h6 { font-weight: 800; line-height: 1.15; color: var(--text); letter-spacing: -0.02em; }
h1 { font-size: clamp(2.5rem, 6vw, 4.5rem); }
h2 { font-size: clamp(2rem, 4vw, 3rem); }
h3 { font-size: clamp(1.5rem, 3vw, 2rem); }
h4 { font-size: clamp(1.2rem, 2vw, 1.5rem); }
p { color: var(--text-muted); font-size: 1.05rem; max-width: 65ch; }
a { color: var(--secondary); text-decoration: none; transition: var(--transition); }
a:hover { color: var(--secondary-light); }
strong, b { font-weight: 700; color: var(--text); }
small { font-size: 0.875rem; }
.text-gradient {
  background: var(--gradient-primary); -webkit-background-clip: text;
  -webkit-text-fill-color: transparent; background-clip: text;
}

/* === CONTENEDOR === */
.container { max-width: 1200px; margin: 0 auto; padding: 0 2rem; }
.container-sm { max-width: 800px; margin: 0 auto; padding: 0 2rem; }
.container-lg { max-width: 1400px; margin: 0 auto; padding: 0 2rem; }

/* === NAVBAR === */
.navbar, nav, .nav, header nav {
  position: fixed; top: 0; left: 0; right: 0; z-index: 1000;
  background: rgba(15, 23, 42, 0.85);
  backdrop-filter: blur(20px) saturate(180%);
  -webkit-backdrop-filter: blur(20px) saturate(180%);
  border-bottom: 1px solid var(--border); padding: 0.75rem 0;
  transition: var(--transition);
}
.navbar.scrolled, .nav.scrolled {
  background: rgba(15, 23, 42, 0.95); box-shadow: var(--shadow-md);
}
.nav-container, .nav-wrapper, .nav-content, .nav-inner {
  max-width: 1200px; margin: 0 auto; padding: 0 2rem;
  display: flex; justify-content: space-between; align-items: center;
}
.nav-logo, .logo, .brand, .navbar-brand {
  font-size: 1.5rem; font-weight: 800; color: var(--text);
  letter-spacing: -0.03em; transition: var(--transition);
}
.nav-logo span, .logo span, .brand span { color: var(--primary); }
.nav-logo:hover, .logo:hover { transform: scale(1.02); }
.nav-links, .nav-menu, .nav-items { display: flex; align-items: center; gap: 0.5rem; list-style: none; }
.nav-links a, .nav-menu a, .nav-link, .nav-item a {
  color: var(--text-muted); font-weight: 500; font-size: 0.9rem;
  padding: 0.5rem 1rem; border-radius: var(--radius-sm);
  transition: var(--transition); position: relative;
}
.nav-links a:hover, .nav-links a.active, .nav-link:hover, .nav-link.active, .nav-item a:hover {
  color: var(--text); background: rgba(99, 102, 241, 0.1);
}
.nav-links a::after, .nav-link::after {
  content: ''; position: absolute; bottom: 0; left: 50%; width: 0; height: 2px;
  background: var(--primary); transition: var(--transition); transform: translateX(-50%);
}
.nav-links a:hover::after, .nav-link:hover::after { width: 60%; }
.nav-cta { margin-left: 1rem; }
.menu-toggle, .nav-toggle, .hamburger {
  display: none; flex-direction: column; gap: 5px; cursor: pointer;
  background: none; border: none; padding: 0.5rem;
}
.menu-toggle span, .nav-toggle span, .hamburger span {
  width: 24px; height: 2px; background: var(--text);
  transition: var(--transition); border-radius: 2px;
}

/* === HERO === */
.hero, .hero-section, header.hero-header, .hero-banner {
  min-height: 100vh; display: flex; align-items: center; justify-content: center;
  background: var(--gradient-hero); position: relative; padding: 8rem 2rem 6rem;
  overflow: hidden;
}
.hero::before {
  content: ''; position: absolute; inset: 0;
  background: radial-gradient(ellipse at 30% 50%, rgba(99, 102, 241, 0.15) 0%, transparent 60%),
              radial-gradient(ellipse at 70% 50%, rgba(6, 182, 212, 0.1) 0%, transparent 60%);
}
.hero-content, .hero-text, .hero-center, .hero-body {
  position: relative; z-index: 1; max-width: 800px; text-align: center;
}
.hero h1, .hero-title, .hero-heading {
  font-size: clamp(2.8rem, 8vw, 5.5rem); font-weight: 800;
  line-height: 1.05; margin-bottom: 1.5rem; color: white;
  text-shadow: 0 2px 40px rgba(0,0,0,0.3);
}
.hero p, .hero-subtitle, .hero-description, .hero-text p {
  font-size: clamp(1.1rem, 2vw, 1.4rem); color: rgba(255,255,255,0.8);
  margin-bottom: 2.5rem; max-width: 600px; margin-left: auto; margin-right: auto;
  line-height: 1.7;
}
.hero-buttons, .hero-cta, .hero-actions, .hero-btns {
  display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap;
}

/* === SECCIONES === */
section, .section, [class*="section-"] { padding: 7rem 0; position: relative; }
.section-alt, .section-gray, .bg-alt { background: var(--bg-alt); }
.section-header, .section-title-wrap, .section-top { text-align: center; margin-bottom: 4rem; }
.section-title, .section-header h2, .section-heading {
  font-size: clamp(2rem, 4vw, 3rem); font-weight: 800;
  margin-bottom: 1rem; position: relative; display: inline-block;
}
.section-title::after, .section-header h2::after {
  content: ''; display: block; width: 60px; height: 4px;
  background: var(--gradient-primary); border-radius: 2px; margin: 1rem auto 0;
}
.section-subtitle, .section-header p, .section-desc {
  color: var(--text-muted); font-size: 1.15rem;
  max-width: 600px; margin: 0 auto; line-height: 1.7;
}

/* === CARDS === */
.card, .feature-card, .pricing-card, .plan-card,
.testimonial-card, .blog-card, .project-card, .service-card {
  background: var(--bg-card); border-radius: var(--radius-lg);
  padding: 2rem; position: relative; overflow: hidden;
  border: 1px solid var(--border); transition: var(--transition);
}
.card::before, .feature-card::before {
  content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px;
  background: var(--gradient-primary); opacity: 0; transition: var(--transition);
}
.card:hover, .feature-card:hover, .pricing-card:hover,
.plan-card:hover, .service-card:hover {
  transform: translateY(-8px);
  box-shadow: var(--shadow-lg), var(--shadow-glow);
  border-color: rgba(99, 102, 241, 0.3);
}
.card:hover::before, .feature-card:hover::before { opacity: 1; }
.card-icon, .feature-icon, .icon-box {
  width: 60px; height: 60px; border-radius: var(--radius);
  background: var(--gradient-primary); display: flex;
  align-items: center; justify-content: center;
  font-size: 1.5rem; margin-bottom: 1.5rem;
  box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
}
.card h3, .feature-card h3, .pricing-card h3 { font-size: 1.3rem; font-weight: 700; margin-bottom: 0.75rem; }
.card p, .feature-card p { color: var(--text-muted); font-size: 0.95rem; line-height: 1.7; }

/* === BOTONES === */
.btn, button, .cta-button, .btn-cta {
  display: inline-flex; align-items: center; justify-content: center;
  gap: 0.5rem; padding: 0.85rem 2rem; border-radius: var(--radius);
  font-weight: 600; font-size: 1rem; cursor: pointer;
  border: none; transition: var(--transition); text-decoration: none;
  font-family: inherit; letter-spacing: -0.01em;
}
.btn-primary, .cta-button, .btn-cta, button[type="submit"],
.btn-main, .btn-solid {
  background: var(--gradient-primary); color: white;
  box-shadow: 0 4px 15px rgba(99, 102, 241, 0.35);
}
.btn-primary:hover, .cta-button:hover, .btn-cta:hover,
button[type="submit"]:hover {
  transform: translateY(-3px); box-shadow: 0 8px 30px rgba(99, 102, 241, 0.45);
}
.btn-secondary, .btn-outline, .btn-ghost {
  background: transparent; color: var(--primary-light);
  border: 2px solid var(--primary);
}
.btn-secondary:hover, .btn-outline:hover {
  background: var(--primary); color: white; transform: translateY(-2px);
}
.btn-sm { padding: 0.6rem 1.2rem; font-size: 0.875rem; }
.btn-lg { padding: 1rem 2.5rem; font-size: 1.1rem; }
.btn-icon { padding: 0.75rem; border-radius: var(--radius-sm); }

/* === GRID === */
.grid { display: grid; gap: 2rem; }
.grid-2, .features-grid, .cols-2 { grid-template-columns: repeat(2, 1fr); }
.grid-3, .plans-grid, .pricing-grid, .cols-3 { grid-template-columns: repeat(3, 1fr); }
.grid-4, .stats-grid, .cols-4 { grid-template-columns: repeat(4, 1fr); }
.grid-auto, .auto-grid { grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); }

/* === IMAGENES === */
img { max-width: 100%; height: auto; display: block; }
.image-wrapper, .img-container, .img-box {
  overflow: hidden; border-radius: var(--radius-lg); position: relative;
}
.image-wrapper::after {
  content: ''; position: absolute; inset: 0;
  background: linear-gradient(to top, rgba(0,0,0,0.3) 0%, transparent 50%);
  pointer-events: none;
}
.img-overlay { position: relative; }
.img-overlay img { transition: var(--transition-slow); }
.img-overlay:hover img { transform: scale(1.05); }

/* === FORMULARIOS === */
.form-group, .input-group { margin-bottom: 1.5rem; }
.form-group label, .input-label {
  display: block; font-weight: 600; font-size: 0.9rem;
  margin-bottom: 0.5rem; color: var(--text);
}
input, textarea, select, .form-input, .form-control {
  width: 100%; padding: 0.9rem 1.2rem; border-radius: var(--radius);
  border: 1px solid var(--border); background: var(--bg-alt);
  color: var(--text); font-size: 1rem; font-family: inherit;
  transition: var(--transition);
}
input:focus, textarea:focus, select:focus, .form-input:focus {
  outline: none; border-color: var(--primary);
  box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.15);
  background: var(--bg-card);
}
textarea { min-height: 120px; resize: vertical; }
.form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }

/* === LISTAS === */
ul, ol { list-style: none; padding: 0; }
li { padding: 0.4rem 0; }
.feature-list li, .check-list li {
  display: flex; align-items: flex-start; gap: 0.75rem; padding: 0.6rem 0;
}
.feature-list li::before, .check-list li::before {
  content: '✓'; color: var(--success); font-weight: 700;
  min-width: 20px; font-size: 1.1rem;
}

/* === TABLA === */
table { width: 100%; border-collapse: collapse; }
th, td { padding: 1rem 1.25rem; text-align: left; }
th { font-weight: 700; color: var(--text); border-bottom: 2px solid var(--border); }
td { border-bottom: 1px solid var(--border-light); }
tr:hover td { background: rgba(99, 102, 241, 0.05); }

/* === TESTIMONIOS === */
.testimonial, .testimonial-card, .review-card {
  background: var(--bg-card); border-radius: var(--radius-lg);
  padding: 2.5rem; border: 1px solid var(--border); position: relative;
}
.testimonial::before, .review-card::before {
  content: '"'; position: absolute; top: 1rem; left: 1.5rem;
  font-size: 5rem; color: var(--primary); opacity: 0.15;
  font-family: Georgia, serif; line-height: 1;
}
.testimonial-quote, .quote, .review-text {
  font-style: italic; color: var(--text-light);
  margin-bottom: 1.5rem; font-size: 1.05rem; line-height: 1.8;
  position: relative; z-index: 1;
}
.testimonial-author, .author, .review-author { display: flex; align-items: center; gap: 1rem; }
.testimonial-avatar, .avatar {
  width: 48px; height: 48px; border-radius: 50%;
  background: var(--gradient-primary); display: flex;
  align-items: center; justify-content: center;
  font-weight: 700; color: white;
}
.testimonial-name, .author-name { font-weight: 700; color: var(--text); }
.testimonial-role, .author-role { font-size: 0.85rem; color: var(--text-dim); }

/* === PRECIOS === */
.pricing-card, .plan-card { text-align: center; padding: 3rem 2rem; }
.pricing-card.featured, .plan-card.featured, .pricing-popular {
  border-color: var(--primary); transform: scale(1.05);
  box-shadow: var(--shadow-glow-lg);
}
.pricing-badge, .plan-badge, .badge-popular {
  position: absolute; top: -1px; left: 50%; transform: translateX(-50%);
  background: var(--gradient-primary); color: white;
  padding: 0.4rem 1.5rem; border-radius: 0 0 var(--radius) var(--radius);
  font-size: 0.8rem; font-weight: 700; text-transform: uppercase;
  letter-spacing: 0.05em;
}
.price, .pricing-amount, .plan-price {
  font-size: 3.5rem; font-weight: 800; color: var(--text);
  line-height: 1; margin: 1.5rem 0;
}
.price span, .pricing-currency { font-size: 1.5rem; vertical-align: top; }
.price-period, .pricing-period, .plan-period { font-size: 1rem; color: var(--text-dim); margin-bottom: 2rem; }
.pricing-features, .plan-features { text-align: left; margin: 2rem 0; }
.pricing-features li, .plan-features li {
  display: flex; align-items: center; gap: 0.75rem;
  padding: 0.75rem 0; border-bottom: 1px solid var(--border-light); color: var(--text-muted);
}
.pricing-features li::before { content: '✓'; color: var(--success); font-weight: 700; }

/* === STATS === */
.stats, .stats-section, .stats-grid {
  display: grid; grid-template-columns: repeat(4, 1fr); gap: 2rem; padding: 4rem 0;
}
.stat-item, .stat, .stat-card { text-align: center; }
.stat-number, .stat-count, .stat-value {
  font-size: clamp(2.5rem, 5vw, 4rem); font-weight: 800;
  color: var(--primary); display: block; line-height: 1; margin-bottom: 0.5rem;
}
.stat-label, .stat-title { color: var(--text-muted); font-size: 0.95rem; font-weight: 500; }

/* === FOOTER === */
footer, .footer, .site-footer {
  background: var(--bg-alt); padding: 5rem 0 2rem; border-top: 1px solid var(--border);
}
.footer-grid, .footer-content {
  display: grid; grid-template-columns: 2fr 1fr 1fr 1fr;
  gap: 3rem; margin-bottom: 3rem;
}
.footer-brand, .footer-about { max-width: 300px; }
.footer-brand p { margin-top: 1rem; font-size: 0.9rem; }
.footer-title, .footer-heading {
  font-size: 1rem; font-weight: 700; color: var(--text);
  margin-bottom: 1.5rem; text-transform: uppercase; letter-spacing: 0.05em;
}
.footer-links { display: flex; flex-direction: column; gap: 0.75rem; }
.footer-links a { color: var(--text-muted); font-size: 0.9rem; transition: var(--transition); }
.footer-links a:hover { color: var(--primary); transform: translateX(4px); }
.footer-social { display: flex; gap: 0.75rem; margin-top: 1.5rem; }
.footer-social a {
  width: 40px; height: 40px; border-radius: var(--radius-sm);
  background: var(--bg-card); display: flex; align-items: center; justify-content: center;
  color: var(--text-muted); transition: var(--transition);
}
.footer-social a:hover { background: var(--primary); color: white; transform: translateY(-3px); }
.footer-bottom {
  padding-top: 2rem; border-top: 1px solid var(--border);
  display: flex; justify-content: space-between; align-items: center;
  color: var(--text-dim); font-size: 0.85rem;
}

/* === BADGES === */
.badge, .tag, .label {
  display: inline-block; padding: 0.35rem 0.9rem;
  border-radius: var(--radius-full); font-size: 0.75rem;
  font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em;
}
.badge-primary { background: rgba(99, 102, 241, 0.15); color: var(--primary-light); }
.badge-success { background: rgba(16, 185, 129, 0.15); color: var(--success); }
.badge-warning { background: rgba(245, 158, 11, 0.15); color: var(--accent); }

/* === TABS === */
.tabs { display: flex; gap: 0.5rem; margin-bottom: 2rem; flex-wrap: wrap; }
.tab-btn {
  padding: 0.75rem 1.5rem; border-radius: var(--radius);
  background: var(--bg-card); color: var(--text-muted);
  border: 1px solid var(--border); cursor: pointer;
  font-weight: 600; transition: var(--transition); font-family: inherit;
}
.tab-btn:hover { border-color: var(--primary); color: var(--text); }
.tab-btn.active { background: var(--primary); color: white; border-color: var(--primary); }
.tab-content { display: none; }
.tab-content.active { display: block; animation: fadeIn 0.3s ease; }

/* === ACCORDION === */
.accordion-item {
  background: var(--bg-card); border-radius: var(--radius);
  margin-bottom: 1rem; border: 1px solid var(--border); overflow: hidden;
}
.accordion-header {
  padding: 1.25rem 1.5rem; cursor: pointer;
  display: flex; justify-content: space-between; align-items: center;
  font-weight: 600; color: var(--text); transition: var(--transition);
}
.accordion-header:hover { background: var(--bg-card-hover); }
.accordion-content {
  padding: 0 1.5rem; max-height: 0; overflow: hidden;
  transition: max-height 0.3s ease, padding 0.3s ease;
}
.accordion-item.active .accordion-content { max-height: 500px; padding: 0 1.5rem 1.5rem; }
.accordion-item.active .accordion-header { color: var(--primary); }
.accordion-icon { transition: transform 0.3s ease; }
.accordion-item.active .accordion-icon { transform: rotate(180deg); }

/* === PROGRESS BAR === */
.progress-bar {
  width: 100%; height: 8px; background: var(--bg-alt);
  border-radius: var(--radius-full); overflow: hidden;
}
.progress-fill {
  height: 100%; background: var(--gradient-primary);
  border-radius: var(--radius-full); transition: width 1s ease;
}

/* === TOOLTIP === */
.tooltip { position: relative; cursor: pointer; }
.tooltip::after {
  content: attr(data-tooltip); position: absolute; bottom: 100%;
  left: 50%; transform: translateX(-50%) translateY(-8px);
  background: var(--bg-card); color: var(--text); padding: 0.5rem 1rem;
  border-radius: var(--radius-sm); font-size: 0.8rem; white-space: nowrap;
  opacity: 0; pointer-events: none; transition: var(--transition);
  box-shadow: var(--shadow-md); border: 1px solid var(--border);
}
.tooltip:hover::after { opacity: 1; transform: translateX(-50%) translateY(-4px); }

/* === MODAL === */
.modal-overlay {
  position: fixed; inset: 0; background: rgba(0,0,0,0.7);
  backdrop-filter: blur(8px); z-index: 2000;
  display: flex; align-items: center; justify-content: center;
  opacity: 0; pointer-events: none; transition: var(--transition);
}
.modal-overlay.active { opacity: 1; pointer-events: all; }
.modal {
  background: var(--bg-card); border-radius: var(--radius-lg);
  padding: 2.5rem; max-width: 500px; width: 90%;
  border: 1px solid var(--border); transform: scale(0.9);
  transition: var(--transition-bounce);
}
.modal-overlay.active .modal { transform: scale(1); }
.modal-close {
  position: absolute; top: 1rem; right: 1rem;
  background: none; border: none; color: var(--text-muted);
  font-size: 1.5rem; cursor: pointer; transition: var(--transition);
}
.modal-close:hover { color: var(--text); transform: rotate(90deg); }

/* === BACK TO TOP === */
.back-to-top {
  position: fixed; bottom: 2rem; right: 2rem;
  width: 50px; height: 50px; border-radius: var(--radius-full);
  background: var(--gradient-primary); color: white;
  display: flex; align-items: center; justify-content: center;
  font-size: 1.2rem; cursor: pointer; border: none;
  box-shadow: var(--shadow-md); opacity: 0; pointer-events: none;
  transition: var(--transition); z-index: 100;
}
.back-to-top.visible { opacity: 1; pointer-events: all; }
.back-to-top:hover { transform: translateY(-5px); box-shadow: var(--shadow-lg); }

/* === SKELETON LOADING === */
.skeleton {
  background: linear-gradient(90deg, var(--bg-card) 25%, var(--bg-card-hover) 50%, var(--bg-card) 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
  border-radius: var(--radius);
}
.skeleton-text { height: 1rem; margin-bottom: 0.5rem; }
.skeleton-title { height: 2rem; width: 60%; margin-bottom: 1rem; }
.skeleton-avatar { width: 48px; height: 48px; border-radius: 50%; }

/* === DIVIDER === */
.divider { width: 100%; height: 1px; background: var(--border); margin: 2rem 0; }
.divider-gradient { height: 2px; background: var(--gradient-primary); width: 80px; margin: 1rem auto; }

/* === ANIMACIONES === */
@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(40px); }
  to { opacity: 1; transform: translateY(0); }
}
@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
@keyframes slideInLeft {
  from { opacity: 0; transform: translateX(-40px); }
  to { opacity: 1; transform: translateX(0); }
}
@keyframes slideInRight {
  from { opacity: 0; transform: translateX(40px); }
  to { opacity: 1; transform: translateX(0); }
}
@keyframes scaleIn {
  from { opacity: 0; transform: scale(0.9); }
  to { opacity: 1; transform: scale(1); }
}
@keyframes pulse { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.05); } }
@keyframes float { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-10px); } }
@keyframes shimmer { 0% { background-position: -200% 0; } 100% { background-position: 200% 0; } }
@keyframes rotate { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
@keyframes bounce { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-20px); } }
@keyframes glow { 0%, 100% { box-shadow: 0 0 20px rgba(99, 102, 241, 0.3); } 50% { box-shadow: 0 0 40px rgba(99, 102, 241, 0.6); } }
.animate-fade-up { animation: fadeInUp 0.7s ease forwards; }
.animate-fade { animation: fadeIn 0.7s ease forwards; }
.animate-slide-left { animation: slideInLeft 0.7s ease forwards; }
.animate-slide-right { animation: slideInRight 0.7s ease forwards; }
.animate-scale { animation: scaleIn 0.5s ease forwards; }
.animate-float { animation: float 3s ease-in-out infinite; }
.animate-pulse { animation: pulse 2s ease-in-out infinite; }
.animate-bounce { animation: bounce 2s ease-in-out infinite; }
.animate-glow { animation: glow 2s ease-in-out infinite; }
.delay-1 { animation-delay: 0.1s; }
.delay-2 { animation-delay: 0.2s; }
.delay-3 { animation-delay: 0.3s; }
.delay-4 { animation-delay: 0.4s; }
.delay-5 { animation-delay: 0.5s; }

/* === UTILIDADES === */
.text-center { text-align: center; }
.text-left { text-align: left; }
.text-right { text-align: right; }
.mx-auto { margin-left: auto; margin-right: auto; }
.mt-1 { margin-top: 0.5rem; }
.mt-2 { margin-top: 1rem; }
.mt-3 { margin-top: 1.5rem; }
.mt-4 { margin-top: 2rem; }
.mb-1 { margin-bottom: 0.5rem; }
.mb-2 { margin-bottom: 1rem; }
.mb-3 { margin-bottom: 1.5rem; }
.mb-4 { margin-bottom: 2rem; }
.gap-1 { gap: 0.5rem; }
.gap-2 { gap: 1rem; }
.gap-3 { gap: 1.5rem; }
.flex { display: flex; }
.flex-center { display: flex; align-items: center; justify-content: center; }
.flex-between { display: flex; justify-content: space-between; align-items: center; }
.flex-wrap { flex-wrap: wrap; }
.hidden { display: none; }
.visible { opacity: 1; }
.overflow-hidden { overflow: hidden; }
.relative { position: relative; }
.w-full { width: 100%; }
.h-full { height: 100%; }
.min-h-screen { min-height: 100vh; }

/* === RESPONSIVE === */
@media (max-width: 1024px) {
  .grid-3, .plans-grid, .pricing-grid { grid-template-columns: repeat(2, 1fr); }
  .grid-4, .stats-grid { grid-template-columns: repeat(2, 1fr); }
  .footer-grid { grid-template-columns: repeat(2, 1fr); }
  .stats, .stats-section { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 768px) {
  .nav-links, .nav-menu, .nav-items {
    display: none; flex-direction: column; position: absolute;
    top: 100%; left: 0; right: 0; background: var(--bg-alt);
    padding: 1rem; border-bottom: 1px solid var(--border);
    box-shadow: var(--shadow-lg);
  }
  .nav-links.active, .nav-menu.active { display: flex; }
  .menu-toggle, .nav-toggle, .hamburger { display: flex; }
  .hero, .hero-section, header.hero-header { padding: 6rem 1.5rem 4rem; }
  .hero h1, .hero-title { font-size: 2.5rem; }
  section, .section { padding: 4rem 0; }
  .grid-2, .grid-3, .grid-4, .features-grid,
  .plans-grid, .pricing-grid, .auto-grid { grid-template-columns: 1fr; }
  .stats, .stats-section, .stats-grid { grid-template-columns: 1fr 1fr; }
  .footer-grid, .footer-content { grid-template-columns: 1fr; }
  .footer-bottom { flex-direction: column; gap: 1rem; text-align: center; }
  .form-row { grid-template-columns: 1fr; }
  .hero-buttons, .hero-cta { flex-direction: column; align-items: center; }
}
@media (max-width: 480px) {
  .container, .container-sm { padding: 0 1rem; }
  .hero h1, .hero-title { font-size: 2rem; }
  .stats, .stats-section { grid-template-columns: 1fr; }
  .pricing-card.featured, .plan-card.featured { transform: none; }
}

/* === PRINT === */
@media print {
  .navbar, .footer, .btn, .menu-toggle, .back-to-top { display: none; }
  body { background: white; color: black; }
  * { box-shadow: none !important; }
}'''
                            path = os.path.join(self.active_project, 'style.css')
                            with open(path, 'w', encoding='utf-8') as f:
                                f.write(fallback_css)
                            tool_result += f"\n[OK] Archivo creado (fallback): style.css ({len(fallback_css)} bytes)"
                        if needs_js:
                            fallback_js = '''// ================================================================
   IAM PREMIUM JAVASCRIPT v5.0 - Interacciones completas
   Features: Nav, Scroll, Animations, Tabs, Accordion, Modal, 
   Dark Mode, Form Validation, Back to Top, Counters, Typing
   ================================================================ */

document.addEventListener('DOMContentLoaded', () => {

  // ==========================================
  // 1. NAVEGACION ACTIVA AL SCROLL
  // ==========================================
  const sections = document.querySelectorAll('section[id]');
  const navLinks = document.querySelectorAll('.nav-link, .nav-links a');
  
  function updateNav() {
    const scrollY = window.scrollY;
    sections.forEach(section => {
      const top = section.offsetTop - 120;
      const height = section.offsetHeight;
      const id = section.getAttribute('id');
      if (scrollY >= top && scrollY < top + height) {
        navLinks.forEach(link => {
          link.classList.remove('active');
          if (link.getAttribute('href') === `#${id}` || 
              link.getAttribute('data-section') === id) {
            link.classList.add('active');
          }
        });
      }
    });
  }

  // ==========================================
  // 2. NAVBAR STICKY CON EFECTO GLASS
  // ==========================================
  const navbar = document.querySelector('.navbar, nav, .nav');
  function handleScroll() {
    if (!navbar) return;
    if (window.scrollY > 50) {
      navbar.classList.add('scrolled');
    } else {
      navbar.classList.remove('scrolled');
    }
  }

  // ==========================================
  // 3. ANIMACIONES AL SCROLL (IntersectionObserver)
  // ==========================================
  const animateElements = document.querySelectorAll('[data-animate], .feature-card, .card, .pricing-card');
  const animateOnScroll = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible', 'animate-fade-up');
        animateOnScroll.unobserve(entry.target);
      }
    });
  }, { threshold: 0.15, rootMargin: '0px 0px -50px 0px' });

  animateElements.forEach(el => animateOnScroll.observe(el));

  // ==========================================
  // 4. MOBILE MENU TOGGLE
  // ==========================================
  const navToggle = document.querySelector('.nav-toggle, .menu-toggle, .hamburger');
  const navLinksContainer = document.querySelector('.nav-links, .nav-menu, .nav-items');
  
  if (navToggle && navLinksContainer) {
    navToggle.addEventListener('click', () => {
      navLinksContainer.classList.toggle('active');
      navToggle.classList.toggle('active');
      // Animar barras del hamburger
      const spans = navToggle.querySelectorAll('span');
      if (spans.length >= 3) {
        spans[0].style.transform = navToggle.classList.contains('active') 
          ? 'rotate(45deg) translate(5px, 5px)' : '';
        spans[1].style.opacity = navToggle.classList.contains('active') ? '0' : '1';
        spans[2].style.transform = navToggle.classList.contains('active') 
          ? 'rotate(-45deg) translate(5px, -5px)' : '';
      }
    });
    // Cerrar menu al hacer click en un link
    navLinksContainer.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        navLinksContainer.classList.remove('active');
        navToggle.classList.remove('active');
      });
    });
  }

  // ==========================================
  // 5. SMOOTH SCROLL PARA LINKS
  // ==========================================
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      e.preventDefault();
      const targetId = this.getAttribute('href');
      if (targetId === '#') return;
      const target = document.querySelector(targetId);
      if (target) {
        const offset = navbar ? navbar.offsetHeight : 80;
        const targetPosition = target.getBoundingClientRect().top + window.scrollY - offset;
        window.scrollTo({ top: targetPosition, behavior: 'smooth' });
      }
    });
  });

  // ==========================================
  // 6. CONTADORES ANIMADOS
  // ==========================================
  function animateCounters() {
    const counters = document.querySelectorAll('[data-count], .stat-number, .counter');
    counters.forEach(counter => {
      if (counter.dataset.animated) return;
      const target = parseInt(counter.getAttribute('data-count') || counter.textContent);
      if (isNaN(target)) return;
      counter.dataset.animated = 'true';
      const duration = 2000;
      const step = target / (duration / 16);
      let current = 0;
      const timer = setInterval(() => {
        current += step;
        if (current >= target) {
          counter.textContent = target.toLocaleString();
          clearInterval(timer);
        } else {
          counter.textContent = Math.floor(current).toLocaleString();
        }
      }, 16);
    });
  }

  // Observar seccion de stats
  const statsSection = document.querySelector('.stats, .stats-section, .stats-grid');
  if (statsSection) {
    const statsObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          animateCounters();
          statsObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.3 });
    statsObserver.observe(statsSection);
  }

  // ==========================================
  // 7. TYPING EFFECT
  // ==========================================
  function typeWriter(element, text, speed = 50) {
    return new Promise(resolve => {
      let i = 0;
      element.textContent = '';
      function type() {
        if (i < text.length) {
          element.textContent += text.charAt(i);
          i++;
          setTimeout(type, speed);
        } else {
          resolve();
        }
      }
      type();
    });
  }

  // Aplicar typing effect a elementos con [data-typing]
  const typingElements = document.querySelectorAll('[data-typing]');
  typingElements.forEach(el => {
    const text = el.getAttribute('data-typing') || el.textContent;
    const speed = parseInt(el.getAttribute('data-speed')) || 50;
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          typeWriter(el, text, speed);
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.5 });
    observer.observe(el);
  });

  // ==========================================
  // 8. FORM VALIDATION
  // ==========================================
  const forms = document.querySelectorAll('form, .contact-form, .form');
  forms.forEach(form => {
    form.addEventListener('submit', function(e) {
      e.preventDefault();
      let isValid = true;
      const errors = [];

      // Validar campos requeridos
      this.querySelectorAll('[required]').forEach(field => {
        field.classList.remove('error');
        const errorEl = field.parentElement.querySelector('.error-message');
        if (errorEl) errorEl.remove();

        if (!field.value.trim()) {
          isValid = false;
          errors.push({ field, message: 'Este campo es requerido' });
          field.classList.add('error');
          const msg = document.createElement('span');
          msg.className = 'error-message';
          msg.style.color = 'var(--danger)';
          msg.style.fontSize = '0.8rem';
          msg.style.marginTop = '0.25rem';
          msg.textContent = 'Este campo es requerido';
          field.parentElement.appendChild(msg);
        }

        // Validar email
        if (field.type === 'email' && field.value) {
          const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
          if (!emailRegex.test(field.value)) {
            isValid = false;
            field.classList.add('error');
            const msg = document.createElement('span');
            msg.className = 'error-message';
            msg.style.color = 'var(--danger)';
            msg.style.fontSize = '0.8rem';
            msg.textContent = 'Email invalido';
            field.parentElement.appendChild(msg);
          }
        }
      });

      if (isValid) {
        // Exito - mostrar feedback
        const btn = this.querySelector('button[type="submit"], .btn-primary');
        if (btn) {
          const originalText = btn.textContent;
          btn.textContent = 'Enviado!';
          btn.style.background = 'var(--success)';
          setTimeout(() => {
            btn.textContent = originalText;
            btn.style.background = '';
            this.reset();
          }, 2000);
        }
      }
    });

    // Limpiar errores al escribir
    this.querySelectorAll('input, textarea').forEach(field => {
      field.addEventListener('input', () => {
        field.classList.remove('error');
        const errorEl = field.parentElement.querySelector('.error-message');
        if (errorEl) errorEl.remove();
      });
    });
  });

  // ==========================================
  // 9. TABS FUNCTIONALITY
  // ==========================================
  const tabContainers = document.querySelectorAll('.tabs, [data-tabs]');
  tabContainers.forEach(container => {
    const buttons = container.querySelectorAll('.tab-btn, [data-tab]');
    const contents = container.parentElement.querySelectorAll('.tab-content, [data-tab-content]');

    buttons.forEach(btn => {
      btn.addEventListener('click', () => {
        const target = btn.getAttribute('data-tab') || btn.getAttribute('href');
        
        // Remover active de todos
        buttons.forEach(b => b.classList.remove('active'));
        contents.forEach(c => c.classList.remove('active'));
        
        // Agregar active al clicked
        btn.classList.add('active');
        const targetContent = container.parentElement.querySelector(
          `.tab-content[data-tab-content="${target}"], .tab-content${target}`
        );
        if (targetContent) targetContent.classList.add('active');
      });
    });
  });

  // ==========================================
  // 10. ACCORDION
  // ==========================================
  const accordionItems = document.querySelectorAll('.accordion-item');
  accordionItems.forEach(item => {
    const header = item.querySelector('.accordion-header, .accordion-trigger');
    if (!header) return;
    
    header.addEventListener('click', () => {
      const isActive = item.classList.contains('active');
      
      // Cerrar todos los demas
      accordionItems.forEach(otherItem => {
        if (otherItem !== item) {
          otherItem.classList.remove('active');
          const otherContent = otherItem.querySelector('.accordion-content');
          if (otherContent) otherContent.style.maxHeight = null;
        }
      });
      
      // Toggle actual
      item.classList.toggle('active');
      const content = item.querySelector('.accordion-content');
      if (content) {
        if (!isActive) {
          content.style.maxHeight = content.scrollHeight + 'px';
        } else {
          content.style.maxHeight = null;
        }
      }
    });
  });

  // ==========================================
  // 11. MODAL
  // ==========================================
  const modalTriggers = document.querySelectorAll('.modal-trigger, [data-modal]');
  const modalOverlays = document.querySelectorAll('.modal-overlay');

  modalTriggers.forEach(trigger => {
    trigger.addEventListener('click', () => {
      const targetId = trigger.getAttribute('data-modal') || trigger.getAttribute('href');
      const modal = document.querySelector(targetId || '.modal-overlay');
      if (modal) {
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
      }
    });
  });

  // Cerrar modal
  document.querySelectorAll('.modal-close, .modal-overlay').forEach(el => {
    el.addEventListener('click', (e) => {
      if (e.target === el || el.classList.contains('modal-close')) {
        const overlay = el.closest('.modal-overlay') || el;
        overlay.classList.remove('active');
        document.body.style.overflow = '';
      }
    });
  });

  // Cerrar con ESC
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      modalOverlays.forEach(overlay => {
        overlay.classList.remove('active');
        document.body.style.overflow = '';
      });
    }
  });

  // ==========================================
  // 12. DARK MODE TOGGLE
  // ==========================================
  const darkModeToggle = document.querySelector('.dark-mode-toggle, [data-dark-mode]');
  if (darkModeToggle) {
    // Verificar preferencia guardada
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'light') {
      document.body.classList.add('light-mode');
    }

    darkModeToggle.addEventListener('click', () => {
      document.body.classList.toggle('light-mode');
      const isLight = document.body.classList.contains('light-mode');
      localStorage.setItem('theme', isLight ? 'light' : 'dark');
    });
  }

  // ==========================================
  // 13. BACK TO TOP BUTTON
  // ==========================================
  const backToTop = document.querySelector('.back-to-top, [data-back-to-top]');
  if (backToTop) {
    window.addEventListener('scroll', () => {
      if (window.scrollY > 500) {
        backToTop.classList.add('visible');
      } else {
        backToTop.classList.remove('visible');
      }
    });

    backToTop.addEventListener('click', () => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  // ==========================================
  // 14. SCROLL EVENT LISTENERS
  // ==========================================
  let ticking = false;
  window.addEventListener('scroll', () => {
    if (!ticking) {
      window.requestAnimationFrame(() => {
        updateNav();
        handleScroll();
        ticking = false;
      });
      ticking = true;
    }
  });

  // ==========================================
  // 15. PARALLAX EFFECT (opcional)
  // ==========================================
  const parallaxElements = document.querySelectorAll('[data-parallax]');
  if (parallaxElements.length > 0) {
    window.addEventListener('scroll', () => {
      const scrollY = window.scrollY;
      parallaxElements.forEach(el => {
        const speed = parseFloat(el.getAttribute('data-parallax')) || 0.5;
        const yPos = -(scrollY * speed);
        el.style.transform = `translateY(${yPos}px)`;
      });
    });
  }

  // ==========================================
  // 16. LOADING SKELETON
  // ==========================================
  function showSkeleton(container) {
    const skeleton = document.createElement('div');
    skeleton.className = 'skeleton';
    skeleton.innerHTML = `
      <div class="skeleton-title skeleton"></div>
      <div class="skeleton-text skeleton"></div>
      <div class="skeleton-text skeleton" style="width: 80%"></div>
      <div class="skeleton-text skeleton" style="width: 60%"></div>
    `;
    container.appendChild(skeleton);
    return skeleton;
  }

  // ==========================================
  // 17. TOOLTIP
  // ==========================================
  const tooltips = document.querySelectorAll('.tooltip');
  tooltips.forEach(tooltip => {
    tooltip.addEventListener('mouseenter', () => {
      const text = tooltip.getAttribute('data-tooltip');
      if (!text) return;
      const tip = document.createElement('div');
      tip.className = 'tooltip-content';
      tip.textContent = text;
      tip.style.cssText = `
        position: absolute; bottom: 100%; left: 50%; transform: translateX(-50%);
        background: var(--bg-card); color: var(--text); padding: 0.5rem 1rem;
        border-radius: var(--radius-sm); font-size: 0.8rem; white-space: nowrap;
        box-shadow: var(--shadow-md); border: 1px solid var(--border); z-index: 1000;
      `;
      tooltip.style.position = 'relative';
      tooltip.appendChild(tip);
    });

    tooltip.addEventListener('mouseleave', () => {
      const tip = tooltip.querySelector('.tooltip-content');
      if (tip) tip.remove();
    });
  });

  // ==========================================
  // INIT - Ejecutar todo al cargar
  // ==========================================
  updateNav();
  handleScroll();

  console.log('IAM Premium JS v5.0 loaded successfully');
});'''
                            path = os.path.join(self.active_project, 'script.js')
                            with open(path, 'w', encoding='utf-8') as f:
                                f.write(fallback_js)
                            tool_result += f"\n[OK] Archivo creado (fallback): script.js ({len(fallback_js)} bytes)"
            
            # PASO FINAL: Asegurar que HTML tenga <script src> y <link href> correctos, y CSS suficiente
            if self.active_project and os.path.isfile(os.path.join(self.active_project, 'index.html')):
                try:
                    html_path = os.path.join(self.active_project, 'index.html')
                    with open(html_path, 'r', encoding='utf-8') as f:
                        html = f.read()
                    modified = False
                    
                    # Verificar si CSS tiene suficiente contenido
                    css_files = [f for f in os.listdir(self.active_project) if f.endswith('.css')]
                    css_ok = False
                    for css_file in css_files:
                        css_path = os.path.join(self.active_project, css_file)
                        try:
                            with open(css_path, 'r', encoding='utf-8') as f:
                                if len(f.readlines()) >= 50:
                                    css_ok = True
                        except:
                            pass
                    
                    # Si CSS no tiene suficiente contenido, reemplazar con fallback completo
                    if not css_ok:
                        fallback_css = '''/* ================================================================
   IAM PREMIUM CSS - Estilos automatizados de alta calidad
   ================================================================ */

/* === VARIABLES === */
:root {
  --primary: #6366f1;
  --primary-light: #818cf8;
  --primary-dark: #4f46e5;
  --secondary: #06b6d4;
  --secondary-light: #22d3ee;
  --accent: #f59e0b;
  --accent-light: #fbbf24;
  --success: #10b981;
  --danger: #ef4444;
  --bg: #0f172a;
  --bg-alt: #1e293b;
  --bg-card: #1e293b;
  --bg-card-hover: #334155;
  --bg-glass: rgba(30, 41, 59, 0.7);
  --text: #f1f5f9;
  --text-light: #e2e8f0;
  --text-muted: #94a3b8;
  --text-dim: #64748b;
  --border: rgba(99, 102, 241, 0.15);
  --border-light: rgba(148, 163, 184, 0.1);
  --shadow-xs: 0 1px 2px rgba(0,0,0,0.3);
  --shadow-sm: 0 2px 8px rgba(0,0,0,0.3);
  --shadow-md: 0 8px 30px rgba(0,0,0,0.35);
  --shadow-lg: 0 20px 60px rgba(0,0,0,0.4);
  --shadow-glow: 0 0 40px rgba(99, 102, 241, 0.25);
  --shadow-glow-lg: 0 0 80px rgba(99, 102, 241, 0.35);
  --gradient-primary: linear-gradient(135deg, #6366f1 0%, #06b6d4 100%);
  --gradient-warm: linear-gradient(135deg, #f59e0b 0%, #ef4444 100%);
  --gradient-cool: linear-gradient(135deg, #06b6d4 0%, #10b981 100%);
  --gradient-dark: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
  --gradient-hero: linear-gradient(160deg, #0f172a 0%, #1a1040 35%, #312e81 65%, #1e293b 100%);
  --gradient-glass: linear-gradient(135deg, rgba(255,255,255,0.05) 0%, rgba(255,255,255,0.02) 100%);
  --radius-sm: 8px;
  --radius: 12px;
  --radius-md: 16px;
  --radius-lg: 24px;
  --radius-xl: 32px;
  --radius-full: 9999px;
  --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  --transition-slow: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
  --transition-bounce: all 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
}

/* === RESET === */
*, *::before, *::after {
  margin: 0; padding: 0; box-sizing: border-box;
}
html {
  scroll-behavior: smooth;
  font-size: 16px;
  scrollbar-width: thin;
  scrollbar-color: var(--primary) var(--bg);
}
body {
  font-family: 'Inter', 'Segoe UI', system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
  background: var(--bg);
  color: var(--text);
  line-height: 1.7;
  overflow-x: hidden;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

/* === SCROLLBAR === */
::-webkit-scrollbar { width: 8px; height: 8px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--primary); border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: var(--primary-light); }
::selection { background: var(--primary); color: white; }

/* === TIPOGRAFIA === */
h1, h2, h3, h4, h5, h6 {
  font-weight: 800; line-height: 1.15;
  color: var(--text); letter-spacing: -0.02em;
}
h1 { font-size: clamp(2.5rem, 6vw, 4.5rem); }
h2 { font-size: clamp(2rem, 4vw, 3rem); }
h3 { font-size: clamp(1.5rem, 3vw, 2rem); }
h4 { font-size: clamp(1.2rem, 2vw, 1.5rem); }
p { color: var(--text-muted); font-size: 1.05rem; max-width: 65ch; }
a { color: var(--secondary); text-decoration: none; transition: var(--transition); }
a:hover { color: var(--secondary-light); }
strong, b { font-weight: 700; color: var(--text); }
small { font-size: 0.875rem; }
.text-gradient {
  background: var(--gradient-primary); -webkit-background-clip: text;
  -webkit-text-fill-color: transparent; background-clip: text;
}

/* === CONTENEDOR === */
.container { max-width: 1200px; margin: 0 auto; padding: 0 2rem; }
.container-sm { max-width: 800px; margin: 0 auto; padding: 0 2rem; }
.container-lg { max-width: 1400px; margin: 0 auto; padding: 0 2rem; }

/* === NAVBAR === */
.navbar, nav, .nav, header nav {
  position: fixed; top: 0; left: 0; right: 0; z-index: 1000;
  background: rgba(15, 23, 42, 0.85);
  backdrop-filter: blur(20px) saturate(180%);
  -webkit-backdrop-filter: blur(20px) saturate(180%);
  border-bottom: 1px solid var(--border);
  padding: 0.75rem 0;
  transition: var(--transition);
}
.navbar.scrolled, .nav.scrolled {
  background: rgba(15, 23, 42, 0.95);
  box-shadow: var(--shadow-md);
}
.nav-container, .nav-wrapper, .nav-content, .nav-inner {
  max-width: 1200px; margin: 0 auto; padding: 0 2rem;
  display: flex; justify-content: space-between; align-items: center;
}
.nav-logo, .logo, .brand, .navbar-brand {
  font-size: 1.5rem; font-weight: 800; color: var(--text);
  letter-spacing: -0.03em; transition: var(--transition);
}
.nav-logo span, .logo span, .brand span { color: var(--primary); }
.nav-logo:hover, .logo:hover { transform: scale(1.02); }
.nav-links, .nav-menu, .nav-items {
  display: flex; align-items: center; gap: 0.5rem; list-style: none;
}
.nav-links a, .nav-menu a, .nav-link, .nav-item a {
  color: var(--text-muted); font-weight: 500; font-size: 0.9rem;
  padding: 0.5rem 1rem; border-radius: var(--radius-sm);
  transition: var(--transition); position: relative;
}
.nav-links a:hover, .nav-links a.active,
.nav-link:hover, .nav-link.active, .nav-item a:hover {
  color: var(--text); background: rgba(99, 102, 241, 0.1);
}
.nav-links a::after, .nav-link::after {
  content: ''; position: absolute; bottom: 0; left: 50%; width: 0; height: 2px;
  background: var(--primary); transition: var(--transition); transform: translateX(-50%);
}
.nav-links a:hover::after, .nav-link:hover::after { width: 60%; }
.nav-cta { margin-left: 1rem; }
.menu-toggle, .nav-toggle, .hamburger {
  display: none; flex-direction: column; gap: 5px; cursor: pointer;
  background: none; border: none; padding: 0.5rem;
}
.menu-toggle span, .nav-toggle span, .hamburger span {
  width: 24px; height: 2px; background: var(--text);
  transition: var(--transition); border-radius: 2px;
}

/* === HERO === */
.hero, .hero-section, header.hero-header, .hero-banner {
  min-height: 100vh; display: flex; align-items: center; justify-content: center;
  background: var(--gradient-hero); position: relative; padding: 8rem 2rem 6rem;
  overflow: hidden;
}
.hero::before {
  content: ''; position: absolute; inset: 0;
  background: radial-gradient(ellipse at 30% 50%, rgba(99, 102, 241, 0.15) 0%, transparent 60%),
              radial-gradient(ellipse at 70% 50%, rgba(6, 182, 212, 0.1) 0%, transparent 60%);
}
.hero-content, .hero-text, .hero-center, .hero-body {
  position: relative; z-index: 1; max-width: 800px; text-align: center;
}
.hero h1, .hero-title, .hero-heading {
  font-size: clamp(2.8rem, 8vw, 5.5rem); font-weight: 800;
  line-height: 1.05; margin-bottom: 1.5rem; color: white;
  text-shadow: 0 2px 40px rgba(0,0,0,0.3);
}
.hero p, .hero-subtitle, .hero-description, .hero-text p {
  font-size: clamp(1.1rem, 2vw, 1.4rem); color: rgba(255,255,255,0.8);
  margin-bottom: 2.5rem; max-width: 600px; margin-left: auto; margin-right: auto;
  line-height: 1.7;
}
.hero-buttons, .hero-cta, .hero-actions, .hero-btns {
  display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap;
}
.hero-image, .hero-img, .hero-visual {
  position: absolute; right: -5%; bottom: -10%; width: 50%; max-width: 600px;
  opacity: 0.15; pointer-events: none;
}

/* === SECCIONES === */
section, .section, [class*="section-"] {
  padding: 7rem 0; position: relative;
}
.section-alt, .section-gray, .bg-alt {
  background: var(--bg-alt);
}
.section-header, .section-title-wrap, .section-top {
  text-align: center; margin-bottom: 4rem;
}
.section-title, .section-header h2, .section-heading {
  font-size: clamp(2rem, 4vw, 3rem); font-weight: 800;
  margin-bottom: 1rem; position: relative; display: inline-block;
}
.section-title::after, .section-header h2::after {
  content: ''; display: block; width: 60px; height: 4px;
  background: var(--gradient-primary); border-radius: 2px;
  margin: 1rem auto 0;
}
.section-subtitle, .section-header p, .section-desc {
  color: var(--text-muted); font-size: 1.15rem;
  max-width: 600px; margin: 0 auto; line-height: 1.7;
}

/* === CARDS === */
.card, .feature-card, .pricing-card, .plan-card,
.testimonial-card, .blog-card, .project-card, .service-card {
  background: var(--bg-card); border-radius: var(--radius-lg);
  padding: 2rem; position: relative; overflow: hidden;
  border: 1px solid var(--border);
  transition: var(--transition);
}
.card::before, .feature-card::before {
  content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px;
  background: var(--gradient-primary); opacity: 0; transition: var(--transition);
}
.card:hover, .feature-card:hover, .pricing-card:hover,
.plan-card:hover, .service-card:hover {
  transform: translateY(-8px);
  box-shadow: var(--shadow-lg), var(--shadow-glow);
  border-color: rgba(99, 102, 241, 0.3);
}
.card:hover::before, .feature-card:hover::before { opacity: 1; }
.card-icon, .feature-icon, .icon-box {
  width: 60px; height: 60px; border-radius: var(--radius);
  background: var(--gradient-primary); display: flex;
  align-items: center; justify-content: center;
  font-size: 1.5rem; margin-bottom: 1.5rem;
  box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
}
.card h3, .feature-card h3, .pricing-card h3 {
  font-size: 1.3rem; font-weight: 700; margin-bottom: 0.75rem;
}
.card p, .feature-card p {
  color: var(--text-muted); font-size: 0.95rem; line-height: 1.7;
}

/* === BOTONES === */
.btn, button, .cta-button, .btn-cta {
  display: inline-flex; align-items: center; justify-content: center;
  gap: 0.5rem; padding: 0.85rem 2rem; border-radius: var(--radius);
  font-weight: 600; font-size: 1rem; cursor: pointer;
  border: none; transition: var(--transition); text-decoration: none;
  font-family: inherit; letter-spacing: -0.01em;
}
.btn-primary, .cta-button, .btn-cta, button[type="submit"],
.btn-main, .btn-solid {
  background: var(--gradient-primary); color: white;
  box-shadow: 0 4px 15px rgba(99, 102, 241, 0.35);
}
.btn-primary:hover, .cta-button:hover, .btn-cta:hover,
button[type="submit"]:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 30px rgba(99, 102, 241, 0.45);
}
.btn-secondary, .btn-outline, .btn-ghost {
  background: transparent; color: var(--primary-light);
  border: 2px solid var(--primary);
}
.btn-secondary:hover, .btn-outline:hover {
  background: var(--primary); color: white; transform: translateY(-2px);
}
.btn-sm { padding: 0.6rem 1.2rem; font-size: 0.875rem; }
.btn-lg { padding: 1rem 2.5rem; font-size: 1.1rem; }
.btn-icon { padding: 0.75rem; border-radius: var(--radius-sm); }

/* === GRID === */
.grid { display: grid; gap: 2rem; }
.grid-2, .features-grid, .cols-2 { grid-template-columns: repeat(2, 1fr); }
.grid-3, .plans-grid, .pricing-grid, .cols-3 { grid-template-columns: repeat(3, 1fr); }
.grid-4, .stats-grid, .cols-4 { grid-template-columns: repeat(4, 1fr); }
.grid-auto, .auto-grid { grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); }

/* === IMAGENES === */
img { max-width: 100%; height: auto; display: block; }
.image-wrapper, .img-container, .img-box {
  overflow: hidden; border-radius: var(--radius-lg); position: relative;
}
.image-wrapper::after {
  content: ''; position: absolute; inset: 0;
  background: linear-gradient(to top, rgba(0,0,0,0.3) 0%, transparent 50%);
  pointer-events: none;
}
.img-overlay { position: relative; }
.img-overlay img { transition: var(--transition-slow); }
.img-overlay:hover img { transform: scale(1.05); }

/* === FORMULARIOS === */
.form-group, .input-group { margin-bottom: 1.5rem; }
.form-group label, .input-label {
  display: block; font-weight: 600; font-size: 0.9rem;
  margin-bottom: 0.5rem; color: var(--text);
}
input, textarea, select, .form-input, .form-control {
  width: 100%; padding: 0.9rem 1.2rem; border-radius: var(--radius);
  border: 1px solid var(--border); background: var(--bg-alt);
  color: var(--text); font-size: 1rem; font-family: inherit;
  transition: var(--transition);
}
input:focus, textarea:focus, select:focus, .form-input:focus {
  outline: none; border-color: var(--primary);
  box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.15);
  background: var(--bg-card);
}
textarea { min-height: 120px; resize: vertical; }
.form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }

/* === LISTAS === */
ul, ol { list-style: none; padding: 0; }
li { padding: 0.4rem 0; }
.feature-list li, .check-list li {
  display: flex; align-items: flex-start; gap: 0.75rem; padding: 0.6rem 0;
}
.feature-list li::before, .check-list li::before {
  content: '✓'; color: var(--success); font-weight: 700;
  min-width: 20px; font-size: 1.1rem;
}

/* === TABLA === */
table { width: 100%; border-collapse: collapse; }
th, td { padding: 1rem 1.25rem; text-align: left; }
th { font-weight: 700; color: var(--text); border-bottom: 2px solid var(--border); }
td { border-bottom: 1px solid var(--border-light); }
tr:hover td { background: rgba(99, 102, 241, 0.05); }

/* === TESTIMONIOS === */
.testimonial, .testimonial-card, .review-card {
  background: var(--bg-card); border-radius: var(--radius-lg);
  padding: 2.5rem; border: 1px solid var(--border);
  position: relative;
}
.testimonial::before, .review-card::before {
  content: '"'; position: absolute; top: 1rem; left: 1.5rem;
  font-size: 5rem; color: var(--primary); opacity: 0.15;
  font-family: Georgia, serif; line-height: 1;
}
.testimonial-quote, .quote, .review-text {
  font-style: italic; color: var(--text-light);
  margin-bottom: 1.5rem; font-size: 1.05rem; line-height: 1.8;
  position: relative; z-index: 1;
}
.testimonial-author, .author, .review-author {
  display: flex; align-items: center; gap: 1rem;
}
.testimonial-avatar, .avatar {
  width: 48px; height: 48px; border-radius: 50%;
  background: var(--gradient-primary); display: flex;
  align-items: center; justify-content: center;
  font-weight: 700; color: white;
}
.testimonial-name, .author-name { font-weight: 700; color: var(--text); }
.testimonial-role, .author-role { font-size: 0.85rem; color: var(--text-dim); }

/* === PRECIOS === */
.pricing-card, .plan-card {
  text-align: center; padding: 3rem 2rem;
}
.pricing-card.featured, .plan-card.featured, .pricing-popular {
  border-color: var(--primary); transform: scale(1.05);
  box-shadow: var(--shadow-glow-lg);
}
.pricing-badge, .plan-badge, .badge-popular {
  position: absolute; top: -1px; left: 50%; transform: translateX(-50%);
  background: var(--gradient-primary); color: white;
  padding: 0.4rem 1.5rem; border-radius: 0 0 var(--radius) var(--radius);
  font-size: 0.8rem; font-weight: 700; text-transform: uppercase;
  letter-spacing: 0.05em;
}
.price, .pricing-amount, .plan-price {
  font-size: 3.5rem; font-weight: 800; color: var(--text);
  line-height: 1; margin: 1.5rem 0;
}
.price span, .pricing-currency { font-size: 1.5rem; vertical-align: top; }
.price-period, .pricing-period, .plan-period {
  font-size: 1rem; color: var(--text-dim); margin-bottom: 2rem;
}
.pricing-features, .plan-features {
  text-align: left; margin: 2rem 0;
}
.pricing-features li, .plan-features li {
  display: flex; align-items: center; gap: 0.75rem;
  padding: 0.75rem 0; border-bottom: 1px solid var(--border-light);
  color: var(--text-muted);
}
.pricing-features li::before { content: '✓'; color: var(--success); font-weight: 700; }

/* === STATS === */
.stats, .stats-section, .stats-grid {
  display: grid; grid-template-columns: repeat(4, 1fr);
  gap: 2rem; padding: 4rem 0;
}
.stat-item, .stat, .stat-card { text-align: center; }
.stat-number, .stat-count, .stat-value {
  font-size: clamp(2.5rem, 5vw, 4rem); font-weight: 800;
  color: var(--primary); display: block; line-height: 1;
  margin-bottom: 0.5rem;
}
.stat-label, .stat-title {
  color: var(--text-muted); font-size: 0.95rem; font-weight: 500;
}

/* === FOOTER === */
footer, .footer, .site-footer {
  background: var(--bg-alt); padding: 5rem 0 2rem;
  border-top: 1px solid var(--border);
}
.footer-grid, .footer-content {
  display: grid; grid-template-columns: 2fr 1fr 1fr 1fr;
  gap: 3rem; margin-bottom: 3rem;
}
.footer-brand, .footer-about { max-width: 300px; }
.footer-brand p { margin-top: 1rem; font-size: 0.9rem; }
.footer-title, .footer-heading {
  font-size: 1rem; font-weight: 700; color: var(--text);
  margin-bottom: 1.5rem; text-transform: uppercase;
  letter-spacing: 0.05em;
}
.footer-links { display: flex; flex-direction: column; gap: 0.75rem; }
.footer-links a { color: var(--text-muted); font-size: 0.9rem; transition: var(--transition); }
.footer-links a:hover { color: var(--primary); transform: translateX(4px); }
.footer-social { display: flex; gap: 0.75rem; margin-top: 1.5rem; }
.footer-social a {
  width: 40px; height: 40px; border-radius: var(--radius-sm);
  background: var(--bg-card); display: flex; align-items: center; justify-content: center;
  color: var(--text-muted); transition: var(--transition);
}
.footer-social a:hover { background: var(--primary); color: white; transform: translateY(-3px); }
.footer-bottom {
  padding-top: 2rem; border-top: 1px solid var(--border);
  display: flex; justify-content: space-between; align-items: center;
  color: var(--text-dim); font-size: 0.85rem;
}

/* === BADGES === */
.badge, .tag, .label {
  display: inline-block; padding: 0.35rem 0.9rem;
  border-radius: var(--radius-full); font-size: 0.75rem;
  font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em;
}
.badge-primary { background: rgba(99, 102, 241, 0.15); color: var(--primary-light); }
.badge-success { background: rgba(16, 185, 129, 0.15); color: var(--success); }
.badge-warning { background: rgba(245, 158, 11, 0.15); color: var(--accent); }

/* === TABS === */
.tabs { display: flex; gap: 0.5rem; margin-bottom: 2rem; flex-wrap: wrap; }
.tab-btn {
  padding: 0.75rem 1.5rem; border-radius: var(--radius);
  background: var(--bg-card); color: var(--text-muted);
  border: 1px solid var(--border); cursor: pointer;
  font-weight: 600; transition: var(--transition); font-family: inherit;
}
.tab-btn:hover { border-color: var(--primary); color: var(--text); }
.tab-btn.active {
  background: var(--primary); color: white;
  border-color: var(--primary);
}

/* === ACCORDION === */
.accordion-item {
  background: var(--bg-card); border-radius: var(--radius);
  margin-bottom: 1rem; border: 1px solid var(--border); overflow: hidden;
}
.accordion-header {
  padding: 1.25rem 1.5rem; cursor: pointer;
  display: flex; justify-content: space-between; align-items: center;
  font-weight: 600; color: var(--text); transition: var(--transition);
}
.accordion-header:hover { background: var(--bg-card-hover); }
.accordion-content {
  padding: 0 1.5rem; max-height: 0; overflow: hidden;
  transition: max-height 0.3s ease, padding 0.3s ease;
}
.accordion-item.active .accordion-content {
  max-height: 500px; padding: 0 1.5rem 1.5rem;
}
.accordion-item.active .accordion-header { color: var(--primary); }

/* === PROGRESS BAR === */
.progress-bar {
  width: 100%; height: 8px; background: var(--bg-alt);
  border-radius: var(--radius-full); overflow: hidden;
}
.progress-fill {
  height: 100%; background: var(--gradient-primary);
  border-radius: var(--radius-full); transition: width 1s ease;
}

/* === TOOLTIP === */
.tooltip {
  position: relative; cursor: pointer;
}
.tooltip::after {
  content: attr(data-tooltip); position: absolute; bottom: 100%;
  left: 50%; transform: translateX(-50%) translateY(-8px);
  background: var(--bg-card); color: var(--text); padding: 0.5rem 1rem;
  border-radius: var(--radius-sm); font-size: 0.8rem; white-space: nowrap;
  opacity: 0; pointer-events: none; transition: var(--transition);
  box-shadow: var(--shadow-md); border: 1px solid var(--border);
}
.tooltip:hover::after { opacity: 1; transform: translateX(-50%) translateY(-4px); }

/* === DIVIDER === */
.divider {
  width: 100%; height: 1px; background: var(--border);
  margin: 2rem 0;
}
.divider-gradient {
  height: 2px; background: var(--gradient-primary);
  width: 80px; margin: 1rem auto;
}

/* === ANIMACIONES === */
@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(40px); }
  to { opacity: 1; transform: translateY(0); }
}
@keyframes fadeIn {
  from { opacity: 0; } to { opacity: 1; }
}
@keyframes slideInLeft {
  from { opacity: 0; transform: translateX(-40px); }
  to { opacity: 1; transform: translateX(0); }
}
@keyframes slideInRight {
  from { opacity: 0; transform: translateX(40px); }
  to { opacity: 1; transform: translateX(0); }
}
@keyframes scaleIn {
  from { opacity: 0; transform: scale(0.9); }
  to { opacity: 1; transform: scale(1); }
}
@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.05); }
}
@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}
@keyframes shimmer {
  0% { background-position: -200% 0; }
  100% { background-position: 200% 0; }
}
.animate-fade-up { animation: fadeInUp 0.7s ease forwards; }
.animate-fade { animation: fadeIn 0.7s ease forwards; }
.animate-slide-left { animation: slideInLeft 0.7s ease forwards; }
.animate-slide-right { animation: slideInRight 0.7s ease forwards; }
.animate-scale { animation: scaleIn 0.5s ease forwards; }
.animate-float { animation: float 3s ease-in-out infinite; }
.animate-pulse { animation: pulse 2s ease-in-out infinite; }
.delay-1 { animation-delay: 0.1s; }
.delay-2 { animation-delay: 0.2s; }
.delay-3 { animation-delay: 0.3s; }
.delay-4 { animation-delay: 0.4s; }
.delay-5 { animation-delay: 0.5s; }

/* === UTILIDADES === */
.text-center { text-align: center; }
.text-left { text-align: left; }
.text-right { text-align: right; }
.mx-auto { margin-left: auto; margin-right: auto; }
.mt-1 { margin-top: 0.5rem; }
.mt-2 { margin-top: 1rem; }
.mt-3 { margin-top: 1.5rem; }
.mt-4 { margin-top: 2rem; }
.mb-1 { margin-bottom: 0.5rem; }
.mb-2 { margin-bottom: 1rem; }
.mb-3 { margin-bottom: 1.5rem; }
.mb-4 { margin-bottom: 2rem; }
.gap-1 { gap: 0.5rem; }
.gap-2 { gap: 1rem; }
.gap-3 { gap: 1.5rem; }
.flex { display: flex; }
.flex-center { display: flex; align-items: center; justify-content: center; }
.flex-between { display: flex; justify-content: space-between; align-items: center; }
.flex-wrap { flex-wrap: wrap; }
.hidden { display: none; }
.visible { opacity: 1; }
.overflow-hidden { overflow: hidden; }
.relative { position: relative; }

/* === RESPONSIVE === */
@media (max-width: 1024px) {
  .grid-3, .plans-grid, .pricing-grid { grid-template-columns: repeat(2, 1fr); }
  .grid-4, .stats-grid { grid-template-columns: repeat(2, 1fr); }
  .footer-grid { grid-template-columns: repeat(2, 1fr); }
  .stats, .stats-section { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 768px) {
  .nav-links, .nav-menu, .nav-items {
    display: none; flex-direction: column; position: absolute;
    top: 100%; left: 0; right: 0; background: var(--bg-alt);
    padding: 1rem; border-bottom: 1px solid var(--border);
    box-shadow: var(--shadow-lg);
  }
  .nav-links.active, .nav-menu.active { display: flex; }
  .menu-toggle, .nav-toggle, .hamburger { display: flex; }
  .hero, .hero-section, header.hero-header { padding: 6rem 1.5rem 4rem; }
  .hero h1, .hero-title { font-size: 2.5rem; }
  section, .section { padding: 4rem 0; }
  .grid-2, .grid-3, .grid-4, .features-grid,
  .plans-grid, .pricing-grid, .auto-grid { grid-template-columns: 1fr; }
  .stats, .stats-section, .stats-grid { grid-template-columns: 1fr 1fr; }
  .footer-grid, .footer-content { grid-template-columns: 1fr; }
  .footer-bottom { flex-direction: column; gap: 1rem; text-align: center; }
  .form-row { grid-template-columns: 1fr; }
  .hero-buttons, .hero-cta { flex-direction: column; align-items: center; }
}
@media (max-width: 480px) {
  .container, .container-sm { padding: 0 1rem; }
  .hero h1, .hero-title { font-size: 2rem; }
  .stats, .stats-section { grid-template-columns: 1fr; }
  .pricing-card.featured, .plan-card.featured { transform: none; }
}

/* === PRINT === */
@media print {
  .navbar, .footer, .btn, .menu-toggle { display: none; }
  body { background: white; color: black; }
  * { box-shadow: none !important; }
}'''
                        with open(css_path, 'w', encoding='utf-8') as f:
                            f.write(fallback_css)
                        tool_result += f"\n[OK] CSS fallback premium: style.css ({len(fallback_css)} bytes)"
                    
                    # Agregar <link rel="stylesheet" href="style.css"> si no existe
                    if 'style.css' not in html and os.path.isfile(os.path.join(self.active_project, 'style.css')):
                        if '</head>' in html:
                            html = html.replace('</head>', '    <link rel="stylesheet" href="style.css">\n</head>')
                            modified = True
                    
                    # Agregar <script src="script.js"> si no existe
                    if 'script.js' not in html and os.path.isfile(os.path.join(self.active_project, 'script.js')):
                        if '</body>' in html:
                            html = html.replace('</body>', '    <script src="script.js"></script>\n</body>')
                            modified = True
                        elif '</html>' in html:
                            html = html.replace('</html>', '    <script src="script.js"></script>\n</html>')
                            modified = True
                        else:
                            html += '\n<script src="script.js"></script>'
                            modified = True
                    
                    if modified:
                        with open(html_path, 'w', encoding='utf-8') as f:
                            f.write(html)
                        tool_result += "\n[OK] Tags CSS/JS agregados al HTML"
                except:
                    pass
            
            # Si no hizo nada - un solo reintento
            if '[OK]' not in tool_result:
                if not self.active_project:
                    detected = self._detect_project_folder(user_message)
                    if detected:
                        self.active_project = detected
                
                if self.active_project:
                    follow_up = self._chat_normal(
                        f"IMPORTANTE: El usuario pidio crear archivos. "
                        f"Usa [TOOL_CALL] para crearlos. "
                        f"Archivos en proyecto: {os.listdir(self.active_project)[:5]}. "
                        f"Crea los archivos AHORA: "
                        f"[TOOL_CALL] action: create_file name: \"index.html\" <!DOCTYPE html>...</html> [/TOOL_CALL]"
                    )
                    if follow_up:
                        follow_result = self._execute_tool_calls(follow_up)
                        if follow_result and '[OK]' in follow_result:
                            tool_result = follow_result
            
            response = tool_result
        
        # Limpiar artefactos de markdown de la respuesta
        if response:
            response = self._cleanup_response(response)
        
        if response:
            self.current_session.add_message("assistant", response)
        
        if thinking_output and response:
            return thinking_output + "\n" + response
        
        return response
    
    def _extract_from_markdown(self, text: str) -> tuple:
        """
        Extraer archivos de bloques markdown ```code```.
        Returns: (tool_blocks, unclosed_block)
        """
        import re
        
        tool_blocks = []
        unclosed_block = None
        
        # Buscar bloques markdown con archivos
        # Formato: **filename** ```language\ncode\n```
        pattern = r'\*\*(\w+\.\w+)\*\*\s*```(\w*)\n(.*?)```'
        matches = re.findall(pattern, text, re.DOTALL)
        
        for filename, lang, content in matches:
            if filename.endswith(('.html', '.css', '.js')):
                tool_block = f'action: create_file name: "{filename}"\n{content.strip()}'
                tool_blocks.append(tool_block)
        
        # Si no encontro con **filename**, buscar solo bloques de codigo
        if not tool_blocks:
            # Buscar ```html ... ``` o ```css ... ``` o ```javascript ... ```
            code_pattern = r'```(?:html|css|javascript|js)\n(.*?)```'
            code_matches = re.findall(code_pattern, text, re.DOTALL)
            
            # Determinar tipo por orden
            extensions = ['.html', '.css', '.js']
            for i, content in enumerate(code_matches):
                if i < len(extensions):
                    filename = f'{"index" if i == 0 else "style" if i == 1 else "script"}{extensions[i]}'
                    tool_block = f'action: create_file name: "{filename}"\n{content.strip()}'
                    tool_blocks.append(tool_block)
        
        # Si aun no encontro, buscar bloques de codigo sin language tag
        if not tool_blocks:
            # Buscar ```\n...``` (sin tag de lenguaje) que contengan HTML/CSS/JS
            raw_pattern = r'```\n(.*?)```'
            raw_matches = re.findall(raw_pattern, text, re.DOTALL)
            
            for content in raw_matches:
                content = content.strip()
                if not content:
                    continue
                # Detectar tipo por contenido
                if '<!DOCTYPE' in content or '<html' in content.lower():
                    tool_block = f'action: create_file name: "index.html"\n{content}'
                    tool_blocks.append(tool_block)
                elif '{' in content and ':' in content and ('.' in content or '#' in content):
                    tool_block = f'action: create_file name: "style.css"\n{content}'
                    tool_blocks.append(tool_block)
                elif 'function' in content or 'const ' in content or 'document.' in content or 'addEventListener' in content:
                    tool_block = f'action: create_file name: "script.js"\n{content}'
                    tool_blocks.append(tool_block)
        
        # Fallback agresivo: buscar código sin bloques markdown
        if not tool_blocks:
            # Buscar HTML/CSS/JS directamente en el texto
            html_pattern = r'(<!DOCTYPE[^>]*>[\s\S]*?</html>)'
            html_matches = re.findall(html_pattern, text, re.DOTALL)
            for content in html_matches:
                tool_block = f'action: create_file name: "index.html"\n{content.strip()}'
                tool_blocks.append(tool_block)
            
            # Buscar CSS
            css_pattern = r'(\{[\s\S]*?\})'
            if not tool_blocks:
                css_matches = re.findall(r'(:root\s*\{[\s\S]*?\})', text, re.DOTALL)
                for content in css_matches:
                    tool_block = f'action: create_file name: "style.css"\n{content.strip()}'
                    tool_blocks.append(tool_block)
            
            # Buscar JS
            js_pattern = r'(document\.[\s\S]*?\})'
            if not tool_blocks:
                js_matches = re.findall(js_pattern, text, re.DOTALL)
                for content in js_matches:
                    tool_block = f'action: create_file name: "script.js"\n{content.strip()}'
                    tool_blocks.append(tool_block)
        
        return tool_blocks, unclosed_block
    
    def _execute_tool_calls(self, response: str) -> str:
        """
        Ejecutar TOOL_CALLs de la IA.
        Soporta formato TOOL_CALL y formato markdown (```code```).
        """
        import re
        
        if not response:
            return response
        
        # Normalizar marcadores
        text = response.replace('<tool_call>', '[TOOL_CALL]').replace('</tool_call>', '[/TOOL_CALL]')
        text = text.replace('[TOOLCALL]', '[TOOL_CALL]').replace('[/TOOLCALL]', '[/TOOL_CALL]')
        
        # Extraer bloques TOOL_CALL completos
        tool_blocks = re.findall(r'\[TOOL_CALL\](.*?)\[/TOOL_CALL\]', text, re.DOTALL)
        
        # Buscar TOOL_CALL sin cerrar al final de la respuesta
        last_open = text.rfind('[TOOL_CALL]')
        last_close = text.rfind('[/TOOL_CALL]')
        
        unclosed_block = None
        if last_open > last_close:
            unclosed_text = text[last_open + len('[TOOL_CALL]'):]
            unclosed_block = unclosed_text.strip()
        
        # Si no hay TOOL_CALLs, buscar bloques markdown
        if not tool_blocks and not unclosed_block:
            tool_blocks, unclosed_block = self._extract_from_markdown(text)
        
        # Si no hay TOOL_CALLs ni markdown, buscar JSON format
        if not tool_blocks and not unclosed_block:
            try:
                json_match = re.search(r'\{[\s\S]*?"name"\s*:\s*"create_file"[\s\S]*?\}', text)
                if json_match:
                    json_obj = json.loads(json_match.group())
                    if 'arguments' in json_obj:
                        args = json_obj['arguments']
                        fname = args.get('name', '')
                        content = args.get('content', '')
                        if fname and content:
                            tool_blocks = [f'action: create_file name: "{fname}" {content}']
            except:
                pass
        
        # Calcular limpieza
        clean = text
        for block in tool_blocks:
            clean = clean.replace('[TOOL_CALL]' + block + '[/TOOL_CALL]', '', 1)
        if unclosed_block:
            clean = clean.replace('[TOOL_CALL]' + unclosed_block, '', 1)
        # Limpiar bloques markdown tambien
        clean = re.sub(r'```[\w]*\n[\s\S]*?```', '', clean)
        clean = re.sub(r'\*\*\w+\.html\*\*\s*', '', clean)
        clean = re.sub(r'\*\*\w+\.css\*\*\s*', '', clean)
        clean = re.sub(r'\*\*\w+\.js\*\*\s*', '', clean)
        clean = clean.strip()
        
        results = []
        
        # Ejecutar TOOL_CALLs cerrados con barra de progreso
        total = len(tool_blocks) + (1 if unclosed_block else 0)
        progress = ToolCallProgress(total)

        for i, block in enumerate(tool_blocks, 1):
            parsed = self._parse_tool_block(block)
            if not parsed:
                results.append(f"[ERROR] TOOL_CALL #{i}: no se pudo parsear")
                progress.update(i, f"TOOL_CALL #{i}", False)
                continue
            
            action = parsed.get('action')
            path = parsed.get('path')
            content = parsed.get('content')
            command = parsed.get('command')
            old_text = parsed.get('old_text')
            new_text = parsed.get('new_text')
            
            # Resolver path contra proyecto activo
            if path and self.active_project and not os.path.isabs(path):
                path = self.resolve_project_path(path)
            
            # Validar
            is_valid, msg = self._validate_tool_call(action, path, content, command)
            if not is_valid:
                results.append(f"[ERROR] TOOL_CALL #{i}: {msg}")
                progress.update(i, f"TOOL_CALL #{i}", False)
                continue
            
            # Ejecutar
            try:
                result = self._run_tool_call(action, path, content, command, old_text, new_text)
                if result:
                    results.append(result)
                    # Extraer nombre del archivo del resultado
                    fname = os.path.basename(path) if path else f"TOOL_CALL #{i}"
                    size_str = ""
                    if "[OK]" in result:
                        # Extraer tamaño del resultado
                        import re
                        size_match = re.search(r'\((\d[\d,]*)\s*bytes\)', result)
                        if size_match:
                            size_str = size_match.group(1) + " bytes"
                    progress.update(i, fname, "[OK]" in result, size_str)
            except Exception as e:
                results.append(f"[ERROR] TOOL_CALL #{i}: {str(e)}")
                progress.update(i, f"TOOL_CALL #{i}", False)
        
        # Ejecutar TOOL_CALL sin cerrar (ultimo bloque cortado)
        # IMPORTANTE: Para contenido largo, intentar crear el archivo aunque el TOOL_CALL no esté cerrado
        if unclosed_block:
            i = len(tool_blocks) + 1
            parsed = self._parse_tool_block(unclosed_block)
            if parsed:
                action = parsed.get('action')
                path = parsed.get('path')
                content = parsed.get('content')
                command = parsed.get('command')
                old_text = parsed.get('old_text')
                new_text = parsed.get('new_text')
                
                if path and self.active_project and not os.path.isabs(path):
                    path = self.resolve_project_path(path)
                
                # Para TOOL_CALLs sin cerrar con contenido, ser más permisivo
                # Si tiene acción y contenido (o path para create_file), intentar ejecutar
                if action and content:
                    is_valid, msg = self._validate_tool_call(action, path, content, command)
                    if is_valid:
                        try:
                            result = self._run_tool_call(action, path, content, command, old_text, new_text)
                            if result:
                                results.append(result)
                                # Marcar como exitoso para no mostrar warning
                                unclosed_block = None
                        except Exception as e:
                            results.append(f"[ERROR] TOOL_CALL #{i} (sin cerrar): {str(e)}")
                    else:
                        # Si falla validación pero tiene contenido, intentar crear archivo directamente
                        if content and action == 'create_file':
                            try:
                                if path:
                                    parent = os.path.dirname(path)
                                    if parent:
                                        os.makedirs(parent, exist_ok=True)
                                    with open(path, 'w', encoding='utf-8') as f:
                                        f.write(content)
                                    results.append(f"[OK] Archivo creado (incompleto): {path}")
                                    unclosed_block = None
                            except Exception as e:
                                results.append(f"[WARN] TOOL_CALL #{i} (sin cerrar): {msg}")
                elif action and not content and path:
                    # TOOL_CALL sin contenido pero con path - podría ser create_file vacío
                    if action == 'create_file':
                        try:
                            if path:
                                parent = os.path.dirname(path)
                                if parent:
                                    os.makedirs(parent, exist_ok=True)
                                with open(path, 'w', encoding='utf-8') as f:
                                    f.write('')
                                results.append(f"[OK] Archivo creado (vacío): {path}")
                                unclosed_block = None
                        except Exception as e:
                            pass
        
        # Agregar resultados con reporte de progreso
        progress_summary = progress.finish()
        if results:
            safe = [str(r) for r in results if r]
            if safe:
                # Agregar reporte de progreso antes de los resultados
                clean = progress_summary + "\n" + "\n".join(safe) + ("\n\n" + clean if clean else "")
        
        # FALLBACK: Si no se creó ningún archivo pero hay proyecto activo,
        # intentar extraer archivos directamente de la respuesta
        if self.active_project and '[OK]' not in (clean or ''):
            try:
                fallback_results = self._extract_files_from_response(text, self.active_project)
                if fallback_results:
                    clean = "\n".join(fallback_results) + ("\n\n" + clean if clean else "")
            except Exception:
                pass
        
        return clean or ""
    
    def _extract_files_from_response(self, response: str, folder: str) -> list:
        """Extraer archivos HTML/CSS/JS directamente de la respuesta como fallback.
        Se usa cuando los TOOL_CALLs no funcionan correctamente."""
        import re
        results = []
        
        if not response or not folder:
            return results
        
        # Limpiar markdown fences del response
        clean_response = response
        clean_response = re.sub(r'```\w*\n', '', clean_response)
        clean_response = re.sub(r'\n```', '', clean_response)
        
        # Detectar HTML completo
        html_match = re.search(r'(<!DOCTYPE[^>]*>[\s\S]*?</html>)', clean_response, re.IGNORECASE)
        if html_match:
            html_content = html_match.group(1).strip()
            # Ignorar paginas de error del proxy
            is_error_page = any(error in html_content.lower() for error in [
                'internal server error', '500 error', 'bad gateway', 
                'service unavailable', 'gateway timeout', '<title>error</title>'
            ])
            if len(html_content) > 50 and not is_error_page:
                path = os.path.join(folder, 'index.html')
                try:
                    os.makedirs(folder, exist_ok=True)
                    with open(path, 'w', encoding='utf-8') as f:
                        f.write(html_content)
                    results.append(f"[OK] Archivo creado (fallback): {path}")
                except Exception as e:
                    results.append(f"[ERROR] Error creando {path}: {e}")
        
        # Detectar HTML parcial (sin </html>) - buscar <html o <body
        if not results or not any('[OK] Archivo creado' in r and 'index.html' in r for r in results):
            html_partial = re.search(r'(<(?:html|body)[^>]*>[\s\S]*)', clean_response, re.IGNORECASE)
            if html_partial:
                html_content = html_partial.group(1).strip()
                # Limpiar al final si hay texto no-HTML
                html_content = re.sub(r'\n[^<\n]*$', '', html_content)
                # Ignorar paginas de error del proxy
                is_error_page = any(error in html_content.lower() for error in [
                    'internal server error', '500 error', 'bad gateway', 
                    'service unavailable', 'gateway timeout', '<title>error</title>'
                ])
                if len(html_content) > 50 and ('<html' in html_content.lower() or '<body' in html_content.lower()) and not is_error_page:
                    path = os.path.join(folder, 'index.html')
                    try:
                        os.makedirs(folder, exist_ok=True)
                        with open(path, 'w', encoding='utf-8') as f:
                            f.write(html_content)
                        results.append(f"[OK] Archivo creado (fallback): {path}")
                    except Exception as e:
                        results.append(f"[ERROR] Error creando {path}: {e}")
        
        # Detectar CSS completo (entre style tags o standalone)
        css_content = None
        
        # Buscar en style tags
        style_matches = re.findall(r'<style[^>]*>([\s\S]*?)</style>', clean_response, re.IGNORECASE)
        if style_matches:
            css_content = '\n\n'.join([m.strip() for m in style_matches])
        
        # Buscar CSS standalone (patrón selector { propiedades })
        if not css_content:
            css_blocks = re.findall(r'([\.\#]?[a-zA-Z][\w\-\s,]*\{[^}]+\})', clean_response, re.DOTALL)
            if css_blocks and len(''.join(css_blocks)) > 50:
                css_content = '\n\n'.join(css_blocks)
        
        if css_content and len(css_content) > 30:
            path = os.path.join(folder, 'style.css')
            try:
                os.makedirs(folder, exist_ok=True)
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(css_content)
                results.append(f"[OK] Archivo creado (fallback): {path}")
            except Exception as e:
                results.append(f"[ERROR] Error creando {path}: {e}")
        
        # Detectar JS
        js_indicators = ['function ', 'const ', 'let ', 'var ', 'document.', 'window.', 'addEventListener']
        js_lines = []
        for line in clean_response.split('\n'):
            stripped = line.strip()
            if any(ind in stripped for ind in js_indicators):
                js_lines.append(line)
        
        if len(js_lines) > 2:
            js_content = '\n'.join(js_lines)
            path = os.path.join(folder, 'script.js')
            try:
                os.makedirs(folder, exist_ok=True)
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(js_content)
                results.append(f"[OK] Archivo creado (fallback): {path}")
            except Exception as e:
                results.append(f"[ERROR] Error creando {path}: {e}")
        
        return results
    
    def _parse_tool_block(self, block: str) -> dict:
        """Parsear un bloque TOOL_CALL y extraer action, path, content, command.
        Versión ultrarrobusta capaz de parsear cualquier variación de formato."""
        import re
        
        result = {'action': None, 'path': None, 'content': None, 'command': None, 'old_text': None, 'new_text': None}
        block = block.strip()
        if not block:
            return None
        
        lines = block.split('\n')
        
        # 1. Detectar Accion
        for line in lines[:5]:
            line_l = line.lower().strip()
            if 'action:' in line_l:
                action_part = line_l.split('action:')[1].strip()
                if 'create_file' in action_part or 'createfile' in action_part:
                    result['action'] = 'create_file'
                elif 'edit_file' in action_part or 'editfile' in action_part:
                    result['action'] = 'edit_file'
                elif 'read_file' in action_part or 'readfile' in action_part:
                    result['action'] = 'read_file'
                elif 'delete_file' in action_part or 'deletefile' in action_part or 'delete' in action_part or 'remove' in action_part:
                    result['action'] = 'delete_file'
                elif 'clear_folder' in action_part or 'clearfolder' in action_part or 'delete_all' in action_part or 'deleteall' in action_part:
                    result['action'] = 'clear_folder'
                elif 'copy_file' in action_part or 'copyfile' in action_part or 'copy' in action_part:
                    result['action'] = 'copy_file'
                elif 'move_file' in action_part or 'movefile' in action_part or 'move' in action_part:
                    result['action'] = 'move_file'
                elif 'rename_file' in action_part or 'renamefile' in action_part or 'rename' in action_part:
                    result['action'] = 'rename_file'
                elif 'search_in_files' in action_part or 'searchinfiles' in action_part or 'search' in action_part or 'grep' in action_part or 'find' in action_part:
                    result['action'] = 'search_in_files'
                elif 'replace_in_files' in action_part or 'replaceinfiles' in action_part or 'replace' in action_part:
                    result['action'] = 'replace_in_files'
                elif 'get_file_info' in action_part or 'getfileinfo' in action_part or 'file_info' in action_part or 'fileinfo' in action_part:
                    result['action'] = 'get_file_info'
                elif 'list_directory' in action_part or 'listdirectory' in action_part or 'list_dir' in action_part or 'listdir' in action_part or 'ls' in action_part or 'dir' in action_part:
                    result['action'] = 'list_directory'
                elif 'create_project' in action_part or 'createproject' in action_part or 'project' in action_part:
                    result['action'] = 'create_project'
                elif 'run_python' in action_part or 'runpython' in action_part or 'python' in action_part:
                    result['action'] = 'run_python'
                elif 'install_package' in action_part or 'installpackage' in action_part or 'install' in action_part or 'pip' in action_part or 'npm' in action_part:
                    result['action'] = 'install_package'
                elif 'git_commit' in action_part or 'gitcommit' in action_part or 'commit' in action_part:
                    result['action'] = 'git_commit'
                elif 'compress_files' in action_part or 'compressfiles' in action_part or 'compress' in action_part or 'zip' in action_part:
                    result['action'] = 'compress_files'
                elif 'extract_files' in action_part or 'extractfiles' in action_part or 'extract' in action_part or 'unzip' in action_part:
                    result['action'] = 'extract_files'
                elif 'download_file' in action_part or 'downloadfile' in action_part or 'download' in action_part or 'wget' in action_part or 'curl' in action_part:
                    result['action'] = 'download_file'
                elif 'set_env' in action_part or 'setenv' in action_part or 'env' in action_part:
                    result['action'] = 'set_env'
                elif 'create_folder' in action_part or 'createfolder' in action_part:
                    result['action'] = 'create_folder'
                elif 'execute' in action_part:
                    result['action'] = 'execute'
                break
        
        # Fallback de Acción si no se declaró explícitamente
        if not result['action']:
            if '<!doctype' in block.lower() or '<html' in block.lower() or 'function' in block.lower() or 'body {' in block.lower() or ':root' in block.lower():
                result['action'] = 'create_file'
            elif 'command:' in block.lower() or 'python ' in block.lower():
                result['action'] = 'execute'
        
        # 2. Detectar Nombre/Path del archivo
        for line in lines[:8]:
            line_s = line.strip()
            # Patrón name: "x" o path: "x"
            m = re.search(r'(?:name|path):\s*["\']?([^"\'\n\r]+)["\']?', line_s, re.IGNORECASE)
            if m:
                found_path = m.group(1).strip()
                # Filtrar palabras clave de formato
                if not found_path.lower().startswith('create_file') and not found_path.lower().startswith('edit_file'):
                    result['path'] = found_path
                    break
        
        # Detectar parámetros adicionales para nuevas acciones
        for line in lines[:10]:
            line_s = line.strip()
            # source/destination para copy/move/rename
            m = re.search(r'source:\s*["\']?([^"\'\n\r]+)["\']?', line_s, re.IGNORECASE)
            if m:
                result['source'] = m.group(1).strip()
            m = re.search(r'destination(?:_path)?:\s*["\']?([^"\'\n\r]+)["\']?', line_s, re.IGNORECASE)
            if m:
                result['destination'] = m.group(1).strip()
            # pattern para search/replace
            m = re.search(r'pattern:\s*["\']?([^"\'\n\r]+)["\']?', line_s, re.IGNORECASE)
            if m:
                result['pattern'] = m.group(1).strip()
            m = re.search(r'new_text:\s*["\']?([^"\'\n\r]+)["\']?', line_s, re.IGNORECASE)
            if m:
                result['new_text'] = m.group(1).strip()
            # query para search
            m = re.search(r'query:\s*["\']?([^"\'\n\r]+)["\']?', line_s, re.IGNORECASE)
            if m:
                result['query'] = m.group(1).strip()
            # url para download
            m = re.search(r'url:\s*["\']?([^"\'\n\r]+)["\']?', line_s, re.IGNORECASE)
            if m:
                result['url'] = m.group(1).strip()
            # package para install
            m = re.search(r'package:\s*["\']?([^"\'\n\r]+)["\']?', line_s, re.IGNORECASE)
            if m:
                result['package'] = m.group(1).strip()
            # message para git commit
            m = re.search(r'message:\s*["\']?([^"\'\n\r]+)["\']?', line_s, re.IGNORECASE)
            if m:
                result['message'] = m.group(1).strip()
            # name/value para env
            m = re.search(r'name:\s*["\']?([^"\'\n\r]+)["\']?', line_s, re.IGNORECASE)
            if m and 'name' not in result:
                result['name'] = m.group(1).strip()
            m = re.search(r'value:\s*["\']?([^"\'\n\r]+)["\']?', line_s, re.IGNORECASE)
            if m:
                result['value'] = m.group(1).strip()
        
        # Inferir path si falta por extensión o estructura
        if result['action'] == 'create_file' and not result['path']:
            if '<!doctype' in block.lower() or '<html' in block.lower():
                result['path'] = 'index.html'
            elif 'addEventListener' in block or 'DOMContentLoaded' in block or 'document.querySelector' in block:
                result['path'] = 'script.js'
            elif ':root' in block or 'font-family:' in block or 'margin:' in block:
                result['path'] = 'style.css'
            else:
                # Buscar cualquier palabra que termine en extensión conocida en las primeras líneas
                m_ext = re.search(r'([\w\-\./]+\.(?:html|css|js|py|json|md|txt))', block[:300], re.IGNORECASE)
                if m_ext:
                    result['path'] = m_ext.group(1)

        # 3. Detectar Comando (para execute)
        if result['action'] == 'execute':
            m_cmd = re.search(r'command:\s*["\']?([^"\'\n\r]+)["\']?', block, re.IGNORECASE)
            if m_cmd:
                result['command'] = m_cmd.group(1).strip()
            else:
                # Extraer primera línea después de action: execute
                for line in lines:
                    if 'action:' not in line.lower() and line.strip():
                        result['command'] = line.strip()
                        break
            return result

        # 4. Extraer Contenido
        content_lines = []
        in_content = False
        
        for line in lines:
            line_str = line.strip()
            
            # El contenido empieza tras la línea del header (action/name/path)
            if not in_content:
                if any(line_str.lower().startswith(k) for k in ['action:', 'name:', 'path:']):
                    continue
                # Si llegamos a una línea vacía o código real
                if line_str == '' or not any(line_str.lower().startswith(k) for k in ['action:', 'name:', 'path:']):
                    in_content = True
            
            if in_content:
                if line_str == '[/TOOL_CALL]' or line_str == '[/tool_call]':
                    break
                content_lines.append(line)
        
        raw_content = '\n'.join(content_lines).strip()
        
        # Limpiar markdown code fences interiores si los hay
        raw_content = re.sub(r'^```\w*\s*\n', '', raw_content)
        raw_content = re.sub(r'\n```\s*$', '', raw_content)
        result['content'] = raw_content.strip()
        
        return result
    
    def _run_tool_call(self, action, path, content, command, old_text, new_text) -> str:
        """Ejecutar una accion de tool call con validacion y correccion automatica
        Incluye animacion contextual breve para cada accion.
        IAM: file history, security checks, read-before-edit."""
        
        # Verificar si el comando esta prohibido
        if action == 'execute' and command:
            if permission_system.is_banned_command(command):
                return f"[DENIED] Comando prohibido: {command}"
            
            # Verificar si es comando seguro de solo lectura
            if permission_system.is_safe_read_command(command):
                pass  # Permitir sin permiso
        
        # Verificar read-before-edit para ediciones
        if action == 'edit_file' and path:
            if not permission_system.was_file_read(path):
                # Auto-leer el archivo primero
                if os.path.exists(path):
                    try:
                        with open(path, 'r', encoding='utf-8') as f:
                            file_content = f.read()
                        import hashlib
                        checksum = hashlib.md5(file_content.encode()).hexdigest()[:12]
                        permission_system.track_file_read(path, checksum)
                    except Exception:
                        pass
        
        # Animacion breve segun la accion
        _loader = LoadingIndicator()
        _action_map = {
            'create_file': ('[FILE]', 'creando', 'build'),
            'edit_file':   ('[EDIT]', 'editando', 'smooth'),
            'read_file':   ('[READ]', 'leyendo', 'type'),
            'delete_file': ('[DEL]', 'eliminando', 'pulse'),
            'clear_folder':('[DEL]', 'limpiando carpeta', 'pulse'),
            'copy_file':   ('[COPY]', 'copiando', 'smooth'),
            'move_file':   ('[MOVE]', 'moviendo', 'smooth'),
            'rename_file': ('[REN]', 'renombrando', 'smooth'),
            'search_in_files': ('[SEARCH]', 'buscando', 'dots_v'),
            'replace_in_files': ('[REPLACE]', 'reemplazando', 'smooth'),
            'get_file_info': ('[INFO]', 'obteniendo info', 'orbit'),
            'list_directory': ('[DIR]', 'listando', 'dots_v'),
            'create_project': ('[PROJ]', 'creando proyecto', 'build'),
            'run_python':  ('[PY]', 'ejecutando Python', 'wave'),
            'install_package': ('[PKG]', 'instalando paquete', 'bars'),
            'git_commit':  ('[GIT]', 'git commit', 'smooth'),
            'compress_files': ('[ZIP]', 'comprimiendo', 'bars'),
            'extract_files': ('[UNZIP]', 'extrayendo', 'bars'),
            'download_file': ('[DL]', 'descargando', 'bars'),
            'set_env':     ('[ENV]', 'configurando env', 'orbit'),
            'execute':     ('[RUN]', 'ejecutando', 'wave'),
            'create_folder':('[DIR]', 'creando carpeta', 'orbit'),
        }
        if action in _action_map:
            _icon, _prefix, _spin = _action_map[action]
            _fname = os.path.basename(path) if path else ""
            _msg = f"{_icon} {_prefix}: {_fname}" if _fname else f"{_icon} {_prefix}"
            _loader.start(_msg, _spin)
        
        try:
            if action == 'create_file' and path:
                # Registrar en historial antes de crear
                existed = os.path.exists(path)
                
                # Crear directorios padres
                parent = os.path.dirname(path)
                if parent:
                    os.makedirs(parent, exist_ok=True)
                
                # Validar y corregir codigo antes de escribir
                if content:
                    ext = os.path.splitext(path)[1].lower()
                    if ext in ['.html', '.htm', '.css', '.js']:
                        is_valid, corrected_content = validate_file(path, content)
                        if not is_valid:
                            content = corrected_content
                
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(content or '')
                
                # Registrar en historial de archivos
                if existed:
                    self.file_history.record_edit(path, content or "")
                else:
                    self.file_history.record_create(path, content or "")
                
                # Registrar escritura para trackeo (IAM)
                import hashlib
                checksum = hashlib.md5((content or "").encode()).hexdigest()[:12]
                self._file_records[path] = {
                    "write_time": datetime.now(),
                    "checksum": checksum,
                    "size": len(content or "")
                }
                permission_system.track_file_write(path, checksum)
                
                # Publicar evento de escritura
                event_type = EventType.UPDATED if existed else EventType.CREATED
                self.events.files.publish(event_type, {
                    "action": "create" if not existed else "update",
                    "path": path,
                    "size": len(content or "")
                })
                
                # Verificar y dar info detallada
                verify = self._verify_execution('create_file', path)
                if verify:
                    try:
                        size = os.path.getsize(path)
                        size_str = f" ({size:,} bytes)" if size > 1000 else f" ({size} bytes)"
                        return verify + size_str
                    except:
                        return verify
                return f"[OK] Archivo creado: {path}"
            
            elif action == 'edit_file' and path:
                if not os.path.exists(path):
                    return f"[ERROR] Archivo no existe: {path}"
                
                # Auto-leer si no se ha leido antes (no bloquear edicion)
                if path not in self._file_records:
                    try:
                        with open(path, 'r', encoding='utf-8') as f:
                            file_content = f.read()
                        import hashlib
                        checksum = hashlib.md5(file_content.encode()).hexdigest()[:12]
                        permission_system.track_file_read(path, checksum)
                        self._file_records[path] = {
                            "read_time": datetime.now(),
                            "checksum": checksum,
                            "size": len(file_content)
                        }
                    except Exception:
                        pass
                
                # Leer contenido actual para historial
                with open(path, 'r', encoding='utf-8') as f:
                    current = f.read()
                
                # Verificar que el archivo no cambio desde la ultima lectura
                import hashlib
                current_checksum = hashlib.md5(current.encode()).hexdigest()[:12]
                if path in self._file_records:
                    last_checksum = self._file_records[path].get("checksum", "")
                    if last_checksum and last_checksum != current_checksum:
                        return f"[ERROR] Archivo fue modificado externamente desde la ultima lectura: {os.path.basename(path)}"
                
                if old_text and new_text:
                    if old_text in current:
                        new = current.replace(old_text, new_text, 1)
                        ext = os.path.splitext(path)[1].lower()
                        if ext in ['.html', '.htm', '.css', '.js']:
                            is_valid, new = validate_file(path, new)
                        with open(path, 'w', encoding='utf-8') as f:
                            f.write(new)
                        
                        # Registrar en historial
                        self.file_history.record_edit(path, new)
                        
                        # Actualizar checksum
                        import hashlib
                        checksum = hashlib.md5(new.encode()).hexdigest()[:12]
                        permission_system.track_file_write(path, checksum)
                        
                        return f"[OK] Archivo editado: {path}"
                    return f"[ERROR] Texto no encontrado en {path}"
                elif content:
                    ext = os.path.splitext(path)[1].lower()
                    if ext in ['.html', '.htm', '.css', '.js']:
                        is_valid, content = validate_file(path, content)
                    with open(path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    # Registrar en historial
                    self.file_history.record_edit(path, content)
                    
                    # Actualizar checksum
                    import hashlib
                    checksum = hashlib.md5(content.encode()).hexdigest()[:12]
                    permission_system.track_file_write(path, checksum)
                    
                    return f"[OK] Archivo reescrito: {path}"
                return f"[ERROR] edit_file sin old_text/new_text ni content"
            
            elif action == 'read_file' and path:
                if not os.path.exists(path):
                    return f"[ERROR] Archivo no existe: {path}"
                with open(path, 'r', encoding='utf-8') as f:
                    c = f.read()
                lines_count = c.count('\n') + 1
                if not hasattr(self, '_file_cache'):
                    self._file_cache = {}
                self._file_cache[path] = c
                
                # Registrar lectura para read-before-edit (IAM)
                import hashlib
                checksum = hashlib.md5(c.encode()).hexdigest()[:12]
                self._file_records[path] = {
                    "read_time": datetime.now(),
                    "checksum": checksum,
                    "size": len(c)
                }
                permission_system.track_file_read(path, checksum)
                self._files_read_this_session.add(path)
                
                # Publicar evento de lectura
                self.events.files.publish(EventType.UPDATED, {
                    "action": "read",
                    "path": path,
                    "lines": lines_count
                })
                
                ext = os.path.splitext(path)[1].lower()
                lang_map = {'.py': 'Python', '.js': 'JavaScript', '.html': 'HTML', '.css': 'CSS', '.json': 'JSON', '.md': 'Markdown'}
                lang = lang_map.get(ext, 'archivo')
                return f"[OK] {lang} leido: {os.path.basename(path)} ({lines_count} lineas)"
            
            elif action == 'create_folder' and path:
                os.makedirs(path, exist_ok=True)
                return f"[OK] Carpeta creada: {path}"
            
            elif action == 'execute' and command:
                # Usar shell persistente (IAM)
                result = self.shell.exec(command, timeout=60, cwd=self.active_project)
                output_parts = []
                if result.stdout:
                    output_parts.append(result.stdout.strip())
                if result.stderr:
                    output_parts.append(f"STDERR: {result.stderr.strip()}")
                if result.exit_code != 0:
                    output_parts.append(f"[ERROR] Comando fallo (codigo {result.exit_code})")
                elif not output_parts:
                    output_parts.append("[OK] Comando ejecutado exitosamente")
                if result.duration_ms > 0:
                    output_parts.append(f"({result.duration_ms}ms)")
                return "\n".join(output_parts)
            
            elif action == 'delete_file' and path:
                if os.path.exists(path):
                    os.remove(path)
                    return f"[OK] Archivo eliminado: {os.path.basename(path)}"
                else:
                    return f"[ERROR] Archivo no existe: {path}"
            
            elif action == 'clear_folder' and path:
                if os.path.isdir(path):
                    import shutil
                    deleted = []
                    errors = []
                    for item in os.listdir(path):
                        item_path = os.path.join(path, item)
                        try:
                            if os.path.isfile(item_path):
                                os.remove(item_path)
                                deleted.append(item)
                            elif os.path.isdir(item_path):
                                shutil.rmtree(item_path)
                                deleted.append(f"{item}/")
                        except Exception as e:
                            errors.append(f"{item}: {str(e)}")
                    
                    if deleted:
                        result = f"[OK] Carpeta limpiada: {len(deleted)} items eliminados"
                        if errors:
                            result += f"\n[WARN] {len(errors)} errores"
                        return result
                    else:
                        return "[WARN] La carpeta ya esta vacia"
                else:
                    return f"[ERROR] No es una carpeta: {path}"
            
            elif action == 'copy_file' and path:
                source = result_dict.get('source', path)
                destination = result_dict.get('destination', '')
                if not destination:
                    return "[ERROR] Falta destination para copy_file"
                if os.path.exists(source):
                    import shutil
                    if os.path.isfile(source):
                        shutil.copy2(source, destination)
                    else:
                        shutil.copytree(source, destination)
                    return f"[OK] Copiado: {os.path.basename(source)} -> {destination}"
                else:
                    return f"[ERROR] Fuente no existe: {source}"
            
            elif action == 'move_file' and path:
                source = result_dict.get('source', path)
                destination = result_dict.get('destination', '')
                if not destination:
                    return "[ERROR] Falta destination para move_file"
                if os.path.exists(source):
                    import shutil
                    shutil.move(source, destination)
                    return f"[OK] Movido: {os.path.basename(source)} -> {destination}"
                else:
                    return f"[ERROR] Fuente no existe: {source}"
            
            elif action == 'rename_file' and path:
                new_name = result_dict.get('destination', '')
                if not new_name:
                    return "[ERROR] Falta destination (nuevo nombre) para rename_file"
                if os.path.exists(path):
                    dir_name = os.path.dirname(path)
                    new_path = os.path.join(dir_name, new_name)
                    os.rename(path, new_path)
                    return f"[OK] Renombrado: {os.path.basename(path)} -> {new_name}"
                else:
                    return f"[ERROR] Archivo no existe: {path}"
            
            elif action == 'search_in_files':
                query = result_dict.get('query', '') or result_dict.get('pattern', '')
                search_path = path or self.active_project or os.getcwd()
                if not query:
                    return "[ERROR] Falta query/pattern para search_in_files"
                results = []
                count = 0
                for root, dirs, files in os.walk(search_path):
                    dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__', '.git']]
                    for f in files:
                        if f.endswith(('.py', '.js', '.html', '.css', '.json', '.md', '.txt')):
                            fpath = os.path.join(root, f)
                            try:
                                with open(fpath, 'r', encoding='utf-8', errors='ignore') as fh:
                                    for i, line in enumerate(fh, 1):
                                        if query.lower() in line.lower():
                                            rel = os.path.relpath(fpath, search_path)
                                            results.append(f"{rel}:{i}: {line.strip()[:80]}")
                                            count += 1
                                            if count >= 20:
                                                break
                            except:
                                pass
                            if count >= 20:
                                break
                    if count >= 20:
                        break
                if results:
                    return f"[OK] {count} coincidencias encontradas:\n" + "\n".join(results[:20])
                else:
                    return "[WARN] Sin coincidencias"
            
            elif action == 'replace_in_files':
                pattern = result_dict.get('pattern', '') or result_dict.get('old_text', '')
                new_text_val = result_dict.get('new_text', '')
                replace_path = path or self.active_project or os.getcwd()
                if not pattern or not new_text_val:
                    return "[ERROR] Falta pattern/old_text y new_text para replace_in_files"
                replaced = 0
                for root, dirs, files in os.walk(replace_path):
                    dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__', '.git']]
                    for f in files:
                        if f.endswith(('.py', '.js', '.html', '.css', '.json')):
                            fpath = os.path.join(root, f)
                            try:
                                with open(fpath, 'r', encoding='utf-8') as fh:
                                    content = fh.read()
                                if pattern in content:
                                    new_content = content.replace(pattern, new_text_val)
                                    with open(fpath, 'w', encoding='utf-8') as fh:
                                        fh.write(new_content)
                                    replaced += 1
                            except:
                                pass
                return f"[OK] Reemplazado en {replaced} archivos"
            
            elif action == 'get_file_info' and path:
                if os.path.exists(path):
                    stat = os.stat(path)
                    size = stat.st_size
                    modified = datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
                    is_dir = os.path.isdir(path)
                    info_type = "Carpeta" if is_dir else "Archivo"
                    if is_dir:
                        items = len(os.listdir(path))
                        return f"[OK] {info_type}: {path}\n- Items: {items}\n- Modificado: {modified}"
                    else:
                        ext = os.path.splitext(path)[1]
                        lines_count = sum(1 for _ in open(path, 'r', encoding='utf-8', errors='ignore'))
                        return f"[OK] {info_type}: {path}\n- Tamano: {size} bytes\n- Extension: {ext}\n- Lineas: {lines_count}\n- Modificado: {modified}"
                else:
                    return f"[ERROR] No existe: {path}"
            
            elif action == 'list_directory':
                list_path = path or self.active_project or os.getcwd()
                if os.path.isdir(list_path):
                    items = os.listdir(list_path)
                    dirs = [d for d in items if os.path.isdir(os.path.join(list_path, d))]
                    files = [f for f in items if os.path.isfile(os.path.join(list_path, f))]
                    result_lines = [f"[OK] Contenido de {os.path.basename(list_path)}:"]
                    if dirs:
                        result_lines.append(f"  Carpetas ({len(dirs)}):")
                        for d in dirs[:15]:
                            result_lines.append(f"    + {d}/")
                    if files:
                        result_lines.append(f"  Archivos ({len(files)}):")
                        for f in files[:15]:
                            size = os.path.getsize(os.path.join(list_path, f))
                            result_lines.append(f"    - {f} ({size} bytes)")
                    return "\n".join(result_lines)
                else:
                    return f"[ERROR] No es una carpeta: {list_path}"
            
            elif action == 'create_project':
                project_name = result_dict.get('name', 'nuevo_proyecto')
                project_type = result_dict.get('type', 'web')
                project_path = os.path.join(self.active_project or os.getcwd(), project_name)
                os.makedirs(project_path, exist_ok=True)
                created = []
                if project_type == 'web':
                    files = {
                        'index.html': '<!DOCTYPE html>\n<html lang="es">\n<head>\n<meta charset="UTF-8">\n<meta name="viewport" content="width=device-width, initial-scale=1.0">\n<title>' + project_name + '</title>\n<link rel="stylesheet" href="style.css">\n</head>\n<body>\n<h1>' + project_name + '</h1>\n<script src="script.js"></script>\n</body>\n</html>',
                        'style.css': '/* Styles */\n* { margin: 0; padding: 0; box-sizing: border-box; }\nbody { font-family: sans-serif; }',
                        'script.js': '// JavaScript\ndocument.addEventListener("DOMContentLoaded", () => {\n  console.log("Ready");\n});'
                    }
                elif project_type == 'python':
                    files = {
                        'main.py': f'#!/usr/bin/env python3\n"""Main module"""\n\ndef main():\n    print("Hello from {project_name}")\n\nif __name__ == "__main__":\n    main()\n',
                        'requirements.txt': '',
                        'README.md': f'# {project_name}\n\nDescription'
                    }
                else:
                    files = {'README.md': f'# {project_name}'}
                for fname, content in files.items():
                    fpath = os.path.join(project_path, fname)
                    with open(fpath, 'w', encoding='utf-8') as fh:
                        fh.write(content)
                    created.append(fname)
                return f"[OK] Proyecto creado: {project_path}\nArchivos: {', '.join(created)}"
            
            elif action == 'run_python' and command:
                import tempfile
                script = command if command.endswith('.py') else None
                if not script:
                    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as tmp:
                        tmp.write(command)
                        script = tmp.name
                result = self.shell.exec(f'python "{script}"', timeout=60, cwd=self.active_project)
                output_parts = []
                if result.stdout:
                    output_parts.append(result.stdout.strip())
                if result.stderr:
                    output_parts.append(f"STDERR: {result.stderr.strip()}")
                if result.exit_code != 0:
                    output_parts.append(f"[ERROR] Python fallo (codigo {result.exit_code})")
                return "\n".join(output_parts) if output_parts else "[OK] Python ejecutado"
            
            elif action == 'install_package':
                package = result_dict.get('package', '') or command or ''
                if not package:
                    return "[ERROR] Falta package para install_package"
                if 'requirements' in package or package.endswith('.txt'):
                    cmd = f'pip install -r "{package}"'
                elif package.startswith('npm') or package.startswith('yarn'):
                    cmd = package
                else:
                    cmd = f'pip install {package}'
                result = self.shell.exec(cmd, timeout=120, cwd=self.active_project)
                if result.exit_code == 0:
                    return f"[OK] Paquete instalado: {package}"
                else:
                    return f"[ERROR] Fallo al instalar: {result.stderr[:200] if result.stderr else 'error desconocido'}"
            
            elif action == 'git_commit':
                message = result_dict.get('message', '') or command or ''
                if not message:
                    return "[ERROR] Falta message para git_commit"
                cmds = ['git add .', f'git commit -m "{message}"']
                results = []
                for cmd in cmds:
                    r = self.shell.exec(cmd, timeout=30, cwd=self.active_project)
                    if r.stdout:
                        results.append(r.stdout.strip())
                    if r.stderr and 'warning' not in r.stderr.lower():
                        results.append(r.stderr.strip())
                return "[OK] Git commit realizado" + ("\n" + "\n".join(results) if results else "")
            
            elif action == 'compress_files':
                import zipfile
                source = result_dict.get('source', path)
                destination = result_dict.get('destination', 'archive.zip')
                if not source:
                    return "[ERROR] Falta source para compress_files"
                with zipfile.ZipFile(destination, 'w', zipfile.ZIP_DEFLATED) as zf:
                    if os.path.isfile(source):
                        zf.write(source, os.path.basename(source))
                    elif os.path.isdir(source):
                        for root, dirs, files in os.walk(source):
                            for f in files:
                                fpath = os.path.join(root, f)
                                arcname = os.path.relpath(fpath, os.path.dirname(source))
                                zf.write(fpath, arcname)
                size = os.path.getsize(destination)
                return f"[OK] Comprimido: {destination} ({size} bytes)"
            
            elif action == 'extract_files':
                import zipfile
                source = result_dict.get('source', path)
                destination = result_dict.get('destination', '.')
                if not source:
                    return "[ERROR] Falta source para extract_files"
                if not os.path.exists(source):
                    return f"[ERROR] Archivo no existe: {source}"
                with zipfile.ZipFile(source, 'r') as zf:
                    zf.extractall(destination)
                return f"[OK] Extraido: {source} -> {destination}"
            
            elif action == 'download_file':
                url = result_dict.get('url', '') or command or ''
                if not url:
                    return "[ERROR] Falta url para download_file"
                destination = result_dict.get('destination', path)
                if not destination:
                    destination = os.path.basename(url.split('?')[0]) or 'downloaded_file'
                response = requests.get(url, timeout=30, stream=True)
                if response.status_code == 200:
                    with open(destination, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            f.write(chunk)
                    size = os.path.getsize(destination)
                    return f"[OK] Descargado: {destination} ({size} bytes)"
                else:
                    return f"[ERROR] HTTP {response.status_code}"
            
            elif action == 'set_env':
                name = result_dict.get('name', '') or result_dict.get('path', '')
                value = result_dict.get('value', '') or content or ''
                if not name:
                    return "[ERROR] Falta name para set_env"
                os.environ[name] = value
                return f"[OK] Variable de entorno: {name}={value[:50]}..."
            
            # Buscar en acciones avanzadas (1000+ funciones)
            if action in ALL_ACTIONS:
                func = ALL_ACTIONS[action]
                kwargs = {}
                # Mapear parametros comunes
                if path:
                    kwargs['path'] = path
                if content:
                    kwargs['content'] = content
                if command:
                    kwargs['command'] = command
                if result_dict.get('source'):
                    kwargs['source'] = result_dict['source']
                if result_dict.get('destination'):
                    kwargs['destination'] = result_dict['destination']
                if result_dict.get('query'):
                    kwargs['query'] = result_dict['query']
                if result_dict.get('pattern'):
                    kwargs['pattern'] = result_dict['pattern']
                if result_dict.get('new_text'):
                    kwargs['new_text'] = result_dict['new_text']
                if result_dict.get('url'):
                    kwargs['url'] = result_dict['url']
                if result_dict.get('package'):
                    kwargs['package'] = result_dict['package']
                if result_dict.get('message'):
                    kwargs['message'] = result_dict['message']
                if result_dict.get('name'):
                    kwargs['name'] = result_dict['name']
                if result_dict.get('value'):
                    kwargs['value'] = result_dict['value']
                # Filtrar kwargs None
                kwargs = {k: v for k, v in kwargs.items() if v is not None}
                try:
                    return func(**kwargs)
                except Exception as e:
                    return f"[ERROR] {action}: {str(e)}"
            
            return f"[ERROR] Accion no reconocida: {action}"
        
        finally:
            _loader.stop()
    
    def generate_web_project(self, folder: str, title: str = "Mi Proyecto", 
                            description: str = "", custom_vars: dict = None) -> list:
        """Generar proyecto web completo usando templates profesionales.
        Retorna lista de archivos creados."""
        results = []
        
        if not folder:
            return ["[ERROR] No se especifico carpeta del proyecto"]
        
        # Crear carpeta
        os.makedirs(folder, exist_ok=True)
        
        # Generar HTML
        html_content = smart_templates.get_base_html(title, description)
        html_path = os.path.join(folder, 'index.html')
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        results.append(f"[OK] Archivo creado: {html_path}")
        
        # Generar CSS
        css_content = smart_templates.get_full_css()
        css_path = os.path.join(folder, 'style.css')
        with open(css_path, 'w', encoding='utf-8') as f:
            f.write(css_content)
        results.append(f"[OK] Archivo creado: {css_path}")
        
        # Generar JS
        js_content = smart_templates.get_base_js()
        js_path = os.path.join(folder, 'script.js')
        with open(js_path, 'w', encoding='utf-8') as f:
            f.write(js_content)
        results.append(f"[OK] Archivo creado: {js_path}")
        
        # Reporte de calidad
        try:
            report = get_quality_report(html_content, css_content, js_content)
            responsive_score = report['responsive']['is_responsive']
            accessibility_score = report['accessibility']['score']
            performance_score = report['performance']['score']
            
            results.append(f"[INFO] Calidad: Responsive={'SI' if responsive_score else 'NO'} | Accesibilidad={accessibility_score}/100 | Rendimiento={performance_score}/100")
        except Exception:
            pass
        
        return results
    
    def get_code_quality_report(self, folder: str) -> str:
        """Obtener reporte de calidad de un proyecto web existente."""
        if not folder or not os.path.isdir(folder):
            return "[ERROR] Carpeta no encontrada"
        
        html_content = ""
        css_content = ""
        js_content = ""
        
        # Leer archivos
        for filename in ['index.html', 'style.css', 'script.js']:
            filepath = os.path.join(folder, filename)
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    if filename.endswith('.html'):
                        html_content = f.read()
                    elif filename.endswith('.css'):
                        css_content = f.read()
                    elif filename.endswith('.js'):
                        js_content = f.read()
        
        if not html_content and not css_content and not js_content:
            return "[ERROR] No se encontraron archivos HTML/CSS/JS en la carpeta"
        
        # Generar reporte
        report = get_quality_report(html_content, css_content, js_content)
        
        lines = ["=== REPORTE DE CALIDAD ===\n"]
        
        # Responsive
        resp = report['responsive']
        lines.append("DISEÑO RESPONSIVE:")
        lines.append(f"  - Media queries: {'SI' if resp['has_media_queries'] else 'NO'}")
        lines.append(f"  - Usa clamp(): {'SI' if resp['has_clamp'] else 'NO'}")
        lines.append(f"  - Flexbox: {'SI' if resp['has_flexbox'] else 'NO'}")
        lines.append(f"  - Grid: {'SI' if resp['has_grid'] else 'NO'}")
        if resp['issues']:
            for issue in resp['issues']:
                lines.append(f"  ! {issue}")
        lines.append("")
        
        # Accesibilidad
        acc = report['accessibility']
        lines.append(f"ACCESIBILIDAD: {acc['score']}/100")
        for good in acc['good']:
            lines.append(f"  + {good}")
        for issue in acc['issues']:
            lines.append(f"  ! {issue}")
        lines.append("")
        
        # Rendimiento
        perf = report['performance']
        lines.append(f"RENDIMIENTO: {perf['score']}/100")
        for good in perf['good']:
            lines.append(f"  + {good}")
        for issue in perf['issues']:
            lines.append(f"  ! {issue}")
        
        return "\n".join(lines)
    
    def _chat_streaming(self, enriched_prompt: str) -> str:
        """Chat con streaming - respuesta rapida"""
        import time, sys
        
        start_time = time.time()
        
        # Para IAM con streaming, no usar loader (el streaming ya muestra progreso)
        if self.engine == "iam":
            try:
                sys.stdout.write(f"\r\033[2m{self._get_mode_message()}...\033[0m ")
                sys.stdout.flush()
            except:
                pass
            response = self._call_iam_fast(enriched_prompt)
            try:
                sys.stdout.write("\r" + " " * 40 + "\r")
                sys.stdout.flush()
            except:
                pass
            return response
        
        loader = LoadingIndicator()
        msg = self._get_mode_message()
        loader.start(msg, self._get_mode_spinner())
        
        try:
            if self.engine == "multi":
                response = self._call_multi_engine(enriched_prompt)
            elif self.engine == "local":
                response = self._call_local_model(enriched_prompt)
            elif self.engine == "gemini":
                response = self._call_tertiary(enriched_prompt)
            elif self.engine == "freetheai":
                response = self._call_secondary(enriched_prompt)
            else:
                response = self._call_multi_engine(enriched_prompt)
            
            elapsed = time.time() - start_time
            return response
        finally:
            loader.stop()
    
    def _chat_normal(self, enriched_prompt: str, max_tokens: int = None) -> str:
        """Chat normal - respuesta rapida"""
        loader = LoadingIndicator()
        msg = self._get_mode_message()
        loader.start(msg, self._get_mode_spinner())
        
        try:
            if self.engine == "multi":
                return self._call_multi_engine(enriched_prompt, max_tokens=max_tokens)
            elif self.engine == "local":
                return self._call_local_model(enriched_prompt)
            elif self.engine == "gemini":
                return self._call_tertiary(enriched_prompt)
            elif self.engine == "freetheai":
                return self._call_secondary(enriched_prompt)
            elif self.engine == "iam":
                return self._call_iam_fast(enriched_prompt, max_tokens=max_tokens)
            else:
                return self._call_multi_engine(enriched_prompt, max_tokens=max_tokens)
        finally:
            loader.stop()
    
    def _call_iam_fast(self, enriched_prompt: str = None, max_tokens: int = None) -> str:
        """Llamar a la API de IA con streaming - fallback automatico entre keys"""
        import time, sys

        context = self.current_session.get_context()
        messages = [{"role": "system", "content": enriched_prompt or self.system_prompt}] + context

        # Si hay imagenes, agregar al ultimo mensaje del usuario
        if hasattr(self, '_pending_images') and self._pending_images:
            last_msg = messages[-1] if messages else {"role": "user", "content": ""}
            content_parts = [{"type": "text", "text": last_msg.get("content", "")}]
            for img_b64 in self._pending_images:
                content_parts.append({
                    "type": "image_url",
                    "image_url": {"url": f"data:image/png;base64,{img_b64}"}
                })
            messages[-1] = {"role": "user", "content": content_parts}
            self._pending_images = []

        payload = {
            "model": "mimo-v2.5-free",
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": max_tokens or 2048,
            "top_p": 0.9,
            "stream": True
        }

        def _stream_response(resp):
            """Leer streaming y mostrar en tiempo real"""
            content_tokens = []
            reasoning_tokens = []
            last_data_time = time.time()
            content_started = False

            for line in resp.iter_lines():
                if time.time() - last_data_time > 120:
                    break
                if line:
                    last_data_time = time.time()
                    line_str = line.decode('utf-8', errors='replace')
                    if line_str.startswith('data: '):
                        data_str = line_str[6:]
                        if data_str.strip() == '[DONE]':
                            break
                        try:
                            chunk = json.loads(data_str)
                            if 'choices' in chunk and chunk['choices']:
                                delta = chunk['choices'][0].get('delta', {})
                                if delta.get('content'):
                                    if not content_started:
                                        sys.stdout.write("\r" + " " * 50 + "\r")
                                        sys.stdout.flush()
                                        content_started = True
                                    content_tokens.append(delta['content'])
                                    sys.stdout.write(delta['content'])
                                    sys.stdout.flush()
                                elif delta.get('reasoning'):
                                    reasoning_tokens.append(delta['reasoning'])
                        except json.JSONDecodeError:
                            continue

            content = ''.join(content_tokens)
            reasoning = ''.join(reasoning_tokens)
            if not content and reasoning:
                if not content_started:
                    sys.stdout.write("\r" + " " * 50 + "\r")
                    sys.stdout.flush()
                content = reasoning
            return content

        def _try_key_stream(api_key, label):
            """Intentar con una key especifica"""
            try:
                sys.stdout.write(f"\r\033[2m{label}...\033[0m ")
                sys.stdout.flush()
                resp = requests.post(
                    "https://opencode.ai/zen/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json",
                        "HTTP-Referer": "https://iam-ai.local",
                        "X-Title": "IAM AI Assistant"
                    },
                    json=payload, timeout=120, stream=True
                )
                if resp.status_code == 200:
                    return _stream_response(resp)
                elif resp.status_code == 429:
                    return None  # Rate limit, intentar siguiente
                else:
                    return None
            except requests.exceptions.Timeout:
                return None
            except requests.exceptions.ConnectionError:
                return None
            except Exception:
                return None
            return None

        # Recolectar todas las keys (principal + 6 fallback)
        all_keys = [(settings.API_KEY, "Key 1")]
        for i, key in enumerate(settings.API_KEYS_FALLBACK, 2):
            all_keys.append((key, f"Key {i}"))

        # Intentar cada key hasta que una funcione
        for api_key, label in all_keys:
            if not api_key:
                continue
            result = _try_key_stream(api_key, label)
            if result is not None:
                return result
            # Verificar ESC
            try:
                from .enhanced_cli import interrupt
                if interrupt.is_interrupted:
                    return "[Interrumpido por ESC]"
            except Exception:
                pass

        return "[ERROR] Todas las API keys fallaron. Verifica tu conexion."
    
    def _call_secondary(self, enriched_prompt: str = None) -> str:
        """Llamar a IA Secundaria"""
        if not freetheai_client.is_available():
            return "[ERROR] Servidor IA no disponible"
        
        return freetheai_client.chat(
            prompt=enriched_prompt or "",
            system_prompt=self.system_prompt
        )
    
    def _call_tertiary(self, enriched_prompt: str = None) -> str:
        """Llamar a IA Terciaria"""
        if not gemini_client.is_available():
            return "[ERROR] Motor IA no disponible"
        
        return gemini_client.chat(
            prompt=enriched_prompt or "",
            system_prompt=self.system_prompt
        )
    
    def _call_multi_engine(self, enriched_prompt: str = None) -> str:
        """Llamar a todas las IAs disponibles simultaneamente y combinar respuestas"""
        import concurrent.futures
        import time
        
        start_time = time.time()
        results = {}
        errors = []
        
        def call_engine(name, func, *args):
            try:
                result = func(*args)
                return name, result, None
            except Exception as e:
                return name, None, str(e)
        
        engines = []
        
        # Motor IA Secundario
        if freetheai_client.is_available():
            engines.append(("Secundario", lambda: freetheai_client.chat(
                prompt=enriched_prompt or "",
                system_prompt=self.system_prompt
            )))
        
        # Motor IA Terciario
        if gemini_client.is_available():
            engines.append(("Terciario", lambda: gemini_client.chat(
                prompt=enriched_prompt or "",
                system_prompt=self.system_prompt
            )))
        
        # IAM (siempre disponible via proxy)
        def call_iam():
            context = self.current_session.get_context()
            messages = [{"role": "system", "content": enriched_prompt or self.system_prompt}] + context

            if settings.API_KEY:
                url = "https://opencode.ai/zen/v1/chat/completions"
                headers = {
                    "Authorization": f"Bearer {settings.API_KEY}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://iam-ai.local",
                    "X-Title": "IAM AI Assistant"
                }
            else:
                proxy_url = os.environ.get("OPENCODE_PROXY_URL", "https://iam-proxy.onrender.com")
                url = f"{proxy_url}/v1/chat/completions"
                headers = {"Content-Type": "application/json"}
            
            response = requests.post(
                url,
                headers=headers,
                json={
                    "model": "mimo-v2.5-free",
                    "messages": messages,
                    "temperature": 0.7,
                    "max_tokens": 4096,
                    "top_p": 0.9
                },
                timeout=60
            )
            if response.status_code == 200:
                data = response.json()
                if "choices" in data and data["choices"]:
                    msg = data["choices"][0]["message"]
                    content = msg.get("content")
                    if not content:
                        content = msg.get("reasoning", "")
                    return content or ""
                elif "error" in data:
                    raise Exception(data['error'])
                else:
                    raise Exception("respuesta inesperada")
            else:
                raise Exception(f"Error {response.status_code}")
        
        engines.append(("IAM", call_iam))
        
        # Ejecutar en paralelo
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            futures = {executor.submit(call_engine, name, func): name for name, func in engines}
            for future in concurrent.futures.as_completed(futures, timeout=90):
                name, result, error = future.result()
                if error:
                    errors.append(f"{name}: {error}")
                else:
                    results[name] = result
        
        elapsed = time.time() - start_time
        
        # Si no hay resultados, usar fallback
        if not results:
            return f"[MULTI-AI] Todas las IAs fallaron: {', '.join(errors)}"
        
        # Si solo hay 1 resultado, mostrarlo directamente
        if len(results) == 1:
            engine_name = list(results.keys())[0]
            return f"[{engine_name}] {results[engine_name]}"
        
        # Si hay multiples resultados, mostrar los nombres y la mejor respuesta
        engine_names = list(results.keys())
        
        # Elegir la respuesta mas larga (generalmente mas completa)
        best_engine = max(results.items(), key=lambda x: len(x[1]))
        
        # Construir respuesta combinada
        output_parts = []
        output_parts.append(f"[MULTI-AI: {', '.join(engine_names)}] ({elapsed:.1f}s)\n")
        
        # Mostrar la mejor respuesta
        output_parts.append(f"--- Respuesta de {best_engine[0]} ---")
        output_parts.append(best_engine[1])
        
        return "\n".join(output_parts)
    
    def _call_iam(self, enriched_prompt: str = None) -> str:
        """Llamar a la API de IA con MiMo v2.5 Free"""
        return self._call_iam_fast(enriched_prompt)
    
    def _call_iam_streaming(self, enriched_prompt: str, loader: LoadingIndicator) -> str:
        """Llamar a la API de IA con streaming - muestra Pensando... y luego respuesta limpia"""
        import time

        if not settings.API_KEY:
            return self._fallback_response("iam")

        context = self.current_session.get_context()
        messages = [{"role": "system", "content": enriched_prompt}] + context

        loader.stop()

        try:
            print(f"\n  {COLORS.TEAL}{self._get_mode_message()}...{COLORS.RESET}", end='', flush=True)
        except:
            pass

        # Intento 1: Directo
        for attempt in range(2):
            try:
                response = requests.post(
                    "https://opencode.ai/zen/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {settings.API_KEY}",
                        "Content-Type": "application/json",
                        "HTTP-Referer": "https://iam-ai.local",
                        "X-Title": "IAM AI Assistant"
                    },
                    json={
                        "model": "mimo-v2.5-free",
                        "messages": messages,
                        "temperature": 0.7,
                        "max_tokens": 2048,
                        "top_p": 0.9,
                        "stream": True
                    },
                    timeout=90,
                    stream=True
                )

                if response.status_code == 200:
                    content_tokens = []
                    reasoning_tokens = []
                    last_data_time = time.time()

                    for line in response.iter_lines():
                        if time.time() - last_data_time > 90:
                            break
                        if line:
                            last_data_time = time.time()
                            line = line.decode('utf-8', errors='replace')
                            if line.startswith('data: '):
                                data = line[6:]
                                if data.strip() == '[DONE]':
                                    break
                                try:
                                    chunk = json.loads(data)
                                    if 'choices' in chunk and len(chunk['choices']) > 0:
                                        delta = chunk['choices'][0].get('delta', {})
                                        if 'content' in delta and delta['content']:
                                            content_tokens.append(delta['content'])
                                        elif 'reasoning' in delta and delta['reasoning']:
                                            reasoning_tokens.append(delta['reasoning'])
                                except json.JSONDecodeError:
                                    continue

                    try:
                        print(f"\r{' ' * 40}\r", end='')
                    except:
                        pass

                    if content_tokens:
                        return ''.join(content_tokens)
                    elif reasoning_tokens:
                        return ''.join(reasoning_tokens)
                    return ""

                if attempt == 0:
                    time.sleep(2)

            except requests.exceptions.Timeout:
                if attempt == 0:
                    time.sleep(2)
                    continue
            except requests.exceptions.ConnectionError:
                if attempt == 0:
                    time.sleep(2)
                    continue
            except Exception as e:
                return f"Error: {str(e)}"

        return "[ERROR] No se pudo conectar con la API de IA. Verifica tu conexion e intenta de nuevo."
    
    def _cleanup_response(self, text: str) -> str:
        """Limpiar artefactos de markdown de la respuesta de la IA.
        Convierte *texto* y **texto** a texto plano, sin tocar bloques de codigo."""
        import re
        if not text:
            return text
        
        # Separar bloques de codigo (``` ... ```) y TOOL_CALLs del resto
        parts = re.split(r'(```[\s\S]*?```|<code>[\s\S]*?</code>|\[TOOL_CALL\][\s\S]*?\[/TOOL_CALL\])', text)
        
        cleaned = []
        for i, part in enumerate(parts):
            # Los bloques de codigo y TOOL_CALLs se dejan intactos
            if part.startswith('```') or part.startswith('<code>') or part.startswith('[TOOL_CALL]'):
                cleaned.append(part)
            else:
                # Remover **texto** (bold markdown) -> texto
                part = re.sub(r'\*\*(.+?)\*\*', r'\1', part)
                # Remover *texto* (italic markdown) -> texto
                part = re.sub(r'\*(.+?)\*', r'\1', part)
                # Remover __texto__ -> texto
                part = re.sub(r'__(.+?)__', r'\1', part)
                # Remover _texto_ -> texto
                part = re.sub(r'_(.+?)_', r'\1', part)
                # Limpiar doble espacio
                part = re.sub(r'  +', ' ', part)
                cleaned.append(part)
        
        return ''.join(cleaned)
    
    def _fallback_response(self, engine: str) -> str:
        """Respuesta cuando no hay API key"""
        if engine == "iam":
            return """API Key de IAM no configurada

La API ya viene configurada. Si no funciona:
1. Verifica tu conexion a internet
2. Reinicia IAM con: python main.py"""
        
        return "Motor no configurado. Usa /engine para cambiar."
    
    def get_status(self) -> Dict[str, Any]:
        """Obtener estado del agente"""
        return {
            "mode": self.current_mode,
            "engine": self.engine,
            "session": self.current_session.id if self.current_session else None,
            "messages": len(self.current_session.messages) if self.current_session else 0,
            "model": settings.MODELS.get(self.current_mode),
            "thinking_level": self.thinking_level.value,
            "show_thinking": self.show_thinking,
            "active_project": self.active_project
        }


class AgentRouter:
    """
    Router que maneja comandos especiales y delega a agentes
    """
    
    def __init__(self, memory: MemorySystem = None):
        self.memory = memory or MemorySystem()
        self.agent = Agent(memory=self.memory)
        self.last_topic = None
        self.last_folder = None  # Ultima carpeta creada/mencionada
        self.screen_monitor = ScreenMonitor()
    
    def process_input(self, user_input: str) -> str:
        """Procesar entrada del usuario"""
        if user_input.startswith("/"):
            return self._handle_command(user_input)
        
        for mode in ["general", "builder", "plan", "frontend", "backend", "debug", "security"]:
            if user_input.lower() == mode:
                self.agent.set_mode(mode)
                agent_info = AGENT_PROMPTS[mode]
                return f"[OK] Modo cambiado a: {agent_info['icon']} {agent_info['name']}"
        
        # Animacion de carga
        loader = LoadingIndicator()
        loader.start(self.agent._get_mode_message(), self.agent._get_mode_spinner())
        
        try:
            # PARAR loader antes de permisos
            loader.stop()
            
            # La IA PIENSA y decide que hacer
            ai_response = self._ai_decide_action(user_input)
            if ai_response:
                # Ejecutar tool calls si los hay
                executed = self.agent._execute_tool_calls(ai_response)
                if executed != ai_response:
                    return executed
                return ai_response
            
            # Si la IA fallo completamente, intentar de nuevo
            loader.start(self.agent._get_mode_message("reintentando"), self.agent._get_mode_spinner())
            loader.stop()
            return self.agent.chat(user_input)
        except Exception as e:
            loader.stop()
            raise e
    
    def _ai_decide_action(self, user_input: str) -> str:
        """La IA analiza el input del usuario y decide que accion tomar.
        Usa el system prompt existente del agente para pensar."""
        try:
            response = self.agent.chat(user_input)
            return response
        except Exception:
            return None
    
    def _detect_natural_action(self, user_input: str) -> str:
        """Detectar acciones del sistema en lenguaje natural y ejecutarlas"""
        import os
        input_lower = user_input.lower()
        
        # Ruta por defecto: escritorio del usuario
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        
        # Diccionario de sinonimos y variaciones comunes
        SYNONYMS = {
            "create_folder": ["crea una carpeta", "crear carpeta", "nueva carpeta", "carpeta llamada", "carpeta nombre", "mkdir", "haz una carpeta", "genera una carpeta", "agrega una carpeta"],
            "read_file": ["lee el archivo", "leer archivo", "abre el archivo", "muestra el contenido", "que dice el archivo", "cat ", "que hay en", "contenido de", "ver archivo", "abre el txt"],
            "create_file": ["crea un archivo", "crear archivo", "nuevo archivo", "archivo llamado", "touch ", "haz un archivo", "genera un archivo", "crea un txt", "crea un py"],
            "list_files": ["lista archivos", "que hay en", "que archivos hay", "que hay aqui", "que hay en esta carpeta", "ls", "dir", "listar", "mostrar archivos"],
            "execute_command": ["ejecuta", "corre", "run ", "exec ", "inicia", "abre ", "ejecutar", "correr"],
            "kill_process": ["mata el proceso", "cierra el programa", "termina el proceso", "kill ", "finaliza"],
            "get_ip": ["cual es mi ip", "mi ip", "ip address", "ip privada", "ip publica", "direccion ip", "que ip tengo"],
            "get_time": ["que hora es", "dame la hora", "cuantos son", "que hora tiene", "hora actual", "hora", "que hora", "que hora es ahora"],
            "get_date": ["que fecha es", "dame la fecha", "que dia es", "fecha actual", "hoy que dia es", "fecha", "que dia", "que dia es hoy"],
            "ping": ["ping a", "haz ping", "prueba de conexion", "verifica conexion", "conectividad"],
            "hardware": ["info del pc", "informacion del pc", "que pc tengo", "hardware", "especificaciones", "caracteristicas"],
            "git_init": ["inicia git", "git init", "crea repositorio", "inicializar git"],
            "git_commit": ["guarda cambios", "git commit", "guardar en git", "subir cambios"],
            "install_package": ["instala", "instalar", "instalar paquete", "agregar paquete"],
            "search": ["busca", "buscar", "encuentra", "encontrar", "search", "find"],
        }
        
        def match_pattern(text, category):
            """Busqueda flexible con sinonimos"""
            text_lower = text.lower()
            patterns = SYNONYMS.get(category, [])
            for pattern in patterns:
                if pattern in text_lower:
                    return True
            return False
        
        def extract_parameter(text, after_words):
            """Extraer parametro despues de ciertas palabras"""
            text_lower = text.lower()
            for phrase in after_words:
                if phrase in text_lower:
                    idx = text_lower.index(phrase) + len(phrase)
                    rest = text[idx:].strip().strip('"').strip("'").strip(".").strip('"').strip("'").strip(":")
                    words_rest = rest.split()
                    stop_words = ["y", "con", "que", "para", "en", "dentro", "donde", "haz", "hacer", "tiene", "tenga", "con", "a", "al", "del", "las", "los", "una", "un", "el", "la"]
                    name_words = []
                    for w in words_rest:
                        clean_w = w.strip('"').strip("'").strip(",").strip(":")
                        if clean_w.lower() in stop_words:
                            break
                        name_words.append(clean_w)
                    if name_words:
                        return " ".join(name_words)
            return None
        
        # === PREGUNTAS SIMPLES ===
        # Hora
        if match_pattern(user_input, "get_time"):
            self.last_topic = "hora"
            return system_info.get_time()
        
        # Fecha
        if match_pattern(user_input, "get_date"):
            self.last_topic = "fecha"
            return system_info.get_date()
        
        # Fecha y hora
        if any(w in input_lower for w in ["fecha y hora", "dia y hora", "cuando es"]):
            self.last_topic = "fecha_hora"
            return system_info.get_datetime()
        
        # Usuario
        if any(w in input_lower for w in ["cual es mi usuario", "mi usuario", "que usuario soy", "quien soy", "nombre de usuario"]):
            import getpass
            return f"Tu usuario: {getpass.getuser()}"
        
        # Hostname
        if any(w in input_lower for w in ["como se llama mi pc", "nombre del pc", "hostname", "nombre de la pc"]):
            import socket
            return f"Tu PC: {socket.gethostname()}"
        
        # === DETECTAR CARPETA EXISTENTE ===
        # "en escritorio hay una carpeta llamada X" / "existe una carpeta X"
        if any(phrase in input_lower for phrase in ["en escritorio hay una carpeta", "existe una carpeta", "hay una carpeta"]):
            # Extraer nombre de la carpeta
            for phrase in ["llamada ", "llamado ", "nombre ", "que se llama "]:
                if phrase in input_lower:
                    idx = input_lower.index(phrase) + len(phrase)
                    rest = user_input[idx:].strip().strip('"').strip("'").strip(".")
                    folder_name = rest.split()[0] if rest.split() else rest
                    folder_path = os.path.join(desktop, folder_name)
                    if os.path.isdir(folder_path):
                        self.last_folder = folder_path
                        return f"Encontre la carpeta '{folder_name}' en: {folder_path}"
                    else:
                        # Crear la carpeta si no existe
                        success, msg = filesystem.create_folder(folder_path)
                        if success:
                            self.last_folder = folder_path
                        return msg
        
        # === CREAR CARPETA ===
        if match_pattern(user_input, "create_folder"):
            name = extract_parameter(user_input, ["llamada:", "llamada ", "nombre:", "nombre ", "llamado:", "llamado "])
            if not name:
                words = user_input.split()
                for i, w in enumerate(words):
                    if w.lower().strip('"').strip("'").strip(":") in ["carpeta", "folder"]:
                        if i + 1 < len(words):
                            name = words[i + 1].strip('"').strip("'").strip(".").strip(":")
                            break
            if name:
                # Limpiar comillas restantes
                name = name.strip('"').strip("'").strip(".")
                path = os.path.join(desktop, name)
                
                # Si la carpeta ya existe, no crearla de nuevo
                if os.path.isdir(path):
                    self.last_folder = path
                    return f"La carpeta '{name}' ya existe en: {path}"
                
                success, msg = filesystem.create_folder(path)
                if success:
                    self.last_folder = path
                return msg
        
        # === LEER ARCHIVO ===
        if any(word in input_lower for word in ["lee el archivo", "leer archivo", "abre el archivo", "muestra el contenido", "que dice el archivo", "cat "]):
            path = None
            for phrase in ["lee el archivo ", "leer archivo ", "abre el archivo ", "muestra el contenido de ", "que dice el archivo ", "cat "]:
                if phrase in input_lower:
                    idx = input_lower.index(phrase) + len(phrase)
                    rest = user_input[idx:].strip().strip('"').strip("'").strip(".")
                    if rest:
                        path = rest
                        break
            if not path:
                words = user_input.split()
                for i, w in enumerate(words):
                    if w.lower() in ["archivo", "file"]:
                        if i + 1 < len(words):
                            path = words[i + 1].strip('"').strip("'").strip(".")
                            break
            if path:
                if not os.path.isabs(path):
                    # Buscar en escritorio y carpeta actual
                    desktop_path = os.path.join(desktop, path)
                    if os.path.exists(desktop_path):
                        path = desktop_path
                    elif os.path.exists(path):
                        pass
                    else:
                        path = desktop_path
                success, content = filesystem.read_file(path)
                if success:
                    lines = content.splitlines()
                    if len(lines) > 50:
                        return f"CONTENIDO: {os.path.basename(path)} ({len(lines)} lineas)\n\n" + "\n".join(lines[:50]) + f"\n\n... ({len(lines)} lineas total)"
                    return f"CONTENIDO: {os.path.basename(path)}\n\n{content}"
                return str(content)
        
        # === CREAR ARCHIVO ===
        if any(word in input_lower for word in ["crea un archivo", "crear archivo", "nuevo archivo", "haz un archivo", "genera un archivo", "archivo llamado"]):
            name = None
            for phrase in ["llamado ", "llamada ", "nombre ", "que se llame "]:
                if phrase in input_lower:
                    idx = input_lower.index(phrase) + len(phrase)
                    rest = user_input[idx:].strip().strip('"').strip("'").strip(".")
                    name = rest.split()[0] if rest.split() else rest
                    break
            if not name:
                words = user_input.split()
                for i, w in enumerate(words):
                    if w.lower() in ["archivo", "file", "arch"]:
                        if i + 1 < len(words):
                            name = words[i + 1].strip('"').strip("'")
                            break
            if name:
                content = ""
                for phrase in ["con ", "que tenga ", "contenido ", "que diga ", "con contenido "]:
                    if phrase in input_lower:
                        idx = input_lower.index(phrase) + len(phrase)
                        content = user_input[idx:].strip()
                        break
                path = os.path.join(desktop, name)
                success, msg = filesystem.create_file(path, content)
                return msg
        
        # === CREAR PROYECTO ===
        if any(word in input_lower for word in ["crea un proyecto", "crear proyecto", "nuevo proyecto", "haz un proyecto", "genera un proyecto", "hazme un proyecto", "creame un proyecto", "haz un proy", "crea un proy", "dentro de esa carpeta has un", "dentro de esa carpeta crea", "dentro de esa has un", "dentro de esa crea", "has un proyecto", "crea la ", "crea el ", "haz la ", "haz el ", "genera la ", "genera el ", "dentro de ella", "en ella", "ahi mismo", "aqui mismo", "puedes hacerla", "hazla", "hasla", "creala", "haz la calculadora", "crea la calculadora", "haz una calculadora", "crea una calculadora"]):
            
            # Detectar carpeta destino
            carpeta_destino = desktop
            usar_directo = False
            found_folder = False
            
            # Detectar "dentro de esa carpeta" / "dentro de ella" / "en ella"
            if any(phrase in input_lower for phrase in ["dentro de esa carpeta", "dentro de esa", "en esa carpeta", "en esa", "ahi", "aqui", "en la misma", "dentro de ella", "en ella", "ahi mismo", "aqui mismo", "puedes hacerla", "hazla", "hasla", "creala"]):
                usar_directo = True
                if self.last_folder and os.path.isdir(self.last_folder):
                    carpeta_destino = self.last_folder
                else:
                    try:
                        folders = [f for f in os.listdir(desktop) if os.path.isdir(os.path.join(desktop, f))]
                        if folders:
                            carpeta_destino = os.path.join(desktop, sorted(folders, key=lambda x: os.path.getmtime(os.path.join(desktop, x)), reverse=True)[0])
                            self.last_folder = carpeta_destino
                    except:
                        pass
            else:
                for phrase in ["en carpeta ", "en la carpeta ", "dentro de la carpeta ", "en la ruta ", "en directorio ", "adentro de "]:
                    if phrase in input_lower:
                        idx = input_lower.index(phrase) + len(phrase)
                        rest = user_input[idx:].strip().strip('"').strip("'").strip(".")
                        if rest:
                            words_rest = rest.split()
                            stop_words = ["que", "y", "con", "para", "llamado", "llamada", "nombre", "un", "una", "el", "la", "del", "las", "los"]
                            folder_words = []
                            for w in words_rest:
                                if w.lower() in stop_words:
                                    break
                                folder_words.append(w)
                            folder_name = " ".join(folder_words) if folder_words else rest
                            
                            if os.path.isabs(folder_name):
                                carpeta_destino = folder_name
                            else:
                                carpeta_destino = os.path.join(desktop, folder_name)
                            found_folder = True
                        break
            
            if not found_folder:
                if any(phrase in input_lower for phrase in ["en escritorio", "en el escritorio", "al escritorio", "para el escritorio", "en mi escritorio"]):
                    carpeta_destino = desktop
            
            if not found_folder and not usar_directo:
                if any(phrase in input_lower for phrase in ["en esa", "ahi", "aqui", "en ella", "dentro"]):
                    if self.last_folder and os.path.isdir(self.last_folder):
                        carpeta_destino = self.last_folder
                        usar_directo = True
            
            # Extraer nombre del proyecto
            nombre_proyecto = "Proyecto"
            for phrase in ["llamado ", "llamada ", "nombre ", "que se llame ", "que se llama "]:
                if phrase in input_lower:
                    idx = input_lower.index(phrase) + len(phrase)
                    rest = user_input[idx:].strip().strip('"').strip("'").strip(".")
                    nombre_proyecto = rest.split()[0].capitalize() if rest.split() else rest.capitalize()
                    break
            
            # Si no hay nombre explicito, intentar extraer del contexto
            if nombre_proyecto == "Proyecto":
                for word in ["calculadora", "juego", "web", "api", "blog", "chat", "tienda", "portfolio", "dashboard", "notas", "tareas", "pomodoro", "reloj", "clima", "password", "cronometro", "contador"]:
                    if word in input_lower:
                        nombre_proyecto = word.capitalize()
                        break
            
            carpeta_proyecto = os.path.join(carpeta_destino, nombre_proyecto)
            filesystem.create_folder(carpeta_proyecto)
            self.last_folder = carpeta_proyecto
            
            # Listar archivos existentes en la carpeta
            archivos_existentes = []
            if os.path.isdir(carpeta_proyecto):
                try:
                    archivos_existentes = [f for f in os.listdir(carpeta_proyecto) if os.path.isfile(os.path.join(carpeta_proyecto, f))]
                except:
                    pass
            
            contexto_archivos = ""
            if archivos_existentes:
                contexto_archivos = f"""
ARCHIVOS QUE YA EXISTEN en {carpeta_proyecto}:
{chr(10).join(f'  - {a}' for a in archivos_existentes)}

IMPORTANTE: Si el usuario pide modificar algo que ya existe, USA edit_file para EDITAR el archivo existente, NO lo recribas completo a menos que sea absolutamente necesario."""
            
            # Dejar que la IA genere el codigo dinamicamente
            prompt_ia = f"""El usuario te pide algo. TU decides que hacer.

PETICION: "{user_input}"

CARPETA: {carpeta_proyecto}
{contexto_archivos}

NO sigas un template. NO sigas instrucciones fijas. TU PIENSAS.

Tu eres un programador experto. Analiza la peticion, decide la mejor solucion, y ejecutala.

Herramientas:
- [TOOL_CALL] action: create_file path: ... content: ... [/TOOL_CALL]
- [TOOL_CALL] action: edit_file path: ... old_text: ... new_text: ... [/TOOL_CALL]
- [TOOL_CALL] action: read_file path: ... [/TOOL_CALL]
- [TOOL_CALL] action: execute command: ... [/TOOL_CALL]

Tu decides que archivos crear, que tecnologias usar, que funcionalidades incluir.

Unico requisito: codigo REAL y FUNCIONAL, nunca placeholders.

Procede."""

            return self.agent.chat(prompt_ia)
        
        # === LISTAR ARCHIVOS ===
        if any(word in input_lower for word in ["que archivos hay", "que hay en", "lista", "muestra archivos", "que tengo", "cuales son los archivos"]):
            path = desktop
            for phrase in ["en el escritorio", "en escritorio", "de el escritorio", "de escritorio"]:
                if phrase in input_lower:
                    path = desktop
                    break
            for phrase in ["en la carpeta ", "en carpeta ", "en directorio ", "en la ruta ", "en ruta "]:
                if phrase in input_lower:
                    idx = input_lower.index(phrase) + len(phrase)
                    rest = user_input[idx:].strip().strip('"').strip("'").strip(".")
                    if rest:
                        path = rest
                        break
            success, items = filesystem.list_directory(path)
            if success:
                output = [f"CONTENIDO DE: {path}\n"]
                for item in items[:30]:
                    icon = "[DIR] " if item['is_dir'] else "      "
                    output.append(f"{icon}{item['name']}")
                output.append(f"\nTOTAL: {len(items)} elementos")
                return "\n".join(output)
            return str(items[0])
        
        # === EJECUTAR COMANDO ===
        if any(word in input_lower for word in ["ejecuta ", "corre ", "run ", "exec "]):
            for phrase in ["ejecuta ", "corre ", "run ", "exec "]:
                if phrase in input_lower:
                    idx = input_lower.index(phrase) + len(phrase)
                    command = user_input[idx:].strip()
                    
                    # Limpiar palabras de relleno en español
                    filler_words = ['el', 'la', 'los', 'las', 'un', 'una', 'lo', 'al', 'del',
                                    'comando', 'orden', 'order', 'command', 'cmd',
                                    'por favor', 'pls', 'please', 'que', 'qe']
                    words = command.split()
                    cleaned = []
                    for w in words:
                        if w.lower().strip('"').strip("'") not in filler_words:
                            cleaned.append(w)
                    command = ' '.join(cleaned) if cleaned else command
                    
                    if not command:
                        return "No se detecto ningun comando para ejecutar. Uso: ejecuta [comando]"
                    
                    # PEDIR PERMISO antes de ejecutar
                    risk_level = permission_system.assess_risk(command)
                    permission_granted, permission_msg = require_permission(
                        PermissionAction.EXECUTE_COMMAND,
                        command,
                        f"Ejecutar comando: {command}",
                        risk_level
                    )
                    
                    if not permission_granted:
                        return f"[DENEGADO] Comando no ejecutado: {permission_msg}"
                    
                    success, output = filesystem.run_command(command)
                    return f"[OK] EJECUTANDO: {command}\n\n{output}" if success else f"[ERROR] {output}"
        
        # === EJECUTAR PYTHON ===
        if any(word in input_lower for word in ["ejecuta python", "corre python"]):
            for phrase in ["ejecuta python ", "corre python "]:
                if phrase in input_lower:
                    idx = input_lower.index(phrase) + len(phrase)
                    code = user_input[idx:].strip()
                    if not code:
                        return "Uso: ejecuta python [codigo]"
                    
                    # PEDIR PERMISO antes de ejecutar Python
                    permission_granted, permission_msg = require_permission(
                        PermissionAction.EXECUTE_COMMAND,
                        f"python {code[:50]}...",
                        f"Ejecutar codigo Python",
                        "medium"
                    )
                    
                    if not permission_granted:
                        return f"[DENEGADO] Python no ejecutado: {permission_msg}"
                    
                    success, output = filesystem.run_python(code)
                    return f"[OK] EJECUTANDO PYTHON...\n\n{output}"
        
        # Detectar "python print(...)" o "python [codigo]"
        if user_input.lower().startswith("python ") and "(" in user_input:
            code = user_input[7:].strip()
            
            # PEDIR PERMISO
            permission_granted, permission_msg = require_permission(
                PermissionAction.EXECUTE_COMMAND,
                f"python {code[:50]}...",
                f"Ejecutar codigo Python inline",
                "medium"
            )
            
            if not permission_granted:
                return f"[DENEGADO] Python no ejecutado: {permission_msg}"
            
            success, output = filesystem.run_python(code)
            return f"[OK] EJECUTANDO PYTHON...\n\n{output}"
        
        # === PROCESOS ===
        if any(word in input_lower for word in ["procesos", "que procesos hay", "lista de procesos", "que esta corriendo", "cuantos procesos"]):
            success, output = process_manager.list_processes()
            if success:
                if isinstance(output, list):
                    return f"Procesos activos: {len(output)}"
                return str(output)
            return str(output)
        
        if any(word in input_lower for word in ["mata el proceso", "matar proceso", "kill process"]):
            for phrase in ["mata el proceso ", "matar proceso ", "kill process "]:
                if phrase in input_lower:
                    idx = input_lower.index(phrase) + len(phrase)
                    target = user_input[idx:].strip()
                    if target.isdigit():
                        success, output = process_manager.kill_process(pid=int(target))
                    else:
                        success, output = process_manager.kill_process(name=target)
                    return output
        
        if any(word in input_lower for word in ["top procesos", "procesos que mas usan", "mas consumidores"]):
            success, output = process_manager.get_top_processes()
            return output if success else str(output)
        
        # === RED ===
        # MAC address (before IP to avoid conflict)
        if any(word in input_lower for word in ["mac", "direccion mac", "mac address", "fisica", "dir mac"]):
            success, output = hardware.get_network_adapters()
            if success and output:
                try:
                    # Parsear la salida para extraer MAC limpia
                    raw = str(output[0]) if isinstance(output, list) else str(output)
                    for line in raw.split('\n'):
                        if 'Ethernet' in line or 'Wi-Fi' in line or 'Up' in line:
                            parts = line.split()
                            for part in parts:
                                if '-' in part and len(part) == 17 and part[2] == '-':
                                    return f"Tu MAC: {part}"
                    return f"Tu MAC: {raw[:50]}"
                except:
                    return f"Tu MAC: {str(output)[:50]}"
            return "No pude obtener tu MAC"
        
        if any(w in input_lower for w in ["mi ip", "direccion ip", "mi direccion ip", "que ip tengo"]):
            self.last_topic = "ip"
            # Detectar si quiere IP publica o privada
            if any(word in input_lower for word in ["publica", "public", "externa", "exterior"]):
                success, output = network.get_ip_info()
                if success and isinstance(output, dict):
                    return f"IP Publica: {output.get('public_ip', 'N/A')}"
                return str(output)
            elif any(word in input_lower for word in ["privada", "private", "local", "interna", "lan"]):
                success, output = network.get_ip_info()
                if success and isinstance(output, dict):
                    return f"IP Privada: {output.get('local_ip', 'N/A')}"
                return str(output)
            else:
                success, output = network.get_ip_info()
                if success and isinstance(output, dict):
                    lines = []
                    if output.get('local_ip'):
                        lines.append(f"IP Privada: {output['local_ip']}")
                    if output.get('public_ip'):
                        lines.append(f"IP Publica: {output['public_ip']}")
                    if output.get('hostname'):
                        lines.append(f"Hostname: {output['hostname']}")
                    return "\n".join(lines) if lines else str(output)
                return str(output)
        
        if any(word in input_lower for word in ["ping ", "haz ping"]):
            for phrase in ["ping ", "haz ping a "]:
                if phrase in input_lower:
                    idx = input_lower.index(phrase) + len(phrase)
                    host = user_input[idx:].strip()
                    success, output = network.ping(host)
                    return output
        
        if any(word in input_lower for word in ["dns ", "resolve ", "que ip tiene"]):
            for phrase in ["dns ", "resolve ", "que ip tiene "]:
                if phrase in input_lower:
                    idx = input_lower.index(phrase) + len(phrase)
                    domain = user_input[idx:].strip()
                    success, output = network.dns_lookup(domain)
                    if success and output:
                        ips = output if isinstance(output, list) else [str(output)]
                        return f"DNS '{domain}': {', '.join(str(ip) for ip in ips[:3])}"
                    return f"DNS '{domain}': {output}"
        
        if any(word in input_lower for word in ["escanea puertos", "scan ports", "puertos abiertos"]):
            host = "localhost"
            for phrase in ["escanea puertos ", "scan ports ", "puertos abiertos de "]:
                if phrase in input_lower:
                    idx = input_lower.index(phrase) + len(phrase)
                    host = user_input[idx:].strip() or "localhost"
                    break
            success, output = network.scan_ports(host, 1, 1024)
            if success and output:
                if isinstance(output, list):
                    ports = [str(p.get('port', p)) if isinstance(p, dict) else str(p) for p in output[:5]]
                    return f"Puertos '{host}': {', '.join(ports)}"
                return f"Puertos '{host}': {str(output)[:100]}"
            return f"Puertos '{host}': {output}"
        
        if any(word in input_lower for word in ["traceroute", "ruta a", "traza ruta"]):
            for phrase in ["traceroute ", "ruta a ", "traza ruta a "]:
                if phrase in input_lower:
                    idx = input_lower.index(phrase) + len(phrase)
                    host = user_input[idx:].strip()
                    success, output = network.traceroute(host)
                    if success and output:
                        return f"Traceroute '{host}': {str(output)[:100]}"
                    return f"Traceroute '{host}': {output}"
        
        # Conectar WiFi (antes que el handler generico de wifi)
        if any(word in input_lower for word in ["conectar wifi", "connect wifi", "unirse a red"]):
            for phrase in ["conectar wifi", "connect wifi", "unirse a red"]:
                if phrase in input_lower:
                    idx = input_lower.index(phrase) + len(phrase)
                    ssid = user_input[idx:].strip()
                    if ssid:
                        success, output = network.connect_wifi(ssid)
                        return f"WiFi '{ssid}': {output}"
        
        if any(word in input_lower for word in ["wifi", "redes wifi", "networks", "redes disponibles", "que redes hay", "wifi networks"]):
            success, output = network.get_wifi_networks()
            if success and output:
                if isinstance(output, list):
                    networks = [n.get('name', str(n)) if isinstance(n, dict) else str(n) for n in output[:5]]
                    return f"WiFi: {', '.join(networks)}"
                return f"WiFi: {str(output)[:100]}"
            return f"WiFi: {output}"
        
        if any(word in input_lower for word in ["conexiones", "connections", "conexiones activas"]):
            success, output = network.get_connections()
            if success and output:
                if isinstance(output, list):
                    return f"Conexiones: {len(output)}"
                return f"Conexiones: {str(output)[:100]}"
            return f"Conexiones: {output}"
        
        # === PROGRAMAS INSTALADOS ===
        if any(word in input_lower for word in ["programas", "aplicaciones", "apps instaladas", "que tengo instalado", "software", "que programas"]):
            success, output = system_info.get_installed_programs()
            if success and output:
                if isinstance(output, list):
                    output_str = f"PROGRAMAS INSTALADOS ({len(output)} total):\n\n"
                    for i, prog in enumerate(output[:25], 1):
                        output_str += f"  {i}. {prog}\n"
                    if len(output) > 25:
                        output_str += f"\n  ... y {len(output) - 25} mas"
                    return output_str
                return str(output)[:200]
            return "No pude obtener la lista de programas"
        
        # === QUE PUEDO HACER ===
        if any(word in input_lower for word in ["que puedes hacer", "que sabes hacer", "ayuda", "opciones", "funciones"]):
            return """Puedo hacer muchas cosas! Aqui algunas:

SISTEMA:
  - Ejecutar comandos (ej: "ejecuta ipconfig")
  - Ver info del PC (CPU, RAM, disco, GPU)
  - Listar/abrir programas instalados
  - Gestionar procesos
  - Ver conexiones de red

ARCHIVOS:
  - Crear, editar, leer archivos
  - Crear carpetas y proyectos completos
  - Buscar archivos por nombre o contenido
  - Comprimir/descomprimir ZIP

RED:
  - Ver mi IP (publica y privada)
  - Hacer ping a servidores
  - Ver redes WiFi disponibles
  - Escanear puertos

CODIGO:
  - Ejecutar Python
  - Analizar codigo
  - Crear proyectos con estructura completa

SEGURIDAD:
  - Ver firewall
  - Gestionar usuarios
  - Ver logs del sistema

Solo dime que necesitas!"""
        
        # === HARDWARE ===
        if any(word in input_lower for word in ["hardware", "info del pc", "informacion del pc", "que tengo"]):
            success, output = hardware.get_full_system_info()
            if success and output:
                if isinstance(output, dict):
                    lines = []
                    for k, v in output.items():
                        if v:
                            lines.append(f"{k}: {str(v)[:50]}")
                    return "\n".join(lines[:5]) if lines else str(output)[:100]
                return str(output)[:100]
            return f"Hardware: {output}"
        
        if any(word in input_lower for word in ["cpu", "procesador"]):
            success, output = hardware.get_cpu_info()
            if success and output:
                if isinstance(output, dict):
                    details = output.get('details', '')
                    for line in details.split('\n'):
                        if 'Name' in line and ':' in line:
                            return f"CPU: {line.split(':', 1)[-1].strip()}"
                    return f"CPU: {output.get('processor', str(output)[:50])}"
                return f"CPU: {str(output)[:100]}"
            return f"CPU: {output}"
        
        # RAM - ser especifico para no confundir con "programas"
        if any(word in input_lower.split() for word in ["ram", "memoria", "memoria ram"]):
            success, output = hardware.get_ram_info()
            if success and output:
                if isinstance(output, dict):
                    details = output.get('details', '')
                    for line in details.split('\n'):
                        if 'TotalGB' in line:
                            total = line.split(':')[-1].strip()
                            return f"RAM: {total} GB"
                    return f"RAM: {output.get('total', str(output)[:50])}"
                return f"RAM: {str(output)[:100]}"
            return f"RAM: {output}"
        
        if any(word in input_lower for word in ["disco", "discos", "almacenamiento", "hdd", "ssd"]):
            success, output = hardware.get_disk_info()
            if success and output:
                if isinstance(output, list):
                    for item in output:
                        if isinstance(item, dict) and 'volumes' in item:
                            lines = []
                            for line in item['volumes'].split('\n'):
                                parts = line.split()
                                if len(parts) >= 6:
                                    drive = parts[0]
                                    if len(drive) == 1 and drive.isalpha():
                                        numeric_parts = [p for p in parts[1:] if any(c.isdigit() for c in p)]
                                        if len(numeric_parts) >= 2:
                                            size = numeric_parts[0]
                                            free = numeric_parts[1]
                                            lines.append(f"{drive}: {size} GB, {free} libre")
                            if lines:
                                return "\n".join(lines[:4])
                    return f"Discos: {str(output)[:100]}"
            return f"Discos: {output}"
        
        if any(word in input_lower for word in ["gpu", "tarjeta grafica", "video"]):
            success, output = hardware.get_gpu_info()
            if success and output:
                if isinstance(output, list) and output:
                    raw = str(output[0])
                    for line in raw.split('\n'):
                        if line.strip().startswith('Name') and ':' in line:
                            name = line.split(':', 1)[-1].strip()
                            if name:
                                return f"GPU: {name}"
                    return f"GPU: {str(output[0])[:50]}"
                return f"GPU: {str(output)[:100]}"
            return f"GPU: {output}"
        
        if any(word in input_lower for word in ["bateria", "battery"]):
            success, output = hardware.get_battery_info()
            if success and output:
                if isinstance(output, dict):
                    level = output.get('charge', output.get('level', '?'))
                    return f"Bateria: {level}%"
                return f"Bateria: {str(output)[:100]}"
            return "No hay bateria detectada"
        
        if any(word in input_lower for word in ["temperatura", "temperature", "calor"]):
            success, output = hardware.get_temperature()
            if success and output:
                if isinstance(output, dict):
                    cpu_temp = output.get('cpu', output.get('temp', '?'))
                    return f"Temperatura CPU: {cpu_temp}"
                return f"Temperatura: {str(output)[:100]}"
            return "No se detectaron sensores de temperatura"
        
        if any(word in input_lower for word in ["usb", "dispositivos usb"]):
            success, output = hardware.get_usb_devices()
            if success and output:
                if isinstance(output, list):
                    return f"USB: {len(output)} dispositivos"
                return f"USB: {str(output)[:100]}"
            return "No se detectaron dispositivos USB"
        
        if any(word in input_lower for word in ["wifi info", "info wifi", "adaptadores de red"]):
            success, output = hardware.get_network_adapters()
            if success and output:
                try:
                    raw = str(output[0]) if isinstance(output, list) else str(output)
                    mac = ""
                    ip = ""
                    for line in raw.split('\n'):
                        if 'Ethernet' in line or 'Wi-Fi' in line:
                            parts = line.split()
                            for part in parts:
                                if '-' in part and len(part) == 17:
                                    mac = part
                                if '.' in part and len(part) > 6:
                                    ip = part
                    info = []
                    if mac: info.append(f"MAC: {mac}")
                    if ip: info.append(f"IP: {ip}")
                    return "\n".join(info) if info else raw[:100]
                except:
                    pass
            return "No se detectaron adaptadores de red"
        
        # === BASE DE DATOS ===
        if any(word in input_lower for word in ["base de datos", "database", "sqlite"]):
            if any(word in input_lower for word in ["crear", "create", "nueva"]):
                for phrase in ["crear ", "create ", "nueva "]:
                    if phrase in input_lower:
                        idx = input_lower.index(phrase) + len(phrase)
                        rest = user_input[idx:].strip()
                        if "base de datos" in rest:
                            rest = rest.replace("base de datos", "").strip()
                        if "database" in rest:
                            rest = rest.replace("database", "").strip()
                        db_name = rest.split()[0] if rest else "test.db"
                        if not db_name.endswith('.db'):
                            db_name += '.db'
                        success, output = database.sqlite_create(db_name)
                        return f"Crear DB: {output}"
            if any(word in input_lower for word in ["query", "ejecutar", "sql"]):
                for phrase in ["query ", "ejecutar ", "sql "]:
                    if phrase in input_lower:
                        idx = input_lower.index(phrase) + len(phrase)
                        query = user_input[idx:].strip()
                        success, output = database.sqlite_query("test.db", query)
                        return f"Query: {str(output)[:100]}"
            if filesystem.file_exists("test.db"):
                success, output = database.sqlite_tables("test.db")
                return f"Tablas: {str(output)[:100]}"
            return "No hay base de datos"
        
        # === GIT ===
        if any(word in input_lower for word in ["git init", "inicializar git", "crear repositorio"]):
            success, output = git.init()
            return output
        
        if any(word in input_lower for word in ["git status", "estado del repositorio"]):
            success, output = git.status()
            return output
        
        if any(word in input_lower for word in ["git commit", "commitear", "guardar cambios"]):
            for phrase in ["git commit ", "commitear ", "guardar cambios "]:
                if phrase in input_lower:
                    idx = input_lower.index(phrase) + len(phrase)
                    message = user_input[idx:].strip() if user_input[idx:].strip() else "Update"
                    success, output = git.commit(message)
                    return output
            success, output = git.commit("Update")
            return output
        
        if any(word in input_lower for word in ["git push", "subir cambios"]):
            success, output = git.push()
            return output
        
        if any(word in input_lower for word in ["git pull", "bajar cambios"]):
            success, output = git.pull()
            return output
        
        if any(word in input_lower for word in ["git log", "historial", "commits"]):
            success, output = git.log()
            return output
        
        if any(word in input_lower for word in ["git branches", "ramas", "listar ramas"]):
            success, output = git.branches()
            return output
        
        # === PAQUETES ===
        if any(word in input_lower for word in ["instalar paquete", "install package", "instalar dependencia"]):
            for phrase in ["instalar paquete ", "install package ", "instalar dependencia "]:
                if phrase in input_lower:
                    idx = input_lower.index(phrase) + len(phrase)
                    pkg = user_input[idx:].strip()
                    if "pip" in input_lower:
                        success, output = packages.pip_install(pkg)
                    elif "npm" in input_lower:
                        success, output = packages.npm_install(pkg)
                    else:
                        success, output = packages.pip_install(pkg)
                    return output
            return "[INFO] Especifica el gestor (pip/npm) y el paquete"
        
        if any(word in input_lower for word in ["lista de paquetes", "paquetes instalados", "list packages"]):
            if "npm" in input_lower:
                success, output = packages.npm_list()
            elif "pip" in input_lower:
                success, output = packages.pip_list()
            else:
                success, output = packages.pip_list()
            return str(output) if success else output
        
        if any(word in input_lower for word in ["actualizar paquete", "upgrade package"]):
            for phrase in ["actualizar paquete ", "upgrade package "]:
                if phrase in input_lower:
                    idx = input_lower.index(phrase) + len(phrase)
                    pkg = user_input[idx:].strip()
                    if "pip" in input_lower:
                        success, output = packages.pip_upgrade(pkg)
                    else:
                        success, output = packages.pip_upgrade(pkg)
                    return output
        
        if any(word in input_lower for word in ["crear requirements", "generar requirements", "genera requirements"]):
            success, output = packages.pip_create_requirements()
            return output
        
        if any(word in input_lower for word in ["instalar requirements", "install requirements"]):
            success, output = packages.pip_install_requirements()
            return output
        
        # === WEB ===
        if any(word in input_lower for word in ["abrir url", "open url", "fetch", "obtener pagina"]):
            for phrase in ["abrir url ", "open url ", "fetch ", "obtener pagina "]:
                if phrase in input_lower:
                    idx = input_lower.index(phrase) + len(phrase)
                    url = user_input[idx:].strip()
                    success, output = web.get(url)
                    return str(output)
        
        if any(word in input_lower for word in ["scrape", "raspar", "extraer texto"]):
            for phrase in ["scrape ", "raspar ", "extraer texto de "]:
                if phrase in input_lower:
                    idx = input_lower.index(phrase) + len(phrase)
                    url = user_input[idx:].strip()
                    success, output = web.scrape_html(url)
                    return output
        
        if any(word in input_lower for word in ["testear api", "test api", "probar endpoint"]):
            for phrase in ["testear api ", "test api ", "probar endpoint "]:
                if phrase in input_lower:
                    idx = input_lower.index(phrase) + len(phrase)
                    url = user_input[idx:].strip()
                    success, output = web.test_api(url)
                    return str(output)
        
        # === ENCRIPTACION ===
        if any(word in input_lower for word in ["cifrar", "encrypt", "encriptar"]):
            for phrase in ["cifrar ", "encrypt ", "encriptar "]:
                if phrase in input_lower:
                    idx = input_lower.index(phrase) + len(phrase)
                    file_path = user_input[idx:].strip()
                    key = "iam_default_key"
                    success, output = encryption.encrypt_file_xor(file_path, file_path + ".enc", key)
                    return output
        
        if any(word in input_lower for word in ["descifrar", "decrypt", "desencriptar"]):
            for phrase in ["descifrar ", "decrypt ", "desencriptar "]:
                if phrase in input_lower:
                    idx = input_lower.index(phrase) + len(phrase)
                    file_path = user_input[idx:].strip()
                    key = "iam_default_key"
                    success, output = encryption.decrypt_file_xor(file_path, file_path + ".dec", key)
                    return output
        
        if any(word in input_lower for word in ["hash", "checksum", "md5", "sha256"]):
            for phrase in ["hash ", "checksum ", "md5 ", "sha256 "]:
                if phrase in input_lower:
                    idx = input_lower.index(phrase) + len(phrase)
                    file_path = user_input[idx:].strip()
                    if "md5" in input_lower:
                        success, output = encryption.hash_file(file_path, "md5")
                    else:
                        success, output = encryption.hash_file(file_path, "sha256")
                    return f"Hash: {output}" if success else output
        
        if any(word in input_lower for word in ["generar clave", "generate key", "generar password"]):
            if "password" in input_lower:
                password = encryption.generate_password()
                return f"Password generada: {password}"
            else:
                key = encryption.generate_key()
                return f"Clave generada: {key}"
        
        # === MONITOREO ===
        if any(word in input_lower for word in ["monitoreo", "monitor", "dashboard", "panel"]):
            success, output = monitor.get_system_dashboard()
            if success and output:
                if isinstance(output, dict):
                    lines = []
                    for k, v in output.items():
                        if v is not None:
                            lines.append(f"{k}: {v}")
                    return "\n".join(lines[:5]) if lines else str(output)[:100]
                return str(output)[:100]
            return f"Dashboard: {output}"
        
        if any(word in input_lower for word in ["uptime", "tiempo encendido", "desde cuando esta"]):
            success, output = monitor.get_system_uptime()
            if success:
                return f"Uptime: {output}"
            return f"Uptime: {output}"
        
        # === FIREWALL ===
        if any(word in input_lower for word in ["firewall"]):
            if any(word in input_lower for word in ["estado", "status", "esta activo"]):
                success, output = security.get_firewall_status()
                if success and output:
                    lines = []
                    for line in str(output).split('\n'):
                        parts = line.split()
                        if len(parts) >= 2 and parts[1] in ['True', 'False']:
                            profile = parts[0]
                            enabled = "activo" if parts[1] == 'True' else "inactivo"
                            lines.append(f"{profile}: {enabled}")
                    return "\n".join(lines) if lines else f"Firewall: {str(output)[:100]}"
                return f"Firewall: {output}"
            if any(word in input_lower for word in ["activar", "enable", "habilitar"]):
                success, output = security.enable_firewall()
                return f"Firewall: {output}"
            if any(word in input_lower for word in ["desactivar", "disable", "deshabilitar"]):
                success, output = security.disable_firewall()
                return f"Firewall: {output}"
            success, output = security.get_firewall_status()
            return f"Firewall: {str(output)[:100]}"
        
        # === USUARIOS ===
        if any(word in input_lower for word in ["usuarios", "que usuarios hay", "lista de usuarios"]):
            success, output = security.list_users()
            if success and output:
                lines = []
                for line in str(output).split('\n'):
                    parts = line.split()
                    if len(parts) >= 2 and parts[0] not in ['Name', '----']:
                        name = parts[0]
                        enabled = parts[1] if len(parts) > 1 else '?'
                        lines.append(f"{name}: {'activo' if enabled == 'True' else 'inactivo'}")
                return "\n".join(lines[:5]) if lines else f"Usuarios: {str(output)[:100]}"
            return f"Usuarios: {output}"
        
        if any(word in input_lower for word in ["crea usuario", "crear usuario", "nuevo usuario"]):
            for phrase in ["crea usuario ", "crear usuario ", "nuevo usuario "]:
                if phrase in input_lower:
                    idx = input_lower.index(phrase) + len(phrase)
                    parts = user_input[idx:].strip().split()
                    if len(parts) >= 2:
                        username = parts[0]
                        password = parts[1]
                        success, output = security.create_user(username, password)
                        return f"Crear usuario: {output}"
        
        # === LOGS ===
        if any(word in input_lower for word in ["logs", "eventos", "bitacora", "historial"]):
            if any(word in input_lower for word in ["seguridad", "security"]):
                success, output = security.get_security_logs()
                if success and output:
                    return f"Logs seguridad: {len(output) if isinstance(output, list) else str(output)[:100]}"
            if any(word in input_lower for word in ["sistema", "system"]):
                success, output = security.get_system_logs()
                if success and output:
                    return f"Logs sistema: {len(output) if isinstance(output, list) else str(output)[:100]}"
            success, output = security.get_application_logs()
            if success and output:
                return f"Logs aplicacion: {len(output) if isinstance(output, list) else str(output)[:100]}"
            return "No se encontraron logs"
        
        # === TAREAS PROGRAMADAS ===
        if any(word in input_lower for word in ["tareas programadas", "scheduled tasks", "cron"]):
            success, output = scheduler.list_tasks()
            if success and output:
                return f"Tareas: {len(output) if isinstance(output, list) else str(output)[:100]}"
            return "No hay tareas programadas"
        
        # === REGISTRO ===
        if any(word in input_lower for word in ["registro", "registry", "reg "]):
            if any(word in input_lower for word in ["buscar", "search"]):
                for phrase in ["buscar ", "search ", "busca en el registro "]:
                    if phrase in input_lower:
                        idx = input_lower.index(phrase) + len(phrase)
                        term = user_input[idx:].strip()
                        success, output = registry.search(term)
                        if success and output:
                            return f"Registro '{term}': {len(output) if isinstance(output, list) else str(output)[:100]}"
                        return f"Registro '{term}': {output}"
            success, output = registry.get_common_paths()
            if success and output:
                return f"Registro: {len(output) if isinstance(output, dict) else str(output)[:100]}"
            return f"Registro: {output}"
        
        # === AUTOMATIZACION ===
        if any(word in input_lower for word in ["escribe ", "escribir ", "type "]):
            for phrase in ["escribe ", "escribir ", "type "]:
                if phrase in input_lower:
                    idx = input_lower.index(phrase) + len(phrase)
                    text = user_input[idx:].strip()
                    success, output = automation.type_text(text)
                    return output
        
        if any(word in input_lower for word in ["abre ", "abrir ", "open "]):
            for phrase in ["abre ", "abrir ", "open "]:
                if phrase in input_lower:
                    idx = input_lower.index(phrase) + len(phrase)
                    target = user_input[idx:].strip()
                    
                    # PEDIR PERMISO antes de abrir
                    permission_granted, permission_msg = require_permission(
                        PermissionAction.EXECUTE_COMMAND,
                        target,
                        f"Abrir: {target}",
                        "low"
                    )
                    
                    if not permission_granted:
                        return f"[DENEGADO] No se abrio: {permission_msg}"
                    
                    if target.startswith("http"):
                        success, output = automation.open_url(target)
                    elif "." in target:
                        success, output = automation.open_file(target)
                    else:
                        success, output = automation.open_app(target)
                    return output
        
        if any(word in input_lower for word in ["click", "haz click"]):
            success, output = automation.click_mouse()
            return output
        
        if any(word in input_lower for word in ["clipboard", "portapapeles"]):
            success, output = automation.get_clipboard()
            if success:
                return f"Portapapeles: {str(output)[:200]}"
            return str(output)
        
        # === CLIPBOARD - COPIAR/PEGAR ===
        if any(word in input_lower for word in ["copia al portapapeles", "copiar al clipboard", "copiar texto"]):
            for phrase in ["copia al portapapeles ", "copiar al clipboard ", "copiar texto "]:
                if phrase in input_lower:
                    idx = input_lower.index(phrase) + len(phrase)
                    text = user_input[idx:].strip()
                    success, output = automation.set_clipboard(text)
                    return f"Copiado: {text[:50]}" if success else str(output)
        
        if any(word in input_lower for word in ["pega", "pegar", "paste"]):
            success, output = automation.get_clipboard()
            if success:
                return f"Portapapeles: {str(output)[:200]}"
            return str(output)
        
        # === CALCULADORA/MATEMATICAS ===
        if any(word in input_lower for word in ["calcula", "cuanto es", "cuanto da", "suma", "resta", "multiplica", "divide"]):
            import re
            # Extraer numeros de la entrada
            numbers = re.findall(r'[\d]+\.?[\d]*', user_input)
            if len(numbers) >= 2:
                n1 = float(numbers[0])
                n2 = float(numbers[1])
                if "suma" in input_lower or "+" in user_input:
                    return f"{n1} + {n2} = {n1 + n2}"
                elif "resta" in input_lower or "-" in user_input:
                    return f"{n1} - {n2} = {n1 - n2}"
                elif "multiplica" in input_lower or "x" in input_lower or "*" in user_input:
                    return f"{n1} x {n2} = {n1 * n2}"
                elif "divide" in input_lower or "/" in user_input:
                    if n2 != 0:
                        return f"{n1} / {n2} = {n1 / n2}"
                    return "No se puede dividir por cero"
            # Intentar evaluar expresion completa
            expr = user_input
            for word in ["calcula", "cuanto es", "cuanto da", "suma", "resta", "multiplica", "divide"]:
                expr = expr.replace(word, "")
            expr = expr.strip()
            try:
                result = eval(expr)
                return f"{expr} = {result}"
            except:
                return "No pude calcular. Ejemplo: 'calcula 5 + 3'"
        
        # === TEMPORIZADOR ===
        if any(word in input_lower for word in ["temporizador", "timer", "alarma", "avísame en", "avísame en"]):
            import re
            import time as time_mod
            numbers = re.findall(r'(\d+)', user_input)
            if numbers:
                seconds = int(numbers[0])
                if "minuto" in input_lower:
                    seconds *= 60
                elif "hora" in input_lower:
                    seconds *= 3600
                # Iniciar temporizador en background
                def timer_callback():
                    time_mod.sleep(seconds)
                    try:
                        import winsound
                        winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
                    except:
                        pass
                import threading
                threading.Thread(target=timer_callback, daemon=True).start()
                mins = seconds // 60
                secs = seconds % 60
                if mins > 0:
                    return f"Temporizador: {mins}m {secs}s"
                return f"Temporizador: {secs}s"
        
        # === VOLUMEN ===
        if any(word in input_lower for word in ["volumen", "subir volumen", "bajar volumen", "silenciar", "mute"]):
            if "subir" in input_lower:
                success, output = automation.press_key("volume_up")
                return "Volumen subido"
            elif "bajar" in input_lower:
                success, output = automation.press_key("volume_down")
                return "Volumen bajado"
            elif "silenciar" in input_lower or "mute" in input_lower:
                success, output = automation.press_key("volume_mute")
                return "Silenciado"
            return "Volumen: subir/bajar/silenciar"
        
        # === SCREENSHOT ===
        if any(word in input_lower for word in ["captura", "screenshot", "toma una captura", "captura de pantalla"]):
            result = self.screen_monitor.capture_now()
            if result:
                return f"Captura: {result.get('path', 'guardada')}"
            return "No pude tomar la captura (mss no instalado)"
        
        # === SERVICIOS ===
        if any(word in input_lower for word in ["servicio", "service", "iniciar servicio", "detener servicio"]):
            for phrase in ["iniciar servicio ", "inicia servicio ", "start service ", "detener servicio ", "deten servicio ", "stop service "]:
                if phrase in input_lower:
                    idx = input_lower.index(phrase) + len(phrase)
                    service_name = user_input[idx:].strip()
                    if any(w in phrase for w in ["iniciar", "inicia", "start"]):
                        success, output = system_info.start_service(service_name)
                    else:
                        success, output = system_info.stop_service(service_name)
                    return f"Servicio '{service_name}': {output}"
            # Listar servicios
            success, output = system_info.list_services()
            if success and isinstance(output, list):
                return f"Servicios: {len(output)} encontrados"
            return f"Servicios: {str(output)[:100]}"
        
        # === TAREAS PROGRAMADAS ===
        if any(word in input_lower for word in ["tarea programada", "scheduled task", "crear tarea"]):
            if "crear" in input_lower:
                for phrase in ["crear tarea ", "crear tarea programada "]:
                    if phrase in input_lower:
                        idx = input_lower.index(phrase) + len(phrase)
                        task_name = user_input[idx:].strip()
                        # Ejemplo basico: crear tarea con el nombre
                        success, output = scheduler.create_task(task_name, "echo Tarea ejecutada")
                        return f"Tarea '{task_name}': {output}"
            success, output = scheduler.list_tasks()
            if success and output:
                return f"Tareas: {len(output) if isinstance(output, list) else str(output)[:100]}"
            return f"Tareas: {output}"
        
        # === COMPRIMIR/DESCOMPRIMIR ===
        # Descomprimir primero para evitar conflictos con "comprimir"
        if any(word in input_lower for word in ["descomprimir", "unzip", "extraer"]):
            for phrase in ["descomprimir ", "unzip ", "extraer "]:
                if phrase in input_lower:
                    idx = input_lower.index(phrase) + len(phrase)
                    path = user_input[idx:].strip()
                    import os
                    output_path = os.path.splitext(path)[0]
                    success, output = filesystem.decompress_zip(path, output_path)
                    return f"Descomprimir: {output}"
        
        if any(word in input_lower for word in ["comprimir", "zip", "archivar", "comprime"]):
            for phrase in ["comprimir ", "zip ", "archivar ", "comprime "]:
                if phrase in input_lower:
                    idx = input_lower.index(phrase) + len(phrase)
                    path = user_input[idx:].strip()
                    import os
                    output_path = path + ".zip"
                    success, output = filesystem.compress_zip(path, output_path)
                    return f"Comprimir: {output}"
        
        # === BUSCAR ARCHIVOS POR CONTENIDO ===
        if any(word in input_lower for word in ["busca en archivos", "search in files", "grep", "buscar contenido"]):
            for phrase in ["busca en archivos ", "search in files ", "grep ", "buscar contenido "]:
                if phrase in input_lower:
                    idx = input_lower.index(phrase) + len(phrase)
                    text = user_input[idx:].strip()
                    success, output = filesystem.search_in_files(text)
                    if success and isinstance(output, list):
                        return f"Resultados '{text}': {len(output)} encontrados"
                    return f"Busqueda '{text}': {str(output)[:100]}"
        
        # === VELOCIDAD DE RED ===
        if any(word in input_lower for word in ["velocidad de internet", "speed test", "velocidad de red", "que velocidad tengo"]):
            success, output = network.speed_test()
            if success and isinstance(output, dict):
                return f"Velocidad: {output.get('result', str(output)[:100])}"
            return f"Velocidad: {str(output)[:100]}"
        
        # === BLUETOOTH ===
        if any(word in input_lower for word in ["bluetooth", "activar bluetooth", "desactivar bluetooth"]):
            return "Bluetooth: funcionalidad no disponible"
        
        # === PROCESO POR NOMBRE ===
        if any(word in input_lower for word in ["mata el proceso", "matar proceso", "kill process", "terminar proceso"]):
            for phrase in ["mata el proceso ", "matar proceso ", "kill process ", "terminar proceso "]:
                if phrase in input_lower:
                    idx = input_lower.index(phrase) + len(phrase)
                    target = user_input[idx:].strip()
                    if target.isdigit():
                        success, output = process_manager.kill_process(pid=int(target))
                    else:
                        success, output = process_manager.kill_process(name=target)
                    return f"Proceso '{target}': {output}"
        
        # === ABRIR APLICACION/ARCHIVO ===
        if any(word in input_lower for word in ["inicia", "lanza", "start", "launch"]):
            for phrase in ["inicia ", "lanza ", "start ", "launch "]:
                if phrase in input_lower:
                    idx = input_lower.index(phrase) + len(phrase)
                    target = user_input[idx:].strip()
                    success, output = automation.open_app(target)
                    return output
        
        return None
    
    def _detect_followup(self, user_input: str) -> str:
        """Detectar preguntas de seguimiento basadas en contexto"""
        input_lower = user_input.lower()
        
        # Seguimiento de IP
        if self.last_topic == "ip":
            if any(w in input_lower for w in ["publica", "public", "externa"]):
                success, output = network.get_ip_info()
                if success and isinstance(output, dict):
                    return f"IP Publica: {output.get('public_ip', 'N/A')}"
            if any(w in input_lower for w in ["privada", "private", "local", "interna"]):
                success, output = network.get_ip_info()
                if success and isinstance(output, dict):
                    return f"IP Privada: {output.get('local_ip', 'N/A')}"
            if any(w in input_lower for w in ["mac", "fisica", "direccion mac"]):
                success, output = hardware.get_network_adapters()
                if success:
                    return str(output)
        
        return None
    
    def _detect_update_action(self, user_input: str) -> str:
        """Detectar peticiones de actualizacion de archivos y escribir el codigo generado"""
        import os
        import re
        input_lower = user_input.lower()
        
        # Patrones que indican actualizacion/modificacion de un archivo
        update_patterns = [
            "actualiza", "modifica", "cambia", "actualizar", "modificar", "cambiar",
            "hasle", "agregale", "ponle", "metele", "dale", "mejora",
            "reescribe", "reemplaza", "sobreescribe"
        ]
        
        if not any(p in input_lower for p in update_patterns):
            return None
        
        # Buscar archivo target
        target_file = None
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        
        # 1. Buscar archivo mencionado explicitamente
        for name in ["calculadora.py", "app.py", "juego.py", "notas.py", "pomodoro.py", "reloj.py"]:
            if name.replace(".py", "") in input_lower or name in input_lower:
                # Buscar en desktop y subcarpetas
                for root, dirs, files in os.walk(desktop):
                    if name in files:
                        target_file = os.path.join(root, name)
                        break
                if target_file:
                    break
        
        # 2. Si no encontro, buscar en la ultima carpeta
        if not target_file and self.last_folder and os.path.isdir(self.last_folder):
            # Buscar archivos python en la carpeta
            for f in os.listdir(self.last_folder):
                if f.endswith('.py'):
                    target_file = os.path.join(self.last_folder, f)
                    break
            if not target_file:
                # Buscar subcarpetas
                for d in os.listdir(self.last_folder):
                    sub = os.path.join(self.last_folder, d)
                    if os.path.isdir(sub):
                        for f in os.listdir(sub):
                            if f.endswith('.py'):
                                target_file = os.path.join(sub, f)
                                break
                    if target_file:
                        break
        
        if not target_file:
            return None
        
        # Preguntar a la IA que genere el nuevo contenido
        # Preparar el prompt para que genere SOLO el codigo
        update_prompt = f"""El usuario quiere actualizar/modificar un archivo existente.

Archivo actual: {target_file}
Peticion del usuario: {user_input}

Genera el CODIGO COMPLETO actualizado para el archivo. Incluye TODO el codigo, no solo partes.
Responde SOLO con el codigo, sin explicaciones, sin bloques markdown, sin ```.
El codigo debe ser funcional y completo."""

        # Obtener respuesta del AI
        ai_response = self.agent.chat(update_prompt)
        
        if not ai_response:
            return "No pude generar el codigo actualizado."
        
        # Limpiar la respuesta: quitar bloques markdown si los hay
        clean_code = ai_response
        # Quitar ```python y ```
        clean_code = re.sub(r'```python\s*\n?', '', clean_code)
        clean_code = re.sub(r'```\s*$', '', clean_code, flags=re.MULTILINE)
        clean_code = clean_code.strip()
        
        # Si la respuesta tiene texto antes/despues del codigo, intentar extraer solo el codigo
        if 'import' in clean_code or 'def ' in clean_code or 'class ' in clean_code:
            # Parece codigo, usarlo
            pass
        else:
            # No parece codigo, usar la respuesta completa
            clean_code = ai_response
        
        # Escribir el archivo
        success, msg = filesystem.create_file(target_file, clean_code)
        
        if success:
            return f"ARCHIVO ACTUALIZADO: {os.path.basename(target_file)}\nUBICACION: {target_file}"
        else:
            return f"Error al actualizar: {msg}"
    
    def _handle_command(self, command: str) -> str:
        """Manejar comandos especiales"""
        parts = command.split()
        cmd = parts[0].lower() if parts else ""
        args = parts[1:] if len(parts) > 1 else []
        
        commands_map = {
            "/help": self._cmd_help,
            "/status": self._cmd_status,
            "/mode": self._cmd_mode,
            "/engine": self._cmd_engine,
            "/clear": self._cmd_clear,
            "/sessions": self._cmd_sessions,
            "/new": self._cmd_new_session,
            "/switch": self._cmd_switch_session,
            "/model": self._cmd_model,
            "/think": self._cmd_thinking,
            "/level": self._cmd_level,
            "/memory": self._cmd_memory,
            "/recall": self._cmd_recall,
            "/forget": self._cmd_forget,
            "/jw": self._cmd_jw,
            # Permisos
            "/permissions": self._cmd_permissions,
            "/perm": self._cmd_permissions,
            "/clear-perms": self._cmd_clear_permissions,
            # Filesystem
            "/mkdir": self._cmd_mkdir,
            "/touch": self._cmd_touch,
            "/ls": self._cmd_ls,
            "/cat": self._cmd_cat,
            "/run": self._cmd_run,
            "/py": self._cmd_py,
            "/edit": self._cmd_edit,
            "/rm": self._cmd_rm,
            "/mv": self._cmd_mv,
            "/cp": self._cmd_cp,
            "/find": self._cmd_find,
            "/grep": self._cmd_grep,
            "/disk": self._cmd_disk,
            "/info": self._cmd_info,
            "/tree": self._cmd_tree,
            "/hash": self._cmd_hash,
            "/diff": self._cmd_diff,
            "/zip": self._cmd_zip,
            "/unzip": self._cmd_unzip,
            "/lines": self._cmd_lines,
            # System
            "/proc": self._cmd_processes,
            "/kill": self._cmd_kill,
            "/net": self._cmd_network,
            "/ping": self._cmd_ping,
            "/ports": self._cmd_ports,
            "/clip": self._cmd_clipboard,
            "/clipset": self._cmd_clipboard_set,
            "/drives": self._cmd_drives,
            "/cpu": self._cmd_cpu,
            "/mem": self._cmd_memory_info,
            "/services": self._cmd_services,
            "/screenshot": self._cmd_screenshot,
            "/programs": self._cmd_programs,
            # Code
            "/analyze": self._cmd_analyze,
            "/format": self._cmd_format,
            "/lang": self._cmd_detect_lang,
            # Network
            "/ip": self._cmd_ip,
            "/dns": self._cmd_dns,
            "/traceroute": self._cmd_traceroute,
            "/scan": self._cmd_scan,
            "/wifi": self._cmd_wifi,
            "/conexiones": self._cmd_connections,
            "/arp": self._cmd_arp,
            "/rutas": self._cmd_routes,
            # Hardware
            "/hardware": self._cmd_hardware,
            "/gpu": self._cmd_gpu,
            "/disco": self._cmd_disk,
            "/bateria": self._cmd_battery,
            "/temp": self._cmd_temp,
            "/usb": self._cmd_usb,
            "/motherboard": self._cmd_motherboard,
            # Security
            "/firewall": self._cmd_firewall,
            "/firewall-on": self._cmd_firewall_on,
            "/firewall-off": self._cmd_firewall_off,
            "/usuarios": self._cmd_users,
            "/crear-user": self._cmd_create_user,
            "/logs": self._cmd_logs,
            "/logs-seguridad": self._cmd_security_logs,
            # Tasks
            "/tareas": self._cmd_scheduled_tasks,
            # Registry
            "/registro": self._cmd_registry,
            "/buscar-registro": self._cmd_registry_search,
            # Project
            "/project": self._cmd_project,
        }
        
        if cmd in commands_map:
            # Animación de carga para comandos
            loader = LoadingIndicator()
            loader.start(f"[cfg] Ejecutando {cmd}", "line")
            try:
                result = commands_map[cmd](args)
            finally:
                loader.stop()
            return result
        
        return f"[X] Comando desconocido: {cmd}\nEscribe /help para ver comandos disponibles"
    
    # === COMANDOS DE AYUDA ===
    
    def _cmd_help(self, args: List[str]) -> str:
        """Mostrar ayuda completa"""
        return f"""
  === COMANDOS - IAM v{settings.VERSION} ===

  MODOS: general, builder, plan, frontend, backend, debug, security

  --- IA ---
  /help           Mostrar ayuda
  /status         Estado del sistema
  /mode [modo]    Cambiar modo
  /engine [e]     Cambiar motor (iam)
  /model [name]   Cambiar modelo
  /think          Activar/desactivar pensamiento
  /level [nivel]  Nivel (basico/analitico/profundo/experto)

  --- MEMORIA ---
  /memory         Ver memoria a largo plazo
  /recall [texto] Buscar en memoria
  /forget [id]    Eliminar entrada de memoria

  --- SESION ---
  /sessions       Listar sesiones
  /new [name]     Nueva sesion
  /switch [id]    Cambiar sesion
  /clear          Limpiar pantalla

  --- ARCHIVOS ---
  /mkdir [ruta]           Crear carpeta
  /touch [ruta] [text]    Crear archivo
  /ls [ruta]              Listar directorio
  /cat [archivo]          Leer archivo
  /edit [arch] [old] [new] Editar archivo
  /rm [ruta]              Eliminar
  /mv [orig] [dest]       Mover
  /cp [orig] [dest]       Copiar
  /find [patron]          Buscar archivos
  /grep [texto]           Buscar texto
  /disk                   Ver disco
  /info [archivo]         Info de archivo
  /tree [ruta]            Arbol de carpetas
  /hash [archivo]         Hash MD5
  /diff [arch1] [arch2]   Comparar archivos
  /zip [orig] [dest]      Comprimir ZIP
  /unzip [arch] [dest]    Descomprimir ZIP
  /lines [archivo]        Contar lineas

  --- SISTEMA ---
  /proc                   Listar procesos
  /kill [pid]             Matar proceso
  /net                    Info de red
  /ping [host]            Ping a host
  /ports                  Puertos abiertos
  /clip                   Ver clipboard
  /clipset [texto]        Copiar al clipboard
  /drives                 Unidades de disco
  /cpu                    Info del CPU
  /mem                    Info de memoria
  /services               Servicios activos
  /screenshot             Tomar screenshot
  /programs               Programas instalados

  --- CODIGO ---
  /analyze [archivo]      Analizar codigo
  /format [archivo]       Formatear codigo
  /lang [archivo]         Detectar lenguaje
  /run [comando]          Ejecutar comando
  /py [codigo]            Ejecutar Python

  --- JW ---
  /jw [query]             Buscar en JW.org

  --- PROYECTO ---
  /project                Abrir selector de carpeta
  /project [ruta]         Establecer por ruta
  /project clear          Desactivar proyecto
  /project info           Ver proyecto activo
"""
    
    def _cmd_status(self, args: List[str]) -> str:
        """Ver estado detallado"""
        status = self.agent.get_status()
        mode_info = AGENT_PROMPTS.get(status["mode"], AGENT_PROMPTS["general"])
        
        return f"""
  === ESTADO DEL SISTEMA ===

  Modo:        {mode_info['icon']} {mode_info['name']}
  Motor:       {status['engine'].upper()}
  Modelo:      {status['model']}
  Sesion:      {status['session'] or 'Ninguna'}
  Mensajes:    {status['messages']}
  Pensamiento: {'ON' if status['show_thinking'] else 'OFF'}
  Nivel:       {status['thinking_level'].upper()}

  APIs:
    IAM:        {'[OK]' if settings.API_KEY else '[X]'}
"""
    
    def _cmd_mode(self, args: List[str]) -> str:
        """Cambiar modo"""
        if not args:
            return f"Modos: {', '.join(AGENT_PROMPTS.keys())}"
        
        mode = args[0]
        if self.agent.set_mode(mode):
            agent_info = AGENT_PROMPTS[mode]
            return f"[OK] Modo: {agent_info['icon']} {agent_info['name']}"
        return f"[X] Modo invalido: {mode}"
    
    def _cmd_engine(self, args: List[str]) -> str:
        """Cambiar motor"""
        if not args:
            return f"Motores: {', '.join(settings.AVAILABLE_ENGINES)}"
        
        engine = args[0]
        if self.agent.set_engine(engine):
            return f"[OK] Motor: {engine.upper()}"
        return f"[X] Motor invalido: {engine}"
    
    def _cmd_model(self, args: List[str]) -> str:
        """Cambiar modelo"""
        if not args:
            return f"Modelo actual: {settings.MODELS.get(self.agent.current_mode)}"
        
        model = args[0]
        settings.MODELS[self.agent.current_mode] = model
        return f"[OK] Modelo: {model}"
    
    def _cmd_thinking(self, args: List[str]) -> str:
        """Activar/desactivar pensamiento"""
        is_on = self.agent.toggle_thinking()
        return f"[OK] Pensamiento: {'ACTIVADO' if is_on else 'DESACTIVADO'}"
    
    def _cmd_level(self, args: List[str]) -> str:
        """Cambiar nivel de pensamiento"""
        if not args:
            return f"Niveles: basico, analitico, profundo, experto"
        
        level = args[0]
        if self.agent.set_thinking_level(level):
            return f"[OK] Nivel: {level.upper()}"
        return f"[X] Nivel invalido: {level}"
    
    def _cmd_memory(self, args: List[str]) -> str:
        """Ver memoria a largo plazo"""
        if not self.agent.memory:
            return "Memoria no inicializada."
        
        # Obtener estadísticas
        stats = self.agent.memory.get_stats()
        
        output = [f"\n  === MEMORIA A LARGO PLAZO ==="]
        output.append(f"  Total entradas: {stats['total_entries']}")
        output.append(f"  Importancia promedio: {stats['avg_importance']:.2f}")
        
        if stats['categories']:
            output.append(f"\n  Categorias:")
            for cat, count in stats['categories'].items():
                output.append(f"    - {cat}: {count}")
        
        # Mostrar memorias recientes
        recent = self.agent.memory.get_recent(limit=5)
        if recent:
            output.append(f"\n  === MEMORIAS RECIENTES ===\n")
            for entry in recent:
                output.append(f"  [{entry.category.upper()}] {entry.content[:80]}...")
                output.append(f"    Tags: {', '.join(entry.tags[:3])}")
                output.append(f"    Importancia: {'#' * int(entry.importance * 10)}")
                output.append("")
        
        # Si hay argumentos, buscar memoria relevante
        if args:
            query = " ".join(args)
            memories = self.agent.memory.recall(query, limit=3)
            if memories:
                output.append(f"\n  === MEMORIAS RELACIONADAS CON: {query} ===\n")
                for entry in memories:
                    output.append(f"  [{entry.category.upper()}] {entry.content[:100]}...")
                    output.append("")
            else:
                output.append(f"\n  No se encontraron memorias para: {query}")
        
        return "\n".join(output)
    
    def _cmd_recall(self, args: List[str]) -> str:
        """Buscar en memoria a largo plazo"""
        if not self.agent.memory:
            return "Memoria no inicializada."
        
        if not args:
            return "Uso: /recall [texto a buscar]"
        
        query = " ".join(args)
        memories = self.agent.memory.recall(query, limit=5)
        
        if not memories:
            return f"No se encontraron memorias para: {query}"
        
        output = [f"\n  === MEMORIAS RELACIONADAS: {query} ===\n"]
        
        for entry in memories:
            output.append(f"  [{entry.category.upper()}] {entry.content[:120]}...")
            output.append(f"    Tags: {', '.join(entry.tags[:5])}")
            output.append(f"    Importancia: {'#' * int(entry.importance * 10)} ({entry.importance:.1f})")
            output.append(f"    Accesos: {entry.access_count} | Creado: {entry.created_at[:10]}")
            output.append("")
        
        return "\n".join(output)
    
    def _cmd_forget(self, args: List[str]) -> str:
        """Eliminar entrada de memoria"""
        if not self.agent.memory:
            return "Memoria no inicializada."
        
        if not args:
            return "Uso: /forget [id]"
        
        entry_id = args[0]
        if self.agent.memory.delete(entry_id):
            return f"[OK] Memoria {entry_id} eliminada."
        else:
            return f"No se encontro memoria con ID: {entry_id}"
    
    def _cmd_clear(self, args: List[str]) -> str:
        """Limpiar pantalla"""
        import os
        os.system('cls' if os.name == 'nt' else 'clear')
        return ""
    
    def _cmd_sessions(self, args: List[str]) -> str:
        """Listar sesiones"""
        sessions = self.agent.session_manager.list_sessions()
        
        if not sessions:
            return "No hay sesiones. Usa /new."
        
        output = ["\n  === SESIONES ===\n"]
        
        for s in sessions:
            active = "*" if s["active"] else " "
            output.append(f"  {active} {s['id']}")
            output.append(f"    Nombre: {s['name']}")
            output.append(f"    Mensajes: {s['messages']} | Modo: {s['mode']}")
            output.append(f"    Ultimo: {s['updated']}\n")
        
        return "\n".join(output)
    
    def _cmd_new_session(self, args: List[str]) -> str:
        """Nueva sesion"""
        name = " ".join(args) if args else None
        session = self.agent.session_manager.create_session(name=name, mode=self.agent.current_mode)
        return f"[OK] Sesion creada: {session.name} ({session.id})"
    
    def _cmd_switch_session(self, args: List[str]) -> str:
        """Cambiar sesion"""
        if not args:
            return "Uso: /switch [session_id]"
        
        session_id = args[0]
        if self.agent.session_manager.switch_session(session_id):
            return f"[OK] Sesion: {session_id}"
        return f"[X] Sesion no encontrada: {session_id}"
    
    def _cmd_jw(self, args: List[str]) -> str:
        """Buscar en JW.org"""
        if not args:
            return "Uso: /jw [termino]"
        
        query = " ".join(args)
        from ..tools.search import JWSearch
        return JWSearch.search(query)
    
    # === COMANDOS DE ARCHIVOS ===
    
    def _cmd_mkdir(self, args: List[str]) -> str:
        if not args: return "Uso: /mkdir [ruta]"
        success, msg = filesystem.create_folder(args[0])
        return msg
    
    def _cmd_touch(self, args: List[str]) -> str:
        if not args: return "Uso: /touch [ruta] [contenido]"
        content = " ".join(args[1:]) if len(args) > 1 else ""
        success, msg = filesystem.create_file(args[0], content)
        return msg
    
    def _cmd_ls(self, args: List[str]) -> str:
        path = args[0] if args else "."
        show_hidden = "--hidden" in args
        
        success, items = filesystem.list_directory(path, show_hidden)
        if not success:
            return str(items[0])
        
        output = [f"\n  === {path} ===\n"]
        
        for item in items[:50]:
            if 'error' in item:
                return f"[ERROR] {item['error']}"
            icon = "[D] " if item['is_dir'] else "    "
            size = item['size_str'] if not item['is_dir'] else "-"
            output.append(f"  {icon}{item['name']:<35} {size:>10}  {item['modified']}")
        
        if len(items) > 50:
            output.append(f"\n  ... y {len(items) - 50} mas")
        
        output.append(f"\n  Total: {len(items)}")
        return "\n".join(output)
    
    def _cmd_cat(self, args: List[str]) -> str:
        if not args: return "Uso: /cat [archivo]"
        
        path = args[0]
        if len(args) >= 3:
            start, end = int(args[1]), int(args[2])
            success, lines = filesystem.read_file_lines(path, start, end)
            return "\n".join(lines) if success else str(lines[0])
        
        success, content = filesystem.read_file(path)
        if success:
            lines = content.splitlines()
            if len(lines) > 100:
                return "\n".join(lines[:100]) + f"\n\n... ({len(lines)} lineas)"
            return content
        return content
    
    def _cmd_edit(self, args: List[str]) -> str:
        if len(args) < 3: return "Uso: /edit [arch] [old] [new]"
        success, msg = filesystem.edit_file(args[0], args[1], args[2])
        return msg
    
    def _cmd_rm(self, args: List[str]) -> str:
        if not args: return "Uso: /rm [ruta]"
        success, msg = filesystem.delete(args[0])
        return msg
    
    def _cmd_mv(self, args: List[str]) -> str:
        if len(args) < 2: return "Uso: /mv [orig] [dest]"
        success, msg = filesystem.move(args[0], args[1])
        return msg
    
    def _cmd_cp(self, args: List[str]) -> str:
        if len(args) < 2: return "Uso: /cp [orig] [dest]"
        success, msg = filesystem.copy(args[0], args[1])
        return msg
    
    def _cmd_find(self, args: List[str]) -> str:
        if not args: return "Uso: /find [patron] [ruta]"
        
        pattern = args[0]
        path = args[1] if len(args) > 1 else "."
        success, results = filesystem.search_files(pattern, path)
        
        if not success: return str(results[0])
        
        output = [f"\n  === {pattern} ({len(results)} archivos) ===\n"]
        for r in results[:20]:
            output.append(f"  {r}")
        if len(results) > 20:
            output.append(f"\n  ... y {len(results) - 20} mas")
        return "\n".join(output)
    
    def _cmd_grep(self, args: List[str]) -> str:
        if not args: return "Uso: /grep [texto] [ruta] [ext]"
        
        text = args[0]
        path = args[1] if len(args) > 1 else "."
        ext = args[2] if len(args) > 2 else "*"
        
        success, results = filesystem.search_in_files(text, path, ext)
        if not success: return str(results[0])
        
        output = [f"\n  === '{text}' ({len(results)} resultados) ===\n"]
        for r in results[:20]:
            if 'error' in r: return f"[ERROR] {r['error']}"
            output.append(f"  {r['file']}:{r['line']}")
            output.append(f"     {r['content']}\n")
        if len(results) > 20:
            output.append(f"  ... y {len(results) - 20} mas")
        return "\n".join(output)
    
    def _cmd_disk(self, args: List[str]) -> str:
        path = args[0] if args else "."
        success, info = filesystem.get_disk_usage(path)
        if not success: return f"[ERROR] {info.get('error', '?')}"
        return f"\n  [DISCO] Total: {info['total']} | Usado: {info['used']} ({info['percent']}%) | Libre: {info['free']}\n"
    
    def _cmd_info(self, args: List[str]) -> str:
        if not args: return "Uso: /info [archivo]"
        
        success, info = filesystem.get_file_info(args[0])
        if not success: return f"[ERROR] {info.get('error', '?')}"
        
        return f"\n  [INFO] {info['name']}\n  Ruta:       {info['path']}\n  Tipo:       {'Dir' if info['is_dir'] else 'File'}\n  Lenguaje:   {info['language']}\n  Tamano:     {info['size_str']}\n  Lineas:     {info.get('lines', '-')}\n  Creado:     {info['created']}\n  Modificado: {info['modified']}\n  Permisos:   {info['permissions']}\n"
    
    def _cmd_tree(self, args: List[str]) -> str:
        path = args[0] if args else "."
        success, tree = filesystem.get_folder_tree(path)
        if not success: return tree
        return f"\n  === ARBOL: {path} ===\n{tree}\n"
    
    def _cmd_hash(self, args: List[str]) -> str:
        if not args: return "Uso: /hash [archivo]"
        
        algo = args[1] if len(args) > 1 else "md5"
        success, result = filesystem.get_file_hash(args[0], algo)
        if not success: return result
        return f"\n  [HASH] {algo.upper()}: {result}\n"
    
    def _cmd_diff(self, args: List[str]) -> str:
        if len(args) < 2: return "Uso: /diff [arch1] [arch2]"
        
        success, result = filesystem.compare_files(args[0], args[1])
        if not success: return f"[ERROR] {result.get('error', '?')}"
        
        if result['same']:
            return "[OK] Los archivos son identicos"
        
        output = [f"\n  [DIFF] {result['differences']} diferencias"]
        output.append(f"  Archivo 1: {result['total_lines1']} lineas")
        output.append(f"  Archivo 2: {result['total_lines2']} lineas\n")
        
        for d in result['diff_lines'][:10]:
            output.append(f"  Linea {d['line']}:")
            output.append(f"    - {d['file1'] or '(vacio)'}")
            output.append(f"    + {d['file2'] or '(vacio)'}")
        
        return "\n".join(output)
    
    def _cmd_zip(self, args: List[str]) -> str:
        if len(args) < 2: return "Uso: /zip [origen] [dest.zip]"
        success, msg = filesystem.compress_zip(args[0], args[1])
        return msg
    
    def _cmd_unzip(self, args: List[str]) -> str:
        if len(args) < 2: return "Uso: /unzip [arch.zip] [destino]"
        success, msg = filesystem.decompress_zip(args[0], args[1])
        return msg
    
    def _cmd_lines(self, args: List[str]) -> str:
        if not args: return "Uso: /lines [archivo]"
        
        success, counts = code_manager.count_lines(args[0])
        if not success: return f"[ERROR] {counts.get('error', '?')}"
        
        return f"\n  [LINEAS] {args[0]}\n  Total:      {counts['total']}\n  Codigo:     {counts['code']}\n  Comentarios: {counts['comments']}\n  Vacias:     {counts['blank']}\n"
    
    # === COMANDOS DE SISTEMA ===
    
    def _cmd_processes(self, args: List[str]) -> str:
        if args:
            success, procs = system_info.search_process(args[0])
        else:
            success, procs = system_info.list_processes()
        
        if not success: return str(procs[0])
        
        output = [f"\n  === PROCESOS ({len(procs)}) ===\n"]
        for p in procs[:20]:
            if 'error' in p: return f"[ERROR] {p['error']}"
            output.append(f"  {p.get('name', '?'):<30} PID: {p.get('pid', '?')}")
        return "\n".join(output)
    
    def _cmd_kill(self, args: List[str]) -> str:
        if not args: return "Uso: /kill [pid]"
        success, msg = system_info.kill_process(args[0])
        return msg
    
    def _cmd_network(self, args: List[str]) -> str:
        info = system_info.get_network_info()
        return f"\n  [RED] Hostname: {info['hostname']}\n  IP Local:  {info['ip_local']}\n  IP Publica: {info['ip_public']}\n"
    
    def _cmd_ping(self, args: List[str]) -> str:
        if not args: return "Uso: /ping [host]"
        success, output = system_info.ping(args[0])
        return output if success else output
    
    def _cmd_ports(self, args: List[str]) -> str:
        success, ports = system_info.get_open_ports()
        if not success: return str(ports[0])
        
        output = [f"\n  === PUERTOS ABIERTOS ===\n"]
        for p in ports[:20]:
            if 'error' in p: return f"[ERROR] {p['error']}"
            output.append(f"  {p.get('info', '')}")
        return "\n".join(output)
    
    def _cmd_clipboard(self, args: List[str]) -> str:
        success, content = system_info.get_clipboard()
        if not success: return content
        return f"\n  [CLIPBOARD]\n  {content}\n"
    
    def _cmd_clipboard_set(self, args: List[str]) -> str:
        if not args: return "Uso: /clipset [texto]"
        text = " ".join(args)
        success, msg = system_info.set_clipboard(text)
        return msg
    
    def _cmd_drives(self, args: List[str]) -> str:
        success, drives = system_info.list_drives()
        if not success: return str(drives[0])
        
        output = [f"\n  === UNIDADES ===\n"]
        for d in drives:
            if 'error' in d: return f"[ERROR] {d['error']}"
            output.append(f"  {d.get('letter', d.get('device', '?'))} - {d.get('name', '')} - Libre: {d.get('free', '?')}")
        return "\n".join(output)
    
    def _cmd_cpu(self, args: List[str]) -> str:
        info = system_info.get_cpu_info()
        return f"\n  [CPU] Procesador: {info.get('processor', '?')}\n  Cores: {info.get('cores', '?')}\n  Arquitectura: {info.get('architecture', '?')}\n"
    
    def _cmd_memory_info(self, args: List[str]) -> str:
        info = system_info.get_memory_info()
        return f"\n  [MEMORIA] Total: {info.get('total', '?')}\n  Usada: {info.get('used', '?')} ({info.get('percent', 0)}%)\n  Libre: {info.get('free', '?')}\n"
    
    def _cmd_services(self, args: List[str]) -> str:
        success, services = system_info.list_services()
        if not success: return str(services[0])
        
        output = [f"\n  === SERVICIOS ({len(services)}) ===\n"]
        for s in services[:20]:
            output.append(f"  {s.get('name', '?')}")
        return "\n".join(output)
    
    def _cmd_screenshot(self, args: List[str]) -> str:
        path = args[0] if args else None
        success, msg = system_info.take_screenshot(path)
        return msg
    
    def _cmd_programs(self, args: List[str]) -> str:
        success, programs = system_info.get_installed_programs()
        if not success: return str(programs[0])
        
        output = [f"\n  === PROGRAMAS INSTALADOS ({len(programs)}) ===\n"]
        for p in programs[:30]:
            output.append(f"  - {p}")
        if len(programs) > 30:
            output.append(f"\n  ... y {len(programs) - 30} mas")
        return "\n".join(output)
    
    # === COMANDOS DE CODIGO ===
    
    def _cmd_analyze(self, args: List[str]) -> str:
        if not args: return "Uso: /analyze [archivo]"
        
        from ..tools.analyzer import CodeAnalyzer
        analyzer = CodeAnalyzer()
        
        success, content = filesystem.read_file(args[0])
        if not success: return content
        
        lang = code_manager.detect_language(args[0])
        issues = analyzer.analyze(content, lang)
        summary = analyzer.get_summary(issues)
        
        output = [f"\n  === ANALISIS: {args[0]} ==="]
        output.append(f"  Lenguaje: {lang}")
        output.append(f"  Total: {summary['total']} problemas")
        output.append(f"  Errores: {summary['errors']}")
        output.append(f"  Advertencias: {summary['warnings']}\n")
        
        for issue in issues[:10]:
            icon = {"error": "[!]", "warning": "[~]", "info": "[i]"}.get(issue.severity, "[?]")
            output.append(f"  {icon} Linea {issue.line}: {issue.message}")
            if issue.suggestion:
                output.append(f"      -> {issue.suggestion}")
        
        return "\n".join(output)
    
    def _cmd_format(self, args: List[str]) -> str:
        if not args: return "Uso: /format [archivo]"
        
        success, content = filesystem.read_file(args[0])
        if not success: return content
        
        lang = code_manager.detect_language(args[0])
        formatted = code_manager.format_code(content, lang)
        
        filesystem.create_file(args[0], formatted)
        return f"[OK] Codigo formateado: {lang}"
    
    def _cmd_detect_lang(self, args: List[str]) -> str:
        if not args: return "Uso: /lang [archivo]"
        
        lang = code_manager.detect_language(args[0])
        return f"[OK] Lenguaje: {lang}"
    
    def _cmd_run(self, args: List[str]) -> str:
        if not args: return "Uso: /run [comando]"
        
        command = " ".join(args)
        print(f"- Ejecutando: {command}")
        success, output = filesystem.run_command(command)
        return output if success else output
    
    def _cmd_py(self, args: List[str]) -> str:
        if not args: return "Uso: /py [codigo]"
        
        code = " ".join(args)
        print(f"- Ejecutando Python...")
        success, output = filesystem.run_python(code)
        return output
    
    # === COMANDOS DE RED ===
    
    def _cmd_ip(self, args: List[str]) -> str:
        success, output = network.get_ip_info()
        if not success: return str(output)
        lines = []
        if output.get('local_ip'):
            lines.append(f"IP Privada: {output['local_ip']}")
        if output.get('public_ip'):
            lines.append(f"IP Publica: {output['public_ip']}")
        if output.get('hostname'):
            lines.append(f"Hostname: {output['hostname']}")
        return "\n".join(lines) if lines else str(output)
    
    def _cmd_dns(self, args: List[str]) -> str:
        if not args: return "Uso: /dns [dominio]"
        success, output = network.dns_lookup(args[0])
        if not success: return str(output)
        ips = output.get('ips', [])
        return f"DNS: {args[0]} -> {', '.join(ips)}" if ips else str(output)
    
    def _cmd_traceroute(self, args: List[str]) -> str:
        if not args: return "Uso: /traceroute [host]"
        success, output = network.traceroute(args[0])
        return output if success else str(output)
    
    def _cmd_scan(self, args: List[str]) -> str:
        host = args[0] if args else "localhost"
        success, output = network.scan_ports(host, 1, 1024)
        if not success: return str(output)
        if isinstance(output, list):
            open_ports = [str(p.get('port', '')) for p in output]
            return f"Puertos abiertos en {host}: {', '.join(open_ports)}" if open_ports else f"No hay puertos abiertos en {host}"
        return str(output)
    
    def _cmd_wifi(self, args: List[str]) -> str:
        success, output = network.get_wifi_networks()
        return output if success else str(output)
    
    def _cmd_connections(self, args: List[str]) -> str:
        success, output = network.get_connections()
        return output if success else str(output)
    
    def _cmd_arp(self, args: List[str]) -> str:
        success, output = network.get_arp_table()
        return output if success else str(output)
    
    def _cmd_routes(self, args: List[str]) -> str:
        success, output = network.get_routes()
        return output if success else str(output)
    
    # === COMANDOS DE HARDWARE ===
    
    def _cmd_hardware(self, args: List[str]) -> str:
        success, output = hardware.get_full_system_info()
        return str(output)
    
    def _cmd_gpu(self, args: List[str]) -> str:
        success, output = hardware.get_gpu_info()
        return str(output)
    
    def _cmd_disk(self, args: List[str]) -> str:
        success, output = hardware.get_disk_info()
        return str(output)
    
    def _cmd_battery(self, args: List[str]) -> str:
        success, output = hardware.get_battery_info()
        return str(output)
    
    def _cmd_temp(self, args: List[str]) -> str:
        success, output = hardware.get_temperature()
        return str(output)
    
    def _cmd_usb(self, args: List[str]) -> str:
        success, output = hardware.get_usb_devices()
        return str(output)
    
    def _cmd_motherboard(self, args: List[str]) -> str:
        success, output = hardware.get_motherboard_info()
        return str(output)
    
    # === COMANDOS DE SEGURIDAD ===
    
    def _cmd_firewall(self, args: List[str]) -> str:
        success, output = security.get_firewall_status()
        return output if success else str(output)
    
    def _cmd_firewall_on(self, args: List[str]) -> str:
        success, output = security.enable_firewall()
        return output
    
    def _cmd_firewall_off(self, args: List[str]) -> str:
        success, output = security.disable_firewall()
        return output
    
    def _cmd_users(self, args: List[str]) -> str:
        success, output = security.list_users()
        return output if success else str(output)
    
    def _cmd_create_user(self, args: List[str]) -> str:
        if len(args) < 2: return "Uso: /crear-user [usuario] [contraseña]"
        success, output = security.create_user(args[0], args[1])
        return output
    
    def _cmd_logs(self, args: List[str]) -> str:
        success, output = security.get_application_logs()
        return output if success else str(output)
    
    def _cmd_security_logs(self, args: List[str]) -> str:
        success, output = security.get_security_logs()
        return output if success else str(output)
    
    # === COMANDOS DE TAREAS PROGRAMADAS ===
    
    def _cmd_scheduled_tasks(self, args: List[str]) -> str:
        success, output = scheduler.list_tasks()
        return output if success else str(output)
    
    # === COMANDOS DE REGISTRO ===
    
    def _cmd_registry(self, args: List[str]) -> str:
        if not args:
            success, output = registry.get_common_paths()
            return str(output)
        success, output = registry.read_key(args[0])
        return output if success else str(output)
    
    def _cmd_registry_search(self, args: List[str]) -> str:
        if not args: return "Uso: /buscar-registro [termino]"
        success, output = registry.search(args[0])
        return output if success else str(output)
    
    # === COMANDOS DE PERMISOS ===
    
    def _cmd_permissions(self, args: List[str]) -> str:
        """Ver/gestionar permisos guardados"""
        if not args:
            # Mostrar permisos guardados
            return permission_system.format_permissions_list()
        
        action = args[0].lower()
        
        if action == "clear" or action == "limpiar":
            permission_system.clear_all_permissions()
            return "[OK] Todos los permisos han sido eliminados"
        
        elif action == "list" or action == "listar":
            perms = permission_system.get_saved_permissions()
            if not perms:
                return "No hay permisos guardados."
            
            output = ["PERMISOS GUARDADOS:\n"]
            for p in perms:
                icon = "[OK]" if p["level"] == "always_allow" else "[X]"
                output.append(f"  {icon} {p['action']}: {p['pattern']}")
            return "\n".join(output)
        
        elif action == "remove" or action == "eliminar":
            if len(args) < 3:
                return "Uso: /perm remove [accion] [targeto]"
            # TODO: Implementar eliminacion de permiso específico
            return "Funcion no implementada"
        
        return """PERMISOS - Uso:
  /permissions           Ver permisos guardados
  /permissions clear     Limpiar todos los permisos
  /permissions list      Listar permisos"""
    
    def _cmd_clear_permissions(self, args: List[str]) -> str:
        """Limpiar todos los permisos"""
        permission_system.clear_all_permissions()
        return "[OK] Todos los permisos han sido eliminados"

    # === COMANDO DE PROYECTO ACTIVO ===
    
    def _cmd_project(self, args: List[str]) -> str:
        """Establecer o gestionar el proyecto activo"""
        if not args:
            # Abrir navegador de archivos para seleccionar carpeta
            try:
                import tkinter as tk
                from tkinter import filedialog
                root = tk.Tk()
                root.withdraw()
                root.attributes('-topmost', True)
                folder = filedialog.askdirectory(
                    title="Seleccionar carpeta del proyecto",
                    initialdir=os.path.join(os.path.expanduser("~"), "Desktop")
                )
                root.destroy()

                if not folder:
                    # Si ya hay proyecto activo, mostrar info
                    if self.agent.active_project:
                        project = self.agent.active_project
                        try:
                            items = os.listdir(project)
                            files = [f for f in items if os.path.isfile(os.path.join(project, f))]
                            dirs = [d for d in items if os.path.isdir(os.path.join(project, d))]
                            return f"""  === PROYECTO ACTIVO ===

  Ruta:       {project}
  Archivos:   {len(files)}
  Carpetas:   {len(dirs)}
  
  Todos los archivos se crean/editan aqui automaticamente.
  Usa /project clear para desactivar."""
                        except:
                            return f"  Proyecto activo: {project}"
                    return "  Seleccion cancelada."

                # Establecer la carpeta seleccionada
                if self.agent.set_active_project(folder):
                    try:
                        items = os.listdir(folder)
                        files = [f for f in items if os.path.isfile(os.path.join(folder, f))]
                        dirs = [d for d in items if os.path.isdir(os.path.join(folder, d))]
                        return f"""[OK] Proyecto activo: {folder}

  Archivos: {len(files)} | Carpetas: {len(dirs)}
  Ahora todos los archivos se crean/editan aqui."""
                    except:
                        return f"[OK] Proyecto activo: {folder}"
                else:
                    return f"[X] No se pudo establecer: {folder}"

            except ImportError:
                return "[X] tkinter no disponible. Usa: /project [ruta]"
            except Exception as e:
                return f"[X] Error al abrir selector: {e}"
        
        action = args[0].lower()
        
        if action == "clear" or action == "limpiar" or action == "off":
            self.agent.clear_active_project()
            return "[OK] Proyecto activo desactivado. Las operaciones usan la ruta actual."
        
        if action == "info":
            if self.agent.active_project:
                return f"  Proyecto activo: {self.agent.active_project}"
            return "  No hay proyecto activo."
        
        # Establecer ruta del proyecto
        project_path = " ".join(args)
        
        # Resolver la ruta
        if not os.path.isabs(project_path):
            # Buscar en escritorio si es nombre relativo
            desktop = os.path.join(os.path.expanduser("~"), "Desktop")
            candidate = os.path.join(desktop, project_path)
            if os.path.isdir(candidate):
                project_path = candidate
            else:
                # Intentar como ruta relativa al cwd
                candidate = os.path.join(os.getcwd(), project_path)
                if os.path.isdir(candidate):
                    project_path = candidate
                else:
                    return f"[X] No se encontro la carpeta: {project_path}\nIntenta con la ruta completa."
        
        if self.agent.set_active_project(project_path):
            try:
                items = os.listdir(project_path)
                files = [f for f in items if os.path.isfile(os.path.join(project_path, f))]
                dirs = [d for d in items if os.path.isdir(os.path.join(project_path, d))]
                return f"""[OK] Proyecto activo: {project_path}

  Archivos: {len(files)} | Carpetas: {len(dirs)}
  Ahora todos los archivos se crean/editan aqui."""
            except:
                return f"[OK] Proyecto activo: {project_path}"
        else:
            return f"[X] No se pudo establecer: {project_path}"
