# -*- coding: utf-8 -*-
"""
IAM Mode Loader - Carga las skills de cada modo (v4.1 Mejorado)
"""

from typing import Dict, Any

def load_all_skills() -> Dict[str, Dict[str, Any]]:
    """Cargar skills de todos los modos"""
    from .general.skills import GENERAL_SKILLS
    from .builder.skills import BUILDER_SKILLS
    from .debug.skills import DEBUG_SKILLS
    from .security.skills import SECURITY_SKILLS
    from .reader.skills import READER_SKILLS
    
    return {
        "general": GENERAL_SKILLS,
        "builder": BUILDER_SKILLS,
        "debug": DEBUG_SKILLS,
        "security": SECURITY_SKILLS,
        "reader": READER_SKILLS
    }

def get_mode_skills(mode: str) -> Dict[str, Any]:
    """Obtener skills de un modo especifico"""
    all_skills = load_all_skills()
    return all_skills.get(mode, all_skills["general"])

def get_mode_tools(mode: str) -> list:
    """Obtener herramientas disponibles para un modo"""
    skills = get_mode_skills(mode)
    return list(skills.get("tools", {}).keys())

def get_mode_capabilities(mode: str) -> list:
    """Obtener capacidades de un modo"""
    skills = get_mode_skills(mode)
    caps = skills.get("capabilities", {})
    result = []
    for category, items in caps.items():
        if isinstance(items, list):
            result.extend(items)
    return result

def get_mode_color(mode: str) -> str:
    """Obtener color de un modo"""
    skills = get_mode_skills(mode)
    return skills.get("color", "#89b4fa")

def get_mode_icon(mode: str) -> str:
    """Obtener icono de un modo"""
    skills = get_mode_skills(mode)
    return skills.get("icon", "[?]")

def get_mode_description(mode: str) -> str:
    """Obtener descripcion de un modo"""
    skills = get_mode_skills(mode)
    return skills.get("description", "Modo desconocido")

def get_mode_triggers(mode: str) -> Dict[str, list]:
    """Obtener triggers de un modo"""
    skills = get_mode_skills(mode)
    return skills.get("triggers", {})

def get_mode_templates(mode: str) -> Dict[str, Any]:
    """Obtener templates de un modo (solo builder)"""
    skills = get_mode_skills(mode)
    return skills.get("templates", {})

def get_mode_quality_checklist(mode: str) -> list:
    """Obtener checklist de calidad (solo builder)"""
    skills = get_mode_skills(mode)
    return skills.get("quality_checklist", [])

def detect_mode_from_message(message: str) -> str:
    """Detectar modo basado en el mensaje del usuario"""
    message_lower = message.lower()
    
    # Triggers para cada modo
    mode_triggers = {
        "builder": ["crea", "haz", "genera", "construye", "desarrolla", "web", "pagina", "landing", "portfolio", "app"],
        "debug": ["error", "fallo", "no funciona", "bug", "arregla", "fix", "corrige"],
        "security": ["seguridad", "vulnerabilidad", "audita", "revisa", "password", "secret", "token"],
        "reader": ["lee", "muestra", "contenido", "explica", "resume", "documenta"],
        "general": ["que es", "como funciona", "ayuda", "explica", "ensena"]
    }
    
    # Contar matches por modo
    scores = {}
    for mode, triggers in mode_triggers.items():
        score = sum(1 for trigger in triggers if trigger in message_lower)
        scores[mode] = score
    
    # Retornar el modo con mayor score
    if scores:
        best_mode = max(scores, key=scores.get)
        if scores[best_mode] > 0:
            return best_mode
    
    return "general"
