# -*- coding: utf-8 -*-
"""
IAM Cost Tracking - Sistema de seguimiento de costos por tokens
"""

import json
import os
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field, asdict
from enum import Enum


class ModelProvider(Enum):
    """Proveedores de modelos"""
    PRIMARY = "primary"
    SECONDARY = "secondary"
    TERTIARY = "tertiary"
    LOCAL = "local"
    MULTI = "multi"


# Precios por 1M tokens (USD) - estimados para modelos gratuitos
MODEL_PRICES = {
    "mimo-v2.5-free": {"input": 0.0, "output": 0.0},
    "mimo-v2.5": {"input": 0.5, "output": 1.5},
    "mimo-v2.5-pro": {"input": 1.0, "output": 3.0},
    "ia-terciaria": {"input": 0.075, "output": 0.3},
    "ia-terciaria-v2": {"input": 0.075, "output": 0.3},
    "llama3-8b-8192": {"input": 0.0, "output": 0.0},
    "default": {"input": 0.0, "output": 0.0},
}

# Limites de contexto por modelo (tokens)
MODEL_CONTEXT_LIMITS = {
    "mimo-v2.5-free": 128000,
    "mimo-v2.5": 128000,
    "mimo-v2.5-pro": 128000,
    "ia-terciaria": 1000000,
    "ia-terciaria-v2": 1000000,
    "llama3-8b-8192": 8192,
    "default": 128000,
}


@dataclass
class TokenUsage:
    """Uso de tokens en una peticion"""
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    cached_tokens: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TokenUsage":
        return cls(**data)


@dataclass
class CostEntry:
    """Entrada de costo"""
    id: str
    session_id: str
    model: str
    provider: str
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    cost_usd: float
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    query_preview: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CostEntry":
        return cls(**data)


@dataclass
class SessionStats:
    """Estadisticas de una sesion"""
    session_id: str
    total_prompt_tokens: int = 0
    total_completion_tokens: int = 0
    total_tokens: int = 0
    total_cost_usd: float = 0.0
    query_count: int = 0
    avg_tokens_per_query: float = 0.0
    first_query_at: str = ""
    last_query_at: str = ""
    model_used: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SessionStats":
        return cls(**data)


class CostTracker:
    """
    Sistema de seguimiento de costos
    IAM: trackea tokens y costos por sesion
    """
    
    def __init__(self, project_path: str = None):
        self.project_path = project_path or os.getcwd()
        self.cost_file = Path(self.project_path) / ".iam" / "cost_tracking.json"
        self.entries: List[CostEntry] = []
        self.session_stats: Dict[str, SessionStats] = {}
        self._load_data()
    
    def _load_data(self):
        """Cargar datos desde disco"""
        if self.cost_file.exists():
            try:
                with open(self.cost_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                self.entries = [CostEntry.from_dict(e) for e in data.get("entries", [])]
                for sid, stats_data in data.get("session_stats", {}).items():
                    self.session_stats[sid] = SessionStats.from_dict(stats_data)
            except Exception:
                self.entries = []
                self.session_stats = {}
    
    def _save_data(self):
        """Guardar datos en disco"""
        self.cost_file.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "entries": [e.to_dict() for e in self.entries[-1000:]],  # Mantener ultimas 1000
            "session_stats": {sid: s.to_dict() for sid, s in self.session_stats.items()},
            "last_updated": datetime.now().isoformat()
        }
        try:
            with open(self.cost_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception:
            pass
    
    def calculate_cost(self, model: str, prompt_tokens: int, completion_tokens: int) -> float:
        """Calcular costo en USD"""
        prices = MODEL_PRICES.get(model, MODEL_PRICES["default"])
        
        input_cost = (prompt_tokens / 1_000_000) * prices["input"]
        output_cost = (completion_tokens / 1_000_000) * prices["output"]
        
        return round(input_cost + output_cost, 6)
    
    def get_context_limit(self, model: str) -> int:
        """Obtener limite de contexto del modelo"""
        return MODEL_CONTEXT_LIMITS.get(model, MODEL_CONTEXT_LIMITS["default"])
    
    def track_query(self, session_id: str, model: str, provider: str,
                    prompt_tokens: int, completion_tokens: int,
                    query_preview: str = "") -> CostEntry:
        """Registrar uso de tokens en una query"""
        total_tokens = prompt_tokens + completion_tokens
        cost_usd = self.calculate_cost(model, prompt_tokens, completion_tokens)
        
        entry = CostEntry(
            id=f"cost_{datetime.now().strftime('%Y%m%d%H%M%S_%f')}",
            session_id=session_id,
            model=model,
            provider=provider,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=total_tokens,
            cost_usd=cost_usd,
            query_preview=query_preview[:100]
        )
        
        self.entries.append(entry)
        
        # Actualizar estadisticas de sesion
        if session_id not in self.session_stats:
            self.session_stats[session_id] = SessionStats(
                session_id=session_id,
                first_query_at=datetime.now().isoformat()
            )
        
        stats = self.session_stats[session_id]
        stats.total_prompt_tokens += prompt_tokens
        stats.total_completion_tokens += completion_tokens
        stats.total_tokens += total_tokens
        stats.total_cost_usd += cost_usd
        stats.query_count += 1
        stats.avg_tokens_per_query = stats.total_tokens / stats.query_count
        stats.last_query_at = datetime.now().isoformat()
        stats.model_used = model
        
        self._save_data()
        return entry
    
    def track_tokens(self, session_id: str, model: str, usage: TokenUsage,
                     query_preview: str = "") -> CostEntry:
        """Registrar uso de tokens usando TokenUsage"""
        return self.track_query(
            session_id=session_id,
            model=model,
            provider="unknown",
            prompt_tokens=usage.prompt_tokens,
            completion_tokens=usage.completion_tokens,
            query_preview=query_preview
        )
    
    def get_session_stats(self, session_id: str) -> Optional[SessionStats]:
        """Obtener estadisticas de una sesion"""
        return self.session_stats.get(session_id)
    
    def get_total_cost(self, session_id: str = None) -> float:
        """Obtener costo total"""
        if session_id:
            stats = self.session_stats.get(session_id)
            return stats.total_cost_usd if stats else 0.0
        
        return sum(e.cost_usd for e in self.entries)
    
    def get_total_tokens(self, session_id: str = None) -> int:
        """Obtener total de tokens"""
        if session_id:
            stats = self.session_stats.get(session_id)
            return stats.total_tokens if stats else 0
        
        return sum(e.total_tokens for e in self.entries)
    
    def get_today_cost(self) -> float:
        """Obtener costo de hoy"""
        today = datetime.now().strftime("%Y-%m-%d")
        return sum(
            e.cost_usd for e in self.entries
            if e.timestamp.startswith(today)
        )
    
    def get_today_tokens(self) -> int:
        """Obtener tokens de hoy"""
        today = datetime.now().strftime("%Y-%m-%d")
        return sum(
            e.total_tokens for e in self.entries
            if e.timestamp.startswith(today)
        )
    
    def get_recent_entries(self, limit: int = 10) -> List[CostEntry]:
        """Obtener entradas recientes"""
        return self.entries[-limit:]
    
    def get_cost_by_model(self) -> Dict[str, float]:
        """Obtener costo por modelo"""
        costs = {}
        for entry in self.entries:
            costs[entry.model] = costs.get(entry.model, 0.0) + entry.cost_usd
        return costs
    
    def get_tokens_by_model(self) -> Dict[str, int]:
        """Obtener tokens por modelo"""
        tokens = {}
        for entry in self.entries:
            tokens[entry.model] = tokens.get(entry.model, 0) + entry.total_tokens
        return tokens
    
    def format_cost_display(self, session_id: str = None) -> str:
        """Formatear display de costos"""
        lines = []
        
        # Costo total
        total_cost = self.get_total_cost(session_id)
        total_tokens = self.get_total_tokens(session_id)
        
        lines.append("COSTOS Y USO DE TOKENS")
        lines.append("=" * 40)
        lines.append(f"  Costo total:    ${total_cost:.6f} USD")
        lines.append(f"  Tokens totales: {total_tokens:,}")
        lines.append("")
        
        # Costo de hoy
        today_cost = self.get_today_cost()
        today_tokens = self.get_today_tokens()
        lines.append(f"  Hoy:  ${today_cost:.6f} USD | {today_tokens:,} tokens")
        lines.append("")
        
        # Por modelo
        model_costs = self.get_cost_by_model()
        model_tokens = self.get_tokens_by_model()
        
        if model_costs:
            lines.append("POR MODELO:")
            for model in sorted(model_costs.keys()):
                cost = model_costs[model]
                tokens = model_tokens.get(model, 0)
                lines.append(f"  {model:<25} ${cost:.6f} | {tokens:,} tokens")
        
        # Estadisticas de sesion
        if session_id:
            stats = self.get_session_stats(session_id)
            if stats:
                lines.append("")
                lines.append(f"SESION: {session_id}")
                lines.append(f"  Queries: {stats.query_count}")
                lines.append(f"  Promedio: {stats.avg_tokens_per_query:.0f} tokens/query")
                lines.append(f"  Modelo: {stats.model_used}")
        
        return "\n".join(lines)
    
    def format_cost_bar(self, session_id: str = None) -> str:
        """Formatear barra de costo compacta"""
        total_cost = self.get_total_cost(session_id)
        total_tokens = self.get_total_tokens(session_id)
        
        if total_cost == 0:
            return "[GRATIS]"
        
        return f"${total_cost:.4f} | {total_tokens:,} tokens"
    
    def estimate_cost(self, model: str, estimated_prompt: int,
                      estimated_completion: int) -> Dict[str, Any]:
        """Estimar costo de una query"""
        cost = self.calculate_cost(model, estimated_prompt, estimated_completion)
        limit = self.get_context_limit(model)
        
        return {
            "estimated_cost_usd": cost,
            "estimated_tokens": estimated_prompt + estimated_completion,
            "context_limit": limit,
            "context_usage_pct": ((estimated_prompt + estimated_completion) / limit) * 100,
            "model": model
        }


# Instancia global
cost_tracker = CostTracker()
