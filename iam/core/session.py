# -*- coding: utf-8 -*-
"""
IAM Session Manager - Gestión de sesiones de chat
Estilo Claude: sesiones persistentes con contexto
"""

import json
import datetime
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any

from ..config.settings import settings


@dataclass
class Message:
    """Representa un mensaje en la sesión"""
    role: str  # "user" | "assistant" | "system"
    content: str
    timestamp: datetime.datetime = field(default_factory=datetime.datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "role": self.role,
            "content": self.content,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Message":
        return cls(
            role=data["role"],
            content=data["content"],
            timestamp=datetime.datetime.fromisoformat(data["timestamp"]),
            metadata=data.get("metadata", {})
        )


@dataclass
class Session:
    """
    Representa una sesión de chat
    Similar a Claude: persistente, con historial y contexto
    """
    id: str
    name: str
    created_at: datetime.datetime = field(default_factory=datetime.datetime.now)
    updated_at: datetime.datetime = field(default_factory=datetime.datetime.now)
    messages: List[Message] = field(default_factory=list)
    mode: str = "general"
    model: str = "llama3-8b-8192"
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def add_message(self, role: str, content: str, metadata: Dict[str, Any] = None) -> Message:
        """Agregar mensaje a la sesión"""
        msg = Message(role=role, content=content, metadata=metadata or {})
        self.messages.append(msg)
        self.updated_at = datetime.datetime.now()
        
        # Mantener límite de mensajes
        if len(self.messages) > settings.MAX_SESSION_MESSAGES:
            # Preservar primer mensaje (system) y últimos N
            self.messages = [self.messages[0]] + self.messages[-(settings.MAX_SESSION_MESSAGES - 1):]
        
        return msg
    
    def get_context(self, max_messages: int = None) -> List[Dict[str, str]]:
        """Obtener contexto para la IA"""
        if max_messages is None:
            max_messages = settings.MAX_CONTEXT_MESSAGES
        
        # Retornar últimos mensajes en formato API
        context = []
        for msg in self.messages[-max_messages:]:
            context.append({
                "role": msg.role,
                "content": msg.content
            })
        return context
    
    def get_last_user_message(self) -> Optional[str]:
        """Obtener último mensaje del usuario"""
        for msg in reversed(self.messages):
            if msg.role == "user":
                return msg.content
        return None
    
    def clear(self):
        """Limpiar sesión (mantener solo system message)"""
        if self.messages and self.messages[0].role == "system":
            self.messages = [self.messages[0]]
        else:
            self.messages = []
        self.updated_at = datetime.datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "messages": [m.to_dict() for m in self.messages],
            "mode": self.mode,
            "model": self.model,
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Session":
        session = cls(
            id=data["id"],
            name=data["name"],
            created_at=datetime.datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.datetime.fromisoformat(data["updated_at"]),
            mode=data.get("mode", "general"),
            model=data.get("model", "llama3-8b-8192"),
            metadata=data.get("metadata", {})
        )
        session.messages = [Message.from_dict(m) for m in data.get("messages", [])]
        return session


class SessionManager:
    """
    Gestor de sesiones estilo Claude
    Persiste sesiones en disco
    """
    
    def __init__(self):
        self.sessions: Dict[str, Session] = {}
        self.current_session: Optional[Session] = None
        self.session_counter: int = 0
        self.sessions_file = settings.DATA_DIR / "sessions.json"
        self._load_sessions()
    
    def _load_sessions(self):
        """Cargar sesiones desde disco"""
        if self.sessions_file.exists():
            try:
                with open(self.sessions_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                self.session_counter = data.get("counter", 0)
                for s_data in data.get("sessions", []):
                    session = Session.from_dict(s_data)
                    self.sessions[session.id] = session
                
                # Restaurar última sesión activa
                current_id = data.get("current_session")
                if current_id and current_id in self.sessions:
                    self.current_session = self.sessions[current_id]
                    
            except Exception:
                pass
    
    def _save_sessions(self):
        """Guardar sesiones en disco"""
        data = {
            "counter": self.session_counter,
            "current_session": self.current_session.id if self.current_session else None,
            "sessions": [s.to_dict() for s in self.sessions.values()]
        }
        
        try:
            with open(self.sessions_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception:
            pass
    
    def create_session(self, name: str = None, mode: str = "general") -> Session:
        """Crear nueva sesión"""
        self.session_counter += 1
        session_id = f"session_{self.session_counter}"
        
        if not name:
            name = f"Sesión {self.session_counter}"
        
        session = Session(
            id=session_id,
            name=name,
            mode=mode,
            model=settings.MODELS.get(mode, settings.MODELS["general"])
        )
        
        self.sessions[session_id] = session
        self.current_session = session
        self._save_sessions()
        
        return session
    
    def switch_session(self, session_id: str) -> bool:
        """Cambiar a otra sesión"""
        if session_id in self.sessions:
            self.current_session = self.sessions[session_id]
            self._save_sessions()
            return True
        return False
    
    def list_sessions(self) -> List[Dict[str, Any]]:
        """Listar todas las sesiones"""
        return [
            {
                "id": s.id,
                "name": s.name,
                "created": s.created_at.strftime("%Y-%m-%d %H:%M"),
                "updated": s.updated_at.strftime("%Y-%m-%d %H:%M"),
                "messages": len(s.messages),
                "mode": s.mode,
                "active": s == self.current_session
            }
            for s in sorted(self.sessions.values(), key=lambda x: x.updated_at, reverse=True)
        ]
