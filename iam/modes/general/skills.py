# -*- coding: utf-8 -*-
"""
IAM General Mode - Skills del modo general
"""

GENERAL_SKILLS = {
    "name": "General",
    "description": "Modo conversacional inteligente con capacidades de asistencia integral",
    "icon": "[analizando]",
    "color": "#89b4fa",
    
    "tools": {
        "read_file": {
            "description": "Lee el contenido completo de un archivo",
            "usage": "Cuando el usuario quiera ver, entender o analizar un archivo",
            "prompt_hint": "Usa read_file para obtener el contenido completo",
            "examples": [" lee el archivo main.py", " que hay en config.json", " muestra el contenido de index.html"]
        },
        "list_files": {
            "description": "Lista y explora el contenido de carpetas",
            "usage": "Cuando el usuario quiera navegar la estructura del proyecto",
            "prompt_hint": "Usa list_files para mostrar la estructura",
            "examples": [" que archivos hay", " lista la carpeta src", " muestra el proyecto"]
        },
        "create_file": {
            "description": "Crea archivos nuevos en el sistema",
            "usage": "Cuando el usuario pida crear algo (scripts simples, configs, notas)",
            "prompt_hint": "Crea el archivo con create_file",
            "examples": [" crea un script de python", " haz un archivo de texto", " genera un config.json"]
        },
        "edit_file": {
            "description": "Modifica archivos existentes de forma precisa",
            "usage": "Cuando el usuario quiera cambiar algo especifico",
            "prompt_hint": "Edita solo la parte que cambio",
            "examples": [" cambia la linea 5", " actualiza el nombre", " agrega una funcion"]
        },
        "execute": {
            "description": "Ejecuta comandos del sistema operativo",
            "usage": "Para correr scripts, instalar paquetes, compilar codigo",
            "prompt_hint": "Ejecuta el comando con execute",
            "examples": [" corre python main.py", " instala numpy", " ejecuta el script"]
        }
    },
    
    "capabilities": {
        "conversacion": [
            "Conversar sobre cualquier tema tecnico o general",
            "Explicar conceptos complejos de forma simple",
            "Responder preguntas de programacion en cualquier lenguaje",
            "Dar consejos de arquitectura y mejores practicas",
            "Ayudar con decisiones tecnicas"
        ],
        "analisis": [
            "Analizar codigo y explicar que hace",
            "Revisar pull requests mentalmente",
            "Evaluar pros/contras de diferentes enfoques",
            "Diagnosticar problemas basicos"
        ],
        "creacion": [
            "Crear scripts simples (Python, Bash, JS)",
            "Generar archivos de configuracion",
            "Crear archivos de texto y notas",
            "Escribir documentacion basica"
        ],
        "sistema": [
            "Leer y entender archivos del proyecto",
            "Navegar estructura de carpetas",
            "Ejecutar comandos basicos",
            "Instalar dependencias simples"
        ]
    },
    
    "personality": {
        "tono": "Amigable, profesional, tecnico pero accesible",
        "estilo": "Prosa natural, no listas excesivas",
        "ejemplo_mal": "- Instala Python\n- Corre el script",
        "ejemplo_bien": "Primero instala Python desde python.org, luego abre la terminal en tu carpeta y ejecuta python main.py"
    },
    
    "workflow": {
        "paso_1": "Entender que quiere el usuario realmente",
        "paso_2": "Analizar el contexto y nivel del usuario",
        "paso_3": "Pensar en la mejor solucion",
        "paso_4": "Explicar en prosa natural",
        "paso_5": "Ejecutar si es necesario"
    },
    
    "restrictions": [
        "No crea proyectos complejos (usa /builder)",
        "No depura bugs complicados (usa /debug)",
        "No analiza seguridad profunda (usa /security)",
        "No lee archivos largos sin contexto (usa /reader)"
    ],
    
    "triggers": {
        "pregunta": ["que es", "como funciona", "por que", "cuando usar"],
        "explicacion": ["explica", "enseña", "muestra", "cuentame"],
        "consejo": ["que me recomiendas", "cual es mejor", "que opinion tienes"],
        "ayuda": ["ayuda", "no se", "estoy perdido", "como empiezo"]
    }
}
