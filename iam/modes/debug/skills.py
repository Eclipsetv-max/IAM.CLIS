# -*- coding: utf-8 -*-
"""
IAM Debug Mode - Skills del modo depuracion (v4.1 Mejorado)
"""

DEBUG_SKILLS = {
    "name": "Debug",
    "description": "Detective de errores con analisis profundo y metodos cientificos",
    "icon": "[depurando]",
    "color": "#f38ba8",
    
    "tools": {
        "read_file": {
            "description": "Lee codigo completo para entender el problema",
            "usage": "SIEMPRE primero - no puedes arreglar lo que no entiendes",
            "prompt_hint": "Lee el archivo para analizar el error",
            "required": True,
            "examples": [" lee el archivo con error", " muestra el codigo", " que hay en main.py"]
        },
        "edit_file": {
            "description": "Aplica la correccion exacta al bug",
            "usage": "Solo DESPUES de entender la causa raiz",
            "prompt_hint": "Edita la linea o funcion especifica",
            "examples": [" arregla la linea 42", " corrige la funcion login", " modifica el condicional"]
        },
        "execute": {
            "description": "Ejecuta el codigo para probar el fix",
            "usage": "Verificar que el arreglo funciona",
            "prompt_hint": "Ejecuta para confirmar que se arreglo",
            "examples": [" corre el script", " ejecuta los tests", " prueba el fix"]
        },
        "list_files": {
            "description": "Busca archivos relacionados al problema",
            "usage": "Cuando el bug puede estar en dependencias",
            "prompt_hint": "Explora archivos para encontrar mas contexto",
            "examples": [" que archivos usa este modulo", " busca imports", " muestra dependencias"]
        }
    },
    
    "capabilities": {
        "diagnostico": [
            "Analizar mensajes de error completos",
            "Identificar el tipo de error (sintaxis, logico, runtime)",
            "Encontrar la causa raiz, no solo el sintoma",
            "Rastrear el flujo de ejecucion",
            "Entender el estado del programa en el error",
            "Detectar race conditions",
            "Identificar memory leaks",
            "Analizar stack traces completas"
        ],
        "correccion": [
            "Corregir errores de sintaxis (Python, JS, HTML, CSS)",
            "Arreglar bugs logicos en funciones",
            "Resolver errores de tipos y null/undefined",
            "Corregir imports y dependencias",
            "Arreglar errores de asincronia (promises, async/await)",
            "Corregir memory leaks",
            "Resolver problemas de scope y closures",
            "Arreglar errores de TypeScript",
            "Corregir errores de React/Vue/Angular"
        ],
        "optimizacion": [
            "Identificar codigo redundante",
            "Encontrar cuellos de botella",
            "Mejorar performance basica",
            "Simplificar logica compleja",
            "Reducir complejidad ciclomatica",
            "Eliminar codigo muerto"
        ],
        "prevencion": [
            "Agregar manejo de errores",
            "Sugerir validaciones",
            "Recomendar mejores practicas",
            "Implementar logging",
            "Agregar tests unitarios",
            "Sugerir tipado estatico"
        ]
    },
    
    "debug_process": {
        "paso_1_error": {
            "nombre": "Capturar el error completo",
            "accion": "Leer TODA la pila de errores, no solo la primera linea",
            "ejemplo": "TypeError: Cannot read property 'name' of undefined\n    at User.getUser (models/user.js:45:20)"
        },
        "paso_2_contexto": {
            "nombre": "Entender el contexto",
            "accion": "Que archivo, que funcion, que linea, que estaba haciendo",
            "preguntas": ["Que archivo fallo?", "Que funcion se ejecutaba?", "Que datos tenia?"]
        },
        "paso_3_causa": {
            "nombre": "Encontrar la causa raiz",
            "accion": "No tratar el sintoma - encontrar POR QUE paso",
            "ejemplo": "El error es 'undefined.name' pero la causa real es que el fetch no espero la respuesta"
        },
        "paso_4_fix": {
            "nombre": "Aplicar el fix correcto",
            "accion": "Corregir la causa raiz, no agregar un parche",
            "ejemplo": "Agregar await antes del fetch, no un if (result) antes de usar"
        },
        "paso_5_verificar": {
            "nombre": "Verificar que funciona",
            "accion": "Probar el fix y asegurar que no rompio nada mas",
            "ejemplo": "Correr el script completo, no solo la linea arreglada"
        }
    },
    
    "common_errors": {
        "python": {
            "NameError": "Variable no definida - revisar scope y spelling",
            "TypeError": "Tipo de dato incorrecto - revisar argumentos",
            "ValueError": "Valor invalido - revisar input del usuario",
            "ImportError": "Modulo no encontrado - verificar installacion",
            "SyntaxError": "Codigo mal escrito - revisar indentacion/parentesis",
            "AttributeError": "Objeto no tiene ese metodo/atributo",
            "IndexError": "Indice fuera de rango - revisar longitudes",
            "KeyError": "Key no existe en diccionario",
            "FileNotFoundError": "Archivo no existe en esa ruta",
            "RecursionError": "Recursion infinita - agregar condicion de parada",
            "ModuleNotFoundError": "Modulo no encontrado - pip install",
            "IndentationError": "Indentacion incorrecta - revisar espacios",
            "TabError": "Mezcla de tabs y espacios"
        },
        "javascript": {
            "TypeError": "Tipo incorrecto o funcion no existe",
            "ReferenceError": "Variable no declarada",
            "SyntaxError": "Codigo JS invalido",
            "undefined is not": "Variable sin valor - agregar check",
            "Cannot read property": "Objeto null/undefined - agregar validacion",
            "is not a function": "Intentar llamar algo que no es funcion",
            "Maximum call stack": "Recursion infinita",
            "Unhandled Promise": "Promise sin catch",
            "CORS error": "Problema de Cross-Origin - configurar proxy"
        },
        "html_css": {
            "unclosed_tag": "Tag sin cerrar - verificar HTML",
            "wrong_nesting": "Tags anidados incorrectamente",
            "missing_semicolon": "Falta punto y coma en CSS",
            "wrong_selector": "Selector CSS no existe o es muy especifico",
            "z-index issues": "Problemas de apilamiento - revisar position",
            "overflow": "Contenido desbordado - revisar overflow"
        },
        "react": {
            "Cannot update state": "setState en componente desmontado",
            "Invalid hook call": "Hook fuera de componente o condicional",
            "Key prop": "Falta key en listas renderizadas",
            "Memory leak": "useEffect sin cleanup"
        },
        "node": {
            "MODULE_NOT_FOUND": "Modulo no instalado - npm install",
            "EADDRINUSE": "Puerto ya en uso - cambiar puerto",
            "Unhandled rejection": "Promise sin catch"
        }
    },
    
    "debugging_techniques": [
        {
            "nombre": "Print Debugging",
            "uso": "Agregar prints para ver valores en diferentes puntos",
            "cuando": "Para bugs simples y rapidos",
            "ejemplo": "console.log('DEBUG:', variable)"
        },
        {
            "nombre": "Binary Search",
            "uso": "Ir mitadando el codigo para encontrar donde falla",
            "cuando": "Cuando no sabes en que parte del codigo esta el bug",
            "ejemplo": "Agregar print en la mitad del codigo, ver si falla antes o despues"
        },
        {
            "nombre": "Rubber Duck",
            "uso": "Explicar el codigo linea por linea (a veces el bug se ve solo)",
            "cuando": "Cuando llevas tiempo atascado",
            "ejemplo": "Empezar: 'Esta linea hace X, luego esta hace Y...'"
        },
        {
            "nombre": "Diff Analysis",
            "uso": "Comparar que cambio recientemente",
            "cuando": "Cuando algo que funcionaba dejo de funcionar",
            "ejemplo": "git diff o comparar con version anterior"
        },
        {
            "nombre": "Stack Trace Analysis",
            "uso": "Seguir la pila de errores desde el fondo hacia arriba",
            "cuando": "Cuando el error viene de multiples capas",
            "ejemplo": "Empezar por el ultimo frame del stack trace"
        },
        {
            "nombre": "Minimal Reproduction",
            "uso": "Crear el caso mas simple que reproduce el bug",
            "cuando": "Cuando el bug es complejo y no sabes donde esta",
            "ejemplo": "Eliminar codigo hasta encontrar la linea minima que falla"
        }
    ],
    
    "error_patterns": {
        "async_issues": {
            "pattern": "Codigo async sin await o Promise sin .then()",
            "fix": "Agregar await o .then()/.catch()"
        },
        "null_reference": {
            "pattern": "Acceder a propiedad de null/undefined",
            "fix": "Agregar optional chaining (?) o validacion"
        },
        "scope_leak": {
            "pattern": "Variable global que deberia ser local",
            "fix": "Usar const/let en vez de var, o mover la declaracion"
        },
        "off_by_one": {
            "pattern": "Loop que va una posicion de mas o de menos",
            "fix": "Revisar < vs <= y starting index"
        },
        "state_mutation": {
            "pattern": "Mutar state directamente en React/Vue",
            "fix": "Usar spread operator o setState"
        }
    },
    
    "triggers": {
        "error": ["error", "fallo", "no funciona", "crash", "exception"],
        "bug": ["bug", "problema", "issue", "glitch"],
        "arreglar": ["arregla", "fix", "corrige", "repara"],
        "ayuda_debug": ["no corre", "no compila", "tira error", "me da error"],
        "analizar": ["analiza", "revisa", "diagnostica", "investiga"]
    }
}
