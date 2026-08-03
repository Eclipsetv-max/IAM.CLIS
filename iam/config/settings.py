# -*- coding: utf-8 -*-
"""
IAM Settings - Configuración global del sistema
"""

import os
from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, Any


def load_env_file():
    """Cargar variables de entorno desde archivo .env"""
    env_path = Path(__file__).parent.parent.parent / ".env"
    if env_path.exists():
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()
                    # No sobreescribir si ya existe
                    if key not in os.environ:
                        os.environ[key] = value

# Cargar .env al importar
load_env_file()


@dataclass
class IAMSettings:
    """Configuración principal de IAM"""
    
    # Paths
    BASE_DIR: Path = Path(__file__).parent.parent.parent
    IAM_DIR: Path = Path(__file__).parent.parent
    DATA_DIR: Path = field(default_factory=lambda: Path(__file__).parent.parent / "data")
    
    # Info del usuario
    USERNAME: str = "User"
    USER_ALIAS: str = "User"
    
    # Versión
    VERSION: str = "3.1.1"
    CODENAME: str = "Acceso Total"
    
    # Configuración de IA
    DEFAULT_ENGINE: str = "mimo"
    AVAILABLE_ENGINES: list = field(default_factory=lambda: ["mimo", "opencode", "local", "gemini", "freetheai"])
    
    # Modelos por defecto (OpenCode - MiMo v2.5 Free)
    MODELS: Dict[str, str] = field(default_factory=lambda: {
        "general": "mimo-v2.5-free",
        "builder": "mimo-v2.5-free",
        "plan": "mimo-v2.5-free",
        "frontend": "mimo-v2.5-free",
        "backend": "mimo-v2.5-free",
        "debug": "mimo-v2.5-free",
        "security": "mimo-v2.5-free"
    })
    
    # Modelo local fine-tuned
    LOCAL_MODEL_DIR: Path = field(default_factory=lambda: Path(__file__).parent.parent / "training" / "models")
    LOCAL_MODEL_NAME: str = "tinyllama"  # Nombre del modelo local por defecto
    
    # Modelos alternativos por motor
    FALLBACK_MODELS: Dict[str, Dict[str, str]] = field(default_factory=lambda: {
        "opencode": {
            "general": "mimo-v2.5",
            "builder": "mimo-v2.5-pro"
        }
    })
    
    # Límites
    MAX_CONTEXT_MESSAGES: int = 20
    MAX_SESSION_MESSAGES: int = 50
    SCREENSHOT_INTERVAL: int = 5
    
    # API Keys (desde variables de entorno)
    HF_API_KEY: str = field(default_factory=lambda: os.environ.get("HF_API_KEY", ""))
    OPENCODE_API_KEY: str = field(default_factory=lambda: os.environ.get("OPENCODE_API_KEY", ""))
    
    def __post_init__(self):
        """Crear directorios necesarios"""
        self.DATA_DIR.mkdir(exist_ok=True)
    
    def get_model(self, mode: str) -> str:
        """Obtener modelo para un modo específico"""
        return self.MODELS.get(mode, self.MODELS["general"])


class COLORS:
    """Constantes de colores ANSI - Estilo OpenCode"""
    
    # Colores principales (estilo OpenCode)
    TEAL = "\033[38;2;0;212;170m"
    WHITE = "\033[38;2;238;238;238m"
    GRAY = "\033[90m"
    BOLD = "\033[1m"
    RESET = "\033[0m"
    YELLOW = "\033[33m"
    CYAN = "\033[36m"
    
    # Colores extendidos (estilo OpenCode)
    RED = "\033[31m"
    GREEN = "\033[32m"
    PURPLE = "\033[38;2;147;51;234m"
    BLUE = "\033[38;2;59;130;246m"
    ORANGE = "\033[38;2;249;115;22m"
    PINK = "\033[38;2;236;72;153m"
    CYAN2 = "\033[38;2;34;211;238m"
    GREEN2 = "\033[38;2;74;222;128m"
    DIM = "\033[2m"
    LINE = "\033[38;2;60;60;70m"
    
    # Colores por modo (estilo OpenCode)
    MODE_COLORS = {
        "general": CYAN2,
        "builder": ORANGE,
        "plan": GREEN2,
        "frontend": PINK,
        "backend": TEAL,
        "debug": RED
    }


# Instancia global de configuración
settings = IAMSettings()
