# -*- coding: utf-8 -*-
"""
IAM - Inteligencia Artificial Multitarea
v4.1 - Multi-AI Assistant

Arquitectura modular con razonamiento profundo, memoria a largo plazo,
historial de archivos, cost tracking, auto-compaction y sub-agentes
"""

__version__ = "4.1"
__author__ = "IAM Team"

from .config.settings import settings, COLORS
from .core.session import Session, SessionManager
from .core.agent import Agent, AgentRouter
from .core.reasoning import ReasoningEngine, ThinkingLevel
from .core.memory import MemorySystem
