# -*- coding: utf-8 -*-
"""
IAM Filesystem - Acceso completo al sistema de archivos
Permite crear, leer, editar, mover, copiar y eliminar archivos/carpetas
"""

import os
import platform
import shutil
import subprocess
import glob
import hashlib
import zipfile
import tarfile
from pathlib import Path
from typing import Tuple, List, Dict, Any, Optional
from datetime import datetime


class FileSystem:
    """
    Sistema de archivos completo para IAM
    Acceso total a la computadora del usuario
    """
    
    def __init__(self):
        self.home_dir = Path.home()
        self.desktop = self.home_dir / "Desktop"
        self.documents = self.home_dir / "Documents"
        self.downloads = self.home_dir / "Downloads"
        self._history_dir = Path.home() / ".iam" / "history"
        self._history_dir.mkdir(parents=True, exist_ok=True)
    
    def _backup_file(self, file_path: Path):
        """Backup de archivo antes de editar (IAM)"""
        try:
            if not file_path.exists():
                return
            import hashlib
            content = file_path.read_bytes()
            file_hash = hashlib.md5(content).hexdigest()[:8]
            backup_name = f"{file_path.name}.{file_hash}.bak"
            backup_path = self._history_dir / backup_name
            if not backup_path.exists():
                backup_path.write_bytes(content)
        except:
            pass
    
    def undo_last_edit(self, file_path: str) -> Tuple[bool, str]:
        """Deshacer ultima edicion (IAM)"""
        try:
            path = Path(file_path)
            # Buscar backup mas reciente
            backups = sorted(self._history_dir.glob(f"{path.name}.*.bak"), key=lambda p: p.stat().st_mtime, reverse=True)
            if not backups:
                return False, "No hay backups disponibles"
            latest = backups[0]
            content = latest.read_bytes()
            path.write_bytes(content)
            return True, f"Archivo restaurado desde: {latest.name}"
        except Exception as e:
            return False, f"Error al restaurar: {e}"
        
        # Templates inteligentes para diferentes tipos de archivo
        self.templates = {
            # Python
            "python": {
                "basic": '# -*- coding: utf-8 -*-\n"""Module description"""\n\n\ndef main():\n    pass\n\n\nif __name__ == "__main__":\n    main()\n',
                "class": '# -*- coding: utf-8 -*-\n"""Module description"""\n\n\nclass {name}:\n    """Class description"""\n    \n    def __init__(self):\n        pass\n    \n    def __repr__(self):\n        return f"<{name}>()"\n',
                "flask": 'from flask import Flask, jsonify, request\n\napp = Flask(__name__)\n\n\n@app.route("/")\ndef index():\n    return jsonify({"status": "ok"})\n\n\n@app.route("/api/<path:endpoint>", methods=["GET", "POST"])\ndef api(endpoint):\n    data = request.get_json() if request.is_json else {}\n    return jsonify({"endpoint": endpoint, "data": data})\n\n\nif __name__ == "__main__":\n    app.run(debug=True, port=5000)\n',
                "fastapi": 'from fastapi import FastAPI, HTTPException\nfrom pydantic import BaseModel\nfrom typing import Optional, Any\n\napp = FastAPI()\n\n\nclass Item(BaseModel):\n    name: str\n    description: Optional[str] = None\n\n\n@app.get("/")\nasync def root():\n    return {"message": "API is running"}\n\n\n@app.get("/items/{item_id}")\nasync def read_item(item_id: int):\n    return {"item_id": item_id}\n\n\n@app.post("/items/")\nasync def create_item(item: Item):\n    return {"item": item}\n',
                "cli": 'import argparse\nimport sys\n\n\ndef main():\n    parser = argparse.ArgumentParser(description="Tool description")\n    parser.add_argument("command", help="Command to execute")\n    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")\n    \n    args = parser.parse_args()\n    \n    if args.verbose:\n        print(f"Executing: {args.command}")\n    \n    # TODO: Implement logic\n    print(f"Command: {args.command}")\n\n\nif __name__ == "__main__":\n    main()\n',
                "gui": 'import tkinter as tk\nfrom tkinter import ttk\n\n\nclass App:\n    def __init__(self, root):\n        self.root = root\n        self.root.title("App Title")\n        self.root.geometry("800x600")\n        \n        self.setup_ui()\n    \n    def setup_ui(self):\n        # Main frame\n        self.frame = ttk.Frame(self.root, padding="10")\n        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))\n        \n        # Label\n        ttk.Label(self.frame, text="Hello World").grid(row=0, column=0, pady=5)\n        \n        # Button\n        ttk.Button(self.frame, text="Click Me", command=self.on_click).grid(row=1, column=0, pady=5)\n    \n    def on_click(self):\n        print("Button clicked!")\n\n\nif __name__ == "__main__":\n    root = tk.Tk()\n    app = App(root)\n    root.mainloop()\n',
                "game": 'import pygame\nimport sys\n\n# Initialize pygame\npygame.init()\n\n# Constants\nSCREEN_WIDTH = 800\nSCREEN_HEIGHT = 600\nFPS = 60\n\n# Colors\nWHITE = (255, 255, 255)\nBLACK = (0, 0, 0)\nRED = (255, 0, 0)\nGREEN = (0, 255, 0)\nBLUE = (0, 0, 255)\n\n\nclass Game:\n    def __init__(self):\n        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))\n        pygame.display.set_caption("Game Title")\n        self.clock = pygame.time.Clock()\n        self.running = True\n    \n    def handle_events(self):\n        for event in pygame.event.get():\n            if event.type == pygame.QUIT:\n                self.running = False\n            elif event.type == pygame.KEYDOWN:\n                if event.key == pygame.K_ESCAPE:\n                    self.running = False\n    \n    def update(self):\n        pass\n    \n    def draw(self):\n        self.screen.fill(BLACK)\n        pygame.display.flip()\n    \n    def run(self):\n        while self.running:\n            self.handle_events()\n            self.update()\n            self.draw()\n            self.clock.tick(FPS)\n        pygame.quit()\n        sys.exit()\n\n\nif __name__ == "__main__":\n    game = Game()\n    game.run()\n',
                "api_client": 'import requests\nfrom typing import Any, Optional\n\n\nclass APIClient:\n    """API Client for REST services"""\n    \n    def __init__(self, base_url: str, api_key: Optional[str] = None):\n        self.base_url = base_url.rstrip("/")\n        self.session = requests.Session()\n        \n        if api_key:\n            self.session.headers["Authorization"] = "Bearer " + api_key\n        \n        self.session.headers["Content-Type"] = "application/json"\n    \n    def get(self, endpoint: str, params: dict = None) -> Any:\n        url = self.base_url + "/" + endpoint.lstrip("/")\n        response = self.session.get(url, params=params)\n        response.raise_for_status()\n        return response.json()\n    \n    def post(self, endpoint: str, data: dict = None) -> Any:\n        url = self.base_url + "/" + endpoint.lstrip("/")\n        response = self.session.post(url, json=data)\n        response.raise_for_status()\n        return response.json()\n    \n    def put(self, endpoint: str, data: dict = None) -> Any:\n        url = self.base_url + "/" + endpoint.lstrip("/")\n        response = self.session.put(url, json=data)\n        response.raise_for_status()\n        return response.json()\n    \n    def delete(self, endpoint: str) -> Any:\n        url = self.base_url + "/" + endpoint.lstrip("/")\n        response = self.session.delete(url)\n        response.raise_for_status()\n        return response.json()\n'
            },
            
            # JavaScript/TypeScript
            "javascript": {
                "basic": '// Module description\n\n/**\n * Main function\n */\nfunction main() {\n    // TODO: Implement\n}\n\nmain();\n',
                "class": '/**\n * Class description\n */\nclass {name} {\n    constructor() {\n        // TODO: Initialize\n    }\n    \n    toString() {\n        return `{name}()`;\n    }\n}\n\nmodule.exports = {name};\n',
                "express": 'const express = require("express");\nconst app = express();\nconst PORT = process.env.PORT || 3000;\n\n// Middleware\napp.use(express.json());\napp.use(express.urlencoded({ extended: true }));\n\n// Routes\napp.get("/", (req, res) => {\n    res.json({ status: "ok" });\n});\n\napp.get("/api/:endpoint", (req, res) => {\n    res.json({ endpoint: req.params.endpoint });\n});\n\napp.post("/api/:endpoint", (req, res) => {\n    res.json({ endpoint: req.params.endpoint, data: req.body });\n});\n\n// Start server\napp.listen(PORT, () => {\n    console.log(`Server running on port ${PORT}`);\n});\n',
                "react": 'import React, { useState, useEffect } from "react";\n\n/**\n * Component description\n */\nfunction {name}() {\n    const [data, setData] = useState(null);\n    const [loading, setLoading] = useState(true);\n    \n    useEffect(() => {\n        // TODO: Fetch data\n        setLoading(false);\n    }, []);\n    \n    if (loading) {\n        return <div>Loading...</div>;\n    }\n    \n    return (\n        <div className="{name}">\n            <h1>{name}</h1>\n        </div>\n    );\n}\n\nexport default {name};\n',
                "test": 'const { expect } = require("chai");\n\n// Test module\n\nit("should do something", function() {\n    // Arrange\n    \n    // Act\n    \n    // Assert\n    expect(true).to.be.true;\n});\n',
                "html": '<!DOCTYPE html>\n<html lang="en">\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>{name}</title>\n    <style>\n        * {\n            margin: 0;\n            padding: 0;\n            box-sizing: border-box;\n        }\n        \n        body {\n            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;\n            line-height: 1.6;\n            color: #333;\n        }\n        \n        .container {\n            max-width: 1200px;\n            margin: 0 auto;\n            padding: 20px;\n        }\n    </style>\n</head>\n<body>\n    <div class="container">\n        <h1>{name}</h1>\n        <p>Welcome to your project.</p>\n    </div>\n</body>\n</html>\n',
                "css": '/* {name} styles */\n\n:root {\n    --primary-color: #3b82f6;\n    --secondary-color: #10b981;\n    --background: #ffffff;\n    --text-color: #1f2937;\n}\n\n* {\n    margin: 0;\n    padding: 0;\n    box-sizing: border-box;\n}\n\nbody {\n    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;\n    background: var(--background);\n    color: var(--text-color);\n    line-height: 1.6;\n}\n\n.container {\n    max-width: 1200px;\n    margin: 0 auto;\n    padding: 20px;\n}\n',
                "node_cli": '#!/usr/bin/env node\n\nconst program = require("commander");\n\nprogram\n    .version("1.0.0")\n    .description("CLI Tool description")\n    .command("<command>")\n    .description("Command to execute")\n    .action((command) => {\n        console.log(`Executing: ${command}`);\n    });\n\nprogram.parse(process.argv);\n'
            },
            
            # Web
            "html": {
                "basic": '<!DOCTYPE html>\n<html lang="en">\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>{name}</title>\n    <link rel="stylesheet" href="style.css">\n</head>\n<body>\n    <header>\n        <nav>\n            <a href="/">Home</a>\n        </nav>\n    </header>\n    \n    <main>\n        <h1>{name}</h1>\n        <p>Welcome to your project.</p>\n    </main>\n    \n    <footer>\n        <p>&copy; 2026</p>\n    </footer>\n    \n    <script src="script.js"></script>\n</body>\n</html>\n',
                "landing": '<!DOCTYPE html>\n<html lang="en">\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>{name}</title>\n    <style>\n        * { margin: 0; padding: 0; box-sizing: border-box; }\n        body { font-family: -apple-system, sans-serif; }\n        .hero { min-height: 100vh; display: flex; align-items: center; justify-content: center; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; text-align: center; }\n        .hero h1 { font-size: 3rem; margin-bottom: 1rem; }\n        .hero p { font-size: 1.25rem; margin-bottom: 2rem; opacity: 0.9; }\n        .btn { background: white; color: #667eea; padding: 1rem 2rem; border-radius: 8px; text-decoration: none; font-weight: 600; transition: transform 0.2s; }\n        .btn:hover { transform: translateY(-2px); }\n    </style>\n</head>\n<body>\n    <section class="hero">\n        <div>\n            <h1>{name}</h1>\n            <p>Start building something amazing</p>\n            <a href="#features" class="btn">Get Started</a>\n        </div>\n    </section>\n</body>\n</html>\n'
            },
            
            # Config files
            "json": {
                "package": '{\n  "name": "{name}",\n  "version": "1.0.0",\n  "description": "",\n  "main": "index.js",\n  "scripts": {\n    "start": "node index.js",\n    "dev": "nodemon index.js",\n    "test": "jest"\n  },\n  "keywords": [],\n  "author": "",\n  "license": "ISC",\n  "dependencies": {},\n  "devDependencies": {}\n}\n',
                "tsconfig": '{\n  "compilerOptions": {\n    "target": "ES2020",\n    "module": "commonjs",\n    "lib": ["ES2020"],\n    "outDir": "./dist",\n    "rootDir": "./src",\n    "strict": true,\n    "esModuleInterop": true,\n    "skipLibCheck": true,\n    "forceConsistentCasingInFileNames": true,\n    "resolveJsonModule": true,\n    "declaration": true,\n    "declarationMap": true,\n    "sourceMap": true\n  },\n  "include": ["src/**/*"],\n  "exclude": ["node_modules", "dist"]\n}\n',
                "vscode": '{\n    "editor.tabSize": 4,\n    "editor.formatOnSave": true,\n    "editor.defaultFormatter": "esbenp.prettier-vscode",\n    "editor.codeActionsOnSave": {\n        "source.fixAll.eslint": true\n    },\n    "emmet.includeLanguages": {\n        "javascript": "javascriptreact"\n    },\n    "files.associations": {\n        "*.js": "javascript",\n        "*.ts": "typescript"\n    },\n    "workbench.colorTheme": "One Dark Pro",\n    "terminal.integrated.defaultProfile.windows": "PowerShell"\n}\n'
            },
            
            # Markdown
            "markdown": {
                "readme": '# {name}\n\n> Brief description of your project\n\n## Features\n\n- Feature 1\n- Feature 2\n- Feature 3\n\n## Installation\n\n```bash\n# Clone the repository\ngit clone <url>\ncd {name}\n\n# Install dependencies\nnpm install\n# or\npip install -r requirements.txt\n```\n\n## Usage\n\n```bash\n# Start the application\nnpm start\n# or\npython main.py\n```\n\n## Configuration\n\nCreate a `.env` file:\n\n```env\nPORT=3000\nNODE_ENV=development\n```\n\n## Contributing\n\n1. Fork the repository\n2. Create your feature branch (`git checkout -b feature/amazing`)\n3. Commit your changes (`git commit -m "Add amazing feature`)\n4. Push to the branch (`git push origin feature/amazing`)\n5. Open a Pull Request\n\n## License\n\nThis project is licensed under the MIT License.\n',
                "docs": '# {name} Documentation\n\n## Overview\n\nThis document provides detailed information about the {name} module.\n\n## Table of Contents\n\n- [Installation](#installation)\n- [Usage](#usage)\n- [API Reference](#api-reference)\n- [Examples](#examples)\n\n## Installation\n\n```bash\nnpm install {name}\n```\n\n## Usage\n\n```javascript\nconst { name } = require("{name}");\n\n// Example usage\nconst instance = new {name}();\n```\n\n## API Reference\n\n### `constructor()`\n\nCreates a new instance.\n\n### `method(param)`\n\nDescription of the method.\n\n**Parameters:**\n- `param` (type): Description\n\n**Returns:**\n- `type`: Description\n\n## Examples\n\nSee the [examples](./examples) directory for more examples.\n'
            },
            
            # Configuration
            "env": '# Environment Variables\n\n# Server\nPORT=3000\nHOST=localhost\nNODE_ENV=development\n\n# Database\nDB_HOST=localhost\nDB_PORT=5432\nDB_NAME=myapp\nDB_USER=user\nDB_PASSWORD=password\n\n# API Keys\nAPI_KEY=your_api_key_here\nSECRET_KEY=your_secret_key_here\n\n# Logging\nLOG_LEVEL=info\nLOG_FILE=app.log\n',
            "gitignore": '# Dependencies\nnode_modules/\n__pycache__/\n*.pyc\n.env\nvenv/\n\n# Build\ndist/\nbuild/\n*.egg-info/\n\n# IDE\n.vscode/\n.idea/\n*.swp\n*.swo\n\n# OS\n.DS_Store\nThumbs.db\n\n# Logs\n*.log\nlogs/\n\n# Testing\n.coverage\nhtmlcov/\n.pytest_cache/\n',
            "dockerfile": 'FROM node:18-alpine AS builder\n\nWORKDIR /app\n\nCOPY package*.json ./\nRUN npm ci --only=production\n\nCOPY . .\nRUN npm run build\n\nFROM node:18-alpine\n\nWORKDIR /app\n\nCOPY --from=builder /app/dist ./dist\nCOPY --from=builder /app/node_modules ./node_modules\nCOPY package*.json ./\n\nEXPOSE 3000\n\nCMD ["npm", "start"]\n',
            "dockercompose": 'version: "3.8"\n\nservices:\n  app:\n    build: .\n    ports:\n      - "3000:3000"\n    environment:\n      - NODE_ENV=production\n      - DB_HOST=db\n    depends_on:\n      - db\n    restart: unless-stopped\n  \n  db:\n    image: postgres:15-alpine\n    environment:\n      - POSTGRES_DB=myapp\n      - POSTGRES_USER=user\n      - POSTGRES_PASSWORD=password\n    volumes:\n      - postgres_data:/var/lib/postgresql/data\n    ports:\n      - "5432:5432"\n    restart: unless-stopped\n\nvolumes:\n  postgres_data:\n',
            "requirements": 'flask==3.0.0\nrequests==2.31.0\npython-dotenv==1.0.0\npydantic==2.5.0\nuvicorn==0.25.0\nsqlalchemy==2.0.23\naiosqlite==0.19.0\npytest==7.4.3\nblack==23.12.1\nruff==0.1.9\n'
        }
    
    # === CREAR ===
    
    def create_folder(self, path: str) -> Tuple[bool, str]:
        """Crear carpeta/directorio"""
        try:
            folder_name = os.path.basename(path)
            parent = os.path.dirname(path)
            Path(path).mkdir(parents=True, exist_ok=True)
            return True, f"CARPETA CREADA: {folder_name} EN {parent}"
        except Exception as e:
            return False, f"ERROR: {e}"
    
    def create_file(self, path: str, content: str = "") -> Tuple[bool, str]:
        """Crear archivo con contenido opcional"""
        try:
            file_path = Path(path)
            file_path.parent.mkdir(parents=True, exist_ok=True)
            # Backup si existe (IAM)
            if file_path.exists():
                self._backup_file(file_path)
            file_path.write_text(content, encoding='utf-8')
            file_name = os.path.basename(path)
            parent = os.path.dirname(path)
            return True, f"ARCHIVO CREADO: {file_name} EN {parent}"
        except Exception as e:
            return False, f"ERROR: {e}"
    
    def create_file_with_template(self, path: str, template_type: str = "basic", **kwargs) -> Tuple[bool, str]:
        """Crear archivo con template inteligente"""
        try:
            ext = Path(path).suffix.lower().lstrip(".")
            file_name = Path(path).stem
            
            # Detectar tipo de template
            content = ""
            
            if ext in ["py", "python"]:
                templates = self.templates.get("python", {})
                template = templates.get(template_type, templates.get("basic", ""))
                content = template.format(name=file_name, **kwargs)
            elif ext in ["js", "ts", "jsx", "tsx"]:
                templates = self.templates.get("javascript", {})
                template = templates.get(template_type, templates.get("basic", ""))
                content = template.format(name=file_name, **kwargs)
            elif ext in ["html", "htm"]:
                templates = self.templates.get("html", {})
                template = templates.get(template_type, templates.get("basic", ""))
                content = template.format(name=file_name, **kwargs)
            elif ext == "json":
                templates = self.templates.get("json", {})
                template = templates.get(template_type, templates.get("package", ""))
                content = template.format(name=file_name, **kwargs)
            elif ext in ["md", "markdown"]:
                templates = self.templates.get("markdown", {})
                template = templates.get(template_type, templates.get("readme", ""))
                content = template.format(name=file_name, **kwargs)
            elif ext == "env":
                content = self.templates.get("env", "")
            elif ext == "gitignore":
                content = self.templates.get("gitignore", "")
            elif ext in ["dockerfile"]:
                content = self.templates.get("dockerfile", "")
            elif ext in ["yml", "yaml"]:
                content = self.templates.get("dockercompose", "")
            elif ext == "txt":
                content = self.templates.get("requirements", "")
            else:
                content = ""
            
            return self.create_file(path, content)
        except Exception as e:
            return False, f"ERROR: {e}"
    
    def create_project_structure(self, project_path: str, project_type: str = "python", name: str = None) -> Tuple[bool, str]:
        """Crear estructura de proyecto completa"""
        try:
            if not name:
                name = os.path.basename(project_path)
            
            # Crear carpeta principal
            self.create_folder(project_path)
            
            created_files = []
            
            if project_type == "python":
                structure = [
                    ("src", True),
                    ("src/__init__.py", False, ""),
                    (f"src/{name.lower()}.py", False, self.templates["python"]["basic"]),
                    ("tests", True),
                    ("tests/__init__.py", False, ""),
                    (f"tests/test_{name.lower()}.py", False, '# -*- coding: utf-8 -*-\nimport pytest\n\n\ndef test_example():\n    assert True\n'),
                    ("docs", True),
                    ("requirements.txt", False, self.templates["requirements"]),
                    (".gitignore", False, self.templates["gitignore"]),
                    ("README.md", False, self.templates["markdown"]["readme"].format(name=name)),
                    (".env", False, self.templates["env"]),
                    ("main.py", False, self.templates["python"]["basic"]),
                ]
            elif project_type == "javascript":
                structure = [
                    ("src", True),
                    ("src/index.js", False, self.templates["javascript"]["basic"]),
                    ("src/utils", True),
                    ("tests", True),
                    ("tests/index.test.js", False, self.templates["javascript"]["test"]),
                    ("docs", True),
                    ("package.json", False, self.templates["json"]["package"].format(name=name)),
                    ("tsconfig.json", False, self.templates["json"]["tsconfig"]),
                    (".gitignore", False, self.templates["gitignore"]),
                    (".env", False, self.templates["env"]),
                    ("README.md", False, self.templates["markdown"]["readme"].format(name=name)),
                    (".vscode/settings.json", False, self.templates["json"]["vscode"]),
                ]
            elif project_type == "web":
                structure = [
                    ("src", True),
                    ("src/css", True),
                    ("src/css/style.css", False, self.templates["javascript"]["css"].format(name=name)),
                    ("src/js", True),
                    ("src/js/main.js", False, self.templates["javascript"]["basic"]),
                    ("src/images", True),
                    ("docs", True),
                    ("index.html", False, self.templates["html"]["landing"].format(name=name)),
                    (".gitignore", False, self.templates["gitignore"]),
                    ("README.md", False, self.templates["markdown"]["readme"].format(name=name)),
                ]
            elif project_type == "flask":
                structure = [
                    ("app", True),
                    ("app/__init__.py", False, '# -*- coding: utf-8 -*-\nfrom flask import Flask\n\n\ndef create_app():\n    app = Flask(__name__)\n    return app\n'),
                    ("app/routes.py", False, self.templates["python"]["flask"]),
                    ("app/templates", True),
                    ("app/static", True),
                    ("tests", True),
                    ("requirements.txt", False, "flask==3.0.0\npython-dotenv==1.0.0\npytest==7.4.3\n"),
                    ("run.py", False, 'from app import create_app\n\napp = create_app()\n\nif __name__ == "__main__":\n    app.run(debug=True)\n'),
                    (".gitignore", False, self.templates["gitignore"]),
                    (".env", False, self.templates["env"]),
                    ("README.md", False, self.templates["markdown"]["readme"].format(name=name)),
                ]
            elif project_type == "fastapi":
                structure = [
                    ("app", True),
                    ("app/__init__.py", False, ""),
                    ("app/main.py", False, self.templates["python"]["fastapi"]),
                    ("app/models", True),
                    ("app/routes", True),
                    ("app/schemas", True),
                    ("app/services", True),
                    ("tests", True),
                    ("requirements.txt", False, "fastapi==0.104.1\nuvicorn==0.25.0\npydantic==2.5.0\nsqlalchemy==2.0.23\n"),
                    ("Dockerfile", False, self.templates["dockerfile"]),
                    ("docker-compose.yml", False, self.templates["dockercompose"]),
                    (".gitignore", False, self.templates["gitignore"]),
                    (".env", False, self.templates["env"]),
                    ("README.md", False, self.templates["markdown"]["readme"].format(name=name)),
                ]
            else:
                structure = [
                    ("src", True),
                    ("tests", True),
                    ("docs", True),
                    (".gitignore", False, self.templates["gitignore"]),
                    ("README.md", False, self.templates["markdown"]["readme"].format(name=name)),
                ]
            
            # Crear estructura
            for item in structure:
                item_path = os.path.join(project_path, item[0])
                
                if item[1]:  # Es carpeta
                    self.create_folder(item_path)
                else:  # Es archivo
                    content = item[2] if len(item) > 2 else ""
                    success, msg = self.create_file(item_path, content)
                    if success:
                        created_files.append(item[0])
            
            summary = f"PROYECTO CREADO: {name}\nTIPO: {project_type}\nARCHIVOS: {len(created_files)}\n\nESTRUCTURA:\n"
            for item in structure:
                icon = "[DIR]" if item[1] else "    "
                summary += f"  {icon} {item[0]}\n"
            
            return True, summary
        except Exception as e:
            return False, f"ERROR: {e}"
    
    # === LEER ===
    
    def read_file(self, path: str) -> Tuple[bool, str]:
        """Leer contenido de archivo"""
        try:
            content = Path(path).read_text(encoding='utf-8')
            file_name = os.path.basename(path)
            return True, f"LEYENDO: {file_name}\n\n{content}"
        except Exception as e:
            return False, f"ERROR: {e}"
    
    def read_file_lines(self, path: str, start: int = 0, end: int = None) -> Tuple[bool, List[str]]:
        """Leer lineas especificas de un archivo"""
        try:
            lines = Path(path).read_text(encoding='utf-8').splitlines()
            if end:
                lines = lines[start:end]
            else:
                lines = lines[start:]
            file_name = os.path.basename(path)
            return True, [f"LEYENDO: {file_name} (lineas {start}-{end if end else 'fin'})"] + lines
        except Exception as e:
            return False, [f"ERROR: {e}"]
    
    def get_file_info(self, path: str) -> Tuple[bool, Dict[str, Any]]:
        """Obtener informacion detallada del archivo"""
        try:
            p = Path(path)
            stat = p.stat()
            
            ext = p.suffix.lower()
            lang_map = {
                '.py': 'python', '.js': 'javascript', '.ts': 'typescript',
                '.html': 'html', '.css': 'css', '.json': 'json',
                '.md': 'markdown', '.txt': 'text', '.jsx': 'react',
                '.java': 'java', '.go': 'go', '.rs': 'rust', '.c': 'c',
                '.cpp': 'cpp', '.h': 'header', '.php': 'php',
                '.rb': 'ruby', '.sh': 'shell', '.bat': 'batch',
                '.ps1': 'powershell', '.yaml': 'yaml', '.yml': 'yaml',
                '.xml': 'xml', '.sql': 'sql', '.env': 'env',
                '.gitignore': 'git', '.dockerignore': 'docker'
            }
            
            info = {
                'name': p.name,
                'path': str(p.absolute()),
                'extension': ext,
                'language': lang_map.get(ext, 'unknown'),
                'size': stat.st_size,
                'size_str': self._format_size(stat.st_size),
                'created': datetime.fromtimestamp(stat.st_ctime).strftime('%Y-%m-%d %H:%M:%S'),
                'modified': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
                'is_file': p.is_file(),
                'is_dir': p.is_dir(),
                'permissions': oct(stat.st_mode)[-3:]
            }
            
            if p.is_file():
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    info['lines'] = len(f.readlines())
            
            return True, info
        except Exception as e:
            return False, {'error': str(e)}
    
    # === EDITAR ===
    
    def edit_file(self, path: str, old_text: str, new_text: str) -> Tuple[bool, str]:
        """Editar archivo reemplazando texto"""
        try:
            content = Path(path).read_text(encoding='utf-8')
            
            if old_text not in content:
                return False, "TEXTO NO ENCONTRADO"
            
            # Backup antes de editar (IAM)
            self._backup_file(Path(path))
            
            count = content.count(old_text)
            new_content = content.replace(old_text, new_text)
            
            Path(path).write_text(new_content, encoding='utf-8')
            file_name = os.path.basename(path)
            return True, f"EDITANDO: {file_name} ({count} cambios)"
        except Exception as e:
            return False, f"ERROR: {e}"
    
    def append_to_file(self, path: str, content: str) -> Tuple[bool, str]:
        """Agregar contenido al final del archivo"""
        try:
            with open(path, 'a', encoding='utf-8') as f:
                f.write(content)
            file_name = os.path.basename(path)
            return True, f"AGREGANDO A: {file_name}"
        except Exception as e:
            return False, f"ERROR: {e}"
    
    def insert_in_file(self, path: str, line_num: int, content: str) -> Tuple[bool, str]:
        """Insertar contenido en una linea especifica"""
        try:
            lines = Path(path).read_text(encoding='utf-8').splitlines()
            lines.insert(line_num - 1, content)
            Path(path).write_text('\n'.join(lines), encoding='utf-8')
            file_name = os.path.basename(path)
            return True, f"INSERTANDO EN: {file_name} LINEA {line_num}"
        except Exception as e:
            return False, f"ERROR: {e}"
    
    def replace_all_in_file(self, path: str, old: str, new: str) -> Tuple[bool, str]:
        """Reemplazar todas las ocurrencias"""
        try:
            content = Path(path).read_text(encoding='utf-8')
            count = content.count(old)
            
            if count == 0:
                return False, "TEXTO NO ENCONTRADO"
            
            new_content = content.replace(old, new)
            Path(path).write_text(new_content, encoding='utf-8')
            
            file_name = os.path.basename(path)
            return True, f"REEMPLAZANDO EN: {file_name} ({count} cambios)"
        except Exception as e:
            return False, f"ERROR: {e}"
    
    # === MOVER/COPIAR/ELIMINAR ===
    
    def move(self, source: str, destination: str) -> Tuple[bool, str]:
        """Mover archivo o carpeta"""
        try:
            file_name = os.path.basename(source)
            shutil.move(source, destination)
            return True, f"MOVIENDO: {file_name} -> {destination}"
        except Exception as e:
            return False, f"ERROR: {e}"
    
    def copy(self, source: str, destination: str) -> Tuple[bool, str]:
        """Copiar archivo o carpeta"""
        try:
            file_name = os.path.basename(source)
            src = Path(source)
            if src.is_dir():
                shutil.copytree(source, destination)
            else:
                shutil.copy2(source, destination)
            return True, f"Copiando: {file_name} -> {destination}"
        except Exception as e:
            return False, f"ERROR: {e}"
    
    def delete(self, path: str) -> Tuple[bool, str]:
        """Eliminar archivo o carpeta"""
        try:
            file_name = os.path.basename(path)
            p = Path(path)
            if p.is_dir():
                shutil.rmtree(path)
            else:
                p.unlink()
            return True, f"ELIMINADO: {file_name}"
        except Exception as e:
            return False, f"ERROR: {e}"
    
    def rename(self, old_name: str, new_name: str) -> Tuple[bool, str]:
        """Renombrar archivo o carpeta"""
        try:
            old_file = os.path.basename(old_name)
            new_file = os.path.basename(new_name)
            Path(old_name).rename(new_name)
            return True, f"RENOMBRADO: {old_file} -> {new_file}"
        except Exception as e:
            return False, f"[ERROR] Error al renombrar: {e}"
    
    # === BUSCAR ===
    
    def list_directory(self, path: str = ".", show_hidden: bool = False) -> Tuple[bool, List[Dict]]:
        """Listar contenido de directorio"""
        try:
            items = []
            for item in sorted(Path(path).iterdir()):
                if not show_hidden and item.name.startswith('.'):
                    continue
                
                stat = item.stat() if item.is_file() else None
                items.append({
                    'name': item.name,
                    'is_dir': item.is_dir(),
                    'size': stat.st_size if stat else 0,
                    'size_str': self._format_size(stat.st_size) if stat else '-',
                    'modified': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M') if stat else '-'
                })
            
            return True, items
        except Exception as e:
            return False, [{'error': str(e)}]
    
    def search_files(self, pattern: str, path: str = ".") -> Tuple[bool, List[str]]:
        """Buscar archivos por patron (glob)"""
        try:
            matches = glob.glob(os.path.join(path, pattern), recursive=True)
            return True, matches
        except Exception as e:
            return False, [f"[ERROR] Error: {e}"]
    
    def search_in_files(self, text: str, path: str = ".", extension: str = "*") -> Tuple[bool, List[Dict]]:
        """Buscar texto dentro de archivos"""
        try:
            results = []
            pattern = os.path.join(path, f"**/*.{extension}")
            
            for filepath in glob.glob(pattern, recursive=True):
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        for i, line in enumerate(f, 1):
                            if text.lower() in line.lower():
                                results.append({
                                    'file': filepath,
                                    'line': i,
                                    'content': line.strip()[:100]
                                })
                except:
                    continue
            
            return True, results
        except Exception as e:
            return False, [{'error': str(e)}]
    
    def find_files_by_name(self, name: str, path: str = ".") -> Tuple[bool, List[str]]:
        """Buscar archivos por nombre"""
        try:
            results = []
            for root, dirs, files in os.walk(path):
                for file in files:
                    if name.lower() in file.lower():
                        results.append(os.path.join(root, file))
            return True, results
        except Exception as e:
            return False, [f"[ERROR] Error: {e}"]
    
    def find_empty_folders(self, path: str = ".") -> Tuple[bool, List[str]]:
        """Buscar carpetas vacias"""
        try:
            empty = []
            for root, dirs, files in os.walk(path):
                if not dirs and not files:
                    empty.append(root)
            return True, empty
        except Exception as e:
            return False, [f"[ERROR] Error: {e}"]
    
    def find_large_files(self, path: str = ".", min_size_mb: int = 100) -> Tuple[bool, List[Dict]]:
        """Buscar archivos grandes"""
        try:
            large_files = []
            min_size = min_size_mb * 1024 * 1024
            
            for root, dirs, files in os.walk(path):
                for file in files:
                    filepath = os.path.join(root, file)
                    try:
                        size = os.path.getsize(filepath)
                        if size >= min_size:
                            large_files.append({
                                'path': filepath,
                                'size': size,
                                'size_str': self._format_size(size)
                            })
                    except:
                        continue
            
            large_files.sort(key=lambda x: x['size'], reverse=True)
            return True, large_files[:20]
        except Exception as e:
            return False, [f"[ERROR] Error: {e}"]
    
    # === EJECUTAR COMANDOS ===
    
    def run_command(self, command: str, timeout: int = 30) -> Tuple[bool, str]:
        """Ejecutar comando del sistema"""
        try:
            # Usar mbcs (Windows) o cp1252 para caracteres latinos
            try:
                import locale
                system_encoding = locale.getpreferredencoding(False) or 'cp1252'
            except:
                system_encoding = 'cp1252'
            
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                timeout=timeout,
                encoding=system_encoding,
                errors='replace'
            )
            
            output = result.stdout
            if result.stderr:
                output += f"\n[STDERR]\n{result.stderr}"
            
            return True, output if output else "[OK] Comando ejecutado (sin salida)"
        except subprocess.TimeoutExpired:
            return False, "[ERROR] Timeout: El comando tardo demasiado"
        except Exception as e:
            return False, f"[ERROR] Error: {e}"
    
    def run_python(self, code: str) -> Tuple[bool, str]:
        """Ejecutar codigo Python"""
        try:
            result = subprocess.run(
                ['python', '-c', code],
                capture_output=True,
                text=True,
                timeout=30,
                encoding='utf-8',
                errors='replace'
            )
            
            output = result.stdout
            if result.returncode != 0:
                output += f"\n[ERROR]\n{result.stderr}"
            
            return True, output if output else "[OK] Ejecutado"
        except Exception as e:
            return False, f"[ERROR] Error: {e}"
    
    # === COMPARAR ===
    
    def compare_files(self, file1: str, file2: str) -> Tuple[bool, Dict]:
        """Comparar dos archivos"""
        try:
            content1 = Path(file1).read_text(encoding='utf-8', errors='ignore')
            content2 = Path(file2).read_text(encoding='utf-8', errors='ignore')
            
            lines1 = content1.splitlines()
            lines2 = content2.splitlines()
            
            diff_lines = []
            max_lines = max(len(lines1), len(lines2))
            
            for i in range(max_lines):
                l1 = lines1[i] if i < len(lines1) else None
                l2 = lines2[i] if i < len(lines2) else None
                
                if l1 != l2:
                    diff_lines.append({
                        'line': i + 1,
                        'file1': l1,
                        'file2': l2
                    })
            
            return True, {
                'same': len(diff_lines) == 0,
                'total_lines1': len(lines1),
                'total_lines2': len(lines2),
                'differences': len(diff_lines),
                'diff_lines': diff_lines[:20]
            }
        except Exception as e:
            return False, {'error': str(e)}
    
    # === HASH/INTEGRIDAD ===
    
    def get_file_hash(self, path: str, algorithm: str = "md5") -> Tuple[bool, str]:
        """Obtener hash de un archivo"""
        try:
            h = hashlib.new(algorithm)
            with open(path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    h.update(chunk)
            return True, h.hexdigest()
        except Exception as e:
            return False, f"[ERROR] Error: {e}"
    
    # === COMPRIMIR/DESCOMPRIMIR ===
    
    def compress_zip(self, source: str, output: str) -> Tuple[bool, str]:
        """Comprimir en ZIP"""
        try:
            with zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED) as zipf:
                if os.path.isfile(source):
                    zipf.write(source, os.path.basename(source))
                else:
                    for root, dirs, files in os.walk(source):
                        for file in files:
                            filepath = os.path.join(root, file)
                            arcname = os.path.relpath(filepath, os.path.dirname(source))
                            zipf.write(filepath, arcname)
            return True, f"[OK] Comprimido: {output}"
        except Exception as e:
            return False, f"[ERROR] Error: {e}"
    
    def decompress_zip(self, source: str, output: str) -> Tuple[bool, str]:
        """Descomprimir ZIP"""
        try:
            with zipfile.ZipFile(source, 'r') as zipf:
                zipf.extractall(output)
            return True, f"[OK] Descomprimido en: {output}"
        except Exception as e:
            return False, f"[ERROR] Error: {e}"
    
    # === PERMISOS ===
    
    def get_permissions(self, path: str) -> Tuple[bool, Dict]:
        """Obtener permisos de archivo"""
        try:
            stat = os.stat(path)
            return True, {
                'readable': os.access(path, os.R_OK),
                'writable': os.access(path, os.W_OK),
                'executable': os.access(path, os.X_OK),
                'mode': oct(stat.st_mode)[-3:],
                'mode_full': oct(stat.st_mode),
                'owner_uid': stat.st_uid,
                'group_gid': stat.st_gid
            }
        except Exception as e:
            return False, {'error': str(e)}
    
    def set_permissions(self, path: str, mode: int = 0o777) -> Tuple[bool, str]:
        """Establecer permisos de archivo"""
        try:
            os.chmod(path, mode)
            return True, f"[OK] Permisos cambiados a {oct(mode)} en {path}"
        except Exception as e:
            return False, f"[ERROR] Error: {e}"
    
    def get_owner(self, path: str) -> Tuple[bool, str]:
        """Obtener propietario del archivo"""
        try:
            if platform.system() == "Windows":
                import ctypes
                import ctypes.wintypes as wintypes
                
                # GetFileInformationByHandle para Windows
                result = subprocess.run(
                    ['powershell', '-Command', f'(Get-Acl "{path}").Owner'],
                    capture_output=True, text=True, timeout=10
                )
                return True, result.stdout.strip()
            else:
                import pwd
                stat = os.stat(path)
                user = pwd.getpwuid(stat.st_uid).pw_name
                return True, user
        except Exception as e:
            return False, f"[ERROR] Error: {e}"
    
    def set_owner(self, path: str, owner: str) -> Tuple[bool, str]:
        """Cambiar propietario del archivo"""
        try:
            if platform.system() == "Windows":
                subprocess.run(
                    ['powershell', '-Command', f'(Get-Acl "{path}").SetOwner("{owner}")'],
                    capture_output=True, timeout=10
                )
            else:
                subprocess.run(['chown', owner, path], capture_output=True, timeout=10)
            return True, f"[OK] Propietario cambiado a {owner}"
        except Exception as e:
            return False, f"[ERROR] Error: {e}"
    
    # === ENLACES ===
    
    def create_symlink(self, source: str, link: str) -> Tuple[bool, str]:
        """Crear enlace simbolico"""
        try:
            os.symlink(source, link)
            return True, f"[OK] Enlace creado: {link} -> {source}"
        except Exception as e:
            return False, f"[ERROR] Error: {e}"
    
    def create_hardlink(self, source: str, link: str) -> Tuple[bool, str]:
        """Crear enlace duro"""
        try:
            os.link(source, link)
            return True, f"[OK] Enlace duro creado: {link} -> {source}"
        except Exception as e:
            return False, f"[ERROR] Error: {e}"
    
    def readlink(self, path: str) -> Tuple[bool, str]:
        """Leer enlace simbolico"""
        try:
            target = os.readlink(path)
            return True, target
        except Exception as e:
            return False, f"[ERROR] Error: {e}"
    
    def is_symlink(self, path: str) -> bool:
        """Verificar si es enlace simbolico"""
        return os.path.islink(path)
    
    # === MONITOREO DE ARCHIVOS ===
    
    def watch_folder(self, path: str, callback=None) -> Tuple[bool, str]:
        """Monitorear carpeta para cambios (polling simple)"""
        try:
            import hashlib
            snapshots = {}
            
            for root, dirs, files in os.walk(path):
                for file in files:
                    filepath = os.path.join(root, file)
                    try:
                        with open(filepath, 'rb') as f:
                            snapshots[filepath] = hashlib.md5(f.read()).hexdigest()
                    except:
                        pass
            
            return True, f"[OK] Snapshot capturado: {len(snapshots)} archivos en {path}"
        except Exception as e:
            return False, f"[ERROR] Error: {e}"
    
    def get_file_changes(self, path: str, snapshot: dict) -> Tuple[bool, Dict]:
        """Detectar cambios desde snapshot"""
        try:
            changes = {'modified': [], 'created': [], 'deleted': []}
            current = {}
            
            for root, dirs, files in os.walk(path):
                for file in files:
                    filepath = os.path.join(root, file)
                    try:
                        with open(filepath, 'rb') as f:
                            h = hashlib.md5(f.read()).hexdigest()
                        current[filepath] = h
                        
                        if filepath in snapshot:
                            if snapshot[filepath] != h:
                                changes['modified'].append(filepath)
                        else:
                            changes['created'].append(filepath)
                    except:
                        pass
            
            for filepath in snapshot:
                if filepath not in current:
                    changes['deleted'].append(filepath)
            
            return True, changes
        except Exception as e:
            return False, {'error': str(e)}
    
    # === BUSQUEDA AVANZADA ===
    
    def search_by_content(self, text: str, path: str = ".", case_sensitive: bool = False) -> Tuple[bool, List[Dict]]:
        """Buscar archivos que contengan texto"""
        try:
            results = []
            for root, dirs, files in os.walk(path):
                for file in files:
                    filepath = os.path.join(root, file)
                    try:
                        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                            if case_sensitive:
                                matches = content.count(text)
                            else:
                                matches = content.lower().count(text.lower())
                            
                            if matches > 0:
                                results.append({
                                    'file': filepath,
                                    'matches': matches,
                                    'size': self._format_size(os.path.getsize(filepath))
                                })
                    except:
                        pass
            
            return True, results
        except Exception as e:
            return False, [{'error': str(e)}]
    
    def search_by_size(self, min_size: int = 0, max_size: int = None, path: str = ".") -> Tuple[bool, List[Dict]]:
        """Buscar archivos por tamano"""
        try:
            results = []
            for root, dirs, files in os.walk(path):
                for file in files:
                    filepath = os.path.join(root, file)
                    try:
                        size = os.path.getsize(filepath)
                        if size >= min_size and (max_size is None or size <= max_size):
                            results.append({
                                'file': filepath,
                                'size': size,
                                'size_str': self._format_size(size)
                            })
                    except:
                        pass
            
            results.sort(key=lambda x: x['size'], reverse=True)
            return True, results[:50]
        except Exception as e:
            return False, [{'error': str(e)}]
    
    def search_by_date(self, days: int = 7, path: str = ".", newer: bool = True) -> Tuple[bool, List[Dict]]:
        """Buscar archivos por fecha"""
        try:
            import time
            cutoff = time.time() - (days * 86400)
            results = []
            
            for root, dirs, files in os.walk(path):
                for file in files:
                    filepath = os.path.join(root, file)
                    try:
                        mtime = os.path.getmtime(filepath)
                        if (newer and mtime > cutoff) or (not newer and mtime < cutoff):
                            results.append({
                                'file': filepath,
                                'modified': datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M'),
                                'size': self._format_size(os.path.getsize(filepath))
                            })
                    except:
                        pass
            
            return True, results[:50]
        except Exception as e:
            return False, [{'error': str(e)}]
    
    def search_by_extension(self, extensions: List[str], path: str = ".") -> Tuple[bool, List[str]]:
        """Buscar archivos por extension"""
        try:
            results = []
            for ext in extensions:
                for root, dirs, files in os.walk(path):
                    for file in files:
                        if file.endswith(f'.{ext}'):
                            results.append(os.path.join(root, file))
            return True, results
        except Exception as e:
            return False, [f"[ERROR] Error: {e}"]
    
    # === BACKUP ===
    
    def create_backup(self, source: str, backup_dir: str) -> Tuple[bool, str]:
        """Crear backup con timestamp"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            folder_name = os.path.basename(source)
            backup_name = f"{folder_name}_{timestamp}"
            backup_path = os.path.join(backup_dir, backup_name)
            
            shutil.copytree(source, backup_path)
            return True, f"[OK] Backup creado: {backup_path}"
        except Exception as e:
            return False, f"[ERROR] Error: {e}"
    
    def restore_backup(self, backup_path: str, restore_path: str) -> Tuple[bool, str]:
        """Restaurar backup"""
        try:
            shutil.copytree(backup_path, restore_path)
            return True, f"[OK] Backup restaurado en: {restore_path}"
        except Exception as e:
            return False, f"[ERROR] Error: {e}"
    
    # === UTILIDADES AVANZADAS ===
    
    def get_disk_usage(self, path: str = ".") -> Tuple[bool, Dict]:
        """Obtener uso de disco"""
        try:
            usage = shutil.disk_usage(path)
            return True, {
                'total': self._format_size(usage.total),
                'used': self._format_size(usage.used),
                'free': self._format_size(usage.free),
                'percent': round((usage.used / usage.total) * 100, 1)
            }
        except Exception as e:
            return False, {'error': str(e)}
    
    def get_directory_size(self, path: str) -> Tuple[bool, str]:
        """Obtener tamano total de un directorio"""
        try:
            total = 0
            for dirpath, dirnames, filenames in os.walk(path):
                for f in filenames:
                    fp = os.path.join(dirpath, f)
                    total += os.path.getsize(fp)
            return True, self._format_size(total)
        except Exception as e:
            return False, f"[ERROR] Error: {e}"
    
    def get_recent_files(self, path: str = ".", count: int = 10) -> Tuple[bool, List[Dict]]:
        """Obtener archivos mas recientes"""
        try:
            files = []
            for item in Path(path).rglob('*'):
                if item.is_file():
                    stat = item.stat()
                    files.append({
                        'name': item.name,
                        'path': str(item),
                        'modified': datetime.fromtimestamp(stat.st_mtime),
                        'size': self._format_size(stat.st_size)
                    })
            
            files.sort(key=lambda x: x['modified'], reverse=True)
            
            for f in files[:count]:
                f['modified'] = f['modified'].strftime('%Y-%m-%d %H:%M:%S')
            
            return True, files[:count]
        except Exception as e:
            return False, [{'error': str(e)}]
    
    def get_folder_tree(self, path: str, max_depth: int = 3) -> Tuple[bool, str]:
        """Obtener arbol de carpetas"""
        try:
            tree = []
            self._build_tree(path, tree, "", max_depth, 0)
            return True, '\n'.join(tree)
        except Exception as e:
            return False, f"[ERROR] Error: {e}"
    
    def _build_tree(self, path: str, tree: list, prefix: str, max_depth: int, current_depth: int):
        """Construir arbol recursivamente"""
        if current_depth >= max_depth:
            return
        
        try:
            items = sorted(Path(path).iterdir())
            dirs = [i for i in items if i.is_dir()]
            files = [i for i in items if i.is_file()]
            
            for i, d in enumerate(dirs):
                is_last = i == len(dirs) - 1 and not files
                connector = "+-- " if is_last else "|-- "
                tree.append(f"{prefix}{connector}{d.name}/")
                new_prefix = prefix + ("    " if is_last else "|   ")
                self._build_tree(str(d), tree, new_prefix, max_depth, current_depth + 1)
            
            for i, f in enumerate(files):
                is_last = i == len(files) - 1
                connector = "+-- " if is_last else "|-- "
                tree.append(f"{prefix}{connector}{f.name}")
        except:
            pass
    
    def _format_size(self, size: int) -> str:
        """Formatear tamano a legible"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024:
                return f"{size:.1f}{unit}"
            size /= 1024
        return f"{size:.1f}PB"


# Instancia global
filesystem = FileSystem()
