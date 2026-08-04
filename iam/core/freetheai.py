"""
Integracion con FreeTheAi - API gratuita OpenAI-compatible
80+ modelos gratis sin tarjeta de credito
Usa proxy server para ocultar API keys
"""
import os
import requests
from pathlib import Path
from typing import Optional, Generator
from dataclasses import dataclass


@dataclass
class FreeTheAiConfig:
    """Configuracion de FreeTheAi"""
    api_key: str = ""
    proxy_url: str = "http://localhost:5000"  # Local proxy
    online_url: str = ""  # URL del servidor online (se configura despues)
    model: str = "opc/deepseek-v4-flash-free"
    temperature: float = 0.7
    max_tokens: int = 2048
    use_proxy: bool = True


class FreeTheAiClient:
    """Cliente para FreeTheAi API (via proxy)"""
    
    def __init__(self, config: FreeTheAiConfig = None):
        self.config = config or self._load_config()
    
    def _load_config(self) -> FreeTheAiConfig:
        """Cargar configuracion"""
        # Intentar cargar desde .env (para modo directo)
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
        if not online_url:
            online_url = os.getenv("FREETHEAI_PROXY_URL", "")
        
        # Determinar URL del proxy
        if online_url:
            proxy_url = online_url
        else:
            proxy_url = "https://iam-ai-proxy.fly.dev"  # Fly.io
        
        # Verificar si el proxy esta disponible
        use_proxy = True
        try:
            response = requests.get(f"{proxy_url}/health", timeout=2)
            if response.status_code != 200:
                use_proxy = False
        except:
            use_proxy = False
        
        return FreeTheAiConfig(
            api_key=api_key,
            proxy_url=proxy_url,
            online_url=online_url,
            use_proxy=use_proxy
        )
    
    def is_available(self) -> bool:
        """Verificar si FreeTheAi esta disponible"""
        if self.config.use_proxy:
            return True  # Proxy siempre disponible
        return bool(self.config.api_key)
    
    def chat(self, prompt: str, system_prompt: str = "") -> str:
        """Enviar mensaje y recibir respuesta"""
        if not self.is_available():
            return "[ERROR] FreeTheAi no disponible"
        
        try:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            if self.config.use_proxy:
                # Usar proxy (local o online)
                url = f"{self.config.proxy_url}/v1/chat/completions"
                headers = {"Content-Type": "application/json"}
                payload = {
                    "model": self.config.model,
                    "messages": messages,
                    "temperature": self.config.temperature,
                    "max_tokens": self.config.max_tokens
                }
            else:
                # Modo directo (fallback)
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
            
            response = requests.post(url, headers=headers, json=payload, timeout=60)
            
            if response.status_code == 200:
                data = response.json()
                if "choices" in data and data["choices"]:
                    return data["choices"][0]["message"]["content"]
                elif "error" in data:
                    return f"[ERROR] FreeTheAi: {data['error']}"
                else:
                    return f"[ERROR] FreeTheAi: respuesta inesperada"
            elif response.status_code == 503:
                return "[MANTENIMIENTO] Servidor temporalmente desactivado"
            else:
                return f"[ERROR] FreeTheAi: {response.status_code}"
                
        except Exception as e:
            return f"[ERROR] FreeTheAi: {str(e)}"
    
    def chat_stream(self, prompt: str, system_prompt: str = "") -> Generator[str, None, None]:
        """Enviar mensaje y recibir respuesta con streaming"""
        if not self.is_available():
            yield "[ERROR] FreeTheAi API key no configurada"
            return
        
        try:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            response = requests.post(
                f"{self.config.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.config.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.config.model,
                    "messages": messages,
                    "temperature": self.config.temperature,
                    "max_tokens": self.config.max_tokens,
                    "stream": True
                },
                stream=True,
                timeout=120
            )
            
            for line in response.iter_lines():
                if line:
                    line = line.decode('utf-8')
                    if line.startswith('data: ') and line != 'data: [DONE]':
                        import json
                        data = json.loads(line[6:])
                        if data['choices'][0]['delta'].get('content'):
                            yield data['choices'][0]['delta']['content']
                            
        except Exception as e:
            yield f"[ERROR] FreeTheAi: {str(e)}"
    
    def list_models(self) -> list:
        """Listar modelos disponibles"""
        if not self.is_available():
            return []
        
        try:
            response = requests.get(
                f"{self.config.base_url}/models",
                headers={
                    "Authorization": f"Bearer {self.config.api_key}"
                },
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                return [m["id"] for m in data.get("data", [])]
            return []
        except:
            return []


# Instancia global
freetheai_client = FreeTheAiClient()
