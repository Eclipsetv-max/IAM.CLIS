# -*- coding: utf-8 -*-
"""
IAM Git - Control de versiones completo
Inicializar, commitear, push, pull, branches, etc.
"""

import subprocess
import os
from typing import Tuple, List, Dict


class Git:
    """
    Control de versiones Git completo
    """
    
    def __init__(self):
        self.git_path = "git"
    
    def _run_git(self, args: List[str], cwd: str = None, timeout: int = 60) -> Tuple[bool, str]:
        """Ejecutar comando git"""
        try:
            result = subprocess.run(
                [self.git_path] + args,
                capture_output=True, text=True, timeout=timeout,
                cwd=cwd, encoding='utf-8', errors='replace'
            )
            output = result.stdout
            if result.stderr:
                output += f"\n{result.stderr}"
            return result.returncode == 0, output.strip() if output else "OK"
        except FileNotFoundError:
            return False, "[ERROR] Git no instalado"
        except Exception as e:
            return False, f"[ERROR] {e}"
    
    # === INICIALIZAR ===
    
    def init(self, path: str = ".") -> Tuple[bool, str]:
        """Inicializar repositorio"""
        return self._run_git(["init"], cwd=path)
    
    def clone(self, url: str, destination: str = None) -> Tuple[bool, str]:
        """Clonar repositorio"""
        args = ["clone", url]
        if destination:
            args.append(destination)
        return self._run_git(args)
    
    # === ESTADO ===
    
    def status(self, path: str = ".") -> Tuple[bool, str]:
        """Ver estado"""
        return self._run_git(["status"], cwd=path)
    
    def status_short(self, path: str = ".") -> Tuple[bool, str]:
        """Estado corto"""
        return self._run_git(["status", "-s"], cwd=path)
    
    def log(self, count: int = 10, path: str = ".") -> Tuple[bool, str]:
        """Ver historial"""
        return self._run_git(["log", f"-{count}", "--oneline"], cwd=path)
    
    def log_detailed(self, count: int = 5, path: str = ".") -> Tuple[bool, str]:
        """Historial detallado"""
        return self._run_git(["log", f"-{count}", "--pretty=format:%h %an %ad %s"], cwd=path)
    
    # === STAGING ===
    
    def add(self, files: List[str] = None, path: str = ".") -> Tuple[bool, str]:
        """Agregar archivos"""
        if files:
            return self._run_git(["add"] + files, cwd=path)
        return self._run_git(["add", "."], cwd=path)
    
    def add_all(self, path: str = ".") -> Tuple[bool, str]:
        """Agregar todo"""
        return self._run_git(["add", "-A"], cwd=path)
    
    def unstage(self, file: str, path: str = ".") -> Tuple[bool, str]:
        """Remover del staging"""
        return self._run_git(["reset", "HEAD", file], cwd=path)
    
    # === COMMITEAR ===
    
    def commit(self, message: str, path: str = ".") -> Tuple[bool, str]:
        """Commitear cambios"""
        return self._run_git(["commit", "-m", message], cwd=path)
    
    def commit_all(self, message: str, path: str = ".") -> Tuple[bool, str]:
        """Agregar todo y commitear"""
        self.add_all(path)
        return self.commit(message, path)
    
    # === RAMAS ===
    
    def branches(self, path: str = ".") -> Tuple[bool, str]:
        """Listar ramas"""
        return self._run_git(["branch", "-a"], cwd=path)
    
    def create_branch(self, name: str, path: str = ".") -> Tuple[bool, str]:
        """Crear rama"""
        return self._run_git(["branch", name], cwd=path)
    
    def switch_branch(self, name: str, path: str = ".") -> Tuple[bool, str]:
        """Cambiar de rama"""
        return self._run_git(["checkout", name], cwd=path)
    
    def create_and_switch(self, name: str, path: str = ".") -> Tuple[bool, str]:
        """Crear y cambiar a rama"""
        return self._run_git(["checkout", "-b", name], cwd=path)
    
    def delete_branch(self, name: str, path: str = ".") -> Tuple[bool, str]:
        """Eliminar rama"""
        return self._run_git(["branch", "-d", name], cwd=path)
    
    def merge(self, branch: str, path: str = ".") -> Tuple[bool, str]:
        """Fusionar rama"""
        return self._run_git(["merge", branch], cwd=path)
    
    # === REMOTO ===
    
    def remotes(self, path: str = ".") -> Tuple[bool, str]:
        """Ver remotos"""
        return self._run_git(["remote", "-v"], cwd=path)
    
    def add_remote(self, name: str, url: str, path: str = ".") -> Tuple[bool, str]:
        """Agregar remoto"""
        return self._run_git(["remote", "add", name, url], cwd=path)
    
    def push(self, remote: str = "origin", branch: str = None, path: str = ".") -> Tuple[bool, str]:
        """Push al remoto"""
        args = ["push", remote]
        if branch:
            args.append(branch)
        return self._run_git(args, cwd=path)
    
    def push_force(self, remote: str = "origin", branch: str = None, path: str = ".") -> Tuple[bool, str]:
        """Push forzado"""
        args = ["push", "--force", remote]
        if branch:
            args.append(branch)
        return self._run_git(args, cwd=path)
    
    def pull(self, remote: str = "origin", branch: str = None, path: str = ".") -> Tuple[bool, str]:
        """Pull del remoto"""
        args = ["pull", remote]
        if branch:
            args.append(branch)
        return self._run_git(args, cwd=path)
    
    def fetch(self, remote: str = "origin", path: str = ".") -> Tuple[bool, str]:
        """Fetch del remoto"""
        return self._run_git(["fetch", remote], cwd=path)
    
    # === DIFF ===
    
    def diff(self, path: str = ".") -> Tuple[bool, str]:
        """Ver diferencias"""
        return self._run_git(["diff"], cwd=path)
    
    def diff_staged(self, path: str = ".") -> Tuple[bool, str]:
        """Diferencias en staging"""
        return self._run_git(["diff", "--staged"], cwd=path)
    
    def diff_branch(self, branch1: str, branch2: str, path: str = ".") -> Tuple[bool, str]:
        """Diferencias entre ramas"""
        return self._run_git(["diff", branch1, branch2], cwd=path)
    
    # === STASH ===
    
    def stash(self, message: str = None, path: str = ".") -> Tuple[bool, str]:
        """Guardar stash"""
        args = ["stash"]
        if message:
            args.extend(["push", "-m", message])
        return self._run_git(args, cwd=path)
    
    def stash_pop(self, path: str = ".") -> Tuple[bool, str]:
        """Aplicar stash"""
        return self._run_git(["stash", "pop"], cwd=path)
    
    def stash_list(self, path: str = ".") -> Tuple[bool, str]:
        """Listar stashes"""
        return self._run_git(["stash", "list"], cwd=path)
    
    def stash_drop(self, stash_id: str = "stash@{0}", path: str = ".") -> Tuple[bool, str]:
        """Eliminar stash"""
        return self._run_git(["stash", "drop", stash_id], cwd=path)
    
    # === TAGS ===
    
    def tags(self, path: str = ".") -> Tuple[bool, str]:
        """Listar tags"""
        return self._run_git(["tag"], cwd=path)
    
    def create_tag(self, name: str, message: str = None, path: str = ".") -> Tuple[bool, str]:
        """Crear tag"""
        if message:
            return self._run_git(["tag", "-a", name, "-m", message], cwd=path)
        return self._run_git(["tag", name], cwd=path)
    
    def delete_tag(self, name: str, path: str = ".") -> Tuple[bool, str]:
        """Eliminar tag"""
        return self._run_git(["tag", "-d", name], cwd=path)
    
    # === BLAME ===
    
    def blame(self, file: str, path: str = ".") -> Tuple[bool, str]:
        """Ver autor de lineas"""
        return self._run_git(["blame", file], cwd=path)
    
    # === ARCHIVOS ===
    
    def show_file(self, file: str, commit: str = "HEAD", path: str = ".") -> Tuple[bool, str]:
        """Mostrar archivo en commit"""
        return self._run_git(["show", f"{commit}:{file}"], cwd=path)
    
    def ls_files(self, path: str = ".") -> Tuple[bool, str]:
        """Listar archivos tracked"""
        return self._run_git(["ls-files"], cwd=path)
    
    def clean(self, path: str = ".") -> Tuple[bool, str]:
        """Limpiar archivos untracked"""
        return self._run_git(["clean", "-fd"], cwd=path)
    
    # === UTILIDADES ===
    
    def is_repo(self, path: str = ".") -> bool:
        """Verificar si es repositorio"""
        success, _ = self._run_git(["rev-parse", "--git-dir"], cwd=path)
        return success
    
    def get_current_branch(self, path: str = ".") -> Tuple[bool, str]:
        """Obtener rama actual"""
        return self._run_git(["branch", "--show-current"], cwd=path)
    
    def get_remote_url(self, remote: str = "origin", path: str = ".") -> Tuple[bool, str]:
        """Obtener URL del remoto"""
        return self._run_git(["remote", "get-url", remote], cwd=path)


# Instancia global
git = Git()
