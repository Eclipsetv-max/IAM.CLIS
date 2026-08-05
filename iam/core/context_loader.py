# -*- coding: utf-8 -*-
"""
IAM Context Loader - Carga automatica de archivos de contexto
IAM: auto-carga archivos de configuracion
"""

import os
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field


# Archivos de contexto buscados (en orden de prioridad)
CONTEXT_FILE_PATTERNS = [
    # IAM
    "iam.md",
    "iam.local.md",
    "IAM.md",
    "IAM.local.md",
    
    # Claude
    "CLAUDE.md",
    "CLAUDE.local.md",
    "claude.md",
    "claude.local.md",
    
    # Cursor
    ".cursorrules",
    "cursor/rules/",
    
    # Copilot
    ".github/copilot-instructions.md",
    
    # IAM
    "IAM.md",
    "iam.md",
    "IAM.local.md",
    
    # Generico
    "AGENTS.md",
    "agents.md",
    "CONTRIBUTING.md",
    "contributing.md",
]

# Archivos de configuracion del proyecto
PROJECT_CONFIG_FILES = [
    "package.json",
    "requirements.txt",
    "Cargo.toml",
    "go.mod",
    "pom.xml",
    "build.gradle",
    "pyproject.toml",
    "setup.py",
    "Gemfile",
    "composer.json",
]


@dataclass
class ContextFile:
    """Archivo de contexto cargado"""
    path: str
    content: str
    size: int
    modified_at: str
    priority: int  # 0 = maxima prioridad
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "path": self.path,
            "size": self.size,
            "modified_at": self.modified_at,
            "priority": self.priority
        }


@dataclass
class ProjectContext:
    """Contexto completo del proyecto"""
    project_path: str
    context_files: List[ContextFile] = field(default_factory=list)
    project_config: Dict[str, Any] = field(default_factory=dict)
    project_type: str = "unknown"
    loaded_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "project_path": self.project_path,
            "context_files": [f.to_dict() for f in self.context_files],
            "project_config": self.project_config,
            "project_type": self.project_type,
            "loaded_at": self.loaded_at
        }


class ContextLoader:
    """
    Sistema de carga de contexto de proyecto
    IAM: auto-carga archivos
    """
    
    MAX_CONTEXT_SIZE = 50000  # Maximo 50KB de contexto combinado
    
    def __init__(self, project_path: str = None):
        self.project_path = project_path or os.getcwd()
        self.context_dir = Path(self.project_path) / ".iam"
        self.context_cache_file = self.context_dir / "context_cache.json"
        self.project_context: Optional[ProjectContext] = None
    
    def load_project_context(self, force: bool = False) -> ProjectContext:
        """Cargar contexto completo del proyecto"""
        # Verificar cache
        if not force and self.context_cache_file.exists():
            try:
                with open(self.context_cache_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                cached = ProjectContext(**data)
                # Verificar si es reciente (menos de 1 hora)
                loaded_at = datetime.fromisoformat(cached.loaded_at)
                if (datetime.now() - loaded_at).seconds < 3600:
                    self.project_context = cached
                    return cached
            except Exception:
                pass
        
        # Crear nuevo contexto
        context = ProjectContext(project_path=self.project_path)
        
        # Buscar archivos de contexto
        context.context_files = self._find_context_files()
        
        # Detectar tipo de proyecto
        context.project_type = self._detect_project_type()
        
        # Cargar configuracion del proyecto
        context.project_config = self._load_project_config()
        
        # Guardar cache
        self._save_cache(context)
        self.project_context = context
        
        return context
    
    def _find_context_files(self) -> List[ContextFile]:
        """Buscar archivos de contexto en el proyecto"""
        context_files = []
        project_path = Path(self.project_path)
        
        for priority, pattern in enumerate(CONTEXT_FILE_PATTERNS):
            if pattern.endswith("/"):
                # Es un directorio, buscar archivos dentro
                dir_path = project_path / pattern
                if dir_path.is_dir():
                    for file_path in dir_path.glob("*.md"):
                        context_file = self._load_context_file(file_path, priority)
                        if context_file:
                            context_files.append(context_file)
            else:
                # Es un archivo
                file_path = project_path / pattern
                if file_path.is_file():
                    context_file = self._load_context_file(file_path, priority)
                    if context_file:
                        context_files.append(context_file)
        
        # Ordenar por prioridad
        context_files.sort(key=lambda f: f.priority)
        
        # Limitar tamano total
        total_size = 0
        filtered_files = []
        for f in context_files:
            if total_size + f.size <= self.MAX_CONTEXT_SIZE:
                filtered_files.append(f)
                total_size += f.size
            else:
                break
        
        return filtered_files
    
    def _load_context_file(self, path: Path, priority: int) -> Optional[ContextFile]:
        """Cargar un archivo de contexto"""
        try:
            stat = path.stat()
            content = path.read_text(encoding='utf-8', errors='ignore')
            
            return ContextFile(
                path=str(path),
                content=content,
                size=stat.st_size,
                modified_at=datetime.fromtimestamp(stat.st_mtime).isoformat(),
                priority=priority
            )
        except Exception:
            return None
    
    def _detect_project_type(self) -> str:
        """Detectar tipo de proyecto"""
        project_path = Path(self.project_path)
        
        # Verificar archivos de configuracion
        if (project_path / "package.json").exists():
            return "nodejs"
        elif (project_path / "requirements.txt").exists() or \
             (project_path / "pyproject.toml").exists() or \
             (project_path / "setup.py").exists():
            return "python"
        elif (project_path / "Cargo.toml").exists():
            return "rust"
        elif (project_path / "go.mod").exists():
            return "go"
        elif (project_path / "pom.xml").exists():
            return "java"
        elif any(list(project_path.glob("*.csproj")) + list(project_path.glob("*.sln"))):
            return "csharp"
        elif (project_path / "Gemfile").exists():
            return "ruby"
        elif (project_path / "composer.json").exists():
            return "php"
        
        return "unknown"
    
    def _load_project_config(self) -> Dict[str, Any]:
        """Cargar configuracion del proyecto"""
        config = {}
        project_path = Path(self.project_path)
        
        # package.json
        pkg_json = project_path / "package.json"
        if pkg_json.exists():
            try:
                with open(pkg_json, 'r', encoding='utf-8') as f:
                    pkg_data = json.load(f)
                config["name"] = pkg_data.get("name", "")
                config["version"] = pkg_data.get("version", "")
                config["description"] = pkg_data.get("description", "")
                config["scripts"] = list(pkg_data.get("scripts", {}).keys())
                config["dependencies"] = list(pkg_data.get("dependencies", {}).keys())
            except Exception:
                pass
        
        # requirements.txt
        req_txt = project_path / "requirements.txt"
        if req_txt.exists():
            try:
                with open(req_txt, 'r', encoding='utf-8') as f:
                    lines = [l.strip() for l in f if l.strip() and not l.startswith('#')]
                config["dependencies"] = [l.split('==')[0].split('>=')[0] for l in lines]
            except Exception:
                pass
        
        return config
    
    def _save_cache(self, context: ProjectContext):
        """Guardar cache de contexto"""
        self.context_dir.mkdir(parents=True, exist_ok=True)
        try:
            with open(self.context_cache_file, 'w', encoding='utf-8') as f:
                json.dump(context.to_dict(), f, indent=2, ensure_ascii=False)
        except Exception:
            pass
    
    def get_context_prompt(self) -> str:
        """Obtener prompt de contexto para la IA"""
        if not self.project_context:
            self.load_project_context()
        
        context = self.project_context
        parts = []
        
        # Informacion del proyecto
        parts.append(f"PROYECTO: {os.path.basename(context.project_path)}")
        parts.append(f"Tipo: {context.project_type}")
        
        if context.project_config.get("name"):
            parts.append(f"Nombre: {context.project_config['name']}")
        
        if context.project_config.get("description"):
            parts.append(f"Descripcion: {context.project_config['description']}")
        
        # Archivos de contexto
        if context.context_files:
            parts.append(f"\nARCHIVOS DE CONTEXTO ({len(context.context_files)}):")
            for cf in context.context_files:
                # Incluir contenido del archivo
                parts.append(f"\n--- {os.path.basename(cf.path)} ---")
                parts.append(cf.content[:5000])  # Maximo 5KB por archivo
                parts.append("---")
        
        # Dependencias
        deps = context.project_config.get("dependencies", [])
        if deps:
            parts.append(f"\nDEPENDENCIAS: {', '.join(deps[:20])}")
        
        # Scripts
        scripts = context.project_config.get("scripts", [])
        if scripts:
            parts.append(f"SCRIPTS: {', '.join(scripts[:10])}")
        
        return "\n".join(parts)
    
    def get_context_summary(self) -> str:
        """Obtener resumen del contexto"""
        if not self.project_context:
            self.load_project_context()
        
        context = self.project_context
        
        lines = [
            f"Proyecto: {os.path.basename(context.project_path)}",
            f"Tipo: {context.project_type}",
            f"Archivos de contexto: {len(context.context_files)}",
        ]
        
        if context.context_files:
            lines.append("Archivos cargados:")
            for cf in context.context_files[:5]:
                lines.append(f"  - {os.path.basename(cf.path)} ({cf.size} bytes)")
        
        return "\n".join(lines)
    
    def reload_context(self):
        """Recargar contexto del proyecto"""
        self.load_project_context(force=True)


# Instancia global
context_loader = ContextLoader()
