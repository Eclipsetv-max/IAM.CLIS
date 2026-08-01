# -*- coding: utf-8 -*-
"""
IAM Packages - Gestion de paquetes
pip, npm, yarn, conda, etc.
"""

import subprocess
import os
from typing import Tuple, List, Dict


class PackageManager:
    """
    Gestion de paquetes de multiples gestores
    """
    
    def __init__(self):
        self.managers = {
            'pip': self._run_pip,
            'npm': self._run_npm,
            'yarn': self._run_yarn,
            'conda': self._run_conda,
            'winget': self._run_winget,
            'choco': self._run_choco
        }
    
    def _run_command(self, cmd: List[str], timeout: int = 120) -> Tuple[bool, str]:
        """Ejecutar comando"""
        try:
            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=timeout,
                encoding='utf-8', errors='replace'
            )
            return True, result.stdout if result.stdout else result.stderr
        except Exception as e:
            return False, str(e)
    
    # === PIP ===
    
    def _run_pip(self, args: List[str]) -> Tuple[bool, str]:
        """Ejecutar pip"""
        return self._run_command(['pip'] + args)
    
    def pip_list(self) -> Tuple[bool, List[str]]:
        """Listar paquetes pip"""
        success, output = self._run_pip(['list', '--format=columns'])
        if success:
            packages = []
            for line in output.strip().split('\n')[2:]:  # Skip header
                parts = line.split()
                if parts:
                    packages.append(f"{parts[0]}=={parts[1]}" if len(parts) > 1 else parts[0])
            return True, packages
        return False, []
    
    def pip_install(self, package: str, version: str = None) -> Tuple[bool, str]:
        """Instalar paquete"""
        pkg = f"{package}=={version}" if version else package
        return self._run_pip(['install', pkg])
    
    def pip_uninstall(self, package: str) -> Tuple[bool, str]:
        """Desinstalar paquete"""
        return self._run_pip(['uninstall', '-y', package])
    
    def pip_upgrade(self, package: str = None) -> Tuple[bool, str]:
        """Actualizar paquete(s)"""
        if package:
            return self._run_pip(['install', '--upgrade', package])
        return self._run_pip(['install', '--upgrade', 'pip'])
    
    def pip_search(self, query: str) -> Tuple[bool, str]:
        """Buscar paquete"""
        return self._run_pip(['search', query])
    
    def pip_show(self, package: str) -> Tuple[bool, str]:
        """Info de paquete"""
        return self._run_pip(['show', package])
    
    def pip_freeze(self) -> Tuple[bool, str]:
        """Lista de requirements"""
        return self._run_pip(['freeze'])
    
    def pip_install_requirements(self, file: str = "requirements.txt") -> Tuple[bool, str]:
        """Instalar desde requirements.txt"""
        return self._run_pip(['install', '-r', file])
    
    def pip_create_requirements(self, output: str = "requirements.txt") -> Tuple[bool, str]:
        """Crear requirements.txt"""
        success, output_freeze = self.pip_freeze()
        if success:
            with open(output, 'w') as f:
                f.write(output_freeze)
            return True, f"[OK] Requirements creado: {output}"
        return False, output_freeze
    
    # === NPM ===
    
    def _run_npm(self, args: List[str]) -> Tuple[bool, str]:
        """Ejecutar npm"""
        return self._run_command(['npm'] + args)
    
    def npm_list(self, global_list: bool = False) -> Tuple[bool, List[str]]:
        """Listar paquetes npm"""
        args = ['list', '--depth=0']
        if global_list:
            args.append('-g')
        success, output = self._run_npm(args)
        return success, output.split('\n') if success else []
    
    def npm_install(self, package: str, global_install: bool = False) -> Tuple[bool, str]:
        """Instalar paquete npm"""
        args = ['install']
        if global_install:
            args.append('-g')
        args.append(package)
        return self._run_npm(args)
    
    def npm_uninstall(self, package: str, global_uninstall: bool = False) -> Tuple[bool, str]:
        """Desinstalar paquete npm"""
        args = ['uninstall']
        if global_uninstall:
            args.append('-g')
        args.append(package)
        return self._run_npm(args)
    
    def npm_update(self) -> Tuple[bool, str]:
        """Actualizar paquetes"""
        return self._run_npm(['update'])
    
    def npm_init(self, path: str = ".") -> Tuple[bool, str]:
        """Inicializar proyecto npm"""
        return self._run_npm(['init', '-y'], )
    
    def npm_start(self, path: str = ".") -> Tuple[bool, str]:
        """Iniciar proyecto npm"""
        return self._run_npm(['start'])
    
    def npm_run(self, script: str) -> Tuple[bool, str]:
        """Ejecutar script npm"""
        return self._run_npm(['run', script])
    
    # === YARN ===
    
    def _run_yarn(self, args: List[str]) -> Tuple[bool, str]:
        """Ejecutar yarn"""
        return self._run_command(['yarn'] + args)
    
    def yarn_list(self) -> Tuple[bool, str]:
        """Listar paquetes yarn"""
        return self._run_yarn(['list', '--depth=0'])
    
    def yarn_add(self, package: str) -> Tuple[bool, str]:
        """Agregar paquete"""
        return self._run_yarn(['add', package])
    
    def yarn_remove(self, package: str) -> Tuple[bool, str]:
        """Remover paquete"""
        return self._run_yarn(['remove', package])
    
    # === CONDA ===
    
    def _run_conda(self, args: List[str]) -> Tuple[bool, str]:
        """Ejecutar conda"""
        return self._run_command(['conda'] + args)
    
    def conda_list(self) -> Tuple[bool, List[str]]:
        """Listar paquetes conda"""
        success, output = self._run_conda(['list'])
        return success, output.split('\n') if success else []
    
    def conda_install(self, package: str, channel: str = None) -> Tuple[bool, str]:
        """Instalar paquete conda"""
        args = ['install', '-y']
        if channel:
            args.extend(['-c', channel])
        args.append(package)
        return self._run_conda(args)
    
    def conda_update(self, package: str = None) -> Tuple[bool, str]:
        """Actualizar conda"""
        if package:
            return self._run_conda(['update', package])
        return self._run_conda(['update', 'conda'])
    
    def conda_create(self, name: str, python_version: str = "3.11") -> Tuple[bool, str]:
        """Crear ambiente conda"""
        return self._run_conda(['create', '-n', name, f'python={python_version}', '-y'])
    
    def conda_activate(self, name: str) -> Tuple[bool, str]:
        """Instrucciones para activar"""
        return True, f"[INFO] Ejecuta: conda activate {name}"
    
    # === WINGET ===
    
    def _run_winget(self, args: List[str]) -> Tuple[bool, str]:
        """Ejecutar winget"""
        return self._run_command(['winget'] + args)
    
    def winget_list(self) -> Tuple[bool, List[str]]:
        """Listar paquetes winget"""
        success, output = self._run_winget(['list'])
        return success, output.split('\n') if success else []
    
    def winget_install(self, package: str) -> Tuple[bool, str]:
        """Instalar con winget"""
        return self._run_winget(['install', '--id', package, '--accept-package-agreements'])
    
    def winget_uninstall(self, package: str) -> Tuple[bool, str]:
        """Desinstalar con winget"""
        return self._run_winget(['uninstall', '--id', package])
    
    def winget_upgrade(self, package: str = None) -> Tuple[bool, str]:
        """Actualizar con winget"""
        if package:
            return self._run_winget(['upgrade', '--id', package])
        return self._run_winget(['upgrade', '--all'])
    
    def winget_search(self, query: str) -> Tuple[bool, str]:
        """Buscar con winget"""
        return self._run_winget(['search', query])
    
    # === CHOCOLATEY ===
    
    def _run_choco(self, args: List[str]) -> Tuple[bool, str]:
        """Ejecutar choco"""
        return self._run_command(['choco'] + args)
    
    def choco_list(self) -> Tuple[bool, List[str]]:
        """Listar paquetes choco"""
        success, output = self._run_choco(['list', '--local-only'])
        return success, output.split('\n') if success else []
    
    def choco_install(self, package: str) -> Tuple[bool, str]:
        """Instalar con choco"""
        return self._run_choco(['install', package, '-y'])
    
    def choco_uninstall(self, package: str) -> Tuple[bool, str]:
        """Desinstalar con choco"""
        return self._run_choco(['uninstall', package, '-y'])
    
    def choco_upgrade(self, package: str = None) -> Tuple[bool, str]:
        """Actualizar con choco"""
        if package:
            return self._run_choco(['upgrade', package, '-y'])
        return self._run_choco(['upgrade', 'all', '-y'])
    
    # === DETECCION AUTOMATICA ===
    
    def detect_project_type(self, path: str = ".") -> str:
        """Detectar tipo de proyecto"""
        files = os.listdir(path)
        
        if 'package.json' in files:
            return 'npm'
        elif 'requirements.txt' in files or 'setup.py' in files or 'pyproject.toml' in files:
            return 'pip'
        elif 'environment.yml' in files:
            return 'conda'
        elif 'Gemfile' in files:
            return 'bundle'
        elif 'go.mod' in files:
            return 'go'
        elif 'Cargo.toml' in files:
            return 'cargo'
        elif 'pom.xml' in files:
            return 'maven'
        
        return 'unknown'
    
    def auto_install(self, path: str = ".") -> Tuple[bool, str]:
        """Instalar dependencias automaticamente"""
        project_type = self.detect_project_type(path)
        
        if project_type == 'npm':
            return self._run_npm(['install'])
        elif project_type == 'pip':
            return self._run_pip(['install', '-r', 'requirements.txt'])
        elif project_type == 'conda':
            return self._run_conda(['env', 'update', '-f', 'environment.yml'])
        
        return False, f"[ERROR] Tipo de proyecto no soportado: {project_type}"


# Instancia global
packages = PackageManager()
