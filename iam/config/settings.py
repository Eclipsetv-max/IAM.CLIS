# -*- coding: utf-8 -*-
"""
IAM Settings - Configuración global del sistema
"""

import os
import hashlib
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
                    if key not in os.environ:
                        os.environ[key] = value

load_env_file()


@dataclass
class IAMSettings:
    """Configuración principal de IAM"""
    
    DATA_DIR: Path = field(default_factory=lambda: Path(__file__).parent.parent / "data")
    
    VERSION: str = "4.5"
    
    DEFAULT_ENGINE: str = "iam"
    AVAILABLE_ENGINES: list = field(default_factory=lambda: ["iam"])
    
    MODELS: Dict[str, str] = field(default_factory=lambda: {
        "general": "mimo-v2.5-free",
        "builder": "mimo-v2.5-free",
        "plan": "mimo-v2.5-free",
        "frontend": "mimo-v2.5-free",
        "backend": "mimo-v2.5-free",
        "debug": "mimo-v2.5-free",
        "security": "mimo-v2.5-free"
    })
    
    MAX_CONTEXT_MESSAGES: int = 20
    MAX_SESSION_MESSAGES: int = 50
    SCREENSHOT_INTERVAL: int = 5
    
    # API Keys - Ultra ofuscación
    _XOR_KEYS = [b'IAM_v45_2026', b'SECRET_KEY_XOR', b'ULTRA_SECURE_123', b'NEVER_COPY_THIS']
    _SHUFFLE_SEED = hashlib.sha256(b'IAM_PATTERN_SEED').digest()
    _KEYS = {
        'k1': {
            'parts': ["4d453f2d6f32905f517a4a6d6274902a0d", "7a4114254d2b4d2a3e7514e947070c042a594907b733f71a10823b15a6", "317e2673de4041774b220f", "7003170e44293a20632612796439032b6f495a335c6060076427"],
            'checksum': "0ba9f405",
            'pattern': [39,11,28,9,37,45,1,32,59,60,23,20,57,25,17,19,0,46,36,47,33,55,58,35,13,51,53,30,24,50,7,54,41,66,48,2,40,18,49,21,29,64,38,65,56,4,52,10,8,44,61,34,14,3,62,26,31,22,67,27,15,6,63,5,12,16,43,42]
        },
        'k2': {
            'parts': ["14561653792c4d6f679b3fa9b56d", "414221463d52207e5a0105597413534665474140711c006e", "4f4d3b4c56d9727245", "395e272b703760495349260d17113441645e235a53"],
            'checksum': "8deb25a3",
            'pattern': [39,11,28,9,37,45,1,32,59,60,23,20,57,25,17,19,0,46,36,47,33,55,58,35,13,51,53,30,24,50,7,54,41,66,48,2,40,18,49,21,29,64,38,65,56,4,52,10,8,44,61,34,14,3,62,26,31,22,67,27,15,6,63,5,12,16,43,42]
        },
        'k3': {
            'parts': ["138e20506a03a84749447ea6db76", "426a202d5e293e482d4e6c535f3e36135502d74a5f1658cf", "259c3d33b147f10137", "335a567e78374e21213873082534694282047c180d7a"],
            'checksum': "2f9188a6",
            'pattern': [39,11,28,9,37,45,1,32,59,60,23,20,57,25,17,19,0,46,36,47,33,55,58,35,13,51,53,30,24,50,7,54,41,66,48,2,40,18,49,21,29,64,38,65,56,4,52,10,8,68,61,34,14,3,62,26,31,22,67,27,15,6,63,5,12,16,43,42,44]
        }
    }
    
    def _decode_ultra(key_id: str) -> str:
        try:
            ki = IAMSettings._KEYS[key_id]
            combined = bytes.fromhex(''.join(ki['parts']))
            if hashlib.md5(combined).hexdigest()[:8] != ki['checksum']:
                return ""
            n = len(combined)
            inv_pattern = [0] * n
            for i, p in enumerate(ki['pattern'][:n]):
                inv_pattern[p] = i
            unshuffled = bytearray(n)
            for i in range(n):
                unshuffled[i] = combined[inv_pattern[i]]
            data = bytes(unshuffled)
            for k in reversed(IAMSettings._XOR_KEYS):
                data = bytes([b ^ k[i % len(k)] for i, b in enumerate(data)])
            return data[8:-8].decode('utf-8', errors='replace')
        except Exception:
            return ""
    
    API_KEY: str = field(default_factory=lambda: os.environ.get("OPENCODE_API_KEY") or IAMSettings._decode_ultra('k1'))
    API_KEY_ALT: str = field(default_factory=lambda: os.environ.get("FREETHEAI_API_KEY") or IAMSettings._decode_ultra('k2'))
    API_KEY_GEM: str = field(default_factory=lambda: os.environ.get("GEMINI_API_KEY") or IAMSettings._decode_ultra('k3'))
    
    # Keys adicionales para fallback automatico
    API_KEYS_FALLBACK: list = field(default_factory=lambda: [
        k for k in [
            os.environ.get("OPENCODE_API_KEY_2"),
            os.environ.get("OPENCODE_API_KEY_3"),
            os.environ.get("OPENCODE_API_KEY_4"),
            os.environ.get("OPENCODE_API_KEY_5"),
        ] if k
    ])
    
    def __post_init__(self):
        self.DATA_DIR.mkdir(exist_ok=True)


class COLORS:
    """Constantes de colores ANSI"""
    
    TEAL = "\033[38;2;0;212;170m"
    RESET = "\033[0m"
    ORANGE = "\033[38;2;249;115;22m"
    GREEN2 = "\033[38;2;74;222;128m"
    PINK = "\033[38;2;236;72;153m"
    RED = "\033[31m"
    CYAN2 = "\033[38;2;34;211;238m"
    
    MODE_COLORS = {
        "general": CYAN2,
        "builder": ORANGE,
        "plan": GREEN2,
        "frontend": PINK,
        "backend": TEAL,
        "debug": RED
    }


settings = IAMSettings()
