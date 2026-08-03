# -*- coding: utf-8 -*-
"""
IAM Patch System - Sistema de patches y diffs
Inspirado en OpenCode: formato de patch custom con fuzzy matching
"""

import os
import re
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import difflib


class ActionType(Enum):
    """Tipos de accion en un patch"""
    ADD = "add"
    DELETE = "delete"
    UPDATE = "update"


@dataclass
class Chunk:
    """Chunk de cambios"""
    orig_index: int
    del_lines: List[str] = field(default_factory=list)
    ins_lines: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "orig_index": self.orig_index,
            "del_lines": self.del_lines,
            "ins_lines": self.ins_lines
        }


@dataclass
class PatchAction:
    """Accion de patch en un archivo"""
    type: ActionType
    new_file: Optional[str] = None
    chunks: List[Chunk] = field(default_factory=list)
    move_path: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.type.value,
            "new_file": self.new_file,
            "chunks": [c.to_dict() for c in self.chunks],
            "move_path": self.move_path
        }


@dataclass
class Patch:
    """Patch completo"""
    actions: Dict[str, PatchAction] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "actions": {k: v.to_dict() for k, v in self.actions.items()}
        }


class PatchParser:
    """
    Parser de formato de patch
    Inspirado en OpenCode: formato custom con fuzzy matching
    """
    
    def __init__(self, current_files: Dict[str, str] = None):
        self.current_files = current_files or {}
        self.lines: List[str] = []
        self.index = 0
        self.patch: Dict[str, PatchAction] = {}
        self.fuzz = 0
    
    def parse(self, text: str) -> Tuple[Patch, int]:
        """
        Parsear texto de patch
        Retorna: (Patch, fuzz_level)
        """
        self.lines = text.strip().split('\n')
        self.index = 0
        self.patch = {}
        self.fuzz = 0
        
        # Buscar inicio
        if not self._find_section('*** Begin Patch'):
            raise ValueError("Invalid patch: missing '*** Begin Patch'")
        
        self._skip_line()
        
        # Parsear secciones
        while self.index < len(self.lines):
            line = self._current_line()
            
            if line.strip() == '*** End Patch':
                break
            
            if line.startswith('*** Update File: '):
                self._parse_update()
            elif line.startswith('*** Add File: '):
                self._parse_add()
            elif line.startswith('*** Delete File: '):
                self._parse_delete()
            else:
                self._skip_line()
        
        return Patch(actions=self.patch), self.fuzz
    
    def _current_line(self) -> str:
        if self.index < len(self.lines):
            return self.lines[self.index]
        return ""
    
    def _skip_line(self):
        self.index += 1
    
    def _find_section(self, section: str) -> bool:
        for i, line in enumerate(self.lines):
            if section in line:
                self.index = i
                return True
        return False
    
    def _parse_update(self):
        """Parsear seccion de update"""
        line = self._current_line()
        filepath = line.replace('*** Update File: ', '').strip()
        self._skip_line()
        
        chunks = []
        current_chunk = None
        
        while self.index < len(self.lines):
            line = self._current_line()
            
            if line.startswith('***') or line.strip() == '*** End Patch':
                break
            
            if line.startswith('@@'):
                # Nuevo chunk
                match = re.match(r'@@ -(\d+)', line)
                if match:
                    orig_index = int(match.group(1)) - 1
                    current_chunk = Chunk(orig_index=orig_index)
                    chunks.append(current_chunk)
                self._skip_line()
                continue
            
            if current_chunk is None:
                self._skip_line()
                continue
            
            if line.startswith('+'):
                current_chunk.ins_lines.append(line[1:])
            elif line.startswith('-'):
                current_chunk.del_lines.append(line[1:])
            elif line.startswith(' '):
                # Linea de contexto, ignorar en este formato
                pass
            else:
                # Linea keeping
                pass
            
            self._skip_line()
        
        if chunks:
            self.patch[filepath] = PatchAction(
                type=ActionType.UPDATE,
                chunks=chunks
            )
    
    def _parse_add(self):
        """Parsear seccion de add"""
        line = self._current_line()
        filepath = line.replace('*** Add File: ', '').strip()
        self._skip_line()
        
        content_lines = []
        
        while self.index < len(self.lines):
            line = self._current_line()
            
            if line.startswith('***') or line.strip() == '*** End Patch':
                break
            
            if line.startswith('+'):
                content_lines.append(line[1:])
            else:
                break
            
            self._skip_line()
        
        self.patch[filepath] = PatchAction(
            type=ActionType.ADD,
            new_file='\n'.join(content_lines)
        )
    
    def _parse_delete(self):
        """Parsear seccion de delete"""
        line = self._current_line()
        filepath = line.replace('*** Delete File: ', '').strip()
        self._skip_line()
        
        self.patch[filepath] = PatchAction(
            type=ActionType.DELETE
        )


class PatchApplier:
    """
    Aplicador de patches con fuzzy matching
    Inspirado en OpenCode: 3-pass fuzzy matching
    """
    
    def __init__(self, files: Dict[str, str] = None):
        self.files = files or {}
    
    def apply(self, patch: Patch) -> Tuple[bool, str, Dict[str, str]]:
        """
        Aplicar patch a los archivos
        Retorna: (exito, mensaje, archivos_modificados)
        """
        modified_files = {}
        
        for filepath, action in patch.actions.items():
            if action.type == ActionType.ADD:
                if filepath in self.files:
                    return False, f"File already exists: {filepath}", {}
                
                self.files[filepath] = action.new_file
                modified_files[filepath] = action.new_file
            
            elif action.type == ActionType.DELETE:
                if filepath not in self.files:
                    return False, f"File not found: {filepath}", {}
                
                del self.files[filepath]
                modified_files[filepath] = None
            
            elif action.type == ActionType.UPDATE:
                if filepath not in self.files:
                    return False, f"File not found: {filepath}", {}
                
                content = self.files[filepath]
                new_content, fuzz = self._apply_chunks(content, action.chunks)
                
                if fuzz > 3:
                    return False, f"Too much fuzz ({fuzz}) for {filepath}", {}
                
                self.files[filepath] = new_content
                modified_files[filepath] = new_content
        
        return True, "Patch applied successfully", modified_files
    
    def _apply_chunks(self, content: str, chunks: List[Chunk]) -> Tuple[str, int]:
        """Aplicar chunks al contenido"""
        lines = content.split('\n')
        total_fuzz = 0
        
        for chunk in chunks:
            result_lines, fuzz = self._apply_chunk(lines, chunk)
            lines = result_lines
            total_fuzz = max(total_fuzz, fuzz)
        
        return '\n'.join(lines), total_fuzz
    
    def _apply_chunk(self, lines: List[str], chunk: Chunk) -> Tuple[List[str], int]:
        """Aplicar un chunk"""
        orig_index = chunk.orig_index
        fuzz = 0
        
        # Buscar contexto con fuzzy matching
        found_index = self._find_context(lines, chunk, orig_index)
        
        if found_index == -1:
            # No encontro contexto, intentar con fuzz
            found_index, fuzz = self._fuzzy_find(lines, chunk, orig_index)
        
        if found_index == -1:
            return lines, 999  # No encontro
        
        # Aplicar cambios
        result = lines[:found_index]
        
        # Agregar lineas insertadas
        result.extend(chunk.ins_lines)
        
        # Saltar lineas eliminadas
        skip_count = len(chunk.del_lines) if chunk.del_lines else 0
        result.extend(lines[found_index + skip_count:])
        
        return result, fuzz
    
    def _find_context(self, lines: List[str], chunk: Chunk, 
                      expected_index: int) -> int:
        """Buscar contexto exacto"""
        if not chunk.del_lines:
            return expected_index
        
        # Buscar en ventana alrededor del indice esperado
        window = range(max(0, expected_index - 5), 
                      min(len(lines), expected_index + 5))
        
        for i in window:
            match = True
            for j, del_line in enumerate(chunk.del_lines):
                if i + j >= len(lines) or lines[i + j].strip() != del_line.strip():
                    match = False
                    break
            if match:
                return i
        
        return -1
    
    def _fuzzy_find(self, lines: List[str], chunk: Chunk, 
                    expected_index: int) -> Tuple[int, int]:
        """Buscar con fuzzy matching (3 niveles)"""
        if not chunk.del_lines:
            return expected_index, 0
        
        # Nivel 1: Buscar sin importar espacios extra
        for i in range(max(0, expected_index - 10), 
                      min(len(lines), expected_index + 10)):
            if self._match_lines(lines, chunk.del_lines, i, trim_spaces=True):
                return i, 1
        
        # Nivel 2: Buscar con trim completo
        for i in range(max(0, expected_index - 20), 
                      min(len(lines), expected_index + 20)):
            if self._match_lines(lines, chunk.del_lines, i, trim_all=True):
                return i, 2
        
        # Nivel 3: Buscar en todo el archivo
        for i in range(len(lines)):
            if self._match_lines(lines, chunk.del_lines, i, trim_all=True):
                return i, 3
        
        return -1, 999
    
    def _match_lines(self, lines: List[str], del_lines: List[str], 
                     start: int, trim_spaces: bool = False, 
                     trim_all: bool = False) -> bool:
        """Verificar si las lineas coinciden"""
        if start + len(del_lines) > len(lines):
            return False
        
        for j, del_line in enumerate(del_lines):
            actual = lines[start + j]
            
            if trim_all:
                actual = ''.join(actual.split())
                del_line = ''.join(del_line.split())
            elif trim_spaces:
                actual = ' '.join(actual.split())
                del_line = ' '.join(del_line.split())
            
            if actual.strip() != del_line.strip():
                return False
        
        return True


class DiffGenerator:
    """
    Generador de diffs
    Inspirado en OpenCode: unified diff con syntax highlighting
    """
    
    @staticmethod
    def generate_diff(old_content: str, new_content: str, 
                      filename: str = "") -> str:
        """Generar diff unificado"""
        old_lines = old_content.splitlines(keepends=True)
        new_lines = new_content.splitlines(keepends=True)
        
        diff = difflib.unified_diff(
            old_lines, new_lines,
            fromfile=f"a/{filename}" if filename else "a/original",
            tofile=f"b/{filename}" if filename else "b/modified",
            lineterm=""
        )
        
        return ''.join(diff)
    
    @staticmethod
    def generate_side_by_side(old_content: str, new_content: str,
                              filename: str = "", 
                              context_lines: int = 3) -> str:
        """Generar diff lado a lado"""
        old_lines = old_content.splitlines()
        new_lines = new_content.splitlines()
        
        matcher = difflib.SequenceMatcher(None, old_lines, new_lines)
        
        output = []
        output.append(f"--- a/{filename}" if filename else "--- original")
        output.append(f"+++ b/{filename}" if filename else "+++ modified")
        output.append("")
        
        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag == 'equal':
                # Lineas iguales (contexto)
                for line in old_lines[i1:i2]:
                    output.append(f"  {line}")
            elif tag == 'delete':
                # Lineas eliminadas
                for line in old_lines[i1:i2]:
                    output.append(f"- {line}")
            elif tag == 'insert':
                # Lineas insertadas
                for line in new_lines[j1:j2]:
                    output.append(f"+ {line}")
            elif tag == 'replace':
                # Lineas reemplazadas
                for line in old_lines[i1:i2]:
                    output.append(f"- {line}")
                for line in new_lines[j1:j2]:
                    output.append(f"+ {line}")
        
        return '\n'.join(output)
    
    @staticmethod
    def count_changes(diff_text: str) -> Tuple[int, int]:
        """Contar cambios en un diff"""
        additions = 0
        removals = 0
        
        for line in diff_text.split('\n'):
            if line.startswith('+') and not line.startswith('+++'):
                additions += 1
            elif line.startswith('-') and not line.startswith('---'):
                removals += 1
        
        return additions, removals
    
    @staticmethod
    def format_stats(additions: int, removals: int) -> str:
        """Formatear estadisticas"""
        parts = []
        if additions > 0:
            parts.append(f"+{additions}")
        if removals > 0:
            parts.append(f"-{removals}")
        return " ".join(parts) if parts else "No changes"


# ==================== FUNCIONES DE UTILIDAD ====================

def apply_patch_to_files(patch_text: str, files: Dict[str, str]) -> Tuple[bool, str, Dict[str, str]]:
    """
    Aplicar patch a archivos
    Retorna: (exito, mensaje, archivos_modificados)
    """
    parser = PatchParser(files)
    try:
        patch, fuzz = parser.parse(patch_text)
    except ValueError as e:
        return False, str(e), {}
    
    applier = PatchApplier(files)
    return applier.apply(patch)


def generate_file_diff(old_path: str, new_content: str) -> str:
    """Generar diff para un archivo"""
    try:
        with open(old_path, 'r', encoding='utf-8') as f:
            old_content = f.read()
    except FileNotFoundError:
        old_content = ""
    
    return DiffGenerator.generate_diff(old_content, new_content, os.path.basename(old_path))
