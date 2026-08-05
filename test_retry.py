import asyncio
import sys
import os

sys.path.insert(0, '.')
os.environ.setdefault('TEST_OUTPUT_DIR', r'C:\Users\casa\Desktop\iam_real_tests')

from iam.core.agent import Agent

def test():
    agent = Agent()
    result = agent.chat(
        'Crea un portfolio personal minimalista con HTML, CSS y JS separados. '
        'Archivos: index.html, style.css, script.js. '
        'Incluye animaciones suaves y modo oscuro.',
        stream=False
    )
    test_dir = agent.active_project
    if test_dir:
        files = os.listdir(test_dir)
        print(f'\n=== FILES CREATED: {files} ===')
        for f in files:
            size = os.path.getsize(os.path.join(test_dir, f))
            print(f'  {f}: {size} bytes')
        if len(files) == 3:
            print('\n*** ALL 3 FILES CREATED! ***')
        else:
            print(f'\n*** MISSING {3 - len(files)} files ***')
    else:
        print('NO PROJECT FOLDER')

if __name__ == '__main__':
    test()
