# -*- coding: utf-8 -*-
"""
IAM v4.1 - Asistente de IA
Punto de entrada principal

Uso: python main.py [--theme claude|cyberpunk|dracula|nord|monokai]
"""

import os
import sys
import io
import time
import argparse

os.environ['PYTHONIOENCODING'] = 'utf-8'
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from iam.config.settings import settings, COLORS
from iam.config.prompts import AGENT_PROMPTS
from iam.core.agent import AgentRouter
from iam.core.memory import MemorySystem
from iam.core.loading import LoadingIndicator
from iam.core.enhanced_cli import EnhancedCLI


def parse_args():
    parser = argparse.ArgumentParser(description="IAM - Claude Code-like Experience")
    parser.add_argument("--theme", default="claude",
                        choices=["claude", "cyberpunk", "dracula", "nord", "monokai", "default"],
                        help="Tema de color")
    parser.add_argument("--compact", action="store_true", help="Modo compacto")
    parser.add_argument("--think", action="store_true", help="Modo pensamiento")
    return parser.parse_args()


def handle_special_commands(cli: EnhancedCLI, user_input: str, router: AgentRouter, memory: MemorySystem) -> bool:
    """Maneja comandos especiales de la CLI. Retorna True si fue procesado."""
    cmd = user_input.lower().strip()

    if cmd in ["exit", "quit", "salir"]:
        print(f"\n  [dim]Bye![/dim]\n")
        return "exit"

    if cmd == "help":
        cli.print_help_table()
        return True

    if cmd == "clear":
        os.system('cls' if os.name == 'nt' else 'clear')
        cli.print_banner()
        return True

    if cmd == "palette":
        cli.print_sessions()
        return True

    if cmd.startswith("/theme"):
        parts = user_input.split()
        if len(parts) > 1:
            if cli.set_theme(parts[1]):
                cli.print_success(f"Tema: {parts[1]}")
            else:
                cli.print_error(f"Tema no encontrado: {parts[1]}")
                cli.print_themes()
        else:
            cli.print_themes()
        return True

    if cmd == "/alias":
        cli.print_aliases()
        return True

    if cmd.startswith("/alias-add"):
        parts = user_input.split(maxsplit=2)
        if len(parts) >= 3:
            cli.aliases.add(parts[1], parts[2])
            cli.print_success(f"Alias '{parts[1]}' -> '{parts[2]}'")
        else:
            cli.print_warning("Uso: /alias-add <nombre> <comando>")
        return True

    if cmd.startswith("/alias-rm"):
        parts = user_input.split()
        if len(parts) >= 2:
            if cli.aliases.remove(parts[1]):
                cli.print_success(f"Alias '{parts[1]}' eliminado")
            else:
                cli.print_error(f"Alias no encontrado o built-in")
        return True

    if cmd == "/stats":
        cli.print_stats()
        return True

    if cmd == "/think":
        mode = cli.toggle_think()
        cli.print_success(f"Modo pensamiento: {'ON' if mode else 'OFF'}")
        return True

    if cmd == "/sessions":
        cli.print_sessions()
        return True

    if cmd == "/save":
        if cli._last_response:
            filepath = cli.save_response(cli._last_query, cli._last_response,
                                          router.agent.current_mode)
            cli.print_success(f"Guardado: {filepath}")
        else:
            cli.print_warning("No hay respuesta reciente")
        return True

    if cmd == "/folder":
        try:
            import tkinter as tk
            from tkinter import filedialog
            root = tk.Tk()
            root.withdraw()
            root.attributes('-topmost', True)
            folder = filedialog.askdirectory(title="Seleccionar carpeta destino para vincular proyecto")
            root.destroy()

            if folder:
                project_path = os.getcwd()
                project_name = os.path.basename(project_path)
                link_path = os.path.join(folder, project_name)

                try:
                    if os.path.exists(link_path):
                        cli.print_warning(f"Ya existe un enlace o carpeta en: {link_path}")
                    else:
                        os.symlink(project_path, link_path)
                        cli.print_success(f"Vinculo creado: {link_path}")
                except OSError as e:
                    if "privilege" in str(e).lower() or "permission" in str(e).lower():
                        cli.print_error("Se necesitan permisos de administrador para crear enlaces simbolicos")
                    else:
                        cli.print_error(f"Error al crear vinculo: {e}")
            else:
                cli.print_info("Operacion cancelada")
        except ImportError:
            cli.print_error("tkinter no disponible. Usa: pip install tk")
        return True

    if cmd == "/history":
        from iam.core.file_history import file_history
        if router.agent.active_project:
            file_history.project_path = router.agent.active_project
        all_files = file_history.get_all_files()
        if all_files:
            print("\n  HISTORIAL DE ARCHIVOS:")
            print("  " + "=" * 40)
            for f in all_files[:20]:
                print(f"  {f['path']} - {f['versions']} versiones")
            print(f"\n  Total: {len(all_files)} archivos trackeados")
        else:
            print("  No hay historial de archivos todavia")
        return True

    if cmd.startswith("/rollback"):
        parts = user_input.split()
        if len(parts) >= 2:
            filepath = parts[1]
            version = parts[2] if len(parts) >= 3 else None
            from iam.core.file_history import file_history
            if router.agent.active_project:
                file_history.project_path = router.agent.active_project
            if version:
                success, msg = file_history.rollback(filepath, version)
            else:
                success, msg = file_history.rollback_last(filepath)
            if success:
                cli.print_success(msg)
            else:
                cli.print_error(msg)
        else:
            print("  Uso: /rollback <archivo> [version]")
        return True

    if cmd.startswith("/history-show"):
        parts = user_input.split()
        if len(parts) >= 2:
            filepath = parts[1]
            from iam.core.file_history import file_history
            if router.agent.active_project:
                file_history.project_path = router.agent.active_project
            print(file_history.format_history(filepath))
        else:
            print("  Uso: /history-show <archivo>")
        return True

    if cmd == "/cost":
        from iam.core.cost_tracking import cost_tracker
        session_id = router.agent.current_session.id if router.agent.current_session else None
        print(cost_tracker.format_cost_display(session_id))
        return True

    if cmd == "/compact":
        from iam.core.auto_compact import auto_compactor
        parts = user_input.split()
        if len(parts) > 1 and parts[1] == "stats":
            print(auto_compactor.format_stats())
        else:
            if router.agent.current_session:
                context = router.agent.current_session.get_context()
                from iam.core.cost_tracking import cost_tracker
                limit = cost_tracker.get_context_limit(
                    settings.MODELS.get(router.agent.current_mode, "mimo-v2.5-free")
                )
                result = auto_compactor.compact(context, limit)
                if result.success:
                    cli.print_success(f"Contexto compactado: {result.original_tokens} -> {result.compacted_tokens} tokens")
                    cli.print_info(f"Compresion: {result.compression_ratio:.1%}")
                else:
                    cli.print_warning("No se pudo compactar")
            else:
                print(auto_compactor.format_stats())
        return True

    if cmd == "/context":
        from iam.core.context_loader import context_loader
        if router.agent.active_project:
            context_loader.project_path = router.agent.active_project
            context_loader.load_project_context(force=True)
            print(context_loader.get_context_summary())
        else:
            print("  Selecciona un proyecto primero con /project")
        return True

    if cmd == "/security":
        from iam.core.permissions import permission_system
        print(permission_system.get_security_report())
        return True

    if cmd.startswith("/subagent"):
        parts = user_input.split(maxsplit=1)
        if len(parts) >= 2:
            from iam.core.sub_agent import sub_agent, SubAgentType
            task = sub_agent.create_task(
                SubAgentType.READER,
                "Tarea de lectura",
                parts[1],
                allowed_paths=[router.agent.active_project] if router.agent.active_project else None
            )
            cli.print_info("Lanzando sub-agente...")
            result = sub_agent.run_task(task)
            if result.status.value == "completed":
                print(result.output[:2000])
            else:
                cli.print_error(f"Error: {result.error}")
        else:
            print("  Uso: /subagent <descripcion de la tarea>")
        return True

    # ==================== NUEVOS COMANDOS v4.2 ====================

    if cmd == "/tree":
        project = router.agent.active_project or os.getcwd()
        print(f"\n  ESTRUCTURA: {project}")
        print("  " + "=" * 50)
        for root, dirs, files in os.walk(project):
            level = root.replace(project, '').count(os.sep)
            indent = '  ' * level
            dirname = os.path.basename(root) or root
            if level <= 3:
                print(f"  {indent}{dirname}/")
                subindent = '  ' * (level + 1)
                for f in files[:15]:
                    if not f.startswith('.'):
                        print(f"  {subindent}{f}")
                if len(files) > 15:
                    print(f"  {subindent}... +{len(files)-15} mas")
        print()
        return True

    if cmd == "/env":
        print("\n  VARIABLES DE ENTorno:")
        print("  " + "=" * 50)
        for k, v in sorted(os.environ.items()):
            if any(x in k.upper() for x in ['PATH', 'HOME', 'USER', 'PYTHON', 'NODE', 'API', 'KEY', 'TOKEN']):
                display = v[:60] + '...' if len(v) > 60 else v
                print(f"  {k}={display}")
        print()
        return True

    if cmd == "/deps":
        project = router.agent.active_project or os.getcwd()
        print(f"\n  DEPENDENCIAS: {project}")
        print("  " + "=" * 50)
        # Python
        req = os.path.join(project, 'requirements.txt')
        if os.path.exists(req):
            print("  [Python] requirements.txt:")
            with open(req, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        print(f"    - {line}")
        # Node
        pkg = os.path.join(project, 'package.json')
        if os.path.exists(pkg):
            import json
            try:
                with open(pkg, 'r') as f:
                    data = json.load(f)
                deps = data.get('dependencies', {})
                devdeps = data.get('devDependencies', {})
                if deps:
                    print("  [Node] dependencies:")
                    for k, v in deps.items():
                        print(f"    - {k}: {v}")
                if devdeps:
                    print("  [Node] devDependencies:")
                    for k, v in devdeps.items():
                        print(f"    - {k}: {v}")
            except Exception:
                pass
        # Cargo
        cargo = os.path.join(project, 'Cargo.toml')
        if os.path.exists(cargo):
            print("  [Rust] Cargo.toml detectado")
        if not os.path.exists(req) and not os.path.exists(pkg) and not os.path.exists(cargo):
            print("  No se encontraron dependencias")
        print()
        return True

    if cmd.startswith("/run"):
        parts = user_input.split(maxsplit=1)
        if len(parts) >= 2:
            script = parts[1].strip()
            cli.print_info(f"Ejecutando: {script}")
            from iam.core.persistent_shell import get_shell
            shell = get_shell()
            result = shell.exec(script, timeout=60, cwd=router.agent.active_project)
            if result.stdout:
                print(result.stdout)
            if result.stderr:
                print(f"STDERR: {result.stderr}")
            if result.exit_code != 0:
                cli.print_error(f"Fallo con codigo {result.exit_code}")
        else:
            print("  Uso: /run <comando>")
        return True

    if cmd.startswith("/search"):
        parts = user_input.split(maxsplit=1)
        if len(parts) >= 2:
            query = parts[1].strip()
            project = router.agent.active_project or os.getcwd()
            cli.print_info(f"Buscando '{query}' en {project}...")
            import subprocess
            try:
                result = subprocess.run(
                    ['findstr', '/S', '/I', '/N', query, '*.py', '*.js', '*.html', '*.css', '*.json', '*.md'],
                    cwd=project, capture_output=True, text=True, timeout=10
                )
                if result.stdout:
                    lines = result.stdout.strip().split('\n')[:30]
                    for line in lines:
                        print(f"  {line}")
                    if len(lines) >= 30:
                        print(f"  ... resultados truncados")
                else:
                    print("  Sin resultados")
            except Exception as e:
                print(f"  Error: {e}")
        else:
            print("  Uso: /search <texto>")
        return True

    if cmd.startswith("/grep"):
        parts = user_input.split(maxsplit=1)
        if len(parts) >= 2:
            pattern = parts[1].strip()
            project = router.agent.active_project or os.getcwd()
            import re
            try:
                regex = re.compile(pattern, re.IGNORECASE)
            except re.error:
                regex = re.compile(re.escape(pattern), re.IGNORECASE)
            print(f"\n  GREP: '{pattern}'")
            print("  " + "=" * 50)
            count = 0
            for root, dirs, files in os.walk(project):
                dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__', '.git']]
                for f in files:
                    if f.endswith(('.py', '.js', '.html', '.css', '.json', '.md', '.toml', '.yaml', '.yml', '.txt')):
                        fpath = os.path.join(root, f)
                        try:
                            with open(fpath, 'r', encoding='utf-8', errors='ignore') as fh:
                                for i, line in enumerate(fh, 1):
                                    if regex.search(line):
                                        rel = os.path.relpath(fpath, project)
                                        print(f"  {rel}:{i}: {line.strip()[:80]}")
                                        count += 1
                                        if count >= 30:
                                            print("  ... truncado (max 30)")
                                            break
                        except Exception:
                            pass
                        if count >= 30:
                            break
                if count >= 30:
                    break
            if count == 0:
                print("  Sin coincidencias")
            print(f"\n  Total: {count} coincidencias")
        else:
            print("  Uso: /grep <patron>")
        return True

    if cmd == "/clear":
        if router.agent.current_session:
            router.agent.current_session.clear()
            cli.print_success("Sesion limpiada")
        else:
            print("  No hay sesion activa")
        return True

    if cmd.startswith("/kill"):
        parts = user_input.split()
        if len(parts) >= 2:
            target = parts[1]
            cli.print_info(f"Terminando proceso: {target}")
            import subprocess
            try:
                subprocess.run(['taskkill', '/F', '/IM', target], capture_output=True, timeout=5)
                cli.print_success(f"Proceso {target} terminado")
            except Exception as e:
                cli.print_error(f"Error: {e}")
        else:
            print("  Uso: /kill <nombre_proceso>")
        return True

    return False


def main():
    args = parse_args()

    os.system('cls' if os.name == 'nt' else 'clear')

    cli = EnhancedCLI(theme=args.theme)

    if args.compact:
        cli.compact_mode = True
    if args.think:
        cli.think_mode = True

    cli.print_banner()

    memory = MemorySystem()
    router = AgentRouter(memory=memory)

    # Callback para cambiar modo con Tab
    MODE_CYCLE = ["general", "builder", "debug", "security", "reader"]
    def switch_mode():
        current = router.agent.current_mode
        idx = MODE_CYCLE.index(current) if current in MODE_CYCLE else 0
        new_mode = MODE_CYCLE[(idx + 1) % len(MODE_CYCLE)]
        router.agent.set_mode(new_mode)
        return new_mode
    cli.mode_switch_callback = switch_mode

    session_id = cli.session_ui.create_session("default")
    cli.print_info(f"Sesion: {session_id}")

    print(f"\n  [dim]Ctrl+K: Palette | Ctrl+R: Search | Tab: Cambiar modo | /help: Ayuda[/dim]")
    print(f"  [dim]/think: Pensamiento | /compact: Modo corto | /context: Contexto | /save: Guardar[/dim]\n")

    # === GATE: Obligar a elegir proyecto antes de chatear ===
    project_set = False
    
    def show_project_gate():
        print()
        print("  +-----------------------------------------------------+")
        print("  |  Para empezar, selecciona tu carpeta de proyecto     |")
        print("  |                                                     |")
        print("  |  Escribe:  /project                                |")
        print("  |                                                     |")
        print("  |  Esto abre un selector de carpetas.                |")
        print("  |  Todos los archivos se crearan ahi.                |")
        print("  +-----------------------------------------------------+")
        print()
    
    show_project_gate()

    # === SCAN INICIAL: La IA revisa la computadora ===
    print(f"  [analizando] Escaneando computadora...", end='', flush=True)
    try:
        import socket
        import getpass
        import platform
        
        system_info = {
            "user": getpass.getuser(),
            "pc_name": socket.gethostname(),
            "os": platform.system() + " " + platform.release(),
            "processor": platform.processor(),
        }
        
        # Disco
        try:
            import shutil
            total, used, free = shutil.disk_usage("C:\\")
            system_info["disk_total_gb"] = round(total / (1024**3), 1)
            system_info["disk_free_gb"] = round(free / (1024**3), 1)
        except:
            pass
        
        # RAM
        try:
            import psutil
            system_info["ram_gb"] = round(psutil.virtual_memory().total / (1024**3), 1)
        except ImportError:
            try:
                import subprocess
                result = subprocess.run('wmic OS get TotalVisibleMemorySize', shell=True, capture_output=True, text=True, timeout=5)
                lines = result.stdout.strip().split('\n')
                for line in lines:
                    if line.strip().isdigit():
                        system_info["ram_gb"] = round(int(line.strip()) / (1024**2), 1)
                        break
            except:
                pass
        except:
            pass
        
        # Escritorio
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        try:
            desktop_items = []
            for item in os.listdir(desktop):
                full_path = os.path.join(desktop, item)
                item_type = "carpeta" if os.path.isdir(full_path) else "archivo"
                desktop_items.append(f"{item} ({item_type})")
            system_info["desktop_items"] = desktop_items[:20]
        except:
            pass
        
        # Proyectos recientes en escritorio
        try:
            projects = []
            for item in os.listdir(desktop):
                full_path = os.path.join(desktop, item)
                if os.path.isdir(full_path):
                    files = os.listdir(full_path) if os.path.isdir(full_path) else []
                    projects.append({"name": item, "files": len(files)})
            system_info["projects"] = projects[:10]
        except:
            pass
        
        # Guardar en memoria
        context_summary = f"""CONTEXTO DE LA COMPUTADORA:
- Usuario: {system_info.get('user', 'N/A')}
- PC: {system_info.get('pc_name', 'N/A')}
- OS: {system_info.get('os', 'N/A')}
- Procesador: {system_info.get('processor', 'N/A')}
- RAM: {system_info.get('ram_gb', 'N/A')} GB
- Disco C: {system_info.get('disk_free_gb', 'N/A')} GB libres de {system_info.get('disk_total_gb', 'N/A')} GB
- Escritorio: {len(system_info.get('desktop_items', []))} items
- Proyectos: {', '.join([p['name'] for p in system_info.get('projects', [])]) if system_info.get('projects') else 'Ninguno'}
"""
        
        memory.store(
            content=context_summary,
            category="system_context",
            context="startup_scan",
            tags=["system", "context", "startup"],
            importance=0.9
        )
        
        # Tambien guardar en el agente para que la IA lo tenga
        router.agent.system_context = system_info
        
        print(f"\r  [analizando] Computadora analizada: {system_info.get('user', '?')}@{system_info.get('pc_name', '?')} | {system_info.get('os', '?')} | {system_info.get('ram_gb', '?')} GB RAM | {system_info.get('disk_free_gb', '?')} GB libres")
        
    except Exception as e:
        print(f"\r  [analizando] Scan completado (parcial)")
    
    while True:
        try:
            mode = router.agent.current_mode

            user_input = cli.get_input(mode)

            if user_input is None:
                print(f"\n  [dim]Bye![/dim]\n")
                break

            if not user_input:
                continue

            result = handle_special_commands(cli, user_input, router, memory)
            if result == "exit":
                break
            if result is True:
                continue

            cli.stats.track_command()

            # === GATE: Si no hay proyecto, bloquear todo excepto comandos de setup ===
            if not project_set:
                # Primero sync por si /project acaba de setear
                if router.agent.active_project:
                    project_set = True
                    cli.active_project = router.agent.active_project
                
                if not project_set:
                    cmd_lower = user_input.lower().strip()
                    allowed_without_project = ["/project", "/help", "/engine", "/theme", "/think", "/compact", "/alias", "help", "exit", "quit", "salir"]
                    
                    if not any(cmd_lower.startswith(a) or cmd_lower == a for a in allowed_without_project):
                        show_project_gate()
                        continue

            # Sincronizar proyecto activo con el CLI
            if router.agent.active_project:
                cli.active_project = router.agent.active_project
                if not project_set:
                    project_set = True
                    print(f"\n  [OK] Proyecto activo: {router.agent.active_project}")
                    print(f"  [dim]Ya puedes empezar a programar![/dim]\n")
            elif cli.active_project and not router.agent.active_project:
                cli.active_project = None

            cli.context_window.add_message("user", user_input)
            cli.session_ui.save_message("user", user_input)

            memory.store(
                content=user_input,
                category="conversation",
                context=f"mode:{mode}|time:{__import__('datetime').datetime.now().isoformat()}",
                tags=[mode, "user_input", "question" if "?" in user_input else "command"],
                importance=0.7 if "?" in user_input else 0.5
            )

            loader = LoadingIndicator()
            
            # Iniciar listener de ESC y limpiar interrupciones previas
            from iam.core.enhanced_cli import interrupt
            interrupt.clear()
            interrupt.start_listening()
            
            loader.start("🧠 procesando", "brain")

            start_time = time.time()
            try:
                response = router.process_input(user_input)
            finally:
                loader.stop()
                interrupt.stop_listening()

            # Verificar si fue interrumpido por ESC
            if interrupt.is_interrupted:
                interrupt.clear()
                cli.print_warning("Interrumpido por ESC")
                continue

            response_time = time.time() - start_time

            if response:
                cli._last_response = response
                cli._last_query = user_input

                cli.context_window.add_message("assistant", response)
                cli.session_ui.save_message("assistant", response)

                if response_time > 0.1:
                    cli.stats.track_ai_query(response_time)

                print()
                cli.render_response(response)

                if response_time > 0.5:
                    print(f"\n  [dim]({response_time:.1f}s)[/dim]")

                print()

                cli.show_suggestions(response, user_input)

                if cli.think_mode:
                    cli.show_context_usage()

                if len(response) > 50:
                    response_type = "knowledge"
                    if any(w in response.lower() for w in ["error", "fallo", "no se pudo"]):
                        response_type = "error"
                    elif any(w in response.lower() for w in ["creado", "ejecutado", "instalado"]):
                        response_type = "action"
                    elif any(w in response.lower() for w in ["codigo", "funcion", "clase"]):
                        response_type = "code"

                    memory.store(
                        content=response[:300],
                        category=response_type,
                        context=f"mode:{mode}|query:{user_input[:100]}",
                        tags=[mode, "response", response_type],
                        importance=0.8 if response_type == "error" else 0.6
                    )

        except KeyboardInterrupt:
            print(f"\n  [dim]Bye![/dim]\n")
            break
        except Exception as e:
            cli.print_error(str(e))


if __name__ == "__main__":
    main()
