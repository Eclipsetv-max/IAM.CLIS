import sys, os, time
sys.path.insert(0, r"C:\Users\casa\Desktop\Yo ia para github")

from iam.core.memory import MemorySystem
from iam.core.agent import Agent

TEST_DIR = r"C:\Users\casa\Desktop\iam_real_tests"
project_dir = os.path.join(TEST_DIR, "test_1_portfolio")
os.makedirs(project_dir, exist_ok=True)

print("Creating agent exactly like test_runner...")
memory = MemorySystem()
agent = Agent(memory=memory)
agent.set_active_project(project_dir)
agent.set_mode("builder")

print("Calling agent.chat()...")
t = time.time()
response = agent.chat("Crea una pagina web de portfolio personal con HTML, CSS y JS. Tema oscuro, moderna, responsive.", stream=False)
print(f"Time: {time.time()-t:.1f}s")
print(f"Response length: {len(response)}")
print(f"Response repr: {repr(response)}")

files = [f for f in os.listdir(project_dir) if os.path.isfile(os.path.join(project_dir, f))]
print(f"Files: {files}")
