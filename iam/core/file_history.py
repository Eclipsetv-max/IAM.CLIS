# -*- coding: utf-8 -*-
"""
IAM File History - Sistema de Versionado de Archivos con Rollback
Inspirado en opencode: trackea cambios de archivos y permite deshacer
"""

import json
import os
import hashlib
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field, asdict
from enum import Enum


class VersionType(Enum):
    """Tipos de version"""
    INITIAL = "initial"
    EDIT = "edit"
    CREATE = "create"
    DELETE = "delete"
    RESTORE = "restore"


@dataclass
class FileVersion:
    """Una version de un archivo"""
    id: str
    session_id: str
    path: str
    content: str
    version_type: VersionType
    version: str
    size: int
    checksum: str
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["version_type"] = self.version_type.value
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "FileVersion":
        data["version_type"] = VersionType(data["version_type"])
        return cls(**data)


@dataclass
class FileTracker:
    """Trackea un archivo con sus versiones"""
    path: str
    versions: List[FileVersion] = field(default_factory=list)
    current_version: str = "initial"
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "path": self.path,
            "versions": [v.to_dict() for v in self.versions],
            "current_version": self.current_version,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "FileTracker":
        tracker = cls(
            path=data["path"],
            current_version=data.get("current_version", "initial"),
            created_at=data.get("created_at", datetime.now().isoformat()),
            updated_at=data.get("updated_at", datetime.now().isoformat())
        )
        tracker.versions = [FileVersion.from_dict(v) for v in data.get("versions", [])]
        return tracker


class FileHistory:
    """
    Sistema de historial de archivos con rollback
    Inspirado en opencode: versionado automatico de cambios
    """
    
    def __init__(self, project_path: str = None):
        self.project_path = project_path or os.getcwd()
        self.history_file = Path(self.project_path) / ".iam" / "file_history.json"
        self.trackers: Dict[str, FileTracker] = {}
        self._session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self._load_history()
    
    def _load_history(self):
        """Cargar historial desde disco"""
        if self.history_file.exists():
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                for path, tracker_data in data.get("trackers", {}).items():
                    self.trackers[path] = FileTracker.from_dict(tracker_data)
            except Exception:
                self.trackers = {}
    
    def _save_history(self):
        """Guardar historial en disco"""
        self.history_file.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "trackers": {path: t.to_dict() for path, t in self.trackers.items()},
            "last_updated": datetime.now().isoformat()
        }
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception:
            pass
    
    def _generate_checksum(self, content: str) -> str:
        """Generar checksum del contenido"""
        return hashlib.md5(content.encode('utf-8')).hexdigest()[:12]
    
    def _generate_version(self, tracker: FileTracker) -> str:
        """Generar siguiente numero de version"""
        if not tracker.versions:
            return "initial"
        
        last_version = tracker.versions[-1].version
        if last_version == "initial":
            return "v1"
        elif last_version.startswith("v"):
            try:
                num = int(last_version[1:])
                return f"v{num + 1}"
            except ValueError:
                return f"v{datetime.now().strftime('%Y%m%d%H%M%S')}"
        return f"v{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    def record_create(self, path: str, content: str, session_id: str = None) -> FileVersion:
        """Registrar creacion de archivo"""
        session_id = session_id or self._session_id
        rel_path = self._get_relative_path(path)
        
        tracker = self.trackers.get(rel_path, FileTracker(path=rel_path))
        
        version = FileVersion(
            id=f"{rel_path}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            session_id=session_id,
            path=rel_path,
            content=content,
            version_type=VersionType.CREATE,
            version="initial",
            size=len(content),
            checksum=self._generate_checksum(content)
        )
        
        tracker.versions.append(version)
        tracker.current_version = "initial"
        tracker.updated_at = datetime.now().isoformat()
        self.trackers[rel_path] = tracker
        self._save_history()
        
        return version
    
    def record_edit(self, path: str, new_content: str, session_id: str = None) -> FileVersion:
        """Registrar edicion de archivo"""
        session_id = session_id or self._session_id
        rel_path = self._get_relative_path(path)
        
        tracker = self.trackers.get(rel_path, FileTracker(path=rel_path))
        new_version = self._generate_version(tracker)
        
        # Verificar si el contenido cambio
        if tracker.versions:
            last_content = tracker.versions[-1].content
            if last_content == new_content:
                return None  # No hay cambio real
        
        version = FileVersion(
            id=f"{rel_path}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            session_id=session_id,
            path=rel_path,
            content=new_content,
            version_type=VersionType.EDIT,
            version=new_version,
            size=len(new_content),
            checksum=self._generate_checksum(new_content)
        )
        
        tracker.versions.append(version)
        tracker.current_version = new_version
        tracker.updated_at = datetime.now().isoformat()
        self.trackers[rel_path] = tracker
        self._save_history()
        
        return version
    
    def record_delete(self, path: str, session_id: str = None) -> FileVersion:
        """Registrar eliminacion de archivo"""
        session_id = session_id or self._session_id
        rel_path = self._get_relative_path(path)
        
        tracker = self.trackers.get(rel_path, FileTracker(path=rel_path))
        
        # Obtener ultimo contenido si existe
        last_content = ""
        if tracker.versions:
            last_content = tracker.versions[-1].content
        
        version = FileVersion(
            id=f"{rel_path}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            session_id=session_id,
            path=rel_path,
            content=last_content,
            version_type=VersionType.DELETE,
            version=f"v{len(tracker.versions)}",
            size=0,
            checksum=""
        )
        
        tracker.versions.append(version)
        tracker.updated_at = datetime.now().isoformat()
        self.trackers[rel_path] = tracker
        self._save_history()
        
        return version
    
    def get_versions(self, path: str) -> List[FileVersion]:
        """Obtener todas las versiones de un archivo"""
        rel_path = self._get_relative_path(path)
        tracker = self.trackers.get(rel_path)
        return tracker.versions if tracker else []
    
    def get_version(self, path: str, version: str) -> Optional[FileVersion]:
        """Obtener una version especifica"""
        rel_path = self._get_relative_path(path)
        tracker = self.trackers.get(rel_path)
        if not tracker:
            return None
        
        for v in tracker.versions:
            if v.version == version:
                return v
        return None
    
    def get_latest_version(self, path: str) -> Optional[FileVersion]:
        """Obtener la ultima version"""
        rel_path = self._get_relative_path(path)
        tracker = self.trackers.get(rel_path)
        if not tracker or not tracker.versions:
            return None
        return tracker.versions[-1]
    
    def rollback(self, path: str, target_version: str) -> Tuple[bool, str]:
        """
        Restaurar un archivo a una version anterior
        Retorna: (exito, mensaje)
        """
        rel_path = self._get_relative_path(path)
        version = self.get_version(rel_path, target_version)
        
        if not version:
            return False, f"Version {target_version} no encontrada"
        
        if version.version_type == VersionType.DELETE:
            return False, "No se puede restaurar una version de eliminacion"
        
        full_path = os.path.join(self.project_path, rel_path)
        
        try:
            # Crear directorio si no existe
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            
            # Escribir contenido
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(version.content)
            
            # Registrar el rollback
            tracker = self.trackers.get(rel_path, FileTracker(path=rel_path))
            rollback_version = FileVersion(
                id=f"{rel_path}_rollback_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                session_id=self._session_id,
                path=rel_path,
                content=version.content,
                version_type=VersionType.RESTORE,
                version=f"v{len(tracker.versions)}",
                size=len(version.content),
                checksum=self._generate_checksum(version.content),
                metadata={"restored_from": target_version}
            )
            
            tracker.versions.append(rollback_version)
            tracker.current_version = rollback_version.version
            tracker.updated_at = datetime.now().isoformat()
            self.trackers[rel_path] = tracker
            self._save_history()
            
            return True, f"Archivo restaurado a version {target_version}"
            
        except Exception as e:
            return False, f"Error al restaurar: {str(e)}"
    
    def rollback_last(self, path: str) -> Tuple[bool, str]:
        """Restaurar a la version anterior"""
        rel_path = self._get_relative_path(path)
        tracker = self.trackers.get(rel_path)
        
        if not tracker or len(tracker.versions) < 2:
            return False, "No hay versiones anteriores"
        
        last_version = tracker.versions[-2]
        return self.rollback(path, last_version.version)
    
    def get_file_history(self, path: str) -> Dict[str, Any]:
        """Obtener historial completo de un archivo"""
        rel_path = self._get_relative_path(path)
        tracker = self.trackers.get(rel_path)
        
        if not tracker:
            return {"path": rel_path, "versions": [], "current_version": None}
        
        return {
            "path": tracker.path,
            "versions": [v.to_dict() for v in tracker.versions],
            "current_version": tracker.current_version,
            "total_versions": len(tracker.versions),
            "created_at": tracker.created_at,
            "updated_at": tracker.updated_at
        }
    
    def get_all_files(self) -> List[Dict[str, Any]]:
        """Obtener historial de todos los archivos"""
        return [
            {
                "path": tracker.path,
                "versions": len(tracker.versions),
                "current_version": tracker.current_version,
                "updated_at": tracker.updated_at
            }
            for tracker in self.trackers.values()
        ]
    
    def clear_history(self, path: str = None):
        """Limpiar historial"""
        if path:
            rel_path = self._get_relative_path(path)
            if rel_path in self.trackers:
                del self.trackers[rel_path]
        else:
            self.trackers.clear()
        self._save_history()
    
    def _get_relative_path(self, path: str) -> str:
        """Obtener ruta relativa al proyecto"""
        if os.path.isabs(path):
            try:
                return os.path.relpath(path, self.project_path)
            except ValueError:
                return path
        return path
    
    def format_history(self, path: str) -> str:
        """Formatear historial para mostrar"""
        history = self.get_file_history(path)
        
        if not history["versions"]:
            return f"No hay historial para: {history['path']}"
        
        lines = [f"HISTORIAL: {history['path']}", ""]
        
        for v in history["versions"]:
            icon = {
                "initial": "[NEW]",
                "create": "[NEW]",
                "edit": "[EDT]",
                "delete": "[DEL]",
                "restore": "[RST]"
            }.get(v["version_type"], "[???]")
            
            date = v["created_at"][:19].replace("T", " ")
            size = f"{v['size']} chars" if v["size"] else "N/A"
            lines.append(f"  {icon} {v['version']:<8} {date}  {size}")
        
        lines.append(f"\n  Total: {history['total_versions']} versiones")
        lines.append(f"  Actual: {history['current_version']}")
        
        return "\n".join(lines)


# Instancia global
file_history = FileHistory()
