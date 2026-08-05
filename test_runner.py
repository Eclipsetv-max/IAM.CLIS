"""Test runner for IAM - creates web projects and validates results"""
import os
import sys
import json
import time

sys.path.insert(0, r"C:\Users\casa\Desktop\Yo ia para github")

from iam.config.settings import settings
from iam.core.memory import MemorySystem
from iam.core.agent import Agent

TEST_DIR = r"C:\Users\casa\Desktop\iam_real_tests"

def test_project(test_num, name, prompt):
    """Run a single test project"""
    project_dir = os.path.join(TEST_DIR, f"test_{test_num}_{name}")
    os.makedirs(project_dir, exist_ok=True)
    
    print(f"\n{'='*60}")
    print(f"TEST {test_num}: {name}")
    print(f"Prompt: {prompt[:80]}...")
    print(f"Dir: {project_dir}")
    print(f"{'='*60}")
    
    memory = MemorySystem()
    agent = Agent(memory=memory)
    agent.set_active_project(project_dir)
    agent.set_mode("builder")
    
    response = agent.chat(prompt, stream=False)
    
    print(f"\nResponse length: {len(response) if response else 0} chars")
    
    # Check what files were created
    files_created = []
    if os.path.exists(project_dir):
        for f in os.listdir(project_dir):
            fpath = os.path.join(project_dir, f)
            if os.path.isfile(fpath):
                size = os.path.getsize(fpath)
                files_created.append((f, size))
    
    print(f"Files created: {len(files_created)}")
    for fname, fsize in files_created:
        print(f"  - {fname} ({fsize} bytes)")
    
    # Validate
    has_html = any(f.endswith('.html') for f, _ in files_created)
    has_css = any(f.endswith('.css') for f, _ in files_created)
    has_js = any(f.endswith('.js') for f, _ in files_created)
    
    issues = []
    if not has_html:
        issues.append("NO HTML file created")
    if not has_css:
        issues.append("NO CSS file created")
    if not has_js:
        issues.append("NO JS file created")
    
    # Check HTML content
    for fname, fsize in files_created:
        if fname.endswith('.html') and fsize < 100:
            issues.append(f"HTML too small ({fsize} bytes)")
        if fname.endswith('.css') and fsize < 50:
            issues.append(f"CSS too small ({fsize} bytes)")
    
    if issues:
        print(f"ISSUES: {', '.join(issues)}")
    else:
        print("ALL CHECKS PASSED")
    
    return {
        "test": test_num,
        "name": name,
        "files": files_created,
        "has_html": has_html,
        "has_css": has_css,
        "has_js": has_js,
        "issues": issues,
        "response_len": len(response) if response else 0
    }


if __name__ == "__main__":
    tests = [
        (1, "portfolio", "Crea una pagina web de portfolio personal con HTML, CSS y JS. Tema oscuro, moderna, responsive."),
        (2, "landing", "Crea una landing page para una app de fitness con HTML, CSS y JS. Usa imagenes de placeholder de picsum.photos."),
        (3, "ecommerce", "Crea una pagina de producto de tienda online con HTML, CSS y JS. Muestra zapatillas deportivas."),
        (4, "blog", "Crea un blog personal con galeria de imagenes usando HTML, CSS y JS."),
        (5, "dashboard", "Crea un dashboard admin panel con HTML, CSS y JS. Paneles de stats, graficos, sidebar."),
    ]
    
    results = []
    for i, (num, name, prompt) in enumerate(tests):
        if i > 0:
            print(f"\nWaiting 3s before next test...")
            time.sleep(3)
        result = test_project(num, name, prompt)
        results.append(result)
    
    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    
    total = len(results)
    passed = sum(1 for r in results if not r["issues"])
    print(f"Passed: {passed}/{total}")
    
    for r in results:
        status = "PASS" if not r["issues"] else "FAIL"
        print(f"  Test {r['test']} ({r['name']}): {status} - {len(r['files'])} files")
        if r["issues"]:
            for issue in r["issues"]:
                print(f"    - {issue}")
    
    # Save results
    with open(os.path.join(TEST_DIR, "test_results.json"), 'w') as f:
        json.dump(results, f, indent=2)
