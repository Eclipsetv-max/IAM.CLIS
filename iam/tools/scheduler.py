# -*- coding: utf-8 -*-
"""
IAM Scheduler - Administracion de tareas programadas del sistema
Permite crear, listar, eliminar y administrar tareas
"""

import subprocess
import platform
import os
from typing import Tuple, List, Dict, Any


class Scheduler:
    """
    Administrador de tareas programadas
    """
    
    def __init__(self):
        self.is_windows = platform.system() == "Windows"
    
    def _run_powershell(self, command: str, timeout: int = 30) -> Tuple[bool, str]:
        """Ejecutar comando de PowerShell"""
        try:
            result = subprocess.run(
                ['powershell', '-Command', command],
                capture_output=True, text=True, timeout=timeout,
                encoding='utf-8', errors='replace'
            )
            return True, result.stdout if result.stdout else result.stderr
        except Exception as e:
            return False, str(e)
    
    # === LISTAR TAREAS ===
    
    def list_tasks(self, folder: str = "\\") -> Tuple[bool, List[Dict]]:
        """Listar todas las tareas programadas"""
        if not self.is_windows:
            return False, []
        
        try:
            cmd = f'''
            Get-ScheduledTask -TaskPath "{folder}*" -ErrorAction SilentlyContinue | 
            Select-Object TaskName, TaskPath, State, @{{
                Name='Actions';Expression={{($_.Actions | ForEach-Object {{ $_.Execute }}) -join ', '}}
            }} | 
            Sort-Object TaskName |
            Format-Table -AutoSize | Out-String
            '''
            success, output = self._run_powershell(cmd, timeout=60)
            return success, output.strip() if success else output
        except Exception as e:
            return False, str(e)
    
    def get_task_info(self, task_name: str) -> Tuple[bool, Dict]:
        """Obtener informacion de una tarea"""
        if not self.is_windows:
            return False, {}
        
        try:
            cmd = f'''
            $task = Get-ScheduledTask -TaskName "{task_name}" -ErrorAction SilentlyContinue
            if ($task) {{
                $info = Get-ScheduledTaskInfo -TaskName "{task_name}" -ErrorAction SilentlyContinue
                [PSCustomObject]@{{
                    Name = $task.TaskName
                    Path = $task.TaskPath
                    State = $task.State
                    LastRun = $info.LastRunTime
                    NextRun = $info.NextRunTime
                    LastResult = $info.LastTaskResult
                    Triggers = ($task.Triggers | ForEach-Object {{ $_.ToString() }}) -join '; '
                    Actions = ($task.Actions | ForEach-Object {{ $_.Execute + ' ' + $_.Arguments }}) -join '; '
                }} | Format-List | Out-String
            }}
            '''
            success, output = self._run_powershell(cmd)
            return success, output.strip() if success else output
        except Exception as e:
            return False, str(e)
    
    # === CREAR TAREA ===
    
    def create_task(self, name: str, command: str, trigger_type: str = "daily",
                    time: str = "09:00", days: str = "*", folder: str = "\\") -> Tuple[bool, str]:
        """Crear tarea programada"""
        if not self.is_windows:
            return False, "Solo disponible en Windows"
        
        try:
            # Crear accion
            action_cmd = f'$action = New-ScheduledTaskAction -Execute "{command}"'
            
            # Crear trigger segun tipo
            if trigger_type == "daily":
                trigger_cmd = f'$trigger = New-ScheduledTaskTrigger -Daily -At "{time}"'
            elif trigger_type == "weekly":
                trigger_cmd = f'$trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek {days} -At "{time}"'
            elif trigger_type == "monthly":
                trigger_cmd = f'$trigger = New-ScheduledTaskTrigger -Monthly -DaysOfMonth {days} -At "{time}"'
            elif trigger_type == "once":
                trigger_cmd = f'$trigger = New-ScheduledTaskTrigger -Once -At "{time}"'
            elif trigger_type == "startup":
                trigger_cmd = '$trigger = New-ScheduledTaskTrigger -AtStartup'
            elif trigger_type == "logon":
                trigger_cmd = '$trigger = New-ScheduledTaskTrigger -AtLogOn'
            else:
                trigger_cmd = f'$trigger = New-ScheduledTaskTrigger -Daily -At "{time}"'
            
            # Registrar tarea
            cmd = f'''
            {action_cmd}
            {trigger_cmd}
            Register-ScheduledTask -TaskName "{name}" -Action $action -Trigger $trigger -Force
            '''
            
            success, output = self._run_powershell(cmd)
            return True, f"[OK] Tarea '{name}' creada" if success else output
        except Exception as e:
            return False, str(e)
    
    def create_simple_task(self, name: str, command: str, 
                          schedule: str = "daily", time: str = "09:00") -> Tuple[bool, str]:
        """Crear tarea simple"""
        return self.create_task(name, command, schedule, time)
    
    # === EJECUTAR TAREA ===
    
    def run_task(self, task_name: str) -> Tuple[bool, str]:
        """Ejecutar tarea inmediatamente"""
        if not self.is_windows:
            return False, "Solo disponible en Windows"
        
        try:
            cmd = f'Start-ScheduledTask -TaskName "{task_name}"'
            success, output = self._run_powershell(cmd)
            return True, f"[OK] Tarea '{task_name}' ejecutada" if success else output
        except Exception as e:
            return False, str(e)
    
    # === HABILITAR/DESHABILITAR ===
    
    def enable_task(self, task_name: str) -> Tuple[bool, str]:
        """Habilitar tarea"""
        if not self.is_windows:
            return False, "Solo disponible en Windows"
        
        try:
            cmd = f'Enable-ScheduledTask -TaskName "{task_name}"'
            success, output = self._run_powershell(cmd)
            return True, f"[OK] Tarea '{task_name}' habilitada" if success else output
        except Exception as e:
            return False, str(e)
    
    def disable_task(self, task_name: str) -> Tuple[bool, str]:
        """Deshabilitar tarea"""
        if not self.is_windows:
            return False, "Solo disponible en Windows"
        
        try:
            cmd = f'Disable-ScheduledTask -TaskName "{task_name}"'
            success, output = self._run_powershell(cmd)
            return True, f"[OK] Tarea '{task_name}' deshabilitada" if success else output
        except Exception as e:
            return False, str(e)
    
    # === ELIMINAR TAREA ===
    
    def delete_task(self, task_name: str) -> Tuple[bool, str]:
        """Eliminar tarea"""
        if not self.is_windows:
            return False, "Solo disponible en Windows"
        
        try:
            cmd = f'Unregister-ScheduledTask -TaskName "{task_name}" -Confirm:$false'
            success, output = self._run_powershell(cmd)
            return True, f"[OK] Tarea '{task_name}' eliminada" if success else output
        except Exception as e:
            return False, str(e)
    
    # === EXPORTAR/IMPORTAR ===
    
    def export_task(self, task_name: str, output_file: str) -> Tuple[bool, str]:
        """Exportar tarea a XML"""
        if not self.is_windows:
            return False, "Solo disponible en Windows"
        
        try:
            cmd = f'''
            $task = Get-ScheduledTask -TaskName "{task_name}"
            $task | Export-ScheduledTask | Out-File "{output_file}" -Encoding UTF8
            '''
            success, output = self._run_powershell(cmd)
            return True, f"[OK] Tarea exportada a: {output_file}" if success else output
        except Exception as e:
            return False, str(e)
    
    def import_task(self, xml_file: str) -> Tuple[bool, str]:
        """Importar tarea desde XML"""
        if not self.is_windows:
            return False, "Solo disponible en Windows"
        
        try:
            cmd = f'Register-ScheduledTask -Xml (Get-Content "{xml_file}" -Raw) -Force'
            success, output = self._run_powershell(cmd)
            return True, f"[OK] Tarea importada desde: {xml_file}" if success else output
        except Exception as e:
            return False, str(e)
    
    # === ESTADISTICAS ===
    
    def get_task_history(self, task_name: str = None, count: int = 10) -> Tuple[bool, str]:
        """Obtener historial de ejecucion"""
        if not self.is_windows:
            return False, "Solo disponible en Windows"
        
        try:
            if task_name:
                cmd = f'''
                Get-ScheduledTask -TaskName "{task_name}" | 
                Get-ScheduledTaskInfo | 
                Select-Object -First {count} |
                Format-Table -AutoSize | Out-String
                '''
            else:
                cmd = f'''
                Get-ScheduledTask | 
                Where-Object {{ $_.State -ne "Disabled" }} |
                Get-ScheduledTaskInfo |
                Select-Object -First {count} |
                Format-Table -AutoSize | Out-String
                '''
            
            success, output = self._run_powershell(cmd, timeout=60)
            return success, output.strip() if success else output
        except Exception as e:
            return False, str(e)
    
    # === TAREAS COMUNES ===
    
    def get_system_tasks(self) -> Tuple[bool, List[str]]:
        """Obtener tareas del sistema predefinidas"""
        common_tasks = [
            "Microsoft\\Windows\\Defrag",
            "Microsoft\\Windows\\DiskCleanup",
            "Microsoft\\Windows\\WindowsUpdate",
            "Microsoft\\Windows\\WindowsBackup",
            "Microsoft\\Windows\\Customer Experience Improvement Program",
            "Microsoft\\Windows\\Application Experience",
            "Microsoft\\Windows\\Maps",
            "Microsoft\\Windows\\CloudExperienceHost",
        ]
        return True, common_tasks


# Instancia global
scheduler = Scheduler()
