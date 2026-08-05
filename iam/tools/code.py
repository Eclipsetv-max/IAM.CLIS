# -*- coding: utf-8 -*-
"""
IAM Code Manager - Gestion de codigo y archivos
    Con mensajes de progreso IAM
"""

import os
from pathlib import Path
from typing import Tuple, Dict, Any, List


class CodeManager:
    """
    Gestion de codigo y archivos
Con mensajes de progreso IAM
    """
    
    def count_lines(self, filepath: str) -> Tuple[bool, Dict[str, int]]:
        """Contar lineas de un archivo"""
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
            
            total = len(lines)
            blank = sum(1 for l in lines if l.strip() == '')
            comment = 0
            code = 0
            
            for line in lines:
                stripped = line.strip()
                if stripped.startswith('#') or stripped.startswith('//') or stripped.startswith('/*'):
                    comment += 1
                elif stripped:
                    code += 1
            
            return True, {
                'total': total,
                'code': code,
                'comments': comment,
                'blank': blank
            }
        except Exception as e:
            return False, {'error': str(e)}
    
    def format_code(self, code: str, language: str = "python") -> str:
        """Formatear codigo"""
        if language.lower() in ["python", "py"]:
            return self._format_python(code)
        elif language.lower() in ["javascript", "js"]:
            return self._format_js(code)
        return code
    
    def _format_python(self, code: str) -> str:
        """Formatear Python basico"""
        lines = code.split('\n')
        formatted = []
        indent = 0
        
        for line in lines:
            stripped = line.strip()
            
            if stripped.startswith(('def ', 'class ', 'if ', 'for ', 'while ', 'try:', 'except', 'finally:', 'with ')):
                if stripped.startswith(('except', 'finally:', 'else:', 'elif')):
                    indent = max(0, indent - 1)
                formatted.append('    ' * indent + stripped)
                if stripped.endswith(':'):
                    indent += 1
            elif stripped.startswith(('return ', 'break', 'continue', 'pass')):
                formatted.append('    ' * indent + stripped)
            else:
                if stripped:
                    formatted.append('    ' * indent + stripped)
                else:
                    formatted.append('')
        
        return '\n'.join(formatted)
    
    def _format_js(self, code: str) -> str:
        """Formatear JavaScript basico"""
        lines = code.split('\n')
        formatted = []
        indent = 0
        
        for line in lines:
            stripped = line.strip()
            
            if stripped.endswith(('{', '[')):
                formatted.append('  ' * indent + stripped)
                indent += 1
            elif stripped.startswith(('}', ']')):
                indent = max(0, indent - 1)
                formatted.append('  ' * indent + stripped)
            else:
                formatted.append('  ' * indent + stripped)
        
        return '\n'.join(formatted)
    
    def detect_language(self, filepath: str) -> str:
        """Detectar lenguaje de programacion"""
        ext_map = {
            '.py': 'python', '.js': 'javascript', '.ts': 'typescript',
            '.html': 'html', '.css': 'css', '.json': 'json',
            '.md': 'markdown', '.txt': 'text', '.jsx': 'react',
            '.tsx': 'typescript-react', '.java': 'java', '.go': 'go',
            '.rs': 'rust', '.c': 'c', '.cpp': 'cpp', '.h': 'c-header',
            '.php': 'php', '.rb': 'ruby', '.sh': 'shell', '.bat': 'batch',
            '.ps1': 'powershell', '.yaml': 'yaml', '.yml': 'yaml',
            '.xml': 'xml', '.sql': 'sql', '.r': 'r', '.swift': 'swift',
            '.kt': 'kotlin', '.scala': 'scala', '.dart': 'dart',
            '.toml': 'toml', '.ini': 'ini', '.cfg': 'config',
            '.env': 'env', '.gitignore': 'git', '.dockerignore': 'docker'
        }
        
        ext = os.path.splitext(filepath)[1].lower()
        return ext_map.get(ext, 'unknown')


# Instancia global
code_manager = CodeManager()
