"""
Motor IA Secundario - Integracion via proxy
"""
import os
import requests
from pathlib import Path
from typing import Optional
from dataclasses import dataclass


@dataclass
class SecondaryConfig:
    """Configuracion del motor IA secundario"""
    api_key: str = ""
    proxy_url: str = "http://localhost:5000"
    online_url: str = ""
    model: str = "opc/deepseek-v4-flash-free"
    temperature: float = 0.7
    max_tokens: int = 2048
    use_proxy: bool = True


class SecondaryClient:
    """Cliente para motor IA secundario (via proxy)"""
    
    def __init__(self, config: SecondaryConfig = None):
        self.config = config or self._load_config()
    
    def _load_config(self) -> SecondaryConfig:
        api_key = ""
        online_url = ""
        env_paths = [
            Path(__file__).parent.parent.parent / ".env",
            Path.cwd() / ".env",
        ]
        
        for env_path in env_paths:
            if env_path.exists():
                with open(env_path, 'r') as f:
                    for line in f:
                        if line.startswith("FREETHEAI_API_KEY="):
                            api_key = line.split("=", 1)[1].strip()
                        elif line.startswith("FREETHEAI_PROXY_URL="):
                            online_url = line.split("=", 1)[1].strip()
        
        if not api_key:
            api_key = os.getenv("FREETHEAI_API_KEY", "")
        if not api_key:
            from iam.config.settings import settings
            api_key = settings.API_KEY_ALT
        if not online_url:
            online_url = os.getenv("FREETHEAI_PROXY_URL", "")
        
        if online_url:
            proxy_url = online_url
        else:
            proxy_url = "https://iam-proxy.onrender.com"
        
        use_proxy = True
        try:
            response = requests.get(f"{proxy_url}/health", timeout=2)
            if response.status_code != 200:
                use_proxy = False
        except:
            use_proxy = False
        
        return SecondaryConfig(
            api_key=api_key,
            proxy_url=proxy_url,
            online_url=online_url,
            use_proxy=use_proxy
        )
    
    def is_available(self) -> bool:
        if self.config.use_proxy:
            return True
        return bool(self.config.api_key)
    
    def chat(self, prompt: str, system_prompt: str = "") -> str:
        import time
        
        if not self.is_available():
            return "[ERROR] Motor IA no disponible"
        
        max_retries = 3
        
        for attempt in range(max_retries):
            try:
                messages = []
                if system_prompt:
                    messages.append({"role": "system", "content": system_prompt})
                messages.append({"role": "user", "content": prompt})
                
                if self.config.use_proxy:
                    url = f"{self.config.proxy_url}/v1/chat/completions"
                    headers = {"Content-Type": "application/json"}
                    payload = {
                        "model": self.config.model,
                        "messages": messages,
                        "temperature": self.config.temperature,
                        "max_tokens": self.config.max_tokens
                    }
                else:
                    url = "https://api.freetheai.xyz/v1/chat/completions"
                    headers = {
                        "Authorization": f"Bearer {self.config.api_key}",
                        "Content-Type": "application/json"
                    }
                    payload = {
                        "model": self.config.model,
                        "messages": messages,
                        "temperature": self.config.temperature,
                        "max_tokens": self.config.max_tokens
                    }
                
                response = requests.post(url, headers=headers, json=payload, timeout=30)
                
                if response.status_code == 200:
                    data = response.json()
                    if "choices" in data and data["choices"]:
                        return data["choices"][0]["message"]["content"]
                    elif "error" in data:
                        return f"[ERROR] Motor IA: {data['error']}"
                    else:
                        return f"[ERROR] Motor IA: respuesta inesperada"
                elif response.status_code == 503:
                    if attempt < max_retries - 1:
                        wait_time = 2 * (attempt + 1)
                        time.sleep(wait_time)
                        continue
                    return "Fernando esta viendo en donde esta el error espere un rato"
                else:
                    return "Fernando esta viendo en donde esta el error espere un rato"
                    
            except Exception as e:
                if attempt < max_retries - 1:
                    time.sleep(2)
                    continue
                return "Fernando esta viendo en donde esta el error espere un rato"
        
        return "[ERROR] Motor IA: max reintentos alcanzados"


# Instancia global
freetheai_client = SecondaryClient()
