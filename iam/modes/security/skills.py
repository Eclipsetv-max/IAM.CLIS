# -*- coding: utf-8 -*-
"""
IAM Security Mode - Skills del modo seguridad
"""

SECURITY_SKILLS = {
    "name": "Security",
    "description": "Auditor de seguridad ofensiva y defensiva",
    "icon": "[verificando]",
    "color": "#f9e2af",
    
    "tools": {
        "read_file": {
            "description": "Analiza codigo fuente en busca de vulnerabilidades",
            "usage": "SIEMPRE primero - entender el attack surface",
            "prompt_hint": "Lee el archivo para analizar seguridad",
            "required": True,
            "examples": [" analiza la autenticacion", " revisa el login", " busca secrets"]
        },
        "edit_file": {
            "description": "Aplica fixes de seguridad",
            "usage": "Corregir vulnerabilidades encontradas",
            "prompt_hint": "Edita con el fix seguro",
            "examples": [" sanitiza el input", " hashea la password", " agrega validacion"]
        },
        "execute": {
            "description": "Ejecuta herramientas de auditoria",
            "usage": "Escanear dependencias, testear endpoints",
            "prompt_hint": "Ejecuta la herramienta de security",
            "examples": [" npm audit", " ejecuta el scan", " verifica dependencias"]
        },
        "list_files": {
            "description": "Mapea archivos expuestos o sensibles",
            "usage": "Encontrar archivos que no deberian ser publicos",
            "prompt_hint": "Lista para ver superficie de ataque",
            "examples": [" busca archivos .env", " muestra archivos sensibles", " que esta expuesto"]
        }
    },
    
    "capabilities": {
        "vulnerabilidades": [
            "Detectar SQL Injection (SQLi)",
            "Detectar Cross-Site Scripting (XSS)",
            "Detectar Cross-Site Request Forgery (CSRF)",
            "Detectar Command Injection",
            "Detectar Path Traversal",
            "Detectar Insecure Deserialization",
            "Detectar XML External Entity (XXE)",
            "Detectar Broken Authentication"
        ],
        "secrets": [
            "Encontrar API keys hardcodeadas",
            "Detectar passwords en codigo",
            "Buscar tokens expuestos",
            "Encontrar credenciales en configs",
            "Detectar private keys"
        ],
        "configuracion": [
            "Revisar headers de seguridad (CSP, HSTS, X-Frame)",
            "Auditar configuracion CORS",
            "Verificar cookies seguras (HttpOnly, Secure, SameSite)",
            "Revisar configuracion TLS/SSL",
            "Auditar permisos de archivos"
        ],
        "dependencias": [
            "Analizar package.json/requirements.txt",
            "Buscar CVEs conocidos",
            "Recomendar upgrades de seguridad",
            "Auditar licencias riesgosas"
        ],
        "autenticacion": [
            "Revisar implementacion de login",
            "Auditar hashing de passwords",
            "Verificar manejo de sesiones",
            "Revisar control de acceso",
            "Auditar JWT tokens"
        ]
    },
    
    "vulnerability_db": {
        "CRITICAL": {
            "sql_injection": {
                "descripcion": "Inyeccion SQL permite ejecutar queries arbitrary",
                "ejemplo": "' OR '1'='1' DROP TABLE users;--",
                "fix": "Usar prepared statements, nunca concatenar inputs"
            },
            "command_injection": {
                "descripcion": "Ejecucion de comandos del sistema via input",
                "ejemplo": "; rm -rf /",
                "fix": "Nunca pasar input directo a exec(), usar subprocess con shell=False"
            },
            "rce": {
                "descripcion": "Remote Code Execution - ejecutar codigo en el servidor",
                "ejemplo": "eval(user_input) con input malicioso",
                "fix": "Nunca usar eval() con input del usuario"
            }
        },
        "HIGH": {
            "xss": {
                "descripcion": "Cross-Site Scripting - inyectar scripts en paginas",
                "ejemplo": "<script>alert('hacked')</script>",
                "fix": "Sanitizar input, usar.textContent en vez de.innerHTML"
            },
            "broken_auth": {
                "descripcion": "Autenticacion rota - passwords debiles, sesiones predecibles",
                "ejemplo": "Password: 123456, Session ID predecible",
                "fix": "Hash bcrypt, tokens aleatorios, 2FA"
            },
            "hardcoded_secrets": {
                "descripcion": "Secrets en codigo fuente",
                "ejemplo": "API_KEY = 'sk-1234567890'",
                "fix": "Variables de entorno, secrets manager"
            }
        },
        "MEDIUM": {
            "cors_misconfig": {
                "descripcion": "CORS permite requests de cualquier origen",
                "ejemplo": "Access-Control-Allow-Origin: *",
                "fix": "Whitelist de origenes permitidos"
            },
            "insecure_cookies": {
                "descripcion": "Cookies sin flags de seguridad",
                "ejemplo": "Set-Cookie: session=abc123",
                "fix": "Agregar HttpOnly, Secure, SameSite=Strict"
            },
            "missing_headers": {
                "descripcion": "Faltan headers de seguridad",
                "ejemplo": "No CSP, no X-Frame-Options",
                "fix": "Configurar todos los headers de seguridad"
            }
        }
    },
    
    "security_headers": {
        "Content-Security-Policy": "Prevenir XSS y injection",
        "Strict-Transport-Security": "Forzar HTTPS",
        "X-Content-Type-Options": "Prevenir MIME sniffing",
        "X-Frame-Options": "Prevenir clickjacking",
        "X-XSS-Protection": "Filtro XSS del browser",
        "Referrer-Policy": "Controlar informacion de referrer",
        "Permissions-Policy": "Restringir features del browser"
    },
    
    "audit_process": [
        "1. MAPEAR - Encontrar todo el attack surface",
        "2. ESCANEAR - Buscar vulnerabilidades conocidas",
        "3. ANALIZAR - Evaluar impacto y explotabilidad",
        "4. PRIORIZAR - Clasificar por severidad",
        "5. FIX - Aplicar correcciones",
        "6. VERIFICAR - Confirmar que el fix funciona"
    ],
    
    "triggers": {
        "analisis": ["seguridad", "vulnerabilidad", "audita", "revisa"],
        "password": ["password", "contraseña", "hash", "credencial"],
        "secret": ["api key", "token", "secret", "clave"],
        "fix_seguro": ["arregla seguridad", "haz seguro", "protege"]
    }
}
