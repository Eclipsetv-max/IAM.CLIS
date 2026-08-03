# -*- coding: utf-8 -*-
"""
IAM Training Data Collector
Recolecta y genera datos de entrenamiento para fine-tuning
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import List, Dict


class TrainingDataCollector:
    """Recolecta datos de entrenamiento desde múltiples fuentes"""

    def __init__(self, output_dir: str = None):
        if output_dir is None:
            output_dir = Path(__file__).parent / "data"
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.examples: List[Dict] = []

    def add_example(self, system: str, user: str, assistant: str, mode: str = "general"):
        """Agregar un ejemplo de entrenamiento"""
        self.examples.append({
            "system": system,
            "user": user,
            "assistant": assistant,
            "mode": mode,
            "timestamp": datetime.now().isoformat(),
        })

    def collect_from_sessions(self, sessions_dir: str = None):
        """Recolectar conversaciones desde sesiones guardadas"""
        if sessions_dir is None:
            sessions_dir = Path(__file__).parent.parent / "data" / "sessions"
        
        sessions_dir = Path(sessions_dir)
        if not sessions_dir.exists():
            print(f"[INFO] Directorio de sesiones no encontrado: {sessions_dir}")
            return

        count = 0
        for session_file in sessions_dir.glob("*.json"):
            try:
                with open(session_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                
                messages = data.get("messages", [])
                mode = data.get("metadata", {}).get("mode", "general")
                
                # Convertir pares de mensajes user/assistant
                for i in range(len(messages) - 1):
                    if messages[i]["role"] == "user" and messages[i+1]["role"] == "assistant":
                        self.add_example(
                            system=self._get_system_prompt(mode),
                            user=messages[i]["content"],
                            assistant=messages[i+1]["content"],
                            mode=mode,
                        )
                        count += 1
            except Exception as e:
                continue
        
        print(f"[OK] Recolectadas {count} conversaciones desde sesiones")

    def collect_from_prompts(self):
        """Generar datos desde los system prompts de cada modo"""
        # Agregar directorio raíz al path
        import sys
        root_dir = Path(__file__).parent.parent.parent
        if str(root_dir) not in sys.path:
            sys.path.insert(0, str(root_dir))
        
        from iam.config.prompts import AGENT_PROMPTS
        
        # Ejemplos sintéticos por modo
        synthetic_data = {
            "general": [
                {
                    "user": "Que hora es?",
                    "assistant": "La hora actual es {time}. Puedes ver mas informacion del sistema con /status.",
                },
                {
                    "user": "Crea un archivo hello.py que imprima hola mundo",
                    "assistant": '[TOOL_CALL] action: create_file name: "hello.py"\n# -*- coding: utf-8 -*-\n"""Hello World"""\n\ndef main():\n    print("Hola mundo!")\n\n\nif __name__ == "__main__":\n    main()\n[/TOOL_CALL]\n\nArchivo creado: hello.py. Ejecutalo con: python hello.py',
                },
                {
                    "user": "Analiza mi codigo de main.py",
                    "assistant": "[TOOL_CALL] action: read_file path: main.py [/TOOL_CALL]\n\nHe leido tu archivo. Aqui va mi analisis...",
                },
                {
                    "user": "Que archivos hay en mi escritorio?",
                    "assistant": "[TOOL_CALL] action: execute command: dir /b %USERPROFILE%\\Desktop [/TOOL_CALL]\n\nEstos son los archivos en tu escritorio:",
                },
                {
                    "user": "Instala flask",
                    "assistant": "[TOOL_CALL] action: execute command: pip install flask [/TOOL_CALL]\n\nFlask ha sido instalado correctamente.",
                },
            ],
            "builder": [
                {
                    "user": "Hazme una web de camiones con navbar, hero, cards y footer",
                    "assistant": '[TOOL_CALL] action: create_file name: "index.html"\n<!DOCTYPE html>\n<html lang="es">\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>Mi Web de Camiones</title>\n    <link rel="stylesheet" href="style.css">\n</head>\n<body>\n    <nav class="navbar">...</nav>\n    <section class="hero">...</section>\n    <section class="cards">...</section>\n    <footer>...</footer>\n    <script src="script.js"></script>\n</body>\n</html>\n[/TOOL_CALL]\n\n[TOOL_CALL] action: create_file name: "style.css"\n:root {\n    --primary: #3b82f6;\n    --bg: #0f172a;\n}\n* { margin: 0; padding: 0; box-sizing: border-box; }\nbody { background: var(--bg); color: white; }\n[/TOOL_CALL]\n\n[TOOL_CALL] action: create_file name: "script.js"\ndocument.addEventListener("DOMContentLoaded", () => {\n    console.log("Web de camiones lista!");\n});\n[/TOOL_CALL]\n\nCree 3 archivos: index.html, style.css y script.js.',
                },
                {
                    "user": "Crea un dashboard con sidebar y charts",
                    "assistant": "[TOOL_CALL] action: create_file name: \"index.html\"\n<!DOCTYPE html>...\n[/TOOL_CALL]\n\n[TOOL_CALL] action: create_file name: \"style.css\"\n...\n[/TOOL_CALL]\n\n[TOOL_CALL] action: create_file name: \"dashboard.js\"\n...\n[/TOOL_CALL]",
                },
            ],
            "debug": [
                {
                    "user": "Mi funcion no funciona, me da error de indentacion",
                    "assistant": "[TOOL_CALL] action: read_file path: main.py [/TOOL_CALL]\n\nEncontre el error: hay un problema de indentacion en la linea 15. La solucion es...",
                },
                {
                    "user": "Tengo un bug en mi API, no retorna los datos",
                    "assistant": "[TOOL_CALL] action: read_file path: api.py [/TOOL_CALL]\n\nEl problema esta en la consulta a la base de datos. La linea 42 tiene...",
                },
            ],
            "security": [
                {
                    "user": "Revisa mi codigo por vulnerabilidades",
                    "assistant": "[TOOL_CALL] action: read_file path: app.py [/TOOL_CALL]\n\nHe encontrado las siguientes vulnerabilidades:\n1. XSS en la linea 23...\n2. SQL Injection en la linea 45...",
                },
            ],
            "reader": [
                {
                    "user": "Lee y explica este archivo",
                    "assistant": "[TOOL_CALL] action: read_file path: README.md [/TOOL_CALL]\n\nEl archivo contiene...",
                },
            ],
        }

        count = 0
        for mode, examples in synthetic_data.items():
            system_prompt = self._get_system_prompt(mode)
            for ex in examples:
                self.add_example(
                    system=system_prompt,
                    user=ex["user"],
                    assistant=ex["assistant"],
                    mode=mode,
                )
                count += 1
        
        print(f"[OK] Generados {count} ejemplos sinteticos desde prompts")

    def collect_code_examples(self):
        """Generar ejemplos de creacion de codigo"""
        # Agregar directorio raíz al path
        import sys
        root_dir = Path(__file__).parent.parent.parent
        if str(root_dir) not in sys.path:
            sys.path.insert(0, str(root_dir))
        
        code_examples = [
            {
                "user": "Crea un script de Python para convertir CSV a JSON",
                "assistant": '[TOOL_CALL] action: create_file name: "csv_to_json.py"\n# -*- coding: utf-8 -*-\n"""Convertidor CSV a JSON"""\n\nimport csv\nimport json\nimport sys\n\n\ndef csv_to_json(csv_path, json_path=None):\n    """Convertir archivo CSV a JSON"""\n    if json_path is None:\n        json_path = csv_path.replace(".csv", ".json")\n    \n    data = []\n    with open(csv_path, "r", encoding="utf-8") as f:\n        reader = csv.DictReader(f)\n        for row in reader:\n            data.append(row)\n    \n    with open(json_path, "w", encoding="utf-8") as f:\n        json.dump(data, f, indent=2, ensure_ascii=False)\n    \n    print(f"Convertido: {csv_path} -> {json_path}")\n    print(f"Registros: {len(data)}")\n    return data\n\n\nif __name__ == "__main__":\n    if len(sys.argv) < 2:\n        print("Uso: python csv_to_json.py archivo.csv [salida.json]")\n        sys.exit(1)\n    \n    csv_to_json(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)\n[/TOOL_CALL]',
            },
            {
                "user": "Hazme un scraper basico de paginas web",
                "assistant": '[TOOL_CALL] action: create_file name: "scraper.py"\n# -*- coding: utf-8 -*-\n"""Scraper basico de paginas web"""\n\nimport requests\nfrom html.parser import HTMLParser\n\n\nclass TitleExtractor(HTMLParser):\n    def __init__(self):\n        super().__init__()\n        self.in_title = False\n        self.title = ""\n    \n    def handle_starttag(self, tag, attrs):\n        if tag == "title":\n            self.in_title = True\n    \n    def handle_data(self, data):\n        if self.in_title:\n            self.title += data\n    \n    def handle_endtag(self, tag):\n        if tag == "title":\n            self.in_title = False\n\n\ndef scrape(url):\n    """Scrapear titulo de una pagina"""\n    response = requests.get(url, timeout=10)\n    parser = TitleExtractor()\n    parser.feed(response.text)\n    return {"url": url, "title": parser.title, "status": response.status_code}\n\n\nif __name__ == "__main__":\n    import sys\n    if len(sys.argv) < 2:\n        print("Uso: python scraper.py <url>")\n        sys.exit(1)\n    \n    result = scrape(sys.argv[1])\n    print(f"URL: {result[\'url\']}")\n    print(f"Titulo: {result[\'title\']}")\n    print(f"Status: {result[\'status\']}")\n[/TOOL_CALL]',
            },
            {
                "user": "Crea una calculadora web con HTML, CSS y JS",
                "assistant": '[TOOL_CALL] action: create_file name: "index.html"\n<!DOCTYPE html>\n<html lang="es">\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>Calculadora</title>\n    <link rel="stylesheet" href="style.css">\n</head>\n<body>\n    <div class="calculator">\n        <input type="text" id="display" readonly>\n        <div class="buttons">\n            <button onclick="clearDisplay()">C</button>\n            <button onclick="appendToDisplay(\'(\')">(</button>\n            <button onclick="appendToDisplay(\')\')")>)</button>\n            <button onclick="deleteLast()">DEL</button>\n            <button onclick="appendToDisplay(\'7\')">7</button>\n            <button onclick="appendToDisplay(\'8\')">8</button>\n            <button onclick="appendToDisplay(\'9\')">9</button>\n            <button onclick="appendToDisplay(\'/\')">/</button>\n            <button onclick="appendToDisplay(\'4\')">4</button>\n            <button onclick="appendToDisplay(\'5\')">5</button>\n            <button onclick="appendToDisplay(\'6\')">6</button>\n            <button onclick="appendToDisplay(\'*\')">*</button>\n            <button onclick="appendToDisplay(\'1\')">1</button>\n            <button onclick="appendToDisplay(\'2\')">2</button>\n            <button onclick="appendToDisplay(\'3\')">3</button>\n            <button onclick="appendToDisplay(\'-\')">-</button>\n            <button onclick="appendToDisplay(\'0\')">0</button>\n            <button onclick="appendToDisplay(\'.\')">.</button>\n            <button onclick="calculate()" class="equals">=</button>\n            <button onclick="appendToDisplay(\'+\')">+</button>\n        </div>\n    </div>\n    <script src="script.js"></script>\n</body>\n</html>\n[/TOOL_CALL]',
            },
        ]

        from iam.config.prompts import AGENT_PROMPTS
        system_prompt = AGENT_PROMPTS["builder"]["system"]
        
        for ex in code_examples:
            self.add_example(
                system=system_prompt,
                user=ex["user"],
                assistant=ex["assistant"],
                mode="builder",
            )
        
        print(f"[OK] Generados {len(code_examples)} ejemplos de codigo")

    def _get_system_prompt(self, mode: str) -> str:
        """Obtener system prompt para un modo"""
        try:
            import sys
            root_dir = Path(__file__).parent.parent.parent
            if str(root_dir) not in sys.path:
                sys.path.insert(0, str(root_dir))
            
            from iam.config.prompts import AGENT_PROMPTS
            return AGENT_PROMPTS.get(mode, AGENT_PROMPTS["general"])["system"]
        except:
            return "Tu eres IAM, un asistente de IA."

    def save(self, filename: str = "training_data.jsonl"):
        """Guarda los datos en formato JSONL para fine-tuning"""
        filepath = self.output_dir / filename
        
        with open(filepath, "w", encoding="utf-8") as f:
            for ex in self.examples:
                # Formato chat para fine-tuning
                conversation = {
                    "messages": [
                        {"role": "system", "content": ex["system"]},
                        {"role": "user", "content": ex["user"]},
                        {"role": "assistant", "content": ex["assistant"]},
                    ],
                    "mode": ex["mode"],
                }
                f.write(json.dumps(conversation, ensure_ascii=False) + "\n")
        
        print(f"[OK] Guardados {len(self.examples)} ejemplos en {filepath}")
        return str(filepath)

    def get_stats(self):
        """Obtener estadisticas de los datos"""
        modes = {}
        for ex in self.examples:
            mode = ex["mode"]
            modes[mode] = modes.get(mode, 0) + 1
        
        total_chars = sum(len(ex["user"]) + len(ex["assistant"]) for ex in self.examples)
        
        return {
            "total_examples": len(self.examples),
            "by_mode": modes,
            "total_chars": total_chars,
            "avg_chars_per_example": total_chars // max(len(self.examples), 1),
        }


def collect_all():
    """Recolectar todos los datos disponibles"""
    collector = TrainingDataCollector()
    
    print("=" * 60)
    print("IAM Training Data Collector")
    print("=" * 60)
    
    # 1. Desde sesiones guardadas
    print("\n[1/4] Recolectando desde sesiones...")
    collector.collect_from_sessions()
    
    # 2. Desde prompts
    print("\n[2/4] Generando desde prompts de modos...")
    collector.collect_from_prompts()
    
    # 3. Ejemplos de codigo
    print("\n[3/4] Generando ejemplos de codigo...")
    collector.collect_code_examples()
    
    # 4. Guardar
    print("\n[4/4] Guardando datos...")
    filepath = collector.save()
    
    # Estadisticas
    stats = collector.get_stats()
    print("\n" + "=" * 60)
    print("ESTADISTICAS:")
    print(f"  Total ejemplos: {stats['total_examples']}")
    print(f"  Por modo: {stats['by_mode']}")
    print(f"  Total caracteres: {stats['total_chars']:,}")
    print(f"  Promedio por ejemplo: {stats['avg_chars_per_example']:,}")
    print("=" * 60)
    
    return filepath


if __name__ == "__main__":
    collect_all()
