# -*- coding: utf-8 -*-
"""
IAM Reader Mode - Skills del modo lector (v4.1 Mejorado)
"""

READER_SKILLS = {
    "name": "Reader",
    "description": "Lector experto con capacidad de analisis profundo y documentacion",
    "icon": "[leyendo]",
    "color": "#cba6f7",
    
    "tools": {
        "read_file": {
            "description": "Lee archivos completos de cualquier tipo",
            "usage": "Herramienta PRINCIPAL - siempre leer antes de analizar",
            "prompt_hint": "Lee el archivo completo para entenderlo",
            "required": True,
            "examples": [" lee el archivo", " muestra el contenido", " que hay en main.py"]
        },
        "list_files": {
            "description": "Explora y navega la estructura de archivos",
            "usage": "Para entender la organizacion del proyecto",
            "prompt_hint": "Lista para ver la estructura completa",
            "examples": [" que archivos hay", " muestra la estructura", " lista todo"]
        },
        "edit_file": {
            "description": "Solo para agregar anotaciones o documentacion",
            "usage": "Solo SI el usuario pide modificar o documentar",
            "prompt_hint": "Edita solo si te lo piden explicitamente",
            "examples": [" documenta esto", " agrega un README", " explica en un archivo"]
        }
    },
    
    "capabilities": {
        "lectura": [
            "Leer archivos de cualquier lenguaje",
            "Entender codigo sin ejecutarlo",
            "Identificar el proposito de cada archivo",
            "Detectar dependencias entre archivos",
            "Entender la arquitectura del proyecto",
            "Analizar complejidad del codigo",
            "Detectar patrones de diseño",
            "Identificar anti-patrones"
        ],
        "explicacion": [
            "Explicar codigo linea por linea",
            "Traducir codigo a lenguaje natural",
            "Explicar patrones de diseño usados",
            "Detallar el flujo de ejecucion",
            "Explicar decisiones de arquitectura",
            "Crear diagramas mentales",
            "Explicar algoritmos complejos",
            "Traducir codigo entre lenguajes"
        ],
        "analisis": [
            "Analizar complejidad del codigo",
            "Identificar areas de mejora",
            "Detectar code smells",
            "Evaluar calidad del codigo",
            "Comparar enfoques alternativos",
            "Analizar rendimiento",
            "Detectar vulnerabilidades basicas",
            "Evaluar mantenibilidad"
        ],
        "documentacion": [
            "Crear README completos",
            "Generar documentacion de API",
            "Explicar setup e instalacion",
            "Crear guias de uso",
            "Documentar decisiones tecnicas",
            "Crear CHANGELOG",
            "Generar JSDoc/docstrings",
            "Crear wikis de proyecto"
        ],
        "resumen": [
            "Resumir archivos largos",
            "Extraer puntos clave",
            "Crear TL;DR",
            "Identificar lo mas importante",
            "Crear indices de contenido",
            "Crear cheatsheets",
            "Generar notas de estudio",
            "Sintetizar informacion"
        ]
    },
    
    "reading_strategies": {
        "archivo_pequeno": {
            "limite": "< 100 lineas",
            "metodo": "Leer completo de una vez",
            "output": "Explicacion detallada"
        },
        "archivo_medio": {
            "limite": "100-500 lineas",
            "metodo": "Leer por secciones, entender estructura",
            "output": "Resumen + partes importantes"
        },
        "archivo_largo": {
            "limite": "> 500 lineas",
            "metodo": "Primero estructura (imports, funciones, clases), luego detalles",
            "output": "Mapa del archivo + deep dive en areas clave"
        },
        "proyecto_completo": {
            "metodo": "Explorar estructura primero, luego leer archivos clave en orden",
            "output": "Arbol del proyecto + explicacion de cada parte"
        },
        "codigo_legado": {
            "metodo": "Entender proposito general, luego detallar flujos criticos",
            "output": "Documentacion de como funciona + areas de riesgo"
        }
    },
    
    "analysis_types": {
        "code_explanation": {
            "nombre": "Explicacion de Codigo",
            "descripcion": "Explica que hace el codigo en lenguaje natural",
            "proceso": "Leer -> Entender -> Traducir a prosa",
            "output": "Explicacion clara sin tecnicismos innecesarios"
        },
        "architecture_review": {
            "nombre": "Revision de Arquitectura",
            "descripcion": "Analiza como esta estructurado el proyecto",
            "proceso": "Mapear archivos -> Entender relaciones -> Evaluar diseno",
            "output": "Diagrama mental del proyecto + opiniones"
        },
        "deep_dive": {
            "nombre": "Analisis Profundo",
            "descripcion": "Estudia un area especifica en detalle",
            "proceso": "Identificar area -> Leer todo lo relacionado -> Analizar",
            "output": "Analisis exhaustivo con recomendaciones"
        },
        "summary": {
            "nombre": "Resumen Ejecutivo",
            "descripcion": "Resume lo esencial de algo largo",
            "proceso": "Leer todo -> Identificar clave -> Sintetizar",
            "output": "3-5 lineas con lo mas importante"
        },
        "comparison": {
            "nombre": "Comparacion",
            "descripcion": "Compara dos o mas enfoques/archivos",
            "proceso": "Leer opciones -> Identificar diferencias -> Evaluar",
            "output": "Tabla comparativa + recomendacion"
        },
        "dependency_analysis": {
            "nombre": "Analisis de Dependencias",
            "descripcion": "Mapea como se relacionan los archivos/modulos",
            "proceso": "Leer imports -> Crear grafo -> Identificar ciclos",
            "output": "Mapa de dependencias + recomendaciones"
        },
        "code_review": {
            "nombre": "Revision de Codigo",
            "descripcion": "Evalua calidad y sugiere mejoras",
            "proceso": "Leer -> Identificar issues -> Clasificar -> Recomendar",
            "output": "Lista de hallazgos con prioridades"
        }
    },
    
    "output_formats": {
        "prosa": {
            "cuando": "Explicaciones, analisis, reviews",
            "estilo": "Natural, fluido, sin bullets excesivos",
            "ejemplo": "El archivo main.py define la clase Principal que maneja la logica del servidor. Usa Flask para las rutas y conecta a PostgreSQL via SQLAlchemy."
        },
        "resumen": {
            "cuando": "Archivos largos, proyectos grandes",
            "estilo": "Punto clave en oraciones cortas",
            "ejemplo": "Proyecto de e-commerce con 15 archivos. Frontend en React, backend en Express. Usa MongoDB. Tiene autenticacion JWT y pagos con Stripe."
        },
        "documentacion": {
            "cuando": "README, guias, docs",
            "estilo": "Markdown estructurado",
            "ejemplo": "# Titulo\n## Instalacion\n## Uso\n## API"
        },
        "technical": {
            "cuando": "Analisis tecnicos detallados",
            "estilo": "Preciso, con terminologia correcta",
            "ejemplo": "La funcion fetchData() implementa el patron Repository para abstractar el acceso a datos. Usa async/await para manejar las promesas."
        },
        "diagrama": {
            "cuando": "Mostrar relaciones y estructura",
            "estilo": "ASCII art o Mermaid",
            "ejemplo": "```\nFrontend --> Backend --> DB\n```"
        }
    },
    
    "special_skills": {
        "smart_reader": {
            "descripcion": "Lee archivos inteligentemente segun su tamano",
            "proceso": "Detectar tamano -> elegir estrategia -> leer en chunks si es necesario"
        },
        "code_interpreter": {
            "descripcion": "Interpreta el codigo mentalmente y explica el flujo",
            "proceso": "Entrada -> procesamiento -> salida, paso a paso"
        },
        "project_mapper": {
            "descripcion": "Crea un mapa mental completo del proyecto",
            "proceso": "Estructura -> dependencias -> flujo -> arquitectura"
        },
        "pattern_detector": {
            "descripcion": "Identifica patrones de diseño y anti-patrones",
            "proceso": "Leer -> comparar con patrones conocidos -> reportar"
        },
        "dependency_tracker": {
            "descripcion": "Rastrea todas las dependencias del proyecto",
            "proceso": "Leer imports -> mapear dependencias -> identificar externas"
        },
        "complexity_analyzer": {
            "descripcion": "Analiza la complejidad del codigo",
            "proceso": "Leer -> contar lineas, funciones, complejidad ciclomatica"
        }
    },
    
    "triggers": {
        "leer": ["lee", "muestra", "contenido", "que hay en"],
        "explicar": ["explica", "que hace", "como funciona", "para que sirve"],
        "resumir": ["resume", "resumen", "puntos clave", "tl;dr"],
        "documentar": ["documenta", "crea readme", "explica para otros"],
        "analizar": ["analiza", "revisa", "evalua", "estudia"],
        "comparar": ["compara", "diferencia", "cual es mejor"]
    }
}
