# -*- coding: utf-8 -*-
"""
IAM Code Analyzer - Analizador de código inteligente
Detecta problemas, sugiere mejoras y optimiza código
"""

import re
import ast
from typing import Dict, Any, List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class CodeIssue:
    """Problema encontrado en el código"""
    line: int
    column: int
    severity: str  # "error", "warning", "info", "suggestion"
    category: str
    message: str
    suggestion: str = ""


class CodeAnalyzer:
    """
    Analizador de código inteligente
    Detecta problemas y sugiere mejoras
    """
    
    def __init__(self):
        self.python_rules = self._init_python_rules()
        self.js_rules = self._init_js_rules()
    
    def _init_python_rules(self) -> List[Dict[str, Any]]:
        """Inicializar reglas de Python"""
        return [
            {
                "pattern": r"print\s*\(",
                "severity": "info",
                "category": "debug",
                "message": "Uso de print() detectado",
                "suggestion": "Considerar usar logging en producción"
            },
            {
                "pattern": r"except\s*:",
                "severity": "warning",
                "category": "error_handling",
                "message": "Excepción genérica sin tipo",
                "suggestion": "Especificar el tipo de excepción (except Exception:)"
            },
            {
                "pattern": r"eval\s*\(",
                "severity": "error",
                "category": "security",
                "message": "Uso de eval() detectado",
                "suggestion": "eval() puede ser inseguro. Usar alternativas más seguras"
            },
            {
                "pattern": r"exec\s*\(",
                "severity": "error",
                "category": "security",
                "message": "Uso de exec() detectado",
                "suggestion": "exec() puede ser inseguro. Evitar su uso"
            },
            {
                "pattern": r"import \*",
                "severity": "warning",
                "category": "best_practice",
                "message": "Import wildcard (*) detectado",
                "suggestion": "Importar solo lo necesario: from module import name"
            },
            {
                "pattern": r"==\s*None",
                "severity": "info",
                "category": "pythonic",
                "message": "Comparación con None usando ==",
                "suggestion": "Usar 'is None' en su lugar"
            },
            {
                "pattern": r"!=\s*None",
                "severity": "info",
                "category": "pythonic",
                "message": "Comparación con None usando !=",
                "suggestion": "Usar 'is not None' en su lugar"
            },
            {
                "pattern": r"def \w+\([^)]*\)\s*:",
                "severity": "info",
                "category": "documentation",
                "message": "Función sin docstring",
                "suggestion": "Agregar docstring para documentar la función"
            },
            {
                "pattern": r"TODO|FIXME|HACK|XXX",
                "severity": "info",
                "category": "maintenance",
                "message": "Comentario TODO/FIXME detectado",
                "suggestion": "Resolver pendientes antes de producción"
            },
            {
                "pattern": r"password\s*=\s*[\"']",
                "severity": "error",
                "category": "security",
                "message": "Password hardcodeado detectado",
                "suggestion": "Usar variables de entorno o secrets manager"
            }
        ]
    
    def _init_js_rules(self) -> List[Dict[str, Any]]:
        """Inicializar reglas de JavaScript"""
        return [
            {
                "pattern": r"console\.log\s*\(",
                "severity": "info",
                "category": "debug",
                "message": "console.log() en código",
                "suggestion": "Eliminar console.log() en producción"
            },
            {
                "pattern": r"var\s+",
                "severity": "warning",
                "category": "modern_js",
                "message": "Uso de 'var' detectado",
                "suggestion": "Usar 'const' o 'let' en su lugar"
            },
            {
                "pattern": r"==(?!=)",
                "severity": "warning",
                "category": "type_safety",
                "message": "Comparación loose equality (==)",
                "suggestion": "Usar strict equality (===)"
            },
            {
                "pattern": r"!=(?!=)",
                "severity": "warning",
                "category": "type_safety",
                "message": "Comparación loose inequality (!=)",
                "suggestion": "Usar strict inequality (!==)"
            },
            {
                "pattern": r"document\.write\s*\(",
                "severity": "error",
                "category": "security",
                "message": "document.write() detectado",
                "suggestion": "Usar DOM manipulation moderna (textContent, innerHTML)"
            },
            {
                "pattern": r"eval\s*\(",
                "severity": "error",
                "category": "security",
                "message": "eval() detectado en JavaScript",
                "suggestion": "eval() es inseguro. Usar alternativas"
            },
            {
                "pattern": r"innerHTML\s*=",
                "severity": "warning",
                "category": "security",
                "message": "Uso de innerHTML detectado",
                "suggestion": "Puede causar XSS. Usar textContent o sanitizar"
            },
            {
                "pattern": r"fetch\s*\(",
                "severity": "info",
                "category": "async",
                "message": "fetch() sin manejo de errores",
                "suggestion": "Agregar .catch() o try/catch con async/await"
            }
        ]
    
    def analyze_python(self, code: str) -> List[CodeIssue]:
        """Analizar código Python"""
        issues = []
        lines = code.split('\n')
        
        for i, line in enumerate(lines, 1):
            for rule in self.python_rules:
                if re.search(rule["pattern"], line):
                    issues.append(CodeIssue(
                        line=i,
                        column=0,
                        severity=rule["severity"],
                        category=rule["category"],
                        message=rule["message"],
                        suggestion=rule["suggestion"]
                    ))
        
        # Análisis AST para problemas más complejos
        try:
            tree = ast.parse(code)
            ast_issues = self._analyze_python_ast(tree)
            issues.extend(ast_issues)
        except SyntaxError:
            issues.append(CodeIssue(
                line=0,
                column=0,
                severity="error",
                category="syntax",
                message="Error de sintaxis en el código Python",
                suggestion="Verificar la sintaxis del código"
            ))
        
        return issues
    
    def _analyze_python_ast(self, tree: ast.AST) -> List[CodeIssue]:
        """Analizar AST de Python"""
        issues = []
        
        for node in ast.walk(tree):
            # Detectar funciones sin docstring
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if not ast.get_docstring(node):
                    issues.append(CodeIssue(
                        line=node.lineno,
                        column=node.col_offset,
                        severity="info",
                        category="documentation",
                        message=f"Función '{node.name}' sin docstring",
                        suggestion="Agregar docstring para documentar la función"
                    ))
            
            # Detectar clases sin docstring
            if isinstance(node, ast.ClassDef):
                if not ast.get_docstring(node):
                    issues.append(CodeIssue(
                        line=node.lineno,
                        column=node.col_offset,
                        severity="info",
                        category="documentation",
                        message=f"Clase '{node.name}' sin docstring",
                        suggestion="Agregar docstring para documentar la clase"
                    ))
        
        return issues
    
    def analyze_javascript(self, code: str) -> List[CodeIssue]:
        """Analizar código JavaScript"""
        issues = []
        lines = code.split('\n')
        
        for i, line in enumerate(lines, 1):
            for rule in self.js_rules:
                if re.search(rule["pattern"], line):
                    issues.append(CodeIssue(
                        line=i,
                        column=0,
                        severity=rule["severity"],
                        category=rule["category"],
                        message=rule["message"],
                        suggestion=rule["suggestion"]
                    ))
        
        return issues
    
    def analyze(self, code: str, language: str = "python") -> List[CodeIssue]:
        """Analizar código según el lenguaje"""
        if language.lower() in ["python", "py"]:
            return self.analyze_python(code)
        elif language.lower() in ["javascript", "js", "typescript", "ts"]:
            return self.analyze_javascript(code)
        else:
            return []
    
    def get_summary(self, issues) -> Dict[str, Any]:
        """Obtener resumen del análisis - acepta lista de CodeIssue o filepath"""
        if isinstance(issues, str):
            # Si es un filepath, analizar el archivo
            try:
                with open(issues, 'r', encoding='utf-8', errors='ignore') as f:
                    code = f.read()
                ext = issues.rsplit('.', 1)[-1].lower() if '.' in issues else 'python'
                if ext in ['js', 'javascript', 'ts', 'typescript']:
                    issues = self.analyze_javascript(code)
                else:
                    issues = self.analyze_python(code)
            except Exception:
                return {"total": 0, "errors": 0, "warnings": 0, "info": 0, "categories": {}}
        
        summary = {
            "total": len(issues),
            "errors": len([i for i in issues if i.severity == "error"]),
            "warnings": len([i for i in issues if i.severity == "warning"]),
            "info": len([i for i in issues if i.severity == "info"]),
            "categories": {}
        }
        
        for issue in issues:
            cat = issue.category
            summary["categories"][cat] = summary["categories"].get(cat, 0) + 1
        
        return summary
    
    def format_issues(self, issues: List[CodeIssue]) -> str:
        """Formatear problemas encontrados"""
        if not issues:
            return "[OK] No se encontraron problemas en el codigo."
        
        severity_colors = {
            "error": "\033[31m",
            "warning": "\033[33m",
            "info": "\033[36m",
            "suggestion": "\033[32m"
        }
        
        severity_icons = {
            "error": "[ERROR]",
            "warning": "[!]",
            "info": "[i]",
            "suggestion": "[*]"
        }
        
        output = ["\n============================================================="]
        output.append("              ANALISIS DE CODIGO")
        output.append("=============================================================\n")
        
        # Resumen
        summary = self.get_summary(issues)
        output.append(f"  Resumen: {summary['total']} problemas encontrados")
        output.append(f"     Errores: {summary['errors']}")
        output.append(f"     Advertencias: {summary['warnings']}")
        output.append(f"     Info: {summary['info']}\n")
        
        # Detalles
        output.append("-------------------------------------------------------------")
        
        for issue in sorted(issues, key=lambda i: ({"error": 0, "warning": 1, "info": 2, "suggestion": 3}[i.severity])):
            icon = severity_icons.get(issue.severity, "-")
            color = severity_colors.get(issue.severity, "")
            
            output.append(f"\n  {icon} Linea {issue.line}: {issue.message}")
            output.append(f"     Categoria: {issue.category}")
            if issue.suggestion:
                output.append(f"     * {issue.suggestion}")
        
        output.append("\n=============================================================")
        
        return "\n".join(output)
