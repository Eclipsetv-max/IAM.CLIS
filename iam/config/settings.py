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
    
    # API Keys - Ultra ofuscación (7 keys cifradas)
    _XOR_KEYS = [b'IAM_v45_2026', b'SECRET_KEY_XOR', b'ULTRA_SECURE_123', b'NEVER_COPY_THIS']
    _KEYS = {
        'k1': {  # Key principal (OpenCode)
            'parts': ['4a3a26413314174d2b5f3b10037932', '700d5a492b5b572a4733567a397e2a', '77076063492660bb6f7320036f74cf', '3744960e1422150f4d1251a37559e5', '4101f32d4027625c644d6a9829252a', '3e31644b3fae494d'],
            'checksum': '3f1cbdb7',
            'pattern': [47,62,33,46,56,15,8,39,61,30,66,32,63,49,71,12,65,36,23,57,79,1,60,40,42,78,74,72,19,20,26,18,52,43,7,34,67,2,16,38,41,22,45,24,5,6,50,75,9,59,21,68,44,10,58,48,0,55,51,76,37,77,82,53,25,70,64,29,27,73,80,4,54,11,69,13,17,28,31,35,3,14,81]
        },
        'k2': {  # Key fallback 1
            'parts': ['0d00014734393e6f1cea60533d467e', '4c264f49b7372f5a116d413f5a5304', '205b65273816521714112be3495ec1', '74793b59894570f871be4146628972', '536723055e671340'],
            'checksum': 'bf4513c5',
            'pattern': [22,18,10,56,50,19,6,30,23,0,26,21,37,40,39,32,12,42,44,5,46,63,57,1,24,54,47,33,58,7,11,62,27,38,64,35,15,8,16,9,29,60,31,41,65,55,45,36,13,4,17,25,61,51,2,52,14,3,66,49,53,67,43,28,34,48,59,20]
        },
        'k3': {  # Key fallback 2
            'parts': ['3e3d4e496a2d6c0442783ee1587a7c', '5f486a53381325377e202155424737', '769b257ea95ece292d69e224212c02', '11475a4e491634735689ee5033135f', 'de4833085718320d4a'],
            'checksum': '33a1a019',
            'pattern': [11,36,26,2,45,14,28,41,52,25,59,63,18,49,43,51,39,60,13,44,16,8,46,29,35,21,27,54,30,17,24,4,42,47,5,37,3,15,57,50,7,1,31,68,56,66,65,34,10,48,23,9,12,38,62,61,53,19,40,55,6,67,32,22,64,33,0,58,20]
        },
        'k4': {  # Key fallback 3
            'parts': ['6d383b46656474324d4d3b45385129', '0f35140092ccb7ef57375577396259', '1657045e21331318ef8b211c32176c', '377d547b7613674361896024122779', '27845b5e27294a52491b056d318f31', 'd417206d0e630572'],
            'checksum': '3c8bc0bb',
            'pattern': [73,71,24,19,36,55,38,32,10,49,14,45,57,67,18,44,23,33,13,5,78,2,80,72,20,1,47,70,40,37,53,39,82,51,54,17,11,56,76,81,34,59,69,15,48,21,25,63,64,50,41,43,3,46,77,26,58,22,68,74,61,6,12,52,66,31,60,16,27,62,35,30,65,79,42,4,8,29,7,9,0,28,75]
        },
        'k5': {  # Key fallback 4
            'parts': ['a0d64a643b3e77397e3e5657231270', '750e342172171b2b6935452eed5439', '0bee0c0f25bd2f274e01710370273b', '135b0856f4532d45403a68ca601643', '414a4717154d0637166b6253c4334f', 'f8054b285a6c487e'],
            'checksum': '323792c3',
            'pattern': [81,1,79,30,34,66,50,31,12,70,21,46,22,41,28,49,9,44,56,48,11,32,45,52,72,17,51,3,18,35,14,0,71,77,29,82,63,57,47,54,60,13,16,68,33,59,53,42,26,5,39,2,62,80,58,36,76,25,15,55,43,4,38,8,23,10,65,73,20,67,64,61,6,75,40,78,69,74,7,27,37,24,19]
        },
        'k6': {  # Key fallback 5
            'parts': ['1240404e22377218b42c5700613941', '7f2c0965380d0a5a21aebb5d700874', '1f51339e2f7334b12913111f563c18', '5e590e165bca7260735f0b5f4d4d6d', '4e175c139f88133b3de4422e7b3b73', '204c6f3e443d1113'],
            'checksum': '5203e2cd',
            'pattern': [41,80,56,39,82,18,46,31,1,63,29,3,30,59,12,25,58,20,51,74,21,65,50,71,77,75,73,60,17,24,68,69,15,81,22,38,48,79,67,61,53,57,52,37,23,2,78,9,44,4,7,72,55,27,45,66,28,47,10,16,40,8,49,42,0,5,35,54,11,6,32,62,64,33,76,43,26,36,34,19,70,13,14]
        },
        'k7': {  # Key fallback 6
            'parts': ['0f4542fa245f3257153a2d73130862', '193f196735337508695a104d0a1a0e', '275a416e064360486b284d58120348', '227a8613111c4218746f0e6d7b3ed5', '56154222203b28915c052cb27f1748', '306f3feb06715004'],
            'checksum': '055f5dab',
            'pattern': [15,26,43,1,49,70,30,47,40,66,11,79,41,31,73,18,62,5,25,54,58,72,17,80,55,53,10,13,81,9,71,19,48,52,21,4,67,23,45,34,64,0,69,59,60,12,36,77,7,32,57,56,20,50,46,63,27,38,6,2,16,61,37,22,33,14,78,75,68,76,65,82,74,8,35,42,51,24,3,28,29,39,44]
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
    
    API_KEY: str = field(default_factory=lambda: IAMSettings._decode_ultra('k1'))
    API_KEY_ALT: str = field(default_factory=lambda: IAMSettings._decode_ultra('k2'))
    API_KEY_GEM: str = field(default_factory=lambda: IAMSettings._decode_ultra('k3'))
    
    # Keys para fallback automatico (k1=principal, k2=alt, k3=gemini)
    API_KEYS_FALLBACK: list = field(default_factory=lambda: [
        IAMSettings._decode_ultra('k4'),
        IAMSettings._decode_ultra('k5'),
        IAMSettings._decode_ultra('k6'),
        IAMSettings._decode_ultra('k7'),
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
