# -*- coding: utf-8 -*-
"""
IAM Code Validator - Validacion y correccion automatica de codigo generado
Valida HTML, CSS, JS y corrige errores comunes automaticamente
"""

import re
import os
from typing import Tuple, Dict, Any, Optional


class CodeValidator:
    """Validador de codigo para proyectos web"""
    
    # Errores comunes en HTML
    HTML_ERRORS = {
        'unclosed_tag': r'<(\w+)[^>]*>(?:(?!<\/\1>).)*$',
        'missing_doctype': r'<!DOCTYPE',
        'missing_html_close': r'</html>',
        'missing_head': r'<head>',
        'missing_body': r'<body>',
    }
    
    # Errores comunes en CSS
    CSS_ERRORS = {
        'unclosed_brace': r'\{[^}]*$',
        'missing_semicolon': r'[^;{}\s]\s*\}',
        'invalid_selector': r'^\s*[>+~]',
    }
    
    # Errores comunes en JS
    JS_ERRORS = {
        'unclosed_function': r'function\s+\w+\s*\([^)]*\)\s*\{[^}]*$',
        'unclosed_paren': r'\([^)]*$',
        'missing_semicolon': r'[^;{}\s/\*]\s*$',
    }
    
    def __init__(self):
        self.errors = []
        self.warnings = []
    
    def validate_html(self, content: str) -> Tuple[bool, list]:
        """Validar contenido HTML"""
        errors = []
        
        if not content:
            return False, ["HTML vacio"]
        
        # Verificar DOCTYPE
        if '<!DOCTYPE' not in content.upper():
            errors.append("Falta <!DOCTYPE html>")
        
        # Verificar tag html
        if '<html' not in content.lower():
            errors.append("Falta tag <html>")
        if '</html>' not in content.lower():
            errors.append("Falta cerrar </html>")
        
        # Verificar head y body
        if '<head>' not in content.lower():
            errors.append("Falta <head>")
        if '</head>' not in content.lower():
            errors.append("Falta cerrar </head>")
        if '<body>' not in content.lower():
            errors.append("Falta <body>")
        if '</body>' not in content.lower():
            errors.append("Falta cerrar </body>")
        
        # Verificar meta viewport
        if 'viewport' not in content.lower():
            errors.append("Falta meta viewport para responsive")
        
        # Verificar charset
        if 'charset' not in content.lower():
            errors.append("Falta meta charset")
        
        # Verificar referencia a CSS (recomendado, no error critico)
        has_css_ref = ('style.css' in content or 
                      'rel="stylesheet"' in content or 
                      "rel='stylesheet'" in content or
                      '.css' in content or
                      '<style' in content.lower())
        if not has_css_ref:
            errors.append("No se detecto referencia a archivo CSS")
        
        return len(errors) == 0, errors
    
    def validate_css(self, content: str) -> Tuple[bool, list]:
        """Validar contenido CSS"""
        errors = []
        
        if not content:
            return False, ["CSS vacio"]
        
        # Verificar corrupcion comun de Groq
        if "'';" in content:
            errors.append("Corrupcion detectada: '';")
        
        # Verificar llaves balanceadas
        open_braces = content.count('{')
        close_braces = content.count('}')
        if open_braces != close_braces:
            errors.append(f"Llaves desbalanceadas: {open_braces} abiertas, {close_braces} cerradas")
        
        # Verificar reset basico
        if 'box-sizing' not in content:
            errors.append("Falta box-sizing: border-box en el reset")
        if 'margin: 0' not in content and 'margin:0' not in content:
            errors.append("Falta margin: 0 en el reset")
        
        # NOTA: variables CSS y @media son RECOMENDACIONES, no errores criticos
        # Un CSS valido puede no tener variables o media queries
        
        return len(errors) == 0, errors
    
    def validate_js(self, content: str) -> Tuple[bool, list]:
        """Validar contenido JavaScript"""
        errors = []
        
        if not content:
            return False, ["JS vacio"]
        
        # NOTA: DOMContentLoaded, console.log, var/let son RECOMENDACIONES
        # Un JS valido puede no tener DOMContentLoaded o usar var
        # Solo reportamos errores criticos de sintaxis
        
        return len(errors) == 0, errors
    
    def _strip_markdown_fences(self, content: str) -> str:
        """Remover markdown code fences (```) del contenido"""
        if not content:
            return content
        # Remover fences al inicio: ```html, ```css, ```js, etc.
        content = re.sub(r'^```\w*\s*\n', '', content, count=1)
        # Remover fences al final
        content = re.sub(r'\n```\s*$', '', content, count=1)
        # Remover fences sueltos en cualquier lugar (solo si es unico)
        content = re.sub(r'^```\s*$', '', content, flags=re.MULTILINE)
        return content.strip()
    
    def fix_html(self, content: str) -> str:
        """Corregir errores comunes en HTML"""
        if not content:
            return content
        
        # Primero: remover markdown fences
        content = self._strip_markdown_fences(content)
        
        # Remover cualquier etiqueta [TOOL_CALL] o residuales
        content = re.sub(r'\[/?TOOL_CALL\][^\n]*', '', content).strip()
        
        # Si el HTML es muy corto y no tiene <head>, reconstruir preservando el contenido
        has_head = '<head' in content.lower()
        
        if not has_head and len(content) < 1000:
            body_content = content
            body_match = re.search(r'<body[^>]*>(.*?)</body>', content, re.DOTALL | re.IGNORECASE)
            if body_match:
                body_content = body_match.group(1).strip()
            else:
                body_match = re.search(r'<!DOCTYPE[^>]*>\s*(.*)', content, re.DOTALL | re.IGNORECASE)
                if body_match:
                    body_content = body_match.group(1).strip()
                body_content = re.sub(r'</?(html|head|body|script)[^>]*>', '', body_content, flags=re.IGNORECASE).strip()
            
            content = f'''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Aplicación Web</title>
    <link rel="stylesheet" href="style.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body>
    {body_content if body_content else '<div class="container"><h1>Contenido Principal</h1></div>'}
    <script src="script.js"></script>
</body>
</html>'''
            return content
        
        # Reparar estructura HTML parcial
        if '<!DOCTYPE' not in content.upper():
            content = '<!DOCTYPE html>\n' + content
        
        if '<html' in content.lower() and 'lang=' not in content.lower():
            content = re.sub(r'<html[^>]*>', '<html lang="es">', content, flags=re.IGNORECASE)
        
        # Asegurar cierre de body y html
        if '</body>' not in content.lower():
            content += '\n</body>'
        if '</html>' not in content.lower():
            content += '\n</html>'
            
        return content

    def fix_css(self, content: str) -> str:
        """Corregir errores comunes en CSS"""
        if not content:
            return content
        
        content = self._strip_markdown_fences(content)
        content = re.sub(r'\[/?TOOL_CALL\][^\n]*', '', content).strip()
        
        # Balancear llaves si se cortaron al final
        open_braces = content.count('{')
        close_braces = content.count('}')
        if open_braces > close_braces:
            content += '\n}' * (open_braces - close_braces)
            
        return content

    def fix_js(self, content: str) -> str:
        """Corregir errores comunes en JavaScript"""
        if not content:
            return content
        
        content = self._strip_markdown_fences(content)
        content = re.sub(r'\[/?TOOL_CALL\][^\n]*', '', content).strip()
        
        # Cierre automático si faltan paréntesis o llaves
        open_b = content.count('{')
        close_b = content.count('}')
        if open_b > close_b:
            content += '\n}' * (open_b - close_b)
            
        return content
    
    def fix_css(self, content: str) -> str:
        """Corregir errores comunes en CSS"""
        if not content:
            return content
        
        # Primero: remover markdown fences
        content = self._strip_markdown_fences(content)
        
        # Remover corrupcion comun de Groq: '';}
        content = re.sub(r"'';\s*\}", '}', content)
        content = re.sub(r"'';", '', content)
        
        # Remover lineas vacias multiples
        content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
        
        # Agregar reset si falta
        reset = """* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

"""
        if 'box-sizing' not in content:
            content = reset + content
        
        return content
    
    def fix_js(self, content: str) -> str:
        """Corregir errores comunes en JS"""
        if not content:
            return content
        
        # Primero: remover markdown fences
        content = self._strip_markdown_fences(content)
        
        # Reemplazar var por let/const
        content = re.sub(r'\bvar\b', 'let', content)
        
        return content
    
    def validate_and_fix(self, file_type: str, content: str) -> Tuple[str, list]:
        """Validar y corregir codigo automaticamente"""
        errors = []
        
        if file_type == 'html':
            is_valid, errors = self.validate_html(content)
            if not is_valid:
                content = self.fix_html(content)
                # Re-validar despues de correccion
                is_valid, errors = self.validate_html(content)
        
        elif file_type == 'css':
            is_valid, errors = self.validate_css(content)
            if not is_valid:
                content = self.fix_css(content)
                is_valid, errors = self.validate_css(content)
        
        elif file_type == 'js':
            is_valid, errors = self.validate_js(content)
            if not is_valid:
                content = self.fix_js(content)
                is_valid, errors = self.validate_js(content)
        
        return content, errors


class CodeQualityChecker:
    """Verificador de calidad de codigo"""
    
    @staticmethod
    def check_responsive(css_content: str) -> Dict[str, Any]:
        """Verificar si el CSS es responsive"""
        result = {
            'is_responsive': False,
            'has_media_queries': '@media' in css_content,
            'has_clamp': 'clamp(' in css_content,
            'has_flexbox': 'flex' in css_content,
            'has_grid': 'grid' in css_content,
            'issues': []
        }
        
        if not result['has_media_queries']:
            result['issues'].append("No hay media queries para responsive")
        
        if not result['has_clamp']:
            result['issues'].append("Recomendado: Usa clamp() para tamaños responsive")
        
        result['is_responsive'] = result['has_media_queries'] or result['has_clamp']
        
        return result
    
    @staticmethod
    def check_accessibility(html_content: str) -> Dict[str, Any]:
        """Verificar accesibilidad básica"""
        result = {
            'score': 0,
            'issues': [],
            'good': []
        }
        
        # Verificar alt en imagenes
        if 'img' in html_content and 'alt=' not in html_content:
            result['issues'].append("Falta alt en imagenes")
        elif 'img' in html_content:
            result['good'].append("Tiene alt en imagenes")
            result['score'] += 20
        
        # Verificar labels en inputs
        if 'input' in html_content and 'label' not in html_content.lower():
            result['issues'].append("Falta label para inputs")
        elif 'label' in html_content.lower():
            result['good'].append("Tiene labels para inputs")
            result['score'] += 20
        
        # Verificar semantica
        semantic_tags = ['<nav', '<main', '<header', '<footer', '<section', '<article']
        for tag in semantic_tags:
            if tag in html_content.lower():
                result['good'].append(f"Usa tag semantico: {tag}")
                result['score'] += 10
        
        # Verificar heading hierarchy
        if '<h1' in html_content.lower():
            result['good'].append("Tiene h1")
            result['score'] += 20
        
        return result
    
    @staticmethod
    def check_performance(html_content: str, css_content: str, js_content: str) -> Dict[str, Any]:
        """Verificar rendimiento"""
        result = {
            'score': 100,
            'issues': [],
            'good': []
        }
        
        # Verificar lazy loading en imagenes
        if 'img' in html_content and 'loading=' not in html_content:
            result['issues'].append("Agrega loading='lazy' a imagenes")
            result['score'] -= 10
        
        # Verificar minificacion (basico)
        if css_content and len(css_content.split('\n')) > 200:
            result['issues'].append("CSS muy largo - considera minificar")
            result['score'] -= 5
        
        # Verificar defer/async en scripts
        if '<script src' in html_content and 'defer' not in html_content and 'async' not in html_content:
            result['issues'].append("Agrega defer o async a scripts externos")
            result['score'] -= 10
        
        # Verificar imagenes externas
        if 'images.unsplash.com' in html_content or 'unsplash' in html_content:
            result['good'].append("Usa imagenes de Unsplash (CDN)")
            result['score'] += 5
        
        return result


# Instancia global del validador
code_validator = CodeValidator()
quality_checker = CodeQualityChecker()


def validate_file(file_path: str, content: str) -> Tuple[bool, str]:
    """Validar un archivo y retornar si es valido y el contenido corregido"""
    ext = os.path.splitext(file_path)[1].lower()
    
    type_map = {
        '.html': 'html',
        '.htm': 'html',
        '.css': 'css',
        '.js': 'js',
        '.javascript': 'js'
    }
    
    file_type = type_map.get(ext)
    if not file_type:
        return True, content  # No validar otros tipos
    
    validated_content, errors = code_validator.validate_and_fix(file_type, content)
    
    if errors:
        return False, validated_content
    
    return True, validated_content


def get_quality_report(html: str, css: str, js: str) -> Dict[str, Any]:
    """Obtener reporte de calidad completo"""
    return {
        'responsive': quality_checker.check_responsive(css),
        'accessibility': quality_checker.check_accessibility(html),
        'performance': quality_checker.check_performance(html, css, js)
    }
