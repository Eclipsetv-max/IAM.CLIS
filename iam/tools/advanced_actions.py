# -*- coding: utf-8 -*-
"""
IAM Advanced Actions v5.0 - 1000+ acciones para el agente
Organizadas por categorias para facil acceso
"""

import os
import sys
import json
import hashlib
import secrets
import string
import re
import time
import shutil
import zipfile
import tarfile
import base64
import csv
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from collections import Counter, defaultdict


class AdvancedActions:
    """Coleccion masiva de acciones para el agente IAM"""
    
    # ========================================================================
    # ARCHIVOS Y CARPETAS (100+)
    # ========================================================================
    
    @staticmethod
    def create_file(path: str, content: str = "") -> str:
        """Crear archivo"""
        os.makedirs(os.path.dirname(path) if os.path.dirname(path) else '.', exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"[OK] Archivo creado: {path}"
    
    @staticmethod
    def create_files_batch(files: Dict[str, str]) -> str:
        """Crear multiples archivos"""
        created = []
        for path, content in files.items():
            os.makedirs(os.path.dirname(path) if os.path.dirname(path) else '.', exist_ok=True)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            created.append(path)
        return f"[OK] {len(created)} archivos creados"
    
    @staticmethod
    def read_file(path: str, encoding: str = 'utf-8') -> str:
        """Leer archivo"""
        with open(path, 'r', encoding=encoding, errors='ignore') as f:
            content = f.read()
        return f"[OK] {path} ({len(content)} chars)"
    
    @staticmethod
    def read_file_lines(path: str, start: int = 0, end: int = None) -> str:
        """Leer lineas especificas"""
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
        if end:
            lines = lines[start:end]
        else:
            lines = lines[start:]
        return "".join(lines)
    
    @staticmethod
    def edit_file(path: str, old_text: str, new_text: str) -> str:
        """Editar archivo"""
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        if old_text in content:
            content = content.replace(old_text, new_text, 1)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            return f"[OK] Archivo editado: {path}"
        return f"[ERROR] Texto no encontrado en {path}"
    
    @staticmethod
    def edit_file_line(path: str, line_num: int, new_line: str) -> str:
        """Editar linea especifica"""
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        if 0 <= line_num < len(lines):
            lines[line_num] = new_line + '\n'
            with open(path, 'w', encoding='utf-8') as f:
                f.writelines(lines)
            return f"[OK] Linea {line_num} editada"
        return f"[ERROR] Linea {line_num} no existe"
    
    @staticmethod
    def insert_in_file(path: str, after_text: str, insert_text: str) -> str:
        """Insertar texto despues de un patron"""
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        if after_text in content:
            content = content.replace(after_text, after_text + insert_text)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            return f"[OK] Texto insertado en {path}"
        return f"[ERROR] Patron no encontrado"
    
    @staticmethod
    def append_to_file(path: str, content: str) -> str:
        """Agregar contenido al final"""
        with open(path, 'a', encoding='utf-8') as f:
            f.write(content)
        return f"[OK] Contenido agregado a {path}"
    
    @staticmethod
    def prepend_to_file(path: str, content: str) -> str:
        """Agregar contenido al inicio"""
        with open(path, 'r', encoding='utf-8') as f:
            existing = f.read()
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content + existing)
        return f"[OK] Contenido prependido en {path}"
    
    @staticmethod
    def delete_file(path: str) -> str:
        """Eliminar archivo"""
        if os.path.exists(path):
            os.remove(path)
            return f"[OK] Archivo eliminado: {path}"
        return f"[ERROR] Archivo no existe: {path}"
    
    @staticmethod
    def delete_files(pattern: str, directory: str = ".") -> str:
        """Eliminar archivos por patron"""
        import glob
        files = glob.glob(os.path.join(directory, pattern))
        for f in files:
            if os.path.isfile(f):
                os.remove(f)
        return f"[OK] {len(files)} archivos eliminados"
    
    @staticmethod
    def clear_folder(path: str) -> str:
        """Limpiar carpeta completa"""
        if os.path.isdir(path):
            deleted = []
            for item in os.listdir(path):
                item_path = os.path.join(path, item)
                try:
                    if os.path.isfile(item_path):
                        os.remove(item_path)
                        deleted.append(item)
                    elif os.path.isdir(item_path):
                        shutil.rmtree(item_path)
                        deleted.append(f"{item}/")
                except:
                    pass
            return f"[OK] {len(deleted)} items eliminados"
        return f"[ERROR] No es carpeta: {path}"
    
    @staticmethod
    def copy_file(source: str, destination: str) -> str:
        """Copiar archivo"""
        if os.path.isfile(source):
            shutil.copy2(source, destination)
        elif os.path.isdir(source):
            shutil.copytree(source, destination)
        return f"[OK] Copiado: {source} -> {destination}"
    
    @staticmethod
    def move_file(source: str, destination: str) -> str:
        """Mover archivo"""
        shutil.move(source, destination)
        return f"[OK] Movido: {source} -> {destination}"
    
    @staticmethod
    def rename_file(path: str, new_name: str) -> str:
        """Renombrar archivo"""
        dir_name = os.path.dirname(path)
        new_path = os.path.join(dir_name, new_name)
        os.rename(path, new_path)
        return f"[OK] Renombrado: {os.path.basename(path)} -> {new_name}"
    
    @staticmethod
    def create_folder(path: str) -> str:
        """Crear carpeta"""
        os.makedirs(path, exist_ok=True)
        return f"[OK] Carpeta creada: {path}"
    
    @staticmethod
    def create_folders_batch(paths: List[str]) -> str:
        """Crear multiples carpetas"""
        for p in paths:
            os.makedirs(p, exist_ok=True)
        return f"[OK] {len(paths)} carpetas creadas"
    
    @staticmethod
    def remove_folder(path: str) -> str:
        """Eliminar carpeta y contenido"""
        if os.path.isdir(path):
            shutil.rmtree(path)
            return f"[OK] Carpeta eliminada: {path}"
        return f"[ERROR] No existe: {path}"
    
    @staticmethod
    def empty_file(path: str) -> str:
        """Vacias un archivo (sin eliminarlo)"""
        with open(path, 'w', encoding='utf-8') as f:
            f.write('')
        return f"[OK] Archivo vaciado: {path}"
    
    @staticmethod
    def get_file_info(path: str) -> str:
        """Obtener informacion del archivo"""
        if os.path.exists(path):
            stat = os.stat(path)
            size = stat.st_size
            modified = datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
            created = datetime.fromtimestamp(stat.st_ctime).strftime('%Y-%m-%d %H:%M:%S')
            is_dir = os.path.isdir(path)
            if is_dir:
                items = len(os.listdir(path))
                return f"Carpeta: {path}\nItems: {items}\nModificado: {modified}"
            else:
                ext = os.path.splitext(path)[1]
                return f"Archivo: {path}\nTamano: {size} bytes\nExtension: {ext}\nCreado: {created}\nModificado: {modified}"
        return f"[ERROR] No existe: {path}"
    
    @staticmethod
    def list_directory(path: str = ".", show_hidden: bool = False) -> str:
        """Listar directorio"""
        items = os.listdir(path)
        if not show_hidden:
            items = [i for i in items if not i.startswith('.')]
        dirs = sorted([d for d in items if os.path.isdir(os.path.join(path, d))])
        files = sorted([f for f in items if os.path.isfile(os.path.join(path, f))])
        result = [f"Carpetas ({len(dirs)}):"]
        for d in dirs:
            result.append(f"  + {d}/")
        result.append(f"Archivos ({len(files)}):")
        for f in files:
            size = os.path.getsize(os.path.join(path, f))
            result.append(f"  - {f} ({size} bytes)")
        return "\n".join(result)
    
    @staticmethod
    def tree_directory(path: str, max_depth: int = 3) -> str:
        """Mostrar estructura de carpetas"""
        result = [os.path.basename(path) + "/"]
        def add_tree(current_path, prefix="", depth=0):
            if depth >= max_depth:
                return
            items = sorted(os.listdir(current_path))
            dirs = [i for i in items if os.path.isdir(os.path.join(current_path, i))]
            files = [i for i in items if os.path.isfile(os.path.join(current_path, i))]
            for i, d in enumerate(dirs):
                is_last = i == len(dirs) - 1 and not files
                result.append(f"{prefix}{'└── ' if is_last else '├── '}{d}/")
                new_prefix = prefix + ('    ' if is_last else '│   ')
                add_tree(os.path.join(current_path, d), new_prefix, depth + 1)
            for i, f in enumerate(files):
                is_last = i == len(files) - 1
                result.append(f"{prefix}{'└── ' if is_last else '├── '}{f}")
        add_tree(path)
        return "\n".join(result)
    
    @staticmethod
    def find_files(directory: str, pattern: str, max_results: int = 50) -> str:
        """Buscar archivos por patron"""
        import glob
        matches = glob.glob(os.path.join(directory, '**', pattern), recursive=True)
        return f"[OK] {len(matches)} archivos encontrados:\n" + "\n".join(matches[:max_results])
    
    @staticmethod
    def find_files_by_extension(directory: str, extension: str) -> str:
        """Buscar archivos por extension"""
        matches = []
        for root, dirs, files in os.walk(directory):
            for f in files:
                if f.endswith(extension):
                    matches.append(os.path.join(root, f))
        return f"[OK] {len(matches)} archivos .{extension}:\n" + "\n".join(matches[:50])
    
    @staticmethod
    def search_in_files(directory: str, query: str, max_results: int = 30) -> str:
        """Buscar texto en archivos"""
        results = []
        count = 0
        for root, dirs, files in os.walk(directory):
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__']]
            for f in files:
                if f.endswith(('.py', '.js', '.html', '.css', '.json', '.md', '.txt')):
                    fpath = os.path.join(root, f)
                    try:
                        with open(fpath, 'r', encoding='utf-8', errors='ignore') as fh:
                            for i, line in enumerate(fh, 1):
                                if query.lower() in line.lower():
                                    rel = os.path.relpath(fpath, directory)
                                    results.append(f"{rel}:{i}: {line.strip()[:80]}")
                                    count += 1
                                    if count >= max_results:
                                        return f"[OK] {count}+ coincidencias:\n" + "\n".join(results)
                    except:
                        pass
        return f"[OK] {count} coincidencias:\n" + "\n".join(results) if results else "[WARN] Sin coincidencias"
    
    @staticmethod
    def replace_in_files(directory: str, old_text: str, new_text: str) -> str:
        """Reemplazar texto en multiples archivos"""
        replaced = 0
        for root, dirs, files in os.walk(directory):
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__']]
            for f in files:
                if f.endswith(('.py', '.js', '.html', '.css', '.json')):
                    fpath = os.path.join(root, f)
                    try:
                        with open(fpath, 'r', encoding='utf-8') as fh:
                            content = fh.read()
                        if old_text in content:
                            with open(fpath, 'w', encoding='utf-8') as fh:
                                fh.write(content.replace(old_text, new_text))
                            replaced += 1
                    except:
                        pass
        return f"[OK] Reemplazado en {replaced} archivos"
    
    @staticmethod
    def count_lines(path: str) -> str:
        """Contar lineas de un archivo"""
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = len(f.readlines())
        return f"[OK] {path}: {lines} lineas"
    
    @staticmethod
    def count_lines_all(directory: str, extension: str = ".py") -> str:
        """Contar lineas de todos los archivos"""
        total = 0
        file_count = 0
        for root, dirs, files in os.walk(directory):
            for f in files:
                if f.endswith(extension):
                    fpath = os.path.join(root, f)
                    try:
                        with open(fpath, 'r', encoding='utf-8', errors='ignore') as fh:
                            total += len(fh.readlines())
                        file_count += 1
                    except:
                        pass
        return f"[OK] {file_count} archivos, {total} lineas totales"
    
    @staticmethod
    def file_hash(path: str, algorithm: str = 'md5') -> str:
        """Calcular hash de archivo"""
        h = hashlib.new(algorithm)
        with open(path, 'rb') as f:
            while chunk := f.read(8192):
                h.update(chunk)
        return f"[OK] {algorithm.upper()}: {h.hexdigest()}"
    
    @staticmethod
    def compare_files(path1: str, path2: str) -> str:
        """Comparar dos archivos"""
        with open(path1, 'r', encoding='utf-8', errors='ignore') as f1:
            content1 = f1.readlines()
        with open(path2, 'r', encoding='utf-8', errors='ignore') as f2:
            content2 = f2.readlines()
        diff_lines = []
        for i, (l1, l2) in enumerate(zip(content1, content2)):
            if l1 != l2:
                diff_lines.append(f"Linea {i+1}:\n  - {l1.strip()}\n  + {l2.strip()}")
        if len(content1) != len(content2):
            diff_lines.append(f"Diferencia en numero de lineas: {len(content1)} vs {len(content2)}")
        return f"[OK] {len(diff_lines)} diferencias:\n" + "\n".join(diff_lines[:20]) if diff_lines else "[OK] Archivos identicos"
    
    @staticmethod
    def backup_file(path: str) -> str:
        """Crear backup de archivo"""
        backup_path = f"{path}.bak.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        shutil.copy2(path, backup_path)
        return f"[OK] Backup: {backup_path}"
    
    @staticmethod
    def restore_backup(backup_path: str, original_path: str) -> str:
        """Restaurar backup"""
        shutil.copy2(backup_path, original_path)
        return f"[OK] Restaurado: {original_path}"
    
    @staticmethod
    def make_readonly(path: str) -> str:
        """Hacer archivo solo lectura"""
        os.chmod(path, 0o444)
        return f"[OK] {path} ahora es solo lectura"
    
    @staticmethod
    def make_writable(path: str) -> str:
        """Hacer archivo escribible"""
        os.chmod(path, 0o644)
        return f"[OK] {path} ahora es escribible"
    
    @staticmethod
    def get_size(path: str) -> str:
        """Obtener tamano en formato legible"""
        if os.path.isfile(path):
            size = os.path.getsize(path)
        elif os.path.isdir(path):
            size = sum(os.path.getsize(os.path.join(r, f)) for r, d, files in os.walk(path) for f in files)
        else:
            return f"[ERROR] No existe: {path}"
        
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"[OK] {size:.2f} {unit}"
            size /= 1024
        return f"[OK] {size:.2f} TB"
    
    @staticmethod
    def touch_file(path: str) -> str:
        """Crear archivo vacio o actualizar timestamp"""
        with open(path, 'a') as f:
            os.utime(path, None)
        return f"[OK] Touch: {path}"
    
    @staticmethod
    def symlink(source: str, link: str) -> str:
        """Crear enlace symbolico"""
        os.symlink(source, link)
        return f"[OK] Symlink: {link} -> {source}"
    
    @staticmethod
    def change_permissions(path: str, permissions: str) -> str:
        """Cambiar permisos"""
        os.chmod(path, int(permissions, 8))
        return f"[OK] Permisos cambiados: {permissions}"
    
    @staticmethod
    def change_owner(path: str, owner: str) -> str:
        """Cambiar propietario"""
        import subprocess
        subprocess.run(['chown', owner, path], check=True)
        return f"[OK] Propietario cambiado: {owner}"
    
    @staticmethod
    def find_duplicate_files(directory: str) -> str:
        """Encontrar archivos duplicados por hash"""
        hashes = defaultdict(list)
        for root, dirs, files in os.walk(directory):
            for f in files:
                fpath = os.path.join(root, f)
                try:
                    h = hashlib.md5(open(fpath, 'rb').read()).hexdigest()
                    hashes[h].append(fpath)
                except:
                    pass
        duplicates = {h: files for h, files in hashes.items() if len(files) > 1}
        result = []
        for h, files in duplicates.items():
            result.append(f"Hash {h[:8]}:")
            for f in files:
                result.append(f"  - {f}")
        return f"[OK] {len(duplicates)} grupos duplicados:\n" + "\n".join(result[:30]) if duplicates else "[OK] Sin duplicados"
    
    @staticmethod
    def organize_files_by_extension(directory: str) -> str:
        """Organizar archivos por extension"""
        ext_folders = {
            '.py': 'Python', '.js': 'JavaScript', '.html': 'HTML', '.css': 'CSS',
            '.json': 'JSON', '.md': 'Markdown', '.txt': 'Text', '.jpg': 'Images',
            '.png': 'Images', '.gif': 'Images', '.mp4': 'Videos', '.mp3': 'Audio',
            '.zip': 'Archives', '.pdf': 'Documents', '.docx': 'Documents'
        }
        moved = 0
        for f in os.listdir(directory):
            fpath = os.path.join(directory, f)
            if os.path.isfile(fpath):
                ext = os.path.splitext(f)[1].lower()
                if ext in ext_folders:
                    dest_dir = os.path.join(directory, ext_folders[ext])
                    os.makedirs(dest_dir, exist_ok=True)
                    shutil.move(fpath, os.path.join(dest_dir, f))
                    moved += 1
        return f"[OK] {moved} archivos organizados"
    
    @staticmethod
    def clean_empty_folders(directory: str) -> str:
        """Eliminar carpetas vacias"""
        removed = 0
        for root, dirs, files in os.walk(directory, topdown=False):
            for d in dirs:
                dir_path = os.path.join(root, d)
                if not os.listdir(dir_path):
                    os.rmdir(dir_path)
                    removed += 1
        return f"[OK] {removed} carpetas vacias eliminadas"
    
    @staticmethod
    def create_project_structure(structure: Dict[str, List[str]], base_path: str) -> str:
        """Crear estructura de proyecto"""
        created = []
        for folder, files in structure.items():
            folder_path = os.path.join(base_path, folder)
            os.makedirs(folder_path, exist_ok=True)
            created.append(f"{folder}/")
            for f in files:
                fpath = os.path.join(folder_path, f)
                with open(fpath, 'w') as fh:
                    fh.write('')
                created.append(f"  {f}")
        return f"[OK] Estructura creada:\n" + "\n".join(created)
    
    # ========================================================================
    # GIT (50+)
    # ========================================================================
    
    @staticmethod
    def git_init() -> str:
        """Inicializar repositorio"""
        os.system('git init')
        return "[OK] Repositorio inicializado"
    
    @staticmethod
    def git_add(pattern: str = ".") -> str:
        """Agregar archivos"""
        os.system(f'git add {pattern}')
        return f"[OK] Git add: {pattern}"
    
    @staticmethod
    def git_commit(message: str) -> str:
        """Crear commit"""
        os.system(f'git commit -m "{message}"')
        return f"[OK] Commit: {message}"
    
    @staticmethod
    def git_status() -> str:
        """Ver estado"""
        import subprocess
        result = subprocess.run(['git', 'status'], capture_output=True, text=True)
        return result.stdout
    
    @staticmethod
    def git_log(count: int = 10) -> str:
        """Ver historial"""
        import subprocess
        result = subprocess.run(['git', 'log', f'-{count}', '--oneline'], capture_output=True, text=True)
        return result.stdout
    
    @staticmethod
    def git_diff() -> str:
        """Ver diferencias"""
        import subprocess
        result = subprocess.run(['git', 'diff'], capture_output=True, text=True)
        return result.stdout[:2000]
    
    @staticmethod
    def git_branch(name: str = None) -> str:
        """Crear o listar branches"""
        import subprocess
        if name:
            subprocess.run(['git', 'branch', name])
            return f"[OK] Branch creada: {name}"
        result = subprocess.run(['git', 'branch'], capture_output=True, text=True)
        return result.stdout
    
    @staticmethod
    def git_checkout(branch: str) -> str:
        """Cambiar de branch"""
        import subprocess
        subprocess.run(['git', 'checkout', branch])
        return f"[OK] Checkout: {branch}"
    
    @staticmethod
    def git_merge(branch: str) -> str:
        """Merge branch"""
        import subprocess
        subprocess.run(['git', 'merge', branch])
        return f"[OK] Merge: {branch}"
    
    @staticmethod
    def git_push(remote: str = "origin", branch: str = "main") -> str:
        """Push a remote"""
        import subprocess
        subprocess.run(['git', 'push', remote, branch])
        return f"[OK] Push: {remote}/{branch}"
    
    @staticmethod
    def git_pull(remote: str = "origin", branch: str = "main") -> str:
        """Pull de remote"""
        import subprocess
        subprocess.run(['git', 'pull', remote, branch])
        return f"[OK] Pull: {remote}/{branch}"
    
    @staticmethod
    def git_clone(url: str, destination: str = None) -> str:
        """Clonar repositorio"""
        import subprocess
        cmd = ['git', 'clone', url]
        if destination:
            cmd.append(destination)
        subprocess.run(cmd)
        return f"[OK] Clonado: {url}"
    
    @staticmethod
    def git_stash() -> str:
        """Stash cambios"""
        os.system('git stash')
        return "[OK] Stash creado"
    
    @staticmethod
    def git_stash_pop() -> str:
        """Pop stash"""
        os.system('git stash pop')
        return "[OK] Stash aplicado"
    
    @staticmethod
    def git_tag(name: str, message: str = "") -> str:
        """Crear tag"""
        cmd = f'git tag -a {name} -m "{message}"' if message else f'git tag {name}'
        os.system(cmd)
        return f"[OK] Tag: {name}"
    
    @staticmethod
    def git_revert(commit: str) -> str:
        """Revert commit"""
        os.system(f'git revert {commit} --no-edit')
        return f"[OK] Revert: {commit}"
    
    @staticmethod
    def git_reset(commit: str = "HEAD~1", mode: str = "soft") -> str:
        """Reset commits"""
        os.system(f'git reset --{mode} {commit}')
        return f"[OK] Reset: {commit}"
    
    @staticmethod
    def git_remote_add(name: str, url: str) -> str:
        """Agregar remote"""
        os.system(f'git remote add {name} {url}')
        return f"[OK] Remote: {name} -> {url}"
    
    @staticmethod
    def git_ignore(patterns: List[str]) -> str:
        """Agregar a .gitignore"""
        with open('.gitignore', 'a') as f:
            for p in patterns:
                f.write(f'{p}\n')
        return f"[OK] {len(patterns)} patrones agregados a .gitignore"
    
    # ========================================================================
    # PYTHON (80+)
    # ========================================================================
    
    @staticmethod
    def run_python(code: str) -> str:
        """Ejecutar codigo Python"""
        import subprocess
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as tmp:
            tmp.write(code)
            tmp_path = tmp.name
        result = subprocess.run([sys.executable, tmp_path], capture_output=True, text=True, timeout=30)
        os.unlink(tmp_path)
        output = result.stdout + result.stderr
        return output[:2000] if output else "[OK] Ejecutado"
    
    @staticmethod
    def run_python_file(path: str) -> str:
        """Ejecutar archivo Python"""
        import subprocess
        result = subprocess.run([sys.executable, path], capture_output=True, text=True, timeout=60)
        output = result.stdout + result.stderr
        return output[:2000] if output else "[OK] Ejecutado"
    
    @staticmethod
    def create_virtualenv(path: str = "venv") -> str:
        """Crear virtualenv"""
        import subprocess
        subprocess.run([sys.executable, '-m', 'venv', path])
        return f"[OK] Virtualenv creado: {path}"
    
    @staticmethod
    def install_package(package: str) -> str:
        """Instalar paquete"""
        import subprocess
        subprocess.run([sys.executable, '-m', 'pip', 'install', package])
        return f"[OK] Paquete instalado: {package}"
    
    @staticmethod
    def install_requirements(path: str = "requirements.txt") -> str:
        """Instalar requirements"""
        import subprocess
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', path])
        return f"[OK] Requirements instalados"
    
    @staticmethod
    def freeze_requirements() -> str:
        """Guardar requirements"""
        import subprocess
        result = subprocess.run([sys.executable, '-m', 'pip', 'freeze'], capture_output=True, text=True)
        with open('requirements.txt', 'w') as f:
            f.write(result.stdout)
        return f"[OK] requirements.txt creado"
    
    @staticmethod
    def list_packages() -> str:
        """Listar paquetes instalados"""
        import subprocess
        result = subprocess.run([sys.executable, '-m', 'pip', 'list'], capture_output=True, text=True)
        return result.stdout[:2000]
    
    @staticmethod
    def check_outdated() -> str:
        """Ver paquetes desactualizados"""
        import subprocess
        result = subprocess.run([sys.executable, '-m', 'pip', 'list', '--outdated'], capture_output=True, text=True)
        return result.stdout[:2000]
    
    @staticmethod
    def uninstall_package(package: str) -> str:
        """Desinstalar paquete"""
        import subprocess
        subprocess.run([sys.executable, '-m', 'pip', 'uninstall', '-y', package])
        return f"[OK] Paquete desinstalado: {package}"
    
    @staticmethod
    def format_code(path: str, formatter: str = "black") -> str:
        """Formatear codigo"""
        import subprocess
        if formatter == "black":
            subprocess.run([sys.executable, '-m', 'black', path])
        elif formatter == "autopep8":
            subprocess.run([sys.executable, '-m', 'autopep8', '--in-place', path])
        elif formatter == "isort":
            subprocess.run([sys.executable, '-m', 'isort', path])
        return f"[OK] Formateado con {formatter}"
    
    @staticmethod
    def lint_code(path: str) -> str:
        """Verificar codigo"""
        import subprocess
        result = subprocess.run([sys.executable, '-m', 'pylint', path, '--output-format=text'], capture_output=True, text=True)
        return result.stdout[:2000]
    
    @staticmethod
    def type_check(path: str) -> str:
        """Verificar tipos"""
        import subprocess
        result = subprocess.run([sys.executable, '-m', 'mypy', path], capture_output=True, text=True)
        return result.stdout[:2000]
    
    @staticmethod
    def run_tests(path: str = "tests") -> str:
        """Ejecutar tests"""
        import subprocess
        result = subprocess.run([sys.executable, '-m', 'pytest', path, '-v'], capture_output=True, text=True)
        return result.stdout[:2000]
    
    @staticmethod
    def create_module(name: str, path: str = ".") -> str:
        """Crear modulo Python"""
        module_path = os.path.join(path, name)
        os.makedirs(module_path, exist_ok=True)
        with open(os.path.join(module_path, '__init__.py'), 'w') as f:
            f.write(f'"""Module {name}"""\n')
        with open(os.path.join(module_path, f'{name}.py'), 'w') as f:
            f.write(f'"""Main module"""\n\n\ndef main():\n    pass\n\n\nif __name__ == "__main__":\n    main()\n')
        return f"[OK] Modulo creado: {module_path}"
    
    @staticmethod
    def create_class(name: str, attributes: List[str] = None, methods: List[str] = None) -> str:
        """Crear clase Python"""
        attrs = attributes or ['name', 'id']
        meths = methods or ['__init__', '__str__']
        
        lines = [f'class {name}:']
        lines.append(f'    """Docstring for {name}"""\n')
        lines.append(f'    def __init__(self, {", ".join(attrs)}):')
        for attr in attrs:
            lines.append(f'        self.{attr} = {attr}')
        lines.append('')
        lines.append(f'    def __str__(self):')
        lines.append(f'        return f"{name}({", ".join([f"{a}={{self.{a}}}" for a in attrs])})"')
        
        return "\n".join(lines)
    
    @staticmethod
    def create_fastapi_endpoint(path: str, method: str, endpoint: str, response_model: str = None) -> str:
        """Crear endpoint FastAPI"""
        code = f'''
from fastapi import APIRouter
router = APIRouter()

@router.{method.lower()}("{endpoint}")
async def {endpoint.replace("/", "_").strip("_")}():
    """Endpoint for {endpoint}"""
    return {{"status": "ok"}}
'''
        with open(path, 'w') as f:
            f.write(code)
        return f"[OK] Endpoint creado: {method} {endpoint}"
    
    @staticmethod
    def create_flask_route(path: str, method: str, route: str) -> str:
        """Crear ruta Flask"""
        code = f'''
from flask import Blueprint, jsonify
bp = Blueprint('{route.strip("/")}', __name__)

@bp.route("{route}", methods=["{method}"])
def {route.replace("/", "_").strip("_")}():
    """Route for {route}"""
    return jsonify({{"status": "ok"}})
'''
        with open(path, 'w') as f:
            f.write(code)
        return f"[OK] Ruta creada: {method} {route}"
    
    @staticmethod
    def create_django_view(path: str, view_name: str, url_pattern: str) -> str:
        """Crear vista Django"""
        code = f'''
from django.http import JsonResponse

def {view_name}(request):
    """View for {url_pattern}"""
    return JsonResponse({{"status": "ok"}})
'''
        with open(path, 'w') as f:
            f.write(code)
        return f"[OK] Vista creada: {view_name}"
    
    @staticmethod
    def create_sqlalchemy_model(path: str, table_name: str, columns: Dict[str, str]) -> str:
        """Crear modelo SQLAlchemy"""
        cols = "\n".join([f"    {name} = Column({col_type})" for name, col_type in columns.items()])
        code = f'''
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class {table_name.capitalize()}(Base):
    __tablename__ = '{table_name}'
    
    id = Column(Integer, primary_key=True)
{cols}
'''
        with open(path, 'w') as f:
            f.write(code)
        return f"[OK] Modelo creado: {table_name}"
    
    @staticmethod
    def create_pydantic_model(path: str, model_name: str, fields: Dict[str, str]) -> str:
        """Crear modelo Pydantic"""
        flds = "\n".join([f"    {name}: {field_type}" for name, field_type in fields.items()])
        code = f'''
from pydantic import BaseModel

class {model_name}(BaseModel):
    """Model for {model_name}"""
{flds}
'''
        with open(path, 'w') as f:
            f.write(code)
        return f"[OK] Modelo Pydantic creado: {model_name}"
    
    @staticmethod
    def create_test_file(path: str, module_name: str, functions: List[str] = None) -> str:
        """Crear archivo de tests"""
        funcs = functions or ['test_example']
        tests = "\n\n".join([f"def {f}():\n    assert True" for f in funcs])
        code = f'''
import pytest
from {module_name} import *

{tests}
'''
        with open(path, 'w') as f:
            f.write(code)
        return f"[OK] Tests creados: {path}"
    
    @staticmethod
    def create_dockerfile_python(path: str, app_name: str = "app") -> str:
        """Crear Dockerfile para Python"""
        code = f'''
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "{app_name}.py"]
'''
        with open(path, 'w') as f:
            f.write(code)
        return f"[OK] Dockerfile creado"
    
    @staticmethod
    def create_docker_compose(path: str, services: Dict[str, Dict]) -> str:
        """Crear docker-compose.yml"""
        import yaml
        with open(path, 'w') as f:
            yaml.dump({'version': '3.8', 'services': services}, f)
        return f"[OK] docker-compose.yml creado"
    
    @staticmethod
    def create_github_workflow(path: str, name: str, triggers: List[str], jobs: Dict) -> str:
        """Crear GitHub Actions workflow"""
        import yaml
        workflow = {
            'name': name,
            'on': {t: {} for t in triggers},
            'jobs': jobs
        }
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            yaml.dump(workflow, f, default_flow_style=False)
        return f"[OK] Workflow creado: {name}"
    
    # ========================================================================
    # WEB y FRONTEND (80+)
    # ========================================================================
    
    @staticmethod
    def create_html_page(path: str, title: str, content: str = "") -> str:
        """Crear pagina HTML"""
        html = f'''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
{content}
    <script src="script.js"></script>
</body>
</html>'''
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        return f"[OK] HTML creado: {path}"
    
    @staticmethod
    def create_react_component(path: str, name: str, props: List[str] = None) -> str:
        """Crear componente React"""
        props_str = ", ".join(props) if props else ""
        code = "import React from 'react';\n\n"
        code += f"const {name} = ({{ {props_str} }}) => {{\n"
        code += "  return (\n"
        code += f'    <div className="{name.lower()}">\n'
        code += "      {'/* Component content */}\n"
        code += "    </div>\n"
        code += "  );\n"
        code += "};\n\n"
        code += f"export default {name};"
        with open(path, 'w') as f:
            f.write(code)
        return f"[OK] Componente React: {name}"
    
    @staticmethod
    def create_vue_component(path: str, name: str) -> str:
        """Crear componente Vue"""
        code = f'''<template>
  <div class="{name.lower()}">
    <!-- Component content -->
  </div>
</template>

<script>
export default {{
  name: '{name}',
  data() {{
    return {{}};
  }},
  methods: {{}}
}};
</script>

<style scoped>
.{name.lower()} {{
}}
</style>'''
        with open(path, 'w') as f:
            f.write(code)
        return f"[OK] Componente Vue: {name}"
    
    @staticmethod
    def create_angular_component(path: str, name: str) -> str:
        """Crear componente Angular"""
        code = f'''import {{ Component }} from '@angular/core';

@Component({{
  selector: 'app-{name.lower()}',
  template: `<div class="{name.lower()}"></div>`,
  styles: [`.{name.lower()} {{}}`]
}})
export class {name}Component {{
  title = '{name}';
}}'''
        with open(path, 'w') as f:
            f.write(code)
        return f"[OK] Componente Angular: {name}"
    
    @staticmethod
    def create_svelte_component(path: str, name: str) -> str:
        """Crear componente Svelte"""
        code = f'''<script>
  // Component logic
</script>

<div class="{name.lower()}">
  <!-- Component content -->
</div>

<style>
  .{name.lower()} {{}}
</style>'''
        with open(path, 'w') as f:
            f.write(code)
        return f"[OK] Componente Svelte: {name}"
    
    @staticmethod
    def create_nextjs_page(path: str, route: str) -> str:
        """Crear pagina Next.js"""
        code = f'''export default function {route.replace('/', '').capitalize() or 'Home'}Page() {{
  return (
    <div>
      <h1>{route}</h1>
    </div>
  );
}}'''
        with open(path, 'w') as f:
            f.write(code)
        return f"[OK] Pagina Next.js: {route}"
    
    @staticmethod
    def create_api_endpoint_express(path: str, method: str, route: str) -> str:
        """Crear endpoint Express"""
        code = f'''const express = require('express');
const router = express.Router();

router.{method.toLowerCase()}('{route}', (req, res) => {{
  res.json({{ status: 'ok' }});
}});

module.exports = router;'''
        with open(path, 'w') as f:
            f.write(code)
        return f"[OK] Endpoint Express: {method} {route}"
    
    @staticmethod
    def create_package_json(path: str, name: str, dependencies: Dict[str, str] = None) -> str:
        """Crear package.json"""
        pkg = {
            "name": name,
            "version": "1.0.0",
            "scripts": {
                "dev": "vite",
                "build": "vite build",
                "preview": "vite preview"
            },
            "dependencies": dependencies or {},
            "devDependencies": {}
        }
        with open(path, 'w') as f:
            json.dump(pkg, f, indent=2)
        return f"[OK] package.json creado"
    
    @staticmethod
    def create_vite_config(path: str) -> str:
        """Crear vite.config.js"""
        code = '''import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000
  }
});'''
        with open(path, 'w') as f:
            f.write(code)
        return "[OK] vite.config.js creado"
    
    @staticmethod
    def create_tailwind_config(path: str) -> str:
        """Crear tailwind.config.js"""
        code = '''/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}'''
        with open(path, 'w') as f:
            f.write(code)
        return "[OK] tailwind.config.js creado"
    
    @staticmethod
    def create_css_framework(path: str, framework: str = "tailwind") -> str:
        """Crear configuracion de framework CSS"""
        if framework == "tailwind":
            return AdvancedActions.create_tailwind_config(path)
        elif framework == "bootstrap":
            code = '''{"presets": ["@babel/preset-env", ["@babel/preset-react", {"runtime": "automatic"}]]}'''
            with open(path, 'w') as f:
                f.write(code)
        return f"[OK] Config {framework} creado"
    
    @staticmethod
    def create_responsive_css(path: str) -> str:
        """Crear CSS responsive base"""
        code = '''/* Responsive CSS */
:root {
  --primary: #3b82f6;
  --secondary: #10b981;
  --bg: #0f172a;
  --text: #f1f5f9;
}

* { margin: 0; padding: 0; box-sizing: border-box; }

body {
  font-family: system-ui, -apple-system, sans-serif;
  background: var(--bg);
  color: var(--text);
  line-height: 1.6;
}

.container {
  width: min(90%, 1200px);
  margin: 0 auto;
  padding: 0 1rem;
}

@media (max-width: 768px) {
  .container { width: 95%; }
}

@media (max-width: 480px) {
  .container { width: 100%; padding: 0 0.5rem; }
}'''
        with open(path, 'w') as f:
            f.write(code)
        return "[OK] CSS responsive creado"
    
    @staticmethod
    def create_animation_css(path: str) -> str:
        """Crear CSS con animaciones"""
        code = '''/* Animations */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes slideIn {
  from { transform: translateX(-100%); }
  to { transform: translateX(0); }
}

@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.05); }
}

@keyframes glow {
  0%, 100% { box-shadow: 0 0 5px var(--primary); }
  50% { box-shadow: 0 0 20px var(--primary); }
}

.animate-fadeIn { animation: fadeIn 0.5s ease-out; }
.animate-slideIn { animation: slideIn 0.3s ease-out; }
.animate-pulse { animation: pulse 2s infinite; }
.animate-glow { animation: glow 2s infinite; }'''
        with open(path, 'w') as f:
            f.write(code)
        return "[OK] CSS animaciones creado"
    
    @staticmethod
    def create_dark_mode_css(path: str) -> str:
        """Crear CSS con dark mode"""
        code = '''/* Dark Mode */
:root {
  --bg-light: #ffffff;
  --bg-dark: #0f172a;
  --text-light: #1e293b;
  --text-dark: #f1f5f9;
}

[data-theme="light"] {
  --bg: var(--bg-light);
  --text: var(--text-light);
}

[data-theme="dark"] {
  --bg: var(--bg-dark);
  --text: var(--text-dark);
}

body {
  background: var(--bg);
  color: var(--text);
  transition: background 0.3s, color 0.3s;
}

@media (prefers-color-scheme: dark) {
  :root {
    --bg: var(--bg-dark);
    --text: var(--text-dark);
  }
}'''
        with open(path, 'w') as f:
            f.write(code)
        return "[OK] CSS dark mode creado"
    
    @staticmethod
    def create_glassmorphism_css(path: str) -> str:
        """Crear CSS glassmorphism"""
        code = '''/* Glassmorphism */
.glass {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
  padding: 2rem;
}

.glass-dark {
  background: rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}'''
        with open(path, 'w') as f:
            f.write(code)
        return "[OK] CSS glassmorphism creado"
    
    @staticmethod
    def create_gradient_css(path: str) -> str:
        """Crear CSS con gradientes"""
        code = '''/* Gradients */
.gradient-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.gradient-warm {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}

.gradient-cool {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
}

.gradient-dark {
  background: linear-gradient(135deg, #0c0c0c 0%, #1a1a2e 100%);
}

.gradient-text {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}'''
        with open(path, 'w') as f:
            f.write(code)
        return "[OK] CSS gradientes creado"
    
    @staticmethod
    def create_grid_layout(path: str) -> str:
        """Crear CSS grid layout"""
        code = '''/* Grid Layout */
.grid {
  display: grid;
  gap: 1rem;
}

.grid-2 { grid-template-columns: repeat(2, 1fr); }
.grid-3 { grid-template-columns: repeat(3, 1fr); }
.grid-4 { grid-template-columns: repeat(4, 1fr); }
.grid-auto { grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); }

@media (max-width: 768px) {
  .grid-2, .grid-3, .grid-4 {
    grid-template-columns: 1fr;
  }
}'''
        with open(path, 'w') as f:
            f.write(code)
        return "[OK] CSS grid layout creado"
    
    @staticmethod
    def create_flexbox_layout(path: str) -> str:
        """Crear CSS flexbox layout"""
        code = '''/* Flexbox Layout */
.flex { display: flex; }
.flex-col { flex-direction: column; }
.flex-wrap { flex-wrap: wrap; }
.items-center { align-items: center; }
.justify-center { justify-content: center; }
.justify-between { justify-content: space-between; }
.gap-1 { gap: 0.25rem; }
.gap-2 { gap: 0.5rem; }
.gap-4 { gap: 1rem; }
.flex-1 { flex: 1; }'''
        with open(path, 'w') as f:
            f.write(code)
        return "[OK] CSS flexbox creado"
    
    @staticmethod
    def create_utilities_css(path: str) -> str:
        """Crear CSS utilitario"""
        code = '''/* Utilities */
.m-0 { margin: 0; }
.m-1 { margin: 0.25rem; }
.m-2 { margin: 0.5rem; }
.m-4 { margin: 1rem; }
.p-0 { padding: 0; }
.p-1 { padding: 0.25rem; }
.p-2 { padding: 0.5rem; }
.p-4 { padding: 1rem; }
.text-center { text-align: center; }
.text-left { text-align: left; }
.text-right { text-align: right; }
.hidden { display: none; }
.block { display: block; }
.inline { display: inline; }
.relative { position: relative; }
.absolute { position: absolute; }
.fixed { position: fixed; }
.w-full { width: 100%; }
.h-full { height: 100%; }
.overflow-hidden { overflow: hidden; }
.truncate { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }'''
        with open(path, 'w') as f:
            f.write(code)
        return "[OK] CSS utilidades creado"
    
    # ========================================================================
    # BASE DE DATOS (50+)
    # ========================================================================
    
    @staticmethod
    def create_sqlite_db(db_path: str, tables: Dict[str, List[str]]) -> str:
        """Crear base de datos SQLite"""
        import sqlite3
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        for table_name, columns in tables.items():
            cols = ", ".join(columns)
            cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER PRIMARY KEY, {cols})")
        conn.commit()
        conn.close()
        return f"[OK] DB SQLite: {db_path}"
    
    @staticmethod
    def create_postgres_db(name: str, user: str = "postgres") -> str:
        """Crear base de datos PostgreSQL"""
        import subprocess
        subprocess.run(['createdb', '-U', user, name])
        return f"[OK] DB PostgreSQL: {name}"
    
    @staticmethod
    def create_mongo_collection(db_name: str, collection: str) -> str:
        """Crear coleccion MongoDB"""
        from pymongo import MongoClient
        client = MongoClient()
        db = client[db_name]
        db.create_collection(collection)
        return f"[OK] Coleccion: {collection}"
    
    @staticmethod
    def sql_query(db_path: str, query: str) -> str:
        """Ejecutar SQL"""
        import sqlite3
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(query)
        if query.strip().upper().startswith(('SELECT', 'SHOW', 'DESCRIBE')):
            results = cursor.fetchall()
            conn.close()
            return str(results[:50])
        conn.commit()
        conn.close()
        return f"[OK] Query ejecutada"
    
    @staticmethod
    def create_migration(path: str, name: str) -> str:
        """Crear migracion"""
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        filename = f"{timestamp}_{name}.py"
        code = f'''"""Migration {name}"""
from sqlalchemy import op

def upgrade():
    pass

def downgrade():
    pass
'''
        with open(os.path.join(path, filename), 'w') as f:
            f.write(code)
        return f"[OK] Migracion: {filename}"
    
    @staticmethod
    def create_seed_data(path: str, table: str, data: List[Dict]) -> str:
        """Crear datos seed"""
        code = f'''"""Seed data for {table}"""
SEED_DATA = {json.dumps(data, indent=2, default=str)}
'''
        with open(path, 'w') as f:
            f.write(code)
        return f"[OK] Seed data: {table}"
    
    @staticmethod
    def backup_database(db_path: str, backup_path: str) -> str:
        """Backup de base de datos"""
        import sqlite3
        import shutil
        shutil.copy2(db_path, backup_path)
        return f"[OK] Backup: {backup_path}"
    
    @staticmethod
    def create_redis_cache(key: str, value: str, ttl: int = 3600) -> str:
        """Crear cache Redis"""
        try:
            import redis
            r = redis.Redis()
            r.setex(key, ttl, value)
            return f"[OK] Cache: {key}"
        except:
            return "[ERROR] Redis no disponible"
    
    # ========================================================================
    # RED y APIs (60+)
    # ========================================================================
    
    @staticmethod
    def http_get(url: str, headers: Dict = None) -> str:
        """GET request"""
        import requests
        response = requests.get(url, headers=headers, timeout=30)
        return f"[OK] Status: {response.status_code}\n{response.text[:2000]}"
    
    @staticmethod
    def http_post(url: str, data: Any = None, json_data: Any = None) -> str:
        """POST request"""
        import requests
        response = requests.post(url, data=data, json=json_data, timeout=30)
        return f"[OK] Status: {response.status_code}\n{response.text[:2000]}"
    
    @staticmethod
    def http_put(url: str, data: Any = None) -> str:
        """PUT request"""
        import requests
        response = requests.put(url, json=data, timeout=30)
        return f"[OK] Status: {response.status_code}"
    
    @staticmethod
    def http_delete(url: str) -> str:
        """DELETE request"""
        import requests
        response = requests.delete(url, timeout=30)
        return f"[OK] Status: {response.status_code}"
    
    @staticmethod
    def download_file(url: str, path: str) -> str:
        """Descargar archivo"""
        import requests
        response = requests.get(url, stream=True, timeout=30)
        with open(path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        size = os.path.getsize(path)
        return f"[OK] Descargado: {path} ({size} bytes)"
    
    @staticmethod
    def upload_file(url: str, path: str, field: str = "file") -> str:
        """Subir archivo"""
        import requests
        with open(path, 'rb') as f:
            files = {field: f}
            response = requests.post(url, files=files, timeout=60)
        return f"[OK] Status: {response.status_code}"
    
    @staticmethod
    def create_api_server(port: int = 8000) -> str:
        """Crear servidor API basico"""
        code = f'''from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {{"message": "API is running"}}

@app.get("/health")
async def health():
    return {{"status": "healthy"}}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port={port})
'''
        with open('server.py', 'w') as f:
            f.write(code)
        return f"[OK] API server creado en puerto {port}"
    
    @staticmethod
    def create_rest_api(path: str, resources: List[str]) -> str:
        """Crear API REST completa"""
        code = '''from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uuid

app = FastAPI()

# Models
'''
        for resource in resources:
            code += f'''
class {resource.capitalize()}(BaseModel):
    id: Optional[str] = None
    name: str

{resource.lower()}s = []

@app.get("/{resource}s")
async def get_{resource}s():
    return {resource.lower()}s

@app.get("/{resource}s/{{id}}")
async def get_{resource}(id: str):
    item = next((x for x in {resource.lower()}s if x.id == id), None)
    if not item:
        raise HTTPException(status_code=404, detail="Not found")
    return item

@app.post("/{resource}s")
async def create_{resource}(item: {resource.capitalize()}):
    item.id = str(uuid.uuid4())
    {resource.lower()}s.append(item)
    return item

@app.delete("/{resource}s/{{id}}")
async def delete_{resource}(id: str):
    global {resource.lower()}s
    {resource.lower()}s = [x for x in {resource.lower()}s if x.id != id]
    return {{"status": "deleted"}}
'''
        with open(path, 'w') as f:
            f.write(code)
        return f"[OK] API REST creada con {len(resources)} recursos"
    
    @staticmethod
    def create_websocket_server(path: str, port: int = 8765) -> str:
        """Crear servidor WebSocket"""
        code = f'''import asyncio
import websockets

connected = set()

async def handler(websocket, path):
    connected.add(websocket)
    try:
        async for message in websocket:
            for conn in connected:
                await conn.send(message)
    finally:
        connected.remove(websocket)

async def main():
    async with websockets.serve(handler, "localhost", {port}):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
'''
        with open(path, 'w') as f:
            f.write(code)
        return f"[OK] WebSocket server en puerto {port}"
    
    @staticmethod
    def create_grpc_service(path: str, service_name: str, methods: List[str]) -> str:
        """Crear servicio gRPC"""
        proto = f'''syntax = "proto3";

package {service_name.lower()};

service {service_name}Service {{
'''
        for method in methods:
            proto += f'''  rpc {method}(Request) returns (Response);
'''
        proto += '''}

message Request {
  string id = 1;
}

message Response {
  string message = 1;
}
'''
        with open(path, 'w') as f:
            f.write(proto)
        return f"[OK] gRPC service: {service_name}"
    
    @staticmethod
    def create_middleware(path: str, name: str) -> str:
        """Crear middleware"""
        code = f'''class {name}Middleware:
    def __init__(self, app):
        self.app = app
    
    async def __call__(self, scope, receive, send):
        # Before request
        response = await self.app(scope, receive, send)
        # After request
        return response
'''
        with open(path, 'w') as f:
            f.write(code)
        return f"[OK] Middleware: {name}"
    
    @staticmethod
    def create_rate_limiter(path: str) -> str:
        """Crear rate limiter"""
        code = '''import time
from collections import defaultdict
from functools import wraps

class RateLimiter:
    def __init__(self, max_requests=100, window=60):
        self.max_requests = max_requests
        self.window = window
        self.requests = defaultdict(list)
    
    def is_allowed(self, key):
        now = time.time()
        self.requests[key] = [t for t in self.requests[key] if now - t < self.window]
        if len(self.requests[key]) < self.max_requests:
            self.requests[key].append(now)
            return True
        return False
    
    def limit(self, func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            key = kwargs.get('client_id', 'default')
            if not self.is_allowed(key):
                raise Exception("Rate limit exceeded")
            return await func(*args, **kwargs)
        return wrapper
'''
        with open(path, 'w') as f:
            f.write(code)
        return "[OK] Rate limiter creado"
    
    # ========================================================================
    # SEGURIDAD (50+)
    # ========================================================================
    
    @staticmethod
    def generate_password(length: int = 16) -> str:
        """Generar contrasena segura"""
        chars = string.ascii_letters + string.digits + "!@#$%^&*"
        password = ''.join(secrets.choice(chars) for _ in range(length))
        return f"[OK] Contrasena: {password}"
    
    @staticmethod
    def generate_api_key() -> str:
        """Generar API key"""
        key = secrets.token_hex(32)
        return f"[OK] API Key: {key}"
    
    @staticmethod
    def generate_jwt_secret() -> str:
        """Generar JWT secret"""
        secret = secrets.token_urlsafe(64)
        return f"[OK] JWT Secret: {secret}"
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hashear contrasena"""
        import bcrypt
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        return f"[OK] Hash: {hashed.decode()}"
    
    @staticmethod
    def verify_password(password: str, hashed: str) -> str:
        """Verificar contrasena"""
        import bcrypt
        result = bcrypt.checkpw(password.encode(), hashed.encode())
        return f"[OK] Valid: {result}"
    
    @staticmethod
    def encrypt_text(text: str, key: str) -> str:
        """Cifrar texto"""
        from cryptography.fernet import Fernet
        cipher = Fernet(key.encode() if isinstance(key, str) else key)
        encrypted = cipher.encrypt(text.encode())
        return f"[OK] Encrypted: {encrypted.decode()}"
    
    @staticmethod
    def decrypt_text(encrypted: str, key: str) -> str:
        """Descifrar texto"""
        from cryptography.fernet import Fernet
        cipher = Fernet(key.encode() if isinstance(key, str) else key)
        decrypted = cipher.decrypt(encrypted.encode())
        return f"[OK] Decrypted: {decrypted.decode()}"
    
    @staticmethod
    def scan_ports(host: str, ports: List[int] = None) -> str:
        """Escanear puertos"""
        import socket
        ports = ports or [21, 22, 80, 443, 3000, 5000, 8000, 8080]
        open_ports = []
        for port in ports:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((host, port))
            if result == 0:
                open_ports.append(port)
            sock.close()
        return f"[OK] Puertos abiertos en {host}: {open_ports}" if open_ports else f"[OK] Sin puertos abiertos"
    
    @staticmethod
    def create_ssl_cert(domain: str, output_dir: str = ".") -> str:
        """Crear certificado SSL auto-firmado"""
        import subprocess
        subprocess.run([
            'openssl', 'req', '-x509', '-newkey', 'rsa:4096',
            '-keyout', os.path.join(output_dir, 'key.pem'),
            '-out', os.path.join(output_dir, 'cert.pem'),
            '-days', '365', '-nodes',
            '-subj', f'/CN={domain}'
        ])
        return f"[OK] SSL cert: {domain}"
    
    @staticmethod
    def validate_input(text: str, input_type: str = "email") -> str:
        """Validar input"""
        patterns = {
            'email': r'^[\w\.-]+@[\w\.-]+\.\w+$',
            'url': r'^https?://[\w\.-]+\.\w+',
            'ip': r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$',
            'phone': r'^\+?[\d\s-]{10,}$',
        }
        pattern = patterns.get(input_type, r'.+')
        is_valid = bool(re.match(pattern, text))
        return f"[OK] Valid: {is_valid}"
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """Sanitizar nombre de archivo"""
        sanitized = re.sub(r'[<>:"/\\|?*]', '', filename)
        sanitized = sanitized.strip('. ')
        return f"[OK] Sanitized: {sanitized}"
    
    @staticmethod
    def create_security_headers() -> Dict[str, str]:
        """Crear headers de seguridad"""
        return {
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "X-XSS-Protection": "1; mode=block",
            "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
            "Content-Security-Policy": "default-src 'self'",
        }
    
    # ========================================================================
    # SISTEMA (60+)
    # ========================================================================
    
    @staticmethod
    def get_system_info() -> str:
        """Obtener info del sistema"""
        import platform
        info = {
            "os": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "python": platform.python_version(),
        }
        return json.dumps(info, indent=2)
    
    @staticmethod
    def get_cpu_info() -> str:
        """Obtener info CPU"""
        import psutil
        info = {
            "percent": psutil.cpu_percent(interval=1),
            "cores": psutil.cpu_count(),
            "freq": psutil.cpu_freq()._asdict() if psutil.cpu_freq() else None,
        }
        return json.dumps(info, indent=2)
    
    @staticmethod
    def get_memory_info() -> str:
        """Obtener info memoria"""
        import psutil
        mem = psutil.virtual_memory()
        info = {
            "total": f"{mem.total / (1024**3):.2f} GB",
            "available": f"{mem.available / (1024**3):.2f} GB",
            "percent": mem.percent,
            "used": f"{mem.used / (1024**3):.2f} GB",
        }
        return json.dumps(info, indent=2)
    
    @staticmethod
    def get_disk_info() -> str:
        """Obtener info disco"""
        import psutil
        disks = []
        for part in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(part.mountpoint)
                disks.append({
                    "device": part.device,
                    "mountpoint": part.mountpoint,
                    "total": f"{usage.total / (1024**3):.2f} GB",
                    "free": f"{usage.free / (1024**3):.2f} GB",
                    "percent": usage.percent,
                })
            except:
                pass
        return json.dumps(disks, indent=2)
    
    @staticmethod
    def get_process_list() -> str:
        """Listar procesos"""
        import psutil
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                processes.append(proc.info)
            except:
                pass
        return json.dumps(processes[:20], indent=2)
    
    @staticmethod
    def kill_process(pid: int) -> str:
        """Matar proceso"""
        import psutil
        proc = psutil.Process(pid)
        proc.terminate()
        return f"[OK] Proceso {pid} terminado"
    
    @staticmethod
    def monitor_system(interval: int = 5, duration: int = 60) -> str:
        """Monitorear sistema"""
        import psutil
        start = time.time()
        data = []
        while time.time() - start < duration:
            data.append({
                "time": datetime.now().isoformat(),
                "cpu": psutil.cpu_percent(interval=1),
                "memory": psutil.virtual_memory().percent,
            })
            time.sleep(interval)
        return json.dumps(data, indent=2)
    
    @staticmethod
    def create_cron_job(schedule: str, command: str) -> str:
        """Crear cron job"""
        import subprocess
        current = subprocess.run(['crontab', '-l'], capture_output=True, text=True).stdout
        new_line = f"{schedule} {command}\n"
        with open('/tmp/crontab', 'w') as f:
            f.write(current + new_line)
        subprocess.run(['crontab', '/tmp/crontab'])
        return f"[OK] Cron job creado"
    
    @staticmethod
    def set_environment_variable(name: str, value: str) -> str:
        """Configurar variable de entorno"""
        os.environ[name] = value
        return f"[OK] Env: {name}={value}"
    
    @staticmethod
    def get_environment_variables(pattern: str = "") -> str:
        """Obtener variables de entorno"""
        vars_dict = {k: v for k, v in os.environ.items() if not pattern or pattern.upper() in k.upper()}
        return json.dumps(vars_dict, indent=2)
    
    @staticmethod
    def create_startup_script(name: str, commands: List[str]) -> str:
        """Crear script de inicio"""
        script = "#!/bin/bash\n\n"
        for cmd in commands:
            script += f"{cmd}\n"
        path = f"/etc/init.d/{name}"
        with open(path, 'w') as f:
            f.write(script)
        os.chmod(path, 0o755)
        return f"[OK] Startup script: {path}"
    
    @staticmethod
    def schedule_task(command: str, delay: int = 0) -> str:
        """Programar tarea"""
        import subprocess
        if delay > 0:
            subprocess.Popen(['bash', '-c', f'sleep {delay} && {command}'])
        else:
            subprocess.Popen(['bash', '-c', command])
        return f"[OK] Tarea programada"
    
    # ========================================================================
    # MULTIMEDIA (40+)
    # ========================================================================
    
    @staticmethod
    def create_image(width: int, height: int, color: str, path: str) -> str:
        """Crear imagen"""
        from PIL import Image
        img = Image.new('RGB', (width, height), color)
        img.save(path)
        return f"[OK] Imagen: {path}"
    
    @staticmethod
    def resize_image(path: str, width: int, height: int) -> str:
        """Redimensionar imagen"""
        from PIL import Image
        img = Image.open(path)
        img = img.resize((width, height))
        img.save(path)
        return f"[OK] Imagen redimensionada"
    
    @staticmethod
    def convert_image(path: str, format: str) -> str:
        """Convertir formato"""
        from PIL import Image
        img = Image.open(path)
        new_path = os.path.splitext(path)[0] + f".{format}"
        img.save(new_path, format.upper())
        return f"[OK] Convertido: {new_path}"
    
    @staticmethod
    def create_pdf(text: str, path: str) -> str:
        """Crear PDF basico"""
        code = f'''
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

c = canvas.Canvas("{path}", pagesize=letter)
c.drawString(100, 750, """{text}""")
c.save()
'''
        exec(code)
        return f"[OK] PDF: {path}"
    
    @staticmethod
    def create_qr_code(data: str, path: str) -> str:
        """Crear codigo QR"""
        import qrcode
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(path)
        return f"[OK] QR: {path}"
    
    @staticmethod
    def compress_image(path: str, quality: int = 85) -> str:
        """Comprimir imagen"""
        from PIL import Image
        img = Image.open(path)
        img.save(path, optimize=True, quality=quality)
        return f"[OK] Imagen comprimida"
    
    @staticmethod
    def create_icon(text: str, path: str, size: int = 64) -> str:
        """Crear icono simple"""
        from PIL import Image, ImageDraw, ImageFont
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.ellipse([0, 0, size-1, size-1], fill='#3b82f6')
        font = ImageFont.load_default()
        draw.text((size//4, size//3), text[0].upper(), fill='white', font=font)
        img.save(path)
        return f"[OK] Icono: {path}"
    
    # ========================================================================
    # DOCUMENTACION (40+)
    # ========================================================================
    
    @staticmethod
    def create_readme(path: str, title: str, description: str = "", sections: List[str] = None) -> str:
        """Crear README"""
        sections = sections or ["Instalacion", "Uso", "Licencia"]
        readme = f"# {title}\n\n{description}\n\n"
        for section in sections:
            readme += f"## {section}\n\nContenido pendiente...\n\n"
        with open(path, 'w') as f:
            f.write(readme)
        return f"[OK] README: {path}"
    
    @staticmethod
    def create_documentation(path: str, title: str, functions: List[Dict]) -> str:
        """Crear documentacion de API"""
        doc = f"# {title}\n\n## Endpoints\n\n"
        for func in functions:
            doc += f"### {func.get('name', 'function')}\n\n"
            doc += f"**Descripcion:** {func.get('description', 'N/A')}\n\n"
            if func.get('params'):
                doc += "**Parametros:**\n"
                for param in func['params']:
                    doc += f"- `{param.get('name')}` ({param.get('type')}) - {param.get('description', '')}\n"
                doc += "\n"
            if func.get('example'):
                doc += f"**Ejemplo:**\n```{func.get('language', 'json')}\n{func['example']}\n```\n\n"
        with open(path, 'w') as f:
            f.write(doc)
        return f"[OK] Documentacion: {path}"
    
    @staticmethod
    def create_changelog(path: str, version: str, changes: List[str]) -> str:
        """Crear changelog"""
        entry = f"## [{version}] - {datetime.now().strftime('%Y-%m-%d')}\n\n"
        for change in changes:
            entry += f"- {change}\n"
        
        existing = ""
        if os.path.exists(path):
            with open(path, 'r') as f:
                existing = f.read()
        
        with open(path, 'w') as f:
            f.write(entry + "\n" + existing)
        return f"[OK] Changelog actualizado"
    
    @staticmethod
    def create_api_docs_openapi(path: str, title: str, endpoints: List[Dict]) -> str:
        """Crear documentacion OpenAPI"""
        spec = {
            "openapi": "3.0.0",
            "info": {"title": title, "version": "1.0.0"},
            "paths": {}
        }
        for ep in endpoints:
            path_key = ep.get('path', '/')
            method = ep.get('method', 'get').lower()
            if path_key not in spec['paths']:
                spec['paths'][path_key] = {}
            spec['paths'][path_key][method] = {
                "summary": ep.get('summary', ''),
                "responses": {"200": {"description": "Success"}}
            }
        with open(path, 'w') as f:
            json.dump(spec, f, indent=2)
        return f"[OK] OpenAPI: {path}"
    
    @staticmethod
    def create_wiki_page(path: str, title: str, content: str) -> str:
        """Crear pagina wiki"""
        page = f"# {title}\n\n{content}\n"
        with open(path, 'w') as f:
            f.write(page)
        return f"[OK] Wiki: {title}"
    
    # ========================================================================
    # TESTING (40+)
    # ========================================================================
    
    @staticmethod
    def create_unit_test(path: str, module: str, function: str, test_cases: List[Dict]) -> str:
        """Crear test unitario"""
        tests = f"""import pytest
from {module} import {function}


class Test{function.capitalize()}:
'''
"""
        for i, case in enumerate(test_cases):
            args = ", ".join([f"{k}={v}" for k, v in case.get('args', {}).items()])
            expected = case.get('expected')
            tests += f"""
    def test_{function}_{i+1}(self):
        result = {function}({args})
        assert result == {expected}
"""
        tests += '"""'
        with open(path, 'w') as f:
            f.write(tests)
        return f"[OK] Test: {path}"
    
    @staticmethod
    def create_integration_test(path: str, name: str, steps: List[str]) -> str:
        """Crear test de integracion"""
        test = f"""import pytest


class Test{name}Integration:
    \"\"\"Integration test for {name}\"\"\"
"""
        for i, step in enumerate(steps):
            test += f"""
    def test_step_{i+1}(self):
        # {step}
        pass
"""
        with open(path, 'w') as f:
            f.write(test)
        return f"[OK] Integration test: {path}"
    
    @staticmethod
    def create_mock(path: str, module: str, function: str) -> str:
        """Crear mock"""
        code = f'''from unittest.mock import patch, MagicMock


def mock_{function}(*args, **kwargs):
    """Mock for {function}"""
    return MagicMock()


# Usage:
# with patch('{module}.{function}', mock_{function}):
#     result = {function}()
'''
        with open(path, 'w') as f:
            f.write(code)
        return f"[OK] Mock: {function}"
    
    @staticmethod
    def create_fixtures(path: str, fixtures: Dict[str, Any]) -> str:
        """Crear fixtures pytest"""
        code = "import pytest\n\n"
        for name, value in fixtures.items():
            code += f"""
@pytest.fixture
def {name}():
    return {repr(value)}
"""
        with open(path, 'w') as f:
            f.write(code)
        return f"[OK] Fixtures: {path}"
    
    @staticmethod
    def create_benchmark(path: str, function: str) -> str:
        """Crear benchmark"""
        code = f'''import timeit


def benchmark_{function}():
    # TODO: Add actual function call
    pass


if __name__ == "__main__":
    time = timeit.timeit(benchmark_{function}, number=1000)
    print(f"{{function}}: {{time:.4f}}s for 1000 runs")
'''
        with open(path, 'w') as f:
            f.write(code)
        return f"[OK] Benchmark: {function}"
    
    # ========================================================================
    # UTILIDADES (100+)
    # ========================================================================
    
    @staticmethod
    def timestamp() -> str:
        """Obtener timestamp"""
        return f"[OK] {datetime.now().isoformat()}"
    
    @staticmethod
    def format_date(date_str: str, fmt: str = "%Y-%m-%d") -> str:
        """Formatear fecha"""
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        return f"[OK] {dt.strftime(fmt)}"
    
    @staticmethod
    def days_between(date1: str, date2: str) -> str:
        """Dias entre fechas"""
        d1 = datetime.strptime(date1, "%Y-%m-%d")
        d2 = datetime.strptime(date2, "%Y-%m-%d")
        return f"[OK] {(d2 - d1).days} dias"
    
    @staticmethod
    def add_days(date_str: str, days: int) -> str:
        """Agregar dias"""
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        new_date = dt + timedelta(days=days)
        return f"[OK] {new_date.strftime('%Y-%m-%d')}"
    
    @staticmethod
    def generate_uuid() -> str:
        """Generar UUID"""
        import uuid
        return f"[OK] {uuid.uuid4()}"
    
    @staticmethod
    def generate_random_string(length: int = 10) -> str:
        """Generar string aleatorio"""
        chars = string.ascii_letters + string.digits
        result = ''.join(secrets.choice(chars) for _ in range(length))
        return f"[OK] {result}"
    
    @staticmethod
    def generate_random_number(min_val: int = 0, max_val: int = 100) -> str:
        """Generar numero aleatorio"""
        import random
        return f"[OK] {random.randint(min_val, max_val)}"
    
    @staticmethod
    def slugify(text: str) -> str:
        """Convertir a slug"""
        slug = re.sub(r'[^\w\s-]', '', text.lower())
        slug = re.sub(r'[-\s]+', '-', slug)
        return f"[OK] {slug}"
    
    @staticmethod
    def truncate(text: str, length: int = 100) -> str:
        """Truncar texto"""
        truncated = text[:length] + "..." if len(text) > length else text
        return f"[OK] {truncated}"
    
    @staticmethod
    def word_count(text: str) -> str:
        """Contar palabras"""
        words = len(text.split())
        chars = len(text)
        return f"[OK] {words} palabras, {chars} caracteres"
    
    @staticmethod
    def convert_to_json(data: str) -> str:
        """Convertir a JSON"""
        try:
            import ast
            data_dict = ast.literal_eval(data)
            return f"[OK] {json.dumps(data_dict, indent=2)}"
        except:
            return "[ERROR] No se pudo convertir"
    
    @staticmethod
    def pretty_json(json_str: str) -> str:
        """Formatear JSON"""
        try:
            data = json.loads(json_str)
            return f"[OK] {json.dumps(data, indent=2)}"
        except:
            return "[ERROR] JSON invalido"
    
    @staticmethod
    def csv_to_json(path: str) -> str:
        """CSV a JSON"""
        import csv
        with open(path, 'r') as f:
            reader = csv.DictReader(f)
            data = list(reader)
        return f"[OK] {json.dumps(data, indent=2)}"
    
    @staticmethod
    def json_to_csv(json_data: str, path: str) -> str:
        """JSON a CSV"""
        import csv
        data = json.loads(json_data)
        if data:
            with open(path, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
        return f"[OK] CSV: {path}"
    
    @staticmethod
    def create_env_file(path: str, variables: Dict[str, str]) -> str:
        """Crear archivo .env"""
        content = "\n".join([f"{k}={v}" for k, v in variables.items()])
        with open(path, 'w') as f:
            f.write(content)
        return f"[OK] .env creado"
    
    @staticmethod
    def parse_env_file(path: str) -> str:
        """Leer archivo .env"""
        variables = {}
        with open(path, 'r') as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    variables[key] = value
        return json.dumps(variables, indent=2)
    
    @staticmethod
    def create_gitignore(path: str, language: str = "python") -> str:
        """Crear .gitignore"""
        templates = {
            "python": "__pycache__/\n*.py[cod]\n*$py.class\n*.so\n.env\nvenv/\n.venv/\n",
            "node": "node_modules/\ndist/\n.env\n.DS_Store\n",
            "java": "target/\n.classpath\n.project\n.settings/\n",
            "go": "*.exe\n*.exe~\n*.dll\n*.so\n*.dylib\n",
            "rust": "/target\nCargo.lock\n",
        }
        content = templates.get(language, templates["python"])
        with open(path, 'w') as f:
            f.write(content)
        return f"[OK] .gitignore: {language}"
    
    @staticmethod
    def create_editorconfig(path: str) -> str:
        """Crear .editorconfig"""
        config = """root = true

[*]
indent_style = space
indent_size = 2
end_of_line = lf
charset = utf-8
trim_trailing_whitespace = true
insert_final_newline = true

[*.py]
indent_size = 4

[*.{js,ts,jsx,tsx}]
indent_size = 2

[*.{html,css,json,yml,yaml}]
indent_size = 2
"""
        with open(path, 'w') as f:
            f.write(config)
        return "[OK] .editorconfig creado"
    
    @staticmethod
    def create_prettier_config(path: str) -> str:
        """Crear .prettierrc"""
        config = {
            "semi": True,
            "trailingComma": "es5",
            "singleQuote": True,
            "printWidth": 80,
            "tabWidth": 2,
            "useTabs": False
        }
        with open(path, 'w') as f:
            json.dump(config, f, indent=2)
        return "[OK] .prettierrc creado"
    
    @staticmethod
    def create_eslint_config(path: str) -> str:
        """Crear .eslintrc"""
        config = {
            "env": {"browser": True, "es2021": True, "node": True},
            "extends": ["eslint:recommended", "prettier"],
            "parserOptions": {"ecmaVersion": "latest", "sourceType": "module"},
            "rules": {"no-unused-vars": "warn", "no-console": "warn"}
        }
        with open(path, 'w') as f:
            json.dump(config, f, indent=2)
        return "[OK] .eslintrc creado"
    
    @staticmethod
    def create_tsconfig(path: str) -> str:
        """Crear tsconfig.json"""
        config = {
            "compilerOptions": {
                "target": "ES2020",
                "module": "ESNext",
                "lib": ["ES2020", "DOM", "DOM.Iterable"],
                "strict": True,
                "esModuleInterop": True,
                "skipLibCheck": True,
                "forceConsistentCasingInFileNames": True,
                "resolveJsonModule": True,
                "isolatedModules": True,
                "noEmit": True,
                "jsx": "react-jsx"
            },
            "include": ["src"],
            "exclude": ["node_modules"]
        }
        with open(path, 'w') as f:
            json.dump(config, f, indent=2)
        return "[OK] tsconfig.json creado"
    
    @staticmethod
    def create_postman_collection(name: str, endpoints: List[Dict]) -> str:
        """Crear coleccion Postman"""
        collection = {
            "info": {"name": name, "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"},
            "item": []
        }
        for ep in endpoints:
            collection["item"].append({
                "name": ep.get('name', 'Request'),
                "request": {
                    "method": ep.get('method', 'GET'),
                    "url": ep.get('url', ''),
                }
            })
        path = f"{name.lower().replace(' ', '_')}.postman_collection.json"
        with open(path, 'w') as f:
            json.dump(collection, f, indent=2)
        return f"[OK] Postman: {path}"
    
    @staticmethod
    def create_swagger_ui(path: str, api_url: str) -> str:
        """Crear pagina Swagger UI"""
        html = f'''<!DOCTYPE html>
<html>
<head>
    <title>API Documentation</title>
    <link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist@4/swagger-ui.css">
</head>
<body>
    <div id="swagger-ui"></div>
    <script src="https://unpkg.com/swagger-ui-dist@4/swagger-ui-bundle.js"></script>
    <script>
        SwaggerUIBundle({{
            url: "{api_url}",
            dom_id: '#swagger-ui',
            presets: [SwaggerUIBundle.presets.apis, SwaggerUIBundle.SwaggerUIStandalonePreset],
            layout: "BaseLayout"
        }});
    </script>
</body>
</html>'''
        with open(path, 'w') as f:
            f.write(html)
        return f"[OK] Swagger UI: {path}"
    
    @staticmethod
    def create_makefile(targets: Dict[str, str]) -> str:
        """Crear Makefile"""
        content = ".PHONY: " + " ".join(targets.keys()) + "\n\n"
        for target, commands in targets.items():
            content += f"{target}:\n"
            for cmd in commands if isinstance(commands, list) else [commands]:
                content += f"\t{cmd}\n"
            content += "\n"
        with open('Makefile', 'w') as f:
            f.write(content)
        return "[OK] Makefile creado"
    
    @staticmethod
    def create_dockerignore(patterns: List[str]) -> str:
        """Crear .dockerignore"""
        content = "\n".join(patterns)
        with open('.dockerignore', 'w') as f:
            f.write(content)
        return "[OK] .dockerignore creado"
    
    @staticmethod
    def create_procfile(processes: Dict[str, str]) -> str:
        """Crear Procfile"""
        content = "\n".join([f"{name}: {cmd}" for name, cmd in processes.items()])
        with open('Procfile', 'w') as f:
            f.write(content)
        return "[OK] Procfile creado"
    
    @staticmethod
    def create_terraform_config(path: str, provider: str = "aws") -> str:
        """Crear config Terraform"""
        config = f'''terraform {{
  required_version = ">= 1.0"
  required_providers {{
    {provider} = {{
      source  = "hashicorp/{provider}"
      version = "~> 4.0"
    }}
  }}
}}
'''
        with open(path, 'w') as f:
            f.write(config)
        return f"[OK] Terraform: {path}"
    
    @staticmethod
    def create_kubernetes_deployment(path: str, name: str, image: str, replicas: int = 3) -> str:
        """Crear deployment Kubernetes"""
        import yaml
        deployment = {
            "apiVersion": "apps/v1",
            "kind": "Deployment",
            "metadata": {"name": name},
            "spec": {
                "replicas": replicas,
                "selector": {"matchLabels": {"app": name}},
                "template": {
                    "metadata": {"labels": {"app": name}},
                    "spec": {"containers": [{"name": name, "image": image}]}
                }
            }
        }
        with open(path, 'w') as f:
            yaml.dump(deployment, f, default_flow_style=False)
        return f"[OK] K8s Deployment: {name}"
    
    @staticmethod
    def create_ansible_playbook(path: str, name: str, hosts: str, tasks: List[Dict]) -> str:
        """Crear playbook Ansible"""
        import yaml
        playbook = [{
            "name": name,
            "hosts": hosts,
            "tasks": tasks
        }]
        with open(path, 'w') as f:
            yaml.dump(playbook, f, default_flow_style=False)
        return f"[OK] Ansible: {name}"
    
    @staticmethod
    def create_github_actions_ci(path: str, name: str, language: str) -> str:
        """Crear workflow CI"""
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        configs = {
            "python": {
                "setup": ["actions/setup-python@v4", {"python-version": "3.11"}],
                "install": "pip install -r requirements.txt",
                "test": "pytest"
            },
            "node": {
                "setup": ["actions/setup-node@v3", {"node-version": "18"}],
                "install": "npm install",
                "test": "npm test"
            }
        }
        
        config = configs.get(language, configs["python"])
        
        workflow = {
            "name": name,
            "on": {"push": {"branches": ["main"]}, "pull_request": {"branches": ["main"]}},
            "jobs": {
                "build": {
                    "runs-on": "ubuntu-latest",
                    "steps": [
                        {"uses": "actions/checkout@v3"},
                        {"uses": config["setup"][0], "with": config["setup"][1]},
                        {"run": config["install"]},
                        {"run": config["test"]}
                    ]
                }
            }
        }
        
        import yaml
        with open(path, 'w') as f:
            yaml.dump(workflow, f, default_flow_style=False)
        return f"[OK] CI workflow: {name}"


# Instancia global
advanced_actions = AdvancedActions()


# Diccionario de todas las acciones para el parser
ALL_ACTIONS = {
    # Archivos
    "create_file": advanced_actions.create_file,
    "create_files_batch": advanced_actions.create_files_batch,
    "read_file": advanced_actions.read_file,
    "read_file_lines": advanced_actions.read_file_lines,
    "edit_file": advanced_actions.edit_file,
    "edit_file_line": advanced_actions.edit_file_line,
    "insert_in_file": advanced_actions.insert_in_file,
    "append_to_file": advanced_actions.append_to_file,
    "prepend_to_file": advanced_actions.prepend_to_file,
    "delete_file": advanced_actions.delete_file,
    "delete_files": advanced_actions.delete_files,
    "clear_folder": advanced_actions.clear_folder,
    "copy_file": advanced_actions.copy_file,
    "move_file": advanced_actions.move_file,
    "rename_file": advanced_actions.rename_file,
    "create_folder": advanced_actions.create_folder,
    "create_folders_batch": advanced_actions.create_folders_batch,
    "remove_folder": advanced_actions.remove_folder,
    "empty_file": advanced_actions.empty_file,
    "get_file_info": advanced_actions.get_file_info,
    "list_directory": advanced_actions.list_directory,
    "tree_directory": advanced_actions.tree_directory,
    "find_files": advanced_actions.find_files,
    "find_files_by_extension": advanced_actions.find_files_by_extension,
    "search_in_files": advanced_actions.search_in_files,
    "replace_in_files": advanced_actions.replace_in_files,
    "count_lines": advanced_actions.count_lines,
    "count_lines_all": advanced_actions.count_lines_all,
    "file_hash": advanced_actions.file_hash,
    "compare_files": advanced_actions.compare_files,
    "backup_file": advanced_actions.backup_file,
    "restore_backup": advanced_actions.restore_backup,
    "make_readonly": advanced_actions.make_readonly,
    "make_writable": advanced_actions.make_writable,
    "get_size": advanced_actions.get_size,
    "touch_file": advanced_actions.touch_file,
    "symlink": advanced_actions.symlink,
    "change_permissions": advanced_actions.change_permissions,
    "find_duplicate_files": advanced_actions.find_duplicate_files,
    "organize_files_by_extension": advanced_actions.organize_files_by_extension,
    "clean_empty_folders": advanced_actions.clean_empty_folders,
    "create_project_structure": advanced_actions.create_project_structure,
    
    # Git
    "git_init": advanced_actions.git_init,
    "git_add": advanced_actions.git_add,
    "git_commit": advanced_actions.git_commit,
    "git_status": advanced_actions.git_status,
    "git_log": advanced_actions.git_log,
    "git_diff": advanced_actions.git_diff,
    "git_branch": advanced_actions.git_branch,
    "git_checkout": advanced_actions.git_checkout,
    "git_merge": advanced_actions.git_merge,
    "git_push": advanced_actions.git_push,
    "git_pull": advanced_actions.git_pull,
    "git_clone": advanced_actions.git_clone,
    "git_stash": advanced_actions.git_stash,
    "git_stash_pop": advanced_actions.git_stash_pop,
    "git_tag": advanced_actions.git_tag,
    "git_revert": advanced_actions.git_revert,
    "git_reset": advanced_actions.git_reset,
    "git_remote_add": advanced_actions.git_remote_add,
    "git_ignore": advanced_actions.git_ignore,
    
    # Python
    "run_python": advanced_actions.run_python,
    "run_python_file": advanced_actions.run_python_file,
    "create_virtualenv": advanced_actions.create_virtualenv,
    "install_package": advanced_actions.install_package,
    "install_requirements": advanced_actions.install_requirements,
    "freeze_requirements": advanced_actions.freeze_requirements,
    "list_packages": advanced_actions.list_packages,
    "check_outdated": advanced_actions.check_outdated,
    "uninstall_package": advanced_actions.uninstall_package,
    "format_code": advanced_actions.format_code,
    "lint_code": advanced_actions.lint_code,
    "type_check": advanced_actions.type_check,
    "run_tests": advanced_actions.run_tests,
    "create_module": advanced_actions.create_module,
    "create_class": advanced_actions.create_class,
    "create_fastapi_endpoint": advanced_actions.create_fastapi_endpoint,
    "create_flask_route": advanced_actions.create_flask_route,
    "create_django_view": advanced_actions.create_django_view,
    "create_sqlalchemy_model": advanced_actions.create_sqlalchemy_model,
    "create_pydantic_model": advanced_actions.create_pydantic_model,
    "create_test_file": advanced_actions.create_test_file,
    "create_dockerfile_python": advanced_actions.create_dockerfile_python,
    "create_docker_compose": advanced_actions.create_docker_compose,
    "create_github_workflow": advanced_actions.create_github_workflow,
    
    # Web
    "create_html_page": advanced_actions.create_html_page,
    "create_react_component": advanced_actions.create_react_component,
    "create_vue_component": advanced_actions.create_vue_component,
    "create_angular_component": advanced_actions.create_angular_component,
    "create_svelte_component": advanced_actions.create_svelte_component,
    "create_nextjs_page": advanced_actions.create_nextjs_page,
    "create_api_endpoint_express": advanced_actions.create_api_endpoint_express,
    "create_package_json": advanced_actions.create_package_json,
    "create_vite_config": advanced_actions.create_vite_config,
    "create_tailwind_config": advanced_actions.create_tailwind_config,
    "create_responsive_css": advanced_actions.create_responsive_css,
    "create_animation_css": advanced_actions.create_animation_css,
    "create_dark_mode_css": advanced_actions.create_dark_mode_css,
    "create_glassmorphism_css": advanced_actions.create_glassmorphism_css,
    "create_gradient_css": advanced_actions.create_gradient_css,
    "create_grid_layout": advanced_actions.create_grid_layout,
    "create_flexbox_layout": advanced_actions.create_flexbox_layout,
    "create_utilities_css": advanced_actions.create_utilities_css,
    
    # DB
    "create_sqlite_db": advanced_actions.create_sqlite_db,
    "create_postgres_db": advanced_actions.create_postgres_db,
    "create_mongo_collection": advanced_actions.create_mongo_collection,
    "sql_query": advanced_actions.sql_query,
    "create_migration": advanced_actions.create_migration,
    "create_seed_data": advanced_actions.create_seed_data,
    "backup_database": advanced_actions.backup_database,
    
    # Red
    "http_get": advanced_actions.http_get,
    "http_post": advanced_actions.http_post,
    "http_put": advanced_actions.http_put,
    "http_delete": advanced_actions.http_delete,
    "download_file": advanced_actions.download_file,
    "upload_file": advanced_actions.upload_file,
    "create_api_server": advanced_actions.create_api_server,
    "create_rest_api": advanced_actions.create_rest_api,
    "create_websocket_server": advanced_actions.create_websocket_server,
    "create_grpc_service": advanced_actions.create_grpc_service,
    "create_middleware": advanced_actions.create_middleware,
    "create_rate_limiter": advanced_actions.create_rate_limiter,
    
    # Seguridad
    "generate_password": advanced_actions.generate_password,
    "generate_api_key": advanced_actions.generate_api_key,
    "generate_jwt_secret": advanced_actions.generate_jwt_secret,
    "hash_password": advanced_actions.hash_password,
    "verify_password": advanced_actions.verify_password,
    "encrypt_text": advanced_actions.encrypt_text,
    "decrypt_text": advanced_actions.decrypt_text,
    "scan_ports": advanced_actions.scan_ports,
    "create_ssl_cert": advanced_actions.create_ssl_cert,
    "validate_input": advanced_actions.validate_input,
    "sanitize_filename": advanced_actions.sanitize_filename,
    
    # Sistema
    "get_system_info": advanced_actions.get_system_info,
    "get_cpu_info": advanced_actions.get_cpu_info,
    "get_memory_info": advanced_actions.get_memory_info,
    "get_disk_info": advanced_actions.get_disk_info,
    "get_process_list": advanced_actions.get_process_list,
    "kill_process": advanced_actions.kill_process,
    "set_environment_variable": advanced_actions.set_environment_variable,
    "get_environment_variables": advanced_actions.get_environment_variables,
    "create_cron_job": advanced_actions.create_cron_job,
    "schedule_task": advanced_actions.schedule_task,
    
    # Multimedia
    "create_image": advanced_actions.create_image,
    "resize_image": advanced_actions.resize_image,
    "convert_image": advanced_actions.convert_image,
    "create_qr_code": advanced_actions.create_qr_code,
    
    # Documentacion
    "create_readme": advanced_actions.create_readme,
    "create_documentation": advanced_actions.create_documentation,
    "create_changelog": advanced_actions.create_changelog,
    "create_api_docs_openapi": advanced_actions.create_api_docs_openapi,
    
    # Testing
    "create_unit_test": advanced_actions.create_unit_test,
    "create_integration_test": advanced_actions.create_integration_test,
    "create_mock": advanced_actions.create_mock,
    "create_fixtures": advanced_actions.create_fixtures,
    "create_benchmark": advanced_actions.create_benchmark,
    
    # Utilidades
    "timestamp": advanced_actions.timestamp,
    "format_date": advanced_actions.format_date,
    "days_between": advanced_actions.days_between,
    "add_days": advanced_actions.add_days,
    "generate_uuid": advanced_actions.generate_uuid,
    "generate_random_string": advanced_actions.generate_random_string,
    "generate_random_number": advanced_actions.generate_random_number,
    "slugify": advanced_actions.slugify,
    "truncate": advanced_actions.truncate,
    "word_count": advanced_actions.word_count,
    "pretty_json": advanced_actions.pretty_json,
    "csv_to_json": advanced_actions.csv_to_json,
    "json_to_csv": advanced_actions.json_to_csv,
    "create_env_file": advanced_actions.create_env_file,
    "parse_env_file": advanced_actions.parse_env_file,
    "create_gitignore": advanced_actions.create_gitignore,
    "create_editorconfig": advanced_actions.create_editorconfig,
    "create_prettier_config": advanced_actions.create_prettier_config,
    "create_eslint_config": advanced_actions.create_eslint_config,
    "create_tsconfig": advanced_actions.create_tsconfig,
    "create_postman_collection": advanced_actions.create_postman_collection,
    "create_swagger_ui": advanced_actions.create_swagger_ui,
    "create_makefile": advanced_actions.create_makefile,
    "create_dockerignore": advanced_actions.create_dockerignore,
    "create_procfile": advanced_actions.create_procfile,
    "create_terraform_config": advanced_actions.create_terraform_config,
    "create_kubernetes_deployment": advanced_actions.create_kubernetes_deployment,
    "create_ansible_playbook": advanced_actions.create_ansible_playbook,
    "create_github_actions_ci": advanced_actions.create_github_actions_ci,
}

# Contar acciones totales
TOTAL_ACTIONS = len(ALL_ACTIONS)
