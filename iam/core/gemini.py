"""
Integracion con Google Gemini API
Usa proxy server para ocultar API keys
"""
import os
import requests
from pathlib import Path
from typing import Optional, Generator
from dataclasses import dataclass


@dataclass
class GeminiConfig:
    """Configuracion de Gemini"""
    api_key: str = ""
    proxy_url: str = "http://localhost:5000"  # Local proxy
    online_url: str = ""  # URL del servidor online
    model: str = "gemini-2.0-flash"
    temperature: float = 0.7
    max_tokens: int = 2048
    top_p: float = 0.9
    use_proxy: bool = True


class GeminiClient:
    """Cliente para Google Gemini API (via proxy)"""
    
    def __init__(self, config: GeminiConfig = None):
        self.config = config or self._load_config()
        self._model = None
    
    def _load_config(self) -> GeminiConfig:
        """Cargar configuracion"""
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
                        if line.startswith("GEMINI_API_KEY="):
                            api_key = line.split("=", 1)[1].strip()
                        elif line.startswith("GEMINI_PROXY_URL="):
                            online_url = line.split("=", 1)[1].strip()
        
        if not api_key:
            api_key = os.getenv("GEMINI_API_KEY", "")
        if not online_url:
            online_url = os.getenv("GEMINI_PROXY_URL", "")
        
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
        
        return GeminiConfig(
            api_key=api_key,
            proxy_url=proxy_url,
            online_url=online_url,
            use_proxy=use_proxy
        )
    
    def is_available(self) -> bool:
        """Verificar si Gemini esta disponible"""
        if self.config.use_proxy:
            return True
        return bool(self.config.api_key)
    
    def chat(self, prompt: str, system_prompt: str = "") -> str:
        """Enviar mensaje y recibir respuesta"""
        if not self.is_available():
            return "[ERROR] Gemini no disponible"
        
        try:
            if self.config.use_proxy:
                # Usar proxy (local o online)
                url = f"{self.config.proxy_url}/v1/gemini"
                response = requests.post(
                    url,
                    json={
                        "prompt": prompt,
                        "system_prompt": system_prompt,
                        "model": self.config.model,
                        "temperature": self.config.temperature,
                        "max_tokens": self.config.max_tokens
                    },
                    timeout=60
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return data.get("response", "")
                elif response.status_code == 503:
                    return "[MANTENIMIENTO] Servidor temporalmente desactivado"
                else:
                    return f"[ERROR] Gemini proxy: {response.status_code}"
            else:
                # Modo directo
                return self._call_direct(prompt, system_prompt)
                
        except Exception as e:
            return f"[ERROR] Gemini: {str(e)}"
    
    def _call_direct(self, prompt: str, system_prompt: str = "") -> str:
        """Llamada directa a Gemini (sin proxy)"""
        try:
            import google.generativeai as genai
            genai.configure(api_key=self.config.api_key)
            
            model = genai.GenerativeModel(self.config.model)
            
            if system_prompt:
                full_prompt = f"[System]: {system_prompt}\n\n[User]: {prompt}"
            else:
                full_prompt = prompt
            
            response = model.generate_content(
                full_prompt,
                generation_config={
                    "temperature": self.config.temperature,
                    "max_output_tokens": self.config.max_tokens,
                    "top_p": self.config.top_p,
                }
            )
            
            return response.text or ""
            
        except Exception as e:
            return f"[ERROR] Gemini: {str(e)}"
    
    def chat_stream(self, prompt: str, system_prompt: str = "") -> Generator[str, None, None]:
        """Enviar mensaje y recibir respuesta con streaming"""
        if not self.is_available():
            yield "[ERROR] Gemini API key no configurada"
            return
        
        try:
            model = self._get_model()
            
            if system_prompt:
                full_prompt = f"[System]: {system_prompt}\n\n[User]: {prompt}"
            else:
                full_prompt = prompt
            
            response = model.generate_content(
                full_prompt,
                generation_config={
                    "temperature": self.config.temperature,
                    "max_output_tokens": self.config.max_tokens,
                    "top_p": self.config.top_p,
                },
                stream=True
            )
            
            for chunk in response:
                if chunk.text:
                    yield chunk.text
                    
        except Exception as e:
            yield f"[ERROR] Gemini: {str(e)}"


# Instancia global
gemini_client = GeminiClient()
