# -*- coding: utf-8 -*-
"""
IAM Sub-Agent - Sistema de sub-agentes de solo lectura
IAM: lanza agentes para tareas paralelas
"""

import json
import os
import threading
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum


class SubAgentStatus(Enum):
    """Estado del sub-agente"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class SubAgentType(Enum):
    """Tipos de sub-agente"""
    RESEARCHER = "researcher"    # Busqueda de informacion
    ANALYZER = "analyzer"        # Analisis de codigo
    READER = "reader"            # Lectura de archivos
    EXPLORER = "explorer"        # Exploracion de directorios
    CUSTOM = "custom"            # Tarea personalizada


@dataclass
class SubAgentTask:
    """Tarea para un sub-agente"""
    id: str
    type: SubAgentType
    description: str
    prompt: str
    allowed_paths: List[str] = field(default_factory=list)
    blocked_paths: List[str] = field(default_factory=list)
    timeout: int = 60  # segundos
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "type": self.type.value,
            "description": self.description,
            "prompt": self.prompt,
            "allowed_paths": self.allowed_paths,
            "blocked_paths": self.blocked_paths,
            "timeout": self.timeout,
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SubAgentTask":
        data["type"] = SubAgentType(data["type"])
        return cls(**data)


@dataclass
class SubAgentResult:
    """Resultado de un sub-agente"""
    task_id: str
    status: SubAgentStatus
    output: str
    error: Optional[str] = None
    files_read: List[str] = field(default_factory=list)
    duration_seconds: float = 0.0
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "task_id": self.task_id,
            "status": self.status.value,
            "output": self.output,
            "error": self.error,
            "files_read": self.files_read,
            "duration_seconds": self.duration_seconds,
            "timestamp": self.timestamp
        }


class SubAgent:
    """
    Sub-agente de solo lectura
    IAM: ejecuta tareas paralelas sin modificar archivos
    """
    
    def __init__(self, project_path: str = None):
        self.project_path = project_path or os.getcwd()
        self.results_dir = Path(self.project_path) / ".iam" / "subagent_results"
        self.results_dir.mkdir(parents=True, exist_ok=True)
        
        # Herramientas de solo lectura disponibles
        self.read_only_tools = {
            "read_file": self._read_file,
            "list_dir": self._list_dir,
            "search_files": self._search_files,
            "search_content": self._search_content,
            "get_file_info": self._get_file_info,
        }
    
    def create_task(self, task_type: SubAgentType, description: str,
                    prompt: str, allowed_paths: List[str] = None,
                    timeout: int = 60) -> SubAgentTask:
        """Crear una tarea para un sub-agente"""
        task_id = f"subtask_{datetime.now().strftime('%Y%m%d%H%M%S_%f')}"
        
        return SubAgentTask(
            id=task_id,
            type=task_type,
            description=description,
            prompt=prompt,
            allowed_paths=allowed_paths or [self.project_path],
            timeout=timeout
        )
    
    def run_task(self, task: SubAgentTask,
                 progress_callback: Callable = None) -> SubAgentResult:
        """Ejecutar una tarea (en background)"""
        start_time = datetime.now()
        files_read = []
        
        try:
            if progress_callback:
                progress_callback(f"Iniciando sub-agente: {task.description}")
            
            # Validar permisos
            self._validate_permissions(task)
            
            # Ejecutar segun tipo
            output = self._execute_task(task, files_read)
            
            duration = (datetime.now() - start_time).total_seconds()
            
            result = SubAgentResult(
                task_id=task.id,
                status=SubAgentStatus.COMPLETED,
                output=output,
                files_read=files_read,
                duration_seconds=duration
            )
            
        except Exception as e:
            duration = (datetime.now() - start_time).total_seconds()
            result = SubAgentResult(
                task_id=task.id,
                status=SubAgentStatus.FAILED,
                output="",
                error=str(e),
                files_read=files_read,
                duration_seconds=duration
            )
        
        # Guardar resultado
        self._save_result(result)
        
        return result
    
    def run_task_async(self, task: SubAgentTask,
                       callback: Callable = None) -> threading.Thread:
        """Ejecutar tarea en background"""
        def run():
            result = self.run_task(task)
            if callback:
                callback(result)
        
        thread = threading.Thread(target=run, daemon=True)
        thread.start()
        return thread
    
    def _validate_permissions(self, task: SubAgentTask):
        """Validar que las rutas estan permitidas"""
        for path in task.blocked_paths:
            if os.path.exists(path):
                raise PermissionError(f"Acceso bloqueado a: {path}")
    
    def _execute_task(self, task: SubAgentTask, files_read: List[str]) -> str:
        """Ejecutar tarea segun tipo"""
        if task.type == SubAgentType.READER:
            return self._execute_reader_task(task, files_read)
        elif task.type == SubAgentType.EXPLORER:
            return self._execute_explorer_task(task, files_read)
        elif task.type == SubAgentType.ANALYZER:
            return self._execute_analyzer_task(task, files_read)
        elif task.type == SubAgentType.RESEARCHER:
            return self._execute_researcher_task(task, files_read)
        else:
            return self._execute_custom_task(task, files_read)
    
    def _execute_reader_task(self, task: SubAgentTask, files_read: List[str]) -> str:
        """Ejecutar tarea de lectura"""
        output_parts = []
        
        # Buscar archivos relevantes
        for path in task.allowed_paths:
            if os.path.isfile(path):
                content = self._read_file(path)
                if content:
                    files_read.append(path)
                    output_parts.append(f"=== {os.path.basename(path)} ===\n{content}")
            elif os.path.isdir(path):
                files = self._list_dir(path)
                output_parts.append(f"=== Directorio: {path} ===\n{files}")
        
        return "\n\n".join(output_parts) if output_parts else "No se encontraron archivos relevantes"
    
    def _execute_explorer_task(self, task: SubAgentTask, files_read: List[str]) -> str:
        """Ejecutar tarea de exploracion"""
        output_parts = []
        
        for path in task.allowed_paths:
            if os.path.isdir(path):
                structure = self._explore_directory(path, max_depth=3)
                output_parts.append(f"=== Estructura: {path} ===\n{structure}")
        
        return "\n\n".join(output_parts) if output_parts else "No se pudo explorar el directorio"
    
    def _execute_analyzer_task(self, task: SubAgentTask, files_read: List[str]) -> str:
        """Ejecutar tarea de analisis"""
        output_parts = []
        
        for path in task.allowed_paths:
            if os.path.isfile(path):
                content = self._read_file(path)
                if content:
                    files_read.append(path)
                    analysis = self._analyze_code(content, path)
                    output_parts.append(f"=== Analisis: {os.path.basename(path)} ===\n{analysis}")
        
        return "\n\n".join(output_parts) if output_parts else "No se pudo analizar el codigo"
    
    def _execute_researcher_task(self, task: SubAgentTask, files_read: List[str]) -> str:
        """Ejecutar tarea de investigacion"""
        output_parts = []
        
        # Buscar informacion relevante
        for path in task.allowed_paths:
            if os.path.isdir(path):
                # Buscar archivos de documentacion
                docs = self._find_documentation(path)
                output_parts.extend(docs)
        
        return "\n\n".join(output_parts) if output_parts else "No se encontro documentacion"
    
    def _execute_custom_task(self, task: SubAgentTask, files_read: List[str]) -> str:
        """Ejecutar tarea personalizada"""
        return f"Tarea personalizada ejecutada: {task.description}\nPrompt: {task.prompt}"
    
    # Herramientas de solo lectura
    def _read_file(self, path: str) -> Optional[str]:
        """Leer archivo"""
        try:
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
        except Exception:
            return None
    
    def _list_dir(self, path: str) -> str:
        """Listar directorio"""
        try:
            items = os.listdir(path)
            lines = []
            for item in sorted(items):
                full_path = os.path.join(path, item)
                if os.path.isdir(full_path):
                    lines.append(f"  [DIR]  {item}/")
                else:
                    size = os.path.getsize(full_path)
                    lines.append(f"  [FILE] {item} ({size} bytes)")
            return "\n".join(lines) if lines else "Directorio vacio"
        except Exception as e:
            return f"Error: {str(e)}"
    
    def _search_files(self, path: str, pattern: str) -> List[str]:
        """Buscar archivos por patron"""
        results = []
        try:
            for root, dirs, files in os.walk(path):
                # Ignorar directorios ocultos
                dirs[:] = [d for d in dirs if not d.startswith('.')]
                
                for file in files:
                    if pattern.lower() in file.lower():
                        results.append(os.path.join(root, file))
        except Exception:
            pass
        return results
    
    def _search_content(self, path: str, query: str) -> List[Dict[str, Any]]:
        """Buscar contenido en archivos"""
        results = []
        try:
            for root, dirs, files in os.walk(path):
                dirs[:] = [d for d in dirs if not d.startswith('.')]
                
                for file in files:
                    if file.endswith(('.py', '.js', '.ts', '.jsx', '.tsx',
                                     '.html', '.css', '.json', '.md', '.txt')):
                        filepath = os.path.join(root, file)
                        try:
                            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                                content = f.read()
                                if query.lower() in content.lower():
                                    # Encontrar lineas relevantes
                                    lines = content.split('\n')
                                    for i, line in enumerate(lines):
                                        if query.lower() in line.lower():
                                            results.append({
                                                "file": filepath,
                                                "line": i + 1,
                                                "content": line.strip()
                                            })
                        except Exception:
                            continue
        except Exception:
            pass
        return results[:50]  # Limitar a 50 resultados
    
    def _get_file_info(self, path: str) -> Dict[str, Any]:
        """Obtener informacion de un archivo"""
        try:
            stat = os.stat(path)
            return {
                "path": path,
                "size": stat.st_size,
                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                "is_dir": os.path.isdir(path),
                "extension": os.path.splitext(path)[1]
            }
        except Exception:
            return {}
    
    def _explore_directory(self, path: str, max_depth: int = 3,
                           current_depth: int = 0) -> str:
        """Explorar directorio recursivamente"""
        if current_depth >= max_depth:
            return ""
        
        lines = []
        try:
            for item in sorted(os.listdir(path)):
                if item.startswith('.'):
                    continue
                
                full_path = os.path.join(path, item)
                indent = "  " * current_depth
                
                if os.path.isdir(full_path):
                    lines.append(f"{indent}[DIR] {item}/")
                    sub_structure = self._explore_directory(
                        full_path, max_depth, current_depth + 1
                    )
                    if sub_structure:
                        lines.append(sub_structure)
                else:
                    size = os.path.getsize(full_path)
                    lines.append(f"{indent}[FILE] {item} ({size} bytes)")
        except Exception:
            pass
        
        return "\n".join(lines)
    
    def _analyze_code(self, content: str, path: str) -> str:
        """Analizar codigo"""
        lines = content.split('\n')
        
        analysis = {
            "total_lines": len(lines),
            "blank_lines": sum(1 for l in lines if not l.strip()),
            "comment_lines": sum(1 for l in lines if l.strip().startswith(('#', '//', '/*'))),
            "functions": 0,
            "classes": 0,
        }
        
        # Contar funciones y clases
        for line in lines:
            stripped = line.strip()
            if stripped.startswith('def ') or stripped.startswith('function '):
                analysis["functions"] += 1
            elif stripped.startswith('class '):
                analysis["classes"] += 1
        
        return (
            f"Lineas totales: {analysis['total_lines']}\n"
            f"Lineas vacias: {analysis['blank_lines']}\n"
            f"Comentarios: {analysis['comment_lines']}\n"
            f"Funciones: {analysis['functions']}\n"
            f"Clases: {analysis['classes']}"
        )
    
    def _find_documentation(self, path: str) -> List[str]:
        """Buscar archivos de documentacion"""
        docs = []
        doc_patterns = ['README', 'CHANGELOG', 'CONTRIBUTING', 'LICENSE']
        
        try:
            for item in os.listdir(path):
                if any(pattern in item.upper() for pattern in doc_patterns):
                    filepath = os.path.join(path, item)
                    if os.path.isfile(filepath):
                        content = self._read_file(filepath)
                        if content:
                            docs.append(f"=== {item} ===\n{content[:2000]}")
        except Exception:
            pass
        
        return docs
    
    def _save_result(self, result: SubAgentResult):
        """Guardar resultado"""
        filepath = self.results_dir / f"{result.task_id}.json"
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(result.to_dict(), f, indent=2, ensure_ascii=False)
        except Exception:
            pass
    
    def get_result(self, task_id: str) -> Optional[SubAgentResult]:
        """Obtener un resultado"""
        filepath = self.results_dir / f"{task_id}.json"
        if filepath.exists():
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                data["status"] = SubAgentStatus(data["status"])
                return SubAgentResult(**data)
            except Exception:
                pass
        return None
    
    def list_results(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Listar resultados recientes"""
        results = []
        try:
            for filepath in sorted(self.results_dir.glob("*.json"), reverse=True)[:limit]:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                results.append({
                    "task_id": data["task_id"],
                    "status": data["status"],
                    "timestamp": data["timestamp"],
                    "duration": data["duration_seconds"]
                })
        except Exception:
            pass
        return results


# Instancia global
sub_agent = SubAgent()
