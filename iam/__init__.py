# -*- coding: utf-8 -*-
"""
IAM - Intencional Artificial Multitarea
v3.0.0 - Claude Style with Deep Reasoning

Arquitectura modular con razonamiento profundo y memoria a largo plazo
"""

__version__ = "3.4"
__author__ = "IAM Team"

from .config.settings import settings, COLORS
from .core.session import Session, SessionManager
from .core.agent import Agent, AgentRouter
from .core.reasoning import ReasoningEngine, ThinkingLevel
from .core.memory import MemorySystem
