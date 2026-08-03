# -*- coding: utf-8 -*-
"""
IAM Security Mode - Skills del modo seguridad (v4.1 Mejorado)
"""

SECURITY_SKILLS = {
    "name": "Security",
    "description": "Auditor de seguridad ofensiva y defensiva con capacidades avanzadas",
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
            "Detectar Broken Authentication",
            "Detectar Insecure Direct Object References",
            "Detectar Security Misconfiguration",
            "Detectar Insufficient Logging",
            "Detectar Server-Side Request Forgery (SSRF)"
        ],
        "secrets": [
            "Encontrar API keys hardcodeadas",
            "Detectar passwords en codigo",
            "Buscar tokens expuestos",
            "Encontrar credenciales en configs",
            "Detectar private keys",
            "Buscar connection strings con passwords",
            "Detectar secrets en .env sin protection",
            "Encontrar tokens en logs"
        ],
        "configuracion": [
            "Revisar headers de seguridad (CSP, HSTS, X-Frame)",
            "Auditar configuracion CORS",
            "Verificar cookies seguras (HttpOnly, Secure, SameSite)",
            "Revisar configuracion TLS/SSL",
            "Auditar permisos de archivos",
            "Verificar configuracion de firewall",
            "Revisar configuracion de rate limiting",
            "Auditar configuracion de autenticacion"
        ],
        "dependencias": [
            "Analizar package.json/requirements.txt",
            "Buscar CVEs conocidos",
            "Recomendar upgrades de seguridad",
            "Auditar licencias riesgosas",
            "Detectar dependencias abandonadas",
            "Verificar integridad de paquetes",
            "Analizar supply chain attacks"
        ],
        "autenticacion": [
            "Revisar implementacion de login",
            "Auditar hashing de passwords",
            "Verificar manejo de sesiones",
            "Revisar control de acceso",
            "Auditar JWT tokens",
            "Verificar implementacion de OAuth",
            "Revisar reset de passwords",
            "Auditar 2FA/MFA"
        ],
        "criptografia": [
            "Verificar uso correcto de hashing",
            "Auditar algoritmos de encriptacion",
            "Revisar manejo de llaves",
            "Verificar longitud de salts",
            "Auditar generacion de numeros aleatorios"
        ]
    },
    
    "vulnerability_db": {
        "CRITICAL": {
            "sql_injection": {
                "descripcion": "Inyeccion SQL permite ejecutar queries arbitrary",
                "ejemplo": "' OR '1'='1' DROP TABLE users;--",
                "fix": "Usar prepared statements, nunca concatenar inputs",
                "impacto": "Perdida total de datos, acceso no autorizado"
            },
            "command_injection": {
                "descripcion": "Ejecucion de comandos del sistema via input",
                "ejemplo": "; rm -rf /",
                "fix": "Nunca pasar input directo a exec(), usar subprocess con shell=False",
                "impacto": "Control total del servidor"
            },
            "rce": {
                "descripcion": "Remote Code Execution - ejecutar codigo en el servidor",
                "ejemplo": "eval(user_input) con input malicioso",
                "fix": "Nunca usar eval() con input del usuario",
                "impacto": "Compromiso total del sistema"
            },
            "deserialization": {
                "descripcion": "Deserializacion insegura de objetos",
                "ejemplo": "pickle.loads(user_data) con data maliciosa",
                "fix": "Nunca deserializar datos no confiables, usar JSON",
                "impacto": "Ejecucion remota de codigo"
            }
        },
        "HIGH": {
            "xss": {
                "descripcion": "Cross-Site Scripting - inyectar scripts en paginas",
                "ejemplo": "<script>alert('hacked')</script>",
                "fix": "Sanitizar input, usar.textContent en vez de.innerHTML",
                "impacto": "Robo de sesiones, defacement"
            },
            "broken_auth": {
                "descripcion": "Autenticacion rota - passwords debiles, sesiones predecibles",
                "ejemplo": "Password: 123456, Session ID predecible",
                "fix": "Hash bcrypt, tokens aleatorios, 2FA",
                "impacto": "Acceso no autorizado a cuentas"
            },
            "hardcoded_secrets": {
                "descripcion": "Secrets en codigo fuente",
                "ejemplo": "API_KEY = 'sk-1234567890'",
                "fix": "Variables de entorno, secrets manager",
                "impacto": "Acceso a servicios y datos sensibles"
            },
            "xxe": {
                "descripcion": "XML External Entity - leer archivos via XML",
                "ejemplo": "<!ENTITY xxe SYSTEM 'file:///etc/passwd'>",
                "fix": "Deshabilitar entidades externas en parsers XML",
                "impacto": "Lectura de archivos sensibles, SSRF"
            }
        },
        "MEDIUM": {
            "cors_misconfig": {
                "descripcion": "CORS permite requests de cualquier origen",
                "ejemplo": "Access-Control-Allow-Origin: *",
                "fix": "Whitelist de origenes permitidos",
                "impacto": "Robo de datos via requests cross-origin"
            },
            "insecure_cookies": {
                "descripcion": "Cookies sin flags de seguridad",
                "ejemplo": "Set-Cookie: session=abc123",
                "fix": "Agregar HttpOnly, Secure, SameSite=Strict",
                "impacto": "Robo de sesiones via XSS"
            },
            "missing_headers": {
                "descripcion": "Faltan headers de seguridad",
                "ejemplo": "No CSP, no X-Frame-Options",
                "fix": "Configurar todos los headers de seguridad",
                "impacto": "Vulnerabilidades adicionales"
            },
            "open_redirect": {
                "descripcion": "Redirecciones a sitios maliciosos",
                "ejemplo": "https://site.com/redirect?url=evil.com",
                "fix": "Validar URLs de redireccionamiento",
                "impacto": "Phishing, robo de credenciales"
            }
        },
        "LOW": {
            "info_disclosure": {
                "descripcion": "Informacion sensible expuesta",
                "ejemplo": "Stack traces en produccion, version de servidor",
                "fix": "Ocultar detalles en produccion",
                "impacto": "Facilita otros ataques"
            },
            "weak_crypto": {
                "descripcion": "Algoritmos de criptografia debiles",
                "ejemplo": "MD5 para passwords, SHA1 para hashes",
                "fix": "Usar bcrypt, Argon2, SHA256+",
                "impacto": "Passwords crackeables"
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
        "Permissions-Policy": "Restringir features del browser",
        "Cross-Origin-Embedder-Policy": "Prevenir side-channel attacks",
        "Cross-Origin-Opener-Policy": "Aislar contexto del browser",
        "Cross-Origin-Resource-Policy": "Controlar recursos cross-origin"
    },
    
    "audit_process": [
        "1. MAPEAR - Encontrar todo el attack surface",
        "2. ESCANEAR - Buscar vulnerabilidades conocidas",
        "3. ANALIZAR - Evaluar impacto y explotabilidad",
        "4. PRIORIZAR - Clasificar por severidad",
        "5. FIX - Aplicar correcciones",
        "6. VERIFICAR - Confirmar que el fix funciona",
        "7. DOCUMENTAR - Registrar hallazgos y remediacion",
        "8. MONITOREAR - Establecer vigilancia continua"
    ],
    
    "security_checklist": {
        "authentication": [
            "Passwords hasheadas con bcrypt/Argon2",
            "Rate limiting en login",
            "Bloqueo de cuenta tras intentos fallidos",
            "2FA disponible",
            "Sesiones expiran tras inactividad",
            "Logout invalida la sesion"
        ],
        "authorization": [
            "Control de acceso basado en roles",
            "Validacion de permisos en cada endpoint",
            "No exponer IDs secuenciales",
            "Verificar ownership de recursos"
        ],
        "input_validation": [
            "Sanitizar todo input del usuario",
            "Validar tipos y longitudes",
            "Usar allowlists en vez de blocklists",
            "Validar en servidor (no solo en cliente)"
        ],
        "data_protection": [
            "Encriptar datos en transito (HTTPS)",
            "Encriptar datos sensibles en reposo",
            "No loggear passwords o tokens",
            "Usar variables de entorno para secrets"
        ],
        "error_handling": [
            "No exponer stack traces en produccion",
            "Mensajes de error genericos",
            "Logear errores sin datos sensibles",
            "Manejar excepciones correctamente"
        ]
    },
    
    "triggers": {
        "analisis": ["seguridad", "vulnerabilidad", "audita", "revisa"],
        "password": ["password", "contraseña", "hash", "credencial"],
        "secret": ["api key", "token", "secret", "clave"],
        "fix_seguro": ["arregla seguridad", "has seguro", "protege"],
        "penetration": ["pentest", "prueba de penetracion", "hackea"],
        "compliance": ["cumplimiento", "regulacion", "GDPR", "合规"]
    }
}
