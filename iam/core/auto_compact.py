# -*- coding: utf-8 -*-
"""
IAM Auto-Compact - Sistema de compactacion automatica de contexto
IAM: cuando el contexto se llena, resume y crea nueva sesion
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field

from ..config.settings import settings


@dataclass
class CompactResult:
    """Resultado de una compactacion"""
    success: bool
    summary: str
    original_tokens: int
    compacted_tokens: int
    compression_ratio: float
    messages_removed: int
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "success": self.success,
            "summary": self.summary,
            "original_tokens": self.original_tokens,
            "compacted_tokens": self.compacted_tokens,
            "compression_ratio": self.compression_ratio,
            "messages_removed": self.messages_removed,
            "timestamp": self.timestamp
        }


class AutoCompactor:
    """
    Sistema de compactacion automatica de contexto
    IAM: cuando el contexto alcanza 95% del limite,
    automaticamente resume la conversacion
    """
    
    # Porcentaje del contexto que activa la compactacion
    COMPACTION_THRESHOLD = 0.85  # 85%
    
    # Numero minimo de mensajes para compactar
    MIN_MESSAGES_FOR_COMPACTION = 10
    
    # Tokens por caracter estimado
    TOKENS_PER_CHAR = 0.25
    
    def __init__(self, project_path: str = None):
        self.project_path = project_path or os.getcwd()
        self.compact_file = Path(self.project_path) / ".iam" / "compaction_history.json"
        self.compaction_history: List[CompactResult] = []
        self._load_history()
    
    def _load_history(self):
        """Cargar historial de compactaciones"""
        if self.compact_file.exists():
            try:
                with open(self.compact_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                self.compaction_history = [
                    CompactResult(**r) for r in data.get("history", [])
                ]
            except Exception:
                self.compaction_history = []
    
    def _save_history(self):
        """Guardar historial de compactaciones"""
        self.compact_file.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "history": [r.to_dict() for r in self.compaction_history[-50:]],
            "last_updated": datetime.now().isoformat()
        }
        try:
            with open(self.compact_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception:
            pass
    
    def estimate_tokens(self, text: str) -> int:
        """Estimar tokens en un texto"""
        return int(len(text) * self.TOKENS_PER_CHAR)
    
    def should_compact(self, messages: List[Dict[str, str]],
                       context_limit: int = 200000) -> bool:
        """Verificar si se debe compactar el contexto"""
        if len(messages) < self.MIN_MESSAGES_FOR_COMPACTION:
            return False
        
        total_tokens = sum(
            self.estimate_tokens(msg.get("content", ""))
            for msg in messages
        )
        
        usage_ratio = total_tokens / context_limit
        return usage_ratio >= self.COMPACTION_THRESHOLD
    
    def compact(self, messages: List[Dict[str, str]],
                context_limit: int = 200000,
                keep_recent: int = 5) -> CompactResult:
        """
        Compactar la conversacion
        Resume el historial y mantiene solo los mensajes recientes
        """
        if not messages:
            return CompactResult(
                success=False,
                summary="",
                original_tokens=0,
                compacted_tokens=0,
                compression_ratio=0.0,
                messages_removed=0
            )
        
        # Calcular tokens originales
        original_tokens = sum(
            self.estimate_tokens(msg.get("content", ""))
            for msg in messages
        )
        
        # Separar mensajes antiguos y recientes
        if len(messages) <= keep_recent:
            recent_messages = messages
            old_messages = []
        else:
            old_messages = messages[:-keep_recent]
            recent_messages = messages[-keep_recent:]
        
        # Crear resumen de mensajes antiguos
        summary = self._create_summary(old_messages)
        
        # Construir mensajes compactados
        compacted_messages = []
        
        # Agregar resumen como primer mensaje
        if summary:
            compacted_messages.append({
                "role": "system",
                "content": f"[Resumen de conversacion anterior]: {summary}"
            })
        
        # Agregar mensajes recientes
        compacted_messages.extend(recent_messages)
        
        # Calcular tokens compactados
        compacted_tokens = sum(
            self.estimate_tokens(msg.get("content", ""))
            for msg in compacted_messages
        )
        
        # Calcular ratio de compresion
        compression_ratio = 1.0 - (compacted_tokens / original_tokens) if original_tokens > 0 else 0.0
        
        result = CompactResult(
            success=True,
            summary=summary,
            original_tokens=original_tokens,
            compacted_tokens=compacted_tokens,
            compression_ratio=compression_ratio,
            messages_removed=len(old_messages)
        )
        
        self.compaction_history.append(result)
        self._save_history()
        
        return result
    
    def _create_summary(self, messages: List[Dict[str, str]]) -> str:
        """Crear resumen de mensajes"""
        if not messages:
            return ""
        
        summary_parts = []
        
        # Extraer topics principales
        topics = set()
        key_points = []
        
        for msg in messages:
            content = msg.get("content", "")
            role = msg.get("role", "unknown")
            
            # Detectar temas importantes
            if any(keyword in content.lower() for keyword in
                   ["error", "bug", "problema", "fix", "solucion"]):
                topics.add("problemas/soluciones")
            
            if any(keyword in content.lower() for keyword in
                   ["crear", "implementar", "nuevo", "new", "construir", "desarrollar"]):
                topics.add("creacion/implementation")
            
            if any(keyword in content.lower() for keyword in
                   ["explicar", "entender", "como", "que es"]):
                topics.add("explicaciones")
            
            # Guardar puntos clave (primeras lineas de mensajes importantes)
            if role == "user" and len(content) > 50:
                first_line = content.split("\n")[0][:100]
                key_points.append(f"User preguntó: {first_line}")
            
            if role == "assistant" and len(content) > 100:
                # Buscar respuestas con codigo o soluciones
                if any(marker in content for marker in ["```", "def ", "class ", "function"]):
                    key_points.append("IA proporcionó codigo")
        
        # Construir resumen
        if topics:
            summary_parts.append(f"Temas discutidos: {', '.join(topics)}")
        
        if key_points:
            # Tomar ultimos 3 puntos clave
            summary_parts.append("Puntos clave:")
            for point in key_points[-3:]:
                summary_parts.append(f"  - {point}")
        
        summary_parts.append(f"Total de mensajes: {len(messages)}")
        
        return "\n".join(summary_parts)
    
    def get_compaction_stats(self) -> Dict[str, Any]:
        """Obtener estadisticas de compactacion"""
        if not self.compaction_history:
            return {
                "total_compactions": 0,
                "avg_compression_ratio": 0.0,
                "total_messages_removed": 0,
                "last_compaction": None
            }
        
        total_compactions = len(self.compaction_history)
        avg_ratio = sum(r.compression_ratio for r in self.compaction_history) / total_compactions
        total_removed = sum(r.messages_removed for r in self.compaction_history)
        last_compaction = self.compaction_history[-1].timestamp
        
        return {
            "total_compactions": total_compactions,
            "avg_compression_ratio": avg_ratio,
            "total_messages_removed": total_removed,
            "last_compaction": last_compaction
        }
    
    def format_stats(self) -> str:
        """Formatear estadisticas"""
        stats = self.get_compaction_stats()
        
        lines = [
            "ESTADISTICAS DE COMPACTACION",
            "=" * 40,
            f"  Total compactaciones: {stats['total_compactions']}",
            f"  Ratio promedio: {stats['avg_compression_ratio']:.1%}",
            f"  Mensajes eliminados: {stats['total_messages_removed']}",
        ]
        
        if stats['last_compaction']:
            lines.append(f"  Ultima compactacion: {stats['last_compaction'][:19]}")
        
        return "\n".join(lines)


# Instancia global
auto_compactor = AutoCompactor()
