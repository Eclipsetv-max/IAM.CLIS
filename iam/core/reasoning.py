# -*- coding: utf-8 -*-
"""
IAM Reasoning Engine - Motor de Razonamiento Profundo
Capacidad de análisis, deducción y pensamiento crítico
"""

from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import json
from datetime import datetime


class ThinkingLevel(Enum):
    """Niveles de profundidad de pensamiento"""
    BASIC = "basico"           # Respuesta directa
    ANALYTICAL = "analitico"   # Análisis medio
    DEEP = "profundo"          # Razonamiento profundo
    EXPERT = "experto"         # Nivel experto


@dataclass
class Thought:
    """Representa un paso de pensamiento"""
    step: int
    content: str
    confidence: float  # 0.0 a 1.0
    reasoning: str
    conclusion: str


@dataclass
class AnalysisResult:
    """Resultado de un análisis completo"""
    topic: str
    thoughts: List[Thought]
    conclusion: str
    confidence: float
    alternatives: List[str]
    risks: List[str]
    recommendations: List[str]


class ReasoningEngine:
    """
    Motor de razonamiento inspirado en Chain of Thought
    Permite a la IA pensar paso a paso antes de responder
    """
    
    def __init__(self):
        self.thinking_level = ThinkingLevel.DEEP
        self.memory: List[Dict[str, Any]] = []
        self.context_patterns: Dict[str, List[str]] = {}
        self._load_patterns()
    
    def _load_patterns(self):
        """Cargar patrones de razonamiento"""
        self.context_patterns = {
            "error_debugging": [
                "Identificar el tipo de error",
                "Localizar la línea exacta",
                "Analizar el contexto del error",
                "Determinar la causa raíz",
                "Proponer solución mínima viable",
                "Verificar que la solución no rompe otras partes"
            ],
            "code_review": [
                "Revisar legibilidad",
                "Verificar lógica del negocio",
                "Detectar posibles bugs",
                "Evaluar rendimiento",
                "Sugerir mejoras",
                "Verificar seguridad"
            ],
            "architecture": [
                "Definir requisitos",
                "Identificar componentes",
                "Diseñar flujo de datos",
                "Establecer patrones",
                "Planificar escalabilidad",
                "Documentar decisiones"
            ],
            "problem_solving": [
                "Comprender el problema",
                "Descomponer en sub-problemas",
                "Identificar restricciones",
                "Generar soluciones alternativas",
                "Evaluar trade-offs",
                "Seleccionar mejor opción"
            ]
        }
    
    def analyze(self, query: str, context: Dict[str, Any] = None) -> AnalysisResult:
        """
        Análisis profundo de una consulta
        Chain of Thought: pensar paso a paso
        """
        thoughts = []
        
        # Paso 1: Comprensión del problema
        t1 = self._understand_problem(query, context)
        thoughts.append(t1)
        
        # Paso 2: Identificación de patrones
        t2 = self._identify_patterns(query, context)
        thoughts.append(t2)
        
        # Paso 3: Análisis de contexto
        t3 = self._analyze_context(query, context)
        thoughts.append(t3)
        
        # Paso 4: Generación de soluciones
        t4 = self._generate_solutions(query, context)
        thoughts.append(t4)
        
        # Paso 5: Evaluación crítica
        t5 = self._critical_evaluation(query, thoughts)
        thoughts.append(t5)
        
        # Paso 6: Conclusión
        conclusion = self._draw_conclusion(thoughts)
        
        # Calcular confianza promedio
        confidence = sum(t.confidence for t in thoughts) / len(thoughts)
        
        # Generar alternativas y riesgos
        alternatives = self._generate_alternatives(query, thoughts)
        risks = self._identify_risks(query, thoughts)
        recommendations = self._generate_recommendations(thoughts)
        
        return AnalysisResult(
            topic=query,
            thoughts=thoughts,
            conclusion=conclusion,
            confidence=confidence,
            alternatives=alternatives,
            risks=risks,
            recommendations=recommendations
        )
    
    def think(self, query: str, level=None, context=None) -> AnalysisResult:
        """Alias para analyze - pensar paso a paso"""
        return self.analyze(query, context)
    
    def _understand_problem(self, query: str, context: Dict[str, Any] = None) -> Thought:
        """Paso 1: Comprender el problema"""
        analysis = f"Analizando consulta: '{query[:100]}...'"
        
        # Detectar tipo de consulta
        query_type = self._detect_query_type(query)
        
        # Extraer entidades clave
        entities = self._extract_entities(query)
        
        # Determinar urgencia
        urgency = self._assess_urgency(query)
        
        confidence = 0.9 if entities else 0.7
        
        return Thought(
            step=1,
            content=f"Consulta identificada como {query_type}",
            confidence=confidence,
            reasoning=f"Entidades detectadas: {entities}. Urgencia: {urgency}",
            conclusion=f"Se procesará como {query_type} con prioridad {urgency}"
        )
    
    def _identify_patterns(self, query: str, context: Dict[str, Any] = None) -> Thought:
        """Paso 2: Identificar patrones conocidos"""
        patterns_found = []
        
        # Buscar patrones en la consulta
        for pattern_name, steps in self.context_patterns.items():
            if any(keyword in query.lower() for keyword in pattern_name.split("_")):
                patterns_found.append(pattern_name)
        
        # Detectar similitudes con problemas anteriores
        similar = self._find_similar_in_memory(query)
        
        confidence = 0.85 if patterns_found else 0.6
        
        return Thought(
            step=2,
            content=f"Patrones detectados: {patterns_found or 'ninguno específico'}",
            confidence=confidence,
            reasoning=f"Problemas similares en memoria: {len(similar)}",
            conclusion=f"Se aplicarán patrones de: {patterns_found or 'análisis general'}"
        )
    
    def _analyze_context(self, query: str, context: Dict[str, Any] = None) -> Thought:
        """Paso 3: Analizar contexto disponible"""
        context_factors = []
        
        if context:
            for key, value in context.items():
                if value:
                    context_factors.append(f"{key}: {str(value)[:50]}")
        
        # Factor de conocimiento previo
        prior_knowledge = self._recall_similar(query)
        
        confidence = 0.8 if context_factors else 0.5
        
        return Thought(
            step=3,
            content=f"Contexto analizado: {len(context_factors)} factores",
            confidence=confidence,
            reasoning=f"Factores: {context_factors[:3]}",
            conclusion=f"Conocimiento previo aplicable: {len(prior_knowledge)} items"
        )
    
    def _generate_solutions(self, query: str, context: Dict[str, Any] = None) -> Thought:
        """Paso 4: Generar posibles soluciones"""
        solutions = []
        
        # Solución directa
        solutions.append("Solución directa: respuesta inmediata al problema")
        
        # Solución alternativa
        solutions.append("Solución alternativa: enfoque diferente")
        
        # Solución preventiva
        solutions.append("Solución preventiva: evitar problemas futuros")
        
        confidence = 0.8
        
        return Thought(
            step=4,
            content=f"{len(solutions)} soluciones generadas",
            confidence=confidence,
            reasoning=f"Tipos: directa, alternativa, preventiva",
            conclusion="Múltiples opciones disponibles para seleccionar la mejor"
        )
    
    def _critical_evaluation(self, query: str, thoughts: List[Thought]) -> Thought:
        """Paso 5: Evaluación crítica de las soluciones"""
        avg_confidence = sum(t.confidence for t in thoughts) / len(thoughts)
        
        # Evaluar fortalezas y debilidades
        strengths = []
        weaknesses = []
        
        if avg_confidence > 0.8:
            strengths.append("Alta confianza en el análisis")
        else:
            weaknesses.append("Confianza moderada, se requiere verificación")
        
        # Verificar coherencia
        coherence = self._check_coherence(thoughts)
        
        confidence = avg_confidence * coherence
        
        return Thought(
            step=5,
            content=f"Evaluación crítica completada",
            confidence=confidence,
            reasoning=f"Fortalezas: {strengths}. Debilidades: {weaknesses}",
            conclusion=f"Coherencia del análisis: {coherence:.0%}"
        )
    
    def _draw_conclusion(self, thoughts: List[Thought]) -> str:
        """Paso 6: Extraer conclusión final"""
        if not thoughts:
            return "No se pudo generar conclusión"
        
        # Tomar la conclusión con mayor confianza
        best_thought = max(thoughts, key=lambda t: t.confidence)
        return best_thought.conclusion
    
    def _detect_query_type(self, query: str) -> str:
        """Detectar tipo de consulta"""
        query_lower = query.lower()
        
        if any(w in query_lower for w in ["error", "bug", "falla", "no funciona"]):
            return "debugging"
        elif any(w in query_lower for w in ["crear", "hacer", "diseñar", "programa"]):
            return "desarrollo"
        elif any(w in query_lower for w in ["explicar", "qué es", "cómo funciona"]):
            return "educativo"
        elif any(w in query_lower for w in ["optimizar", "mejorar", "rendimiento"]):
            return "optimización"
        elif any(w in query_lower for w in ["seguridad", "vulnerabilidad", "proteger"]):
            return "seguridad"
        elif any(w in query_lower for w in ["planificar", "estrategia", "roadmap"]):
            return "planificación"
        else:
            return "general"
    
    def _extract_entities(self, query: str) -> List[str]:
        """Extraer entidades clave de la consulta"""
        entities = []
        
        # Lenguajes de programación
        languages = ["python", "javascript", "typescript", "java", "c++", "go", "rust", "ruby", "php"]
        for lang in languages:
            if lang in query.lower():
                entities.append(f"lenguaje:{lang}")
        
        # Tecnologías
        techs = ["react", "vue", "angular", "node", "django", "fastapi", "flask", "express", "docker", "kubernetes"]
        for tech in techs:
            if tech in query.lower():
                entities.append(f"tecnología:{tech}")
        
        # Conceptos
        concepts = ["api", "base de datos", "frontend", "backend", "testing", "deploy"]
        for concept in concepts:
            if concept in query.lower():
                entities.append(f"concepto:{concept}")
        
        return entities
    
    def _assess_urgency(self, query: str) -> str:
        """Evaluar urgencia de la consulta"""
        urgent_keywords = ["urgente", "rápido", "ya", "ahora", "importante", "crítico"]
        if any(w in query.lower() for w in urgent_keywords):
            return "alta"
        elif "?" in query:
            return "media"
        return "normal"
    
    def _find_similar_in_memory(self, query: str) -> List[Dict[str, Any]]:
        """Buscar problemas similares en memoria"""
        similar = []
        query_words = set(query.lower().split())
        
        for item in self.memory:
            item_words = set(item.get("query", "").lower().split())
            overlap = len(query_words & item_words)
            if overlap >= 2:
                similar.append(item)
        
        return similar[:5]
    
    def _recall_similar(self, query: str) -> List[str]:
        """Recordar conocimiento similar"""
        knowledge = []
        
        # Conocimiento base de programación
        if "python" in query.lower():
            knowledge.append("Python: lenguaje interpretado, tipado dinámico")
        if "javascript" in query.lower():
            knowledge.append("JavaScript: lenguaje de scripting web")
        if "api" in query.lower():
            knowledge.append("API: interfaz de programación de aplicaciones")
        if "error" in query.lower():
            knowledge.append("Errores: siempre revisar traceback completo")
        
        return knowledge
    
    def _check_coherence(self, thoughts: List[Thought]) -> float:
        """Verificar coherencia entre pasos de pensamiento"""
        if len(thoughts) < 2:
            return 1.0
        
        # Verificar que las confianzas no varíen demasiado
        confidences = [t.confidence for t in thoughts]
        avg = sum(confidences) / len(confidences)
        variance = sum((c - avg) ** 2 for c in confidences) / len(confidences)
        
        # Menor varianza = mayor coherencia
        coherence = max(0.5, 1.0 - variance)
        return coherence
    
    def _generate_alternatives(self, query: str, thoughts: List[Thought]) -> List[str]:
        """Generar alternativas"""
        alternatives = [
            "Considerar enfoque diferente al problema",
            "Evaluar si el problema es realmente lo que parece",
            "Buscar soluciones en comunidades de desarrollo"
        ]
        return alternatives
    
    def _identify_risks(self, query: str, thoughts: List[Thought]) -> List[str]:
        """Identificar riesgos potenciales"""
        risks = []
        
        if "producción" in query.lower():
            risks.append("Cambios en producción pueden causar downtime")
        if "datos" in query.lower():
            risks.append("Posible pérdida de datos si no se hace backup")
        if "seguridad" in query.lower():
            risks.append("Vulnerabilidades de seguridad si no se revisa")
        
        risks.append("Solución puede no cubrir todos los casos edge")
        
        return risks
    
    def _generate_recommendations(self, thoughts: List[Thought]) -> List[str]:
        """Generar recomendaciones"""
        recommendations = [
            "Implementar la solución de forma incremental",
            "Escribir tests antes de cambiar código existente",
            "Documentar la solución implementada",
            "Revisar con un par antes de desplegar"
        ]
        return recommendations
    
    def store_in_memory(self, query: str, solution: str, tags: List[str] = None):
        """Almacenar en memoria a largo plazo"""
        self.memory.append({
            "query": query,
            "solution": solution,
            "tags": tags or [],
            "timestamp": datetime.now().isoformat()
        })
        
        # Mantener memoria limitada
        if len(self.memory) > 100:
            self.memory = self.memory[-100:]
    
    def format_thinking(self, analysis: AnalysisResult) -> str:
        """Formatear el proceso de pensamiento para mostrar al usuario"""
        output = []
        
        output.append("==================================================")
        output.append("           PROCESO DE PENSAMIENTO")
        output.append("==================================================")
        
        for thought in analysis.thoughts:
            conf_bar = "#" * int(thought.confidence * 10)
            output.append(f"\n  Paso {thought.step}: {thought.content}")
            output.append(f"  Confianza: [{conf_bar}] {thought.confidence:.0%}")
            output.append(f"  Razonamiento: {thought.reasoning}")
            output.append(f"  > {thought.conclusion}")
        
        output.append("\n-----------------------------------------------")
        output.append(f"  CONCLUSION: {analysis.conclusion}")
        output.append(f"  CONFIANZA GLOBAL: {analysis.confidence:.0%}")
        
        if analysis.risks:
            output.append(f"\n  ! RIESGOS IDENTIFICADOS:")
            for risk in analysis.risks[:3]:
                output.append(f"    - {risk}")
        
        output.append("==================================================")
        
        return "\n".join(output)
