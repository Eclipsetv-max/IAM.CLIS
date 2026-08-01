# -*- coding: utf-8 -*-
"""
IAM Mode Loader - Carga las skills de cada modo
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
    return skills.get("capabilities", [])

def get_mode_color(mode: str) -> str:
    """Obtener color de un modo"""
    skills = get_mode_skills(mode)
    return skills.get("color", "#89b4fa")

def get_mode_icon(mode: str) -> str:
    """Obtener icono de un modo"""
    skills = get_mode_skills(mode)
    return skills.get("icon", "[?]")
