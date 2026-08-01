# -*- coding: utf-8 -*-
"""
IAM Memory - Sistema de Memoria a Largo Plazo
Permite a la IA recordar interacciones y conocimiento previo
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field, asdict
import hashlib

from ..config.settings import settings


@dataclass
class MemoryEntry:
    """Entrada en la memoria"""
    id: str
    category: str  # "conversation", "knowledge", "code", "preference"
    content: str
    context: str
    tags: List[str] = field(default_factory=list)
    importance: float = 0.5  # 0.0 a 1.0
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    accessed_at: str = field(default_factory=lambda: datetime.now().isoformat())
    access_count: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MemoryEntry":
        return cls(**data)


class MemorySystem:
    """
    Sistema de memoria persistente
    Almacena y recuerda información a largo plazo
    """
    
    def __init__(self):
        self.memory_file = settings.DATA_DIR / "long_term_memory.json"
        self.context_file = settings.DATA_DIR / "context_memory.json"
        self.entries: List[MemoryEntry] = []
        self.context: Dict[str, Any] = {}
        self._load_memory()
        self._load_context()
    
    def _load_memory(self):
        """Cargar memoria desde disco"""
        if self.memory_file.exists():
            try:
                with open(self.memory_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                self.entries = [MemoryEntry.from_dict(e) for e in data.get("entries", [])]
            except Exception:
                self.entries = []
    
    def _save_memory(self):
        """Guardar memoria en disco"""
        data = {
            "entries": [e.to_dict() for e in self.entries],
            "last_updated": datetime.now().isoformat()
        }
        try:
            with open(self.memory_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception:
            pass
    
    def _load_context(self):
        """Cargar contexto de memoria"""
        if self.context_file.exists():
            try:
                with open(self.context_file, 'r', encoding='utf-8') as f:
                    self.context = json.load(f)
            except Exception:
                self.context = {}
        else:
            self.context = {
                "user_preferences": {},
                "project_context": {},
                "conversation_topics": [],
                "recent_files": [],
                "current_task": None,
                "session_count": 0,
                "last_session": None
            }
    
    def _save_context(self):
        """Guardar contexto de memoria"""
        self.context["last_updated"] = datetime.now().isoformat()
        try:
            with open(self.context_file, 'w', encoding='utf-8') as f:
                json.dump(self.context, f, indent=2, ensure_ascii=False)
        except Exception:
            pass
    
    def _generate_id(self, content: str) -> str:
        """Generar ID único para entrada"""
        hash_input = f"{content}{datetime.now().isoformat()}"
        return hashlib.md5(hash_input.encode()).hexdigest()[:12]
    
    def store(self, content: str, category: str = "conversation", 
              context: str = "", tags: List[str] = None, 
              importance: float = 0.5) -> MemoryEntry:
        """Almacenar información en memoria"""
        entry = MemoryEntry(
            id=self._generate_id(content),
            category=category,
            content=content,
            context=context,
            tags=tags or [],
            importance=importance
        )
        
        self.entries.append(entry)
        
        # Mantener límite de memoria
        if len(self.entries) > 500:
            # Eliminar las menos importantes
            self.entries.sort(key=lambda e: e.importance, reverse=True)
            self.entries = self.entries[:400]
        
        self._save_memory()
        return entry
    
    def recall(self, query: str, category: str = None, 
               limit: int = 5) -> List[MemoryEntry]:
        """Recuperar información relevante de la memoria"""
        query_lower = query.lower()
        query_words = set(query_lower.split())
        
        scored_entries = []
        
        for entry in self.entries:
            # Filtrar por categoría si se especifica
            if category and entry.category != category:
                continue
            
            # Calcular relevancia
            score = self._calculate_relevance(query_words, entry)
            
            if score > 0.3:
                scored_entries.append((score, entry))
        
        # Ordenar por relevancia
        scored_entries.sort(key=lambda x: x[0], reverse=True)
        
        # Actualizar contador de acceso
        results = []
        for score, entry in scored_entries[:limit]:
            entry.accessed_at = datetime.now().isoformat()
            entry.access_count += 1
            results.append(entry)
        
        self._save_memory()
        return results
    
    def _calculate_relevance(self, query_words: set, entry: MemoryEntry) -> float:
        """Calcular relevancia de una entrada"""
        score = 0.0
        
        # Relevancia por contenido
        content_words = set(entry.content.lower().split())
        overlap = len(query_words & content_words)
        if query_words:
            score += (overlap / len(query_words)) * 0.4
        
        # Relevancia por tags
        tag_overlap = len(set(entry.tags) & query_words)
        if entry.tags:
            score += (tag_overlap / len(entry.tags)) * 0.3
        
        # Relevancia por importancia
        score += entry.importance * 0.2
        
        # Relevancia por recencia
        try:
            created = datetime.fromisoformat(entry.created_at)
            days_old = (datetime.now() - created).days
            recency_score = max(0, 1 - (days_old / 30))
            score += recency_score * 0.1
        except Exception:
            pass
        
        return min(1.0, score)
    
    def get_by_category(self, category: str, limit: int = 10) -> List[MemoryEntry]:
        """Obtener entradas por categoría"""
        entries = [e for e in self.entries if e.category == category]
        entries.sort(key=lambda e: e.created_at, reverse=True)
        return entries[:limit]
    
    def get_important(self, limit: int = 10) -> List[MemoryEntry]:
        """Obtener entradas más importantes"""
        entries = sorted(self.entries, key=lambda e: e.importance, reverse=True)
        return entries[:limit]
    
    def get_recent(self, limit: int = 10) -> List[MemoryEntry]:
        """Obtener entradas más recientes"""
        entries = sorted(self.entries, key=lambda e: e.created_at, reverse=True)
        return entries[:limit]
    
    def search(self, query: str) -> List[MemoryEntry]:
        """Buscar en memoria"""
        query_lower = query.lower()
        results = []
        
        for entry in self.entries:
            if query_lower in entry.content.lower():
                results.append(entry)
            elif any(query_lower in tag.lower() for tag in entry.tags):
                results.append(entry)
        
        return results[:10]
    
    def delete(self, entry_id: str) -> bool:
        """Eliminar una entrada"""
        for i, entry in enumerate(self.entries):
            if entry.id == entry_id:
                self.entries.pop(i)
                self._save_memory()
                return True
        return False
    
    def get_session_count(self) -> int:
        """Obtener contador de sesiones"""
        return self.context.get("session_count", 0)
    
    def get_stats(self) -> Dict[str, Any]:
        """Obtener estadísticas de la memoria"""
        categories = {}
        for entry in self.entries:
            cat = entry.category
            categories[cat] = categories.get(cat, 0) + 1
        
        return {
            "total_entries": len(self.entries),
            "categories": categories,
            "avg_importance": sum(e.importance for e in self.entries) / max(len(self.entries), 1),
            "most_accessed": sorted(self.entries, key=lambda e: e.access_count, reverse=True)[:5],
            "session_count": self.get_session_count(),
            "user_preferences": len(self.context.get("user_preferences", {})),
            "tracked_projects": len(self.context.get("project_context", {}))
        }
