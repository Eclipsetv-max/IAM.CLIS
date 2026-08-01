# -*- coding: utf-8 -*-
"""
Pruebas del sistema IAM
"""

import os
import sys
import tempfile
import shutil

# Agregar directorio al path
sys.path.insert(0, r'C:\Users\casa\Desktop\Yo ia')

def test_loading_animation():
    """Probar que la animacion de carga funciona"""
    from iam.core.loading import LoadingIndicator
    import time
    
    print("Test 1: Animacion de carga...")
    loader = LoadingIndicator()
    loader.start("[construyendo]", "build")
    time.sleep(0.5)
    loader.stop()
    print("  OK: Animacion funciona")
    return True

def test_mode_messages():
    """Probar mensajes por modo"""
    from iam.core.agent import Agent
    
    print("Test 2: Mensajes por modo...")
    agent = Agent()
    
    modes = {
        "general": "[analizando]",
        "builder": "[construyendo]",
        "debug": "[depurando]",
        "security": "[verificando]",
        "reader": "[leyendo]"
    }
    
    for mode, expected in modes.items():
        agent.current_mode = mode
        msg = agent._get_mode_message()
        if expected not in msg:
            print(f"  ERROR: {mode} esperaba '{expected}', obtuvo '{msg}'")
            return False
    
    print("  OK: Todos los mensajes son correctos")
    return True

def test_mode_spinners():
    """Probar spinners por modo"""
    from iam.core.agent import Agent
    
    print("Test 3: Spinners por modo...")
    agent = Agent()
    
    spinners = {
        "general": "dots",
        "builder": "build",
        "debug": "line",
        "security": "pulse",
        "reader": "clock"
    }
    
    for mode, expected in spinners.items():
        agent.current_mode = mode
        spinner = agent._get_mode_spinner()
        if spinner != expected:
            print(f"  ERROR: {mode} esperaba '{expected}', obtuvo '{spinner}'")
            return False
    
    print("  OK: Todos los spinners son correctos")
    return True

def test_tool_call_parser():
    """Probar parser de TOOL_CALLs"""
    from iam.core.agent import Agent
    
    print("Test 4: Parser de TOOL_CALLs...")
    agent = Agent()
    
    # Test 1: TOOL_CALL con action y name
    test1 = '''[TOOL_CALL]
action: create_file
name: "index.html"
<!DOCTYPE html>
<html>
</html>
[/TOOL_CALL]'''
    
    result = agent._parse_tool_block(test1)
    if not result or result.get('action') != 'create_file':
        print("  ERROR: No parseo create_file correctamente")
        return False
    if not result.get('path'):
        print("  ERROR: No encontro el path")
        return False
    
    # Test 2: TOOL_CALL con contenido HTML auto-detect
    test2 = '''[TOOL_CALL]
action: create_file
<!DOCTYPE html>
<html><body>Test</body></html>
[/TOOL_CALL]'''
    
    result2 = agent._parse_tool_block(test2)
    if not result2 or result2.get('action') != 'create_file':
        print("  ERROR: No auto-detecto create_file")
        return False
    
    print("  OK: Parser funciona correctamente")
    return True

def test_file_operations():
    """Probar operaciones de archivos en directorio temporal"""
    from iam.core.agent import Agent
    
    print("Test 5: Operaciones de archivos...")
    agent = Agent()
    
    # Crear directorio temporal
    temp_dir = tempfile.mkdtemp()
    agent.active_project = temp_dir
    
    try:
        # Test create_file
        result = agent._run_tool_call("create_file", os.path.join(temp_dir, "test.html"), "<!DOCTYPE html><html></html>", None, None, None)
        if '[OK]' not in result:
            print(f"  ERROR: create_file fallo: {result}")
            return False
        
        # Test read_file
        result = agent._run_tool_call("read_file", os.path.join(temp_dir, "test.html"), None, None, None, None)
        if '[OK]' not in result:
            print(f"  ERROR: read_file fallo: {result}")
            return False
        
        # Test edit_file
        result = agent._run_tool_call("edit_file", os.path.join(temp_dir, "test.html"), "<html></html>", None, "<html>", "<html><body>edited</body></html>")
        if '[OK]' not in result:
            print(f"  ERROR: edit_file fallo: {result}")
            return False
        
        print("  OK: Operaciones de archivos funcionan")
        return True
    
    finally:
        shutil.rmtree(temp_dir)

def test_prompt_quality():
    """Probar que los prompts tienen las instrucciones correctas"""
    from iam.config.prompts import AGENT_PROMPTS
    
    print("Test 6: Calidad de prompts...")
    
    # Verificar que general tiene instruccion de ejecutar
    if "EJECUTA" not in AGENT_PROMPTS["general"]["system"]:
        print("  ERROR: Prompt general no tiene instruccion EJECUTA")
        return False
    
    # Verificar que builder tiene instrucciones de calidad
    if "CALIDAD" not in AGENT_PROMPTS["builder"]["system"]:
        print("  ERROR: Prompt builder no tiene seccion CALIDAD")
        return False
    
    # Verificar que todos los modos tienen system prompt
    for mode in ["general", "builder", "debug", "security", "reader"]:
        if "system" not in AGENT_PROMPTS[mode]:
            print(f"  ERROR: Modo {mode} no tiene system prompt")
            return False
    
    print("  OK: Prompts tienen instrucciones correctas")
    return True

def test_skills_structure():
    """Probar estructura de skills"""
    from iam.modes.loader import load_all_skills
    
    print("Test 7: Estructura de skills...")
    
    skills = load_all_skills()
    
    expected_modes = ["general", "builder", "debug", "security", "reader"]
    for mode in expected_modes:
        if mode not in skills:
            print(f"  ERROR: Falta modo {mode}")
            return False
        if "tools" not in skills[mode]:
            print(f"  ERROR: Modo {mode} no tiene tools")
            return False
        if "capabilities" not in skills[mode]:
            print(f"  ERROR: Modo {mode} no tiene capabilities")
            return False
    
    print("  OK: Estructura de skills completa")
    return True

def run_all_tests():
    """Ejecutar todas las pruebas"""
    print("=" * 50)
    print("PRUEBAS DEL SISTEMA IAM")
    print("=" * 50)
    print()
    
    tests = [
        test_loading_animation,
        test_mode_messages,
        test_mode_spinners,
        test_tool_call_parser,
        test_file_operations,
        test_prompt_quality,
        test_skills_structure
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"  EXCEPCION: {e}")
            failed += 1
        print()
    
    print("=" * 50)
    print(f"RESULTADOS: {passed} pasaron, {failed} fallaron")
    print("=" * 50)
    
    return failed == 0

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
