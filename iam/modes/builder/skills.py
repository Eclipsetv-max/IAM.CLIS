# -*- coding: utf-8 -*-
"""
IAM Builder Mode - Skills del modo constructor (v4.1 Mejorado)
"""

BUILDER_SKILLS = {
    "name": "Builder",
    "description": "Constructor de proyectos completos y profesionales con capacidades fullstack",
    "icon": "[construyendo]",
    "color": "#a6e3a1",
    
    "tools": {
        "create_file": {
            "description": "Crea archivos completos y funcionales",
            "usage": "Para crear HTML, CSS, JS, Python, configuraciones",
            "prompt_hint": "SIEMPRE usa TOOL_CALL create_file para crear archivos",
            "required": True,
            "examples": [" crea index.html", " genera style.css", " haz main.js"]
        },
        "create_folder": {
            "description": "Crea carpetas para organizar el proyecto",
            "usage": "Para estructurar el proyecto correctamente",
            "prompt_hint": "Crea carpetas antes de los archivos",
            "examples": [" crea carpeta src", " estructura el proyecto", " organiza en carpetas"]
        },
        "edit_file": {
            "description": "Modifica archivos existentes sin reescribir todo",
            "usage": "Cuando algo necesita ajuste o mejora",
            "prompt_hint": "Edita especificamente lo que cambio",
            "examples": [" agrega una seccion", " mejora el CSS", " corrige el responsive"]
        },
        "execute": {
            "description": "Ejecuta comandos de build, instalacion y servidor",
            "usage": "Para npm install, python server, git init, etc",
            "prompt_hint": "Ejecuta comandos del proyecto",
            "examples": [" instala dependencias", " corre el servidor", " inicializa git"]
        },
        "read_file": {
            "description": "Lee archivos existentes antes de modificar",
            "usage": "SIEMPRE antes de editar - entender el estado actual",
            "prompt_hint": "Lee primero para no romper nada",
            "examples": [" lee el package.json", " que hay en index.html"]
        }
    },
    
    "capabilities": {
        "frontend": [
            "Crear paginas HTML5 semanticas y modernas",
            "Disenos CSS responsivos con Flexbox/Grid",
            "JavaScript vanilla interactivo",
            "Animaciones CSS y transiciones",
            "Forms con validacion",
            "Galerias y sliders",
            "Landing pages profesionales",
            "Dashboards y admin panels",
            "PWA basicas (manifest, service worker)",
            "Accesibilidad basica (ARIA, semantic HTML)"
        ],
        "backend": [
            "APIs REST con Express.js",
            "APIs con FastAPI (Python)",
            "Servidores HTTP basicos",
            "CRUD completo",
            "Autenticacion basica",
            "Websockets simples",
            "GraphQL basico",
            "Microservicios simples"
        ],
        "fullstack": [
            "Proyectos completos frontend+backend",
            "Conectar frontend con API",
            "Estructura de proyecto profesional",
            "Configuracion de build",
            "Deploy basico",
            "Testing integrado"
        ],
        "devops": [
            "Inicializar repositorios git",
            "Crear archivos .gitignore",
            "Docker basico",
            "Scripts de package.json",
            "CI/CD basico",
            "Variables de entorno"
        ],
        "mobile": [
            "Landing pages mobile-first",
            "Apps basicas con HTML/CSS/JS",
            "PWA con manifest",
            "Scroll effects"
        ]
    },
    
    "design_system": {
        "colores": {
            "primarios": ["#0f172a", "#1e293b", "#334155"],
            "acentos": ["#3b82f6", "#10b981", "#f59e0b", "#ef4444"],
            "gradientes": ["linear-gradient(135deg, #667eea 0%, #764ba2 100%)"],
            "glassmorphism": "backdrop-filter: blur(10px); background: rgba(255,255,255,0.1)",
            "neon": "box-shadow: 0 0 10px #3b82f6, 0 0 20px #3b82f6",
            "modern": "background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%)"
        },
        "tipografia": {
            "titulares": "font-size: clamp(2rem, 5vw, 4rem)",
            "cuerpo": "font-size: 1rem; line-height: 1.6",
            "fuentes": ["Inter", "Poppins", "Montserrat", "Space Grotesk", "Outfit"],
            "weights": ["300", "400", "500", "600", "700"]
        },
        "espaciado": {
            "secciones": "padding: clamp(4rem, 10vw, 8rem) 0",
            "cards": "padding: 2rem; gap: 1.5rem",
            "grid": "gap: clamp(1rem, 3vw, 2rem)"
        },
        "efectos": {
            "hover": "transform: translateY(-4px); transition: all 0.3s ease",
            "sombra": "box-shadow: 0 10px 40px rgba(0,0,0,0.1)",
            "blur": "backdrop-filter: blur(20px)",
            "border": "border-radius: 16px; border: 1px solid rgba(255,255,255,0.1)",
            "glow": "box-shadow: 0 0 20px rgba(59, 130, 246, 0.5)",
            "float": "animation: float 3s ease-in-out infinite"
        }
    },
    
    "templates": {
        "landing_page": {
            "estructura": ["navbar", "hero", "features", "testimonials", "cta", "footer"],
            "archivos": ["index.html", "style.css", "main.js"],
            "descripcion": "Pagina de aterrizaje moderna con una sola scroll",
            "ejemplo_hero": "Gradiente oscuro + titulo grande + boton CTA animado",
            "ejemplo_features": "Grid de cards con iconos y hover effects"
        },
        "portfolio": {
            "estructura": ["header", "about", "projects", "skills", "contact"],
            "archivos": ["index.html", "style.css", "script.js"],
            "descripcion": "Sitio personal para mostrar trabajos",
            "ejemplo_projects": "Grid de proyectos con filtros y modal"
        },
        "dashboard": {
            "estructura": ["sidebar", "header", "stats", "charts", "table"],
            "archivos": ["index.html", "style.css", "dashboard.js"],
            "descripcion": "Panel de administracion con datos",
            "ejemplo_stats": "Cards con numeros animados y graficos"
        },
        "ecommerce": {
            "estructura": ["navbar", "hero", "products", "cart", "footer"],
            "archivos": ["index.html", "style.css", "products.js", "cart.js"],
            "descripcion": "Tienda online basica",
            "ejemplo_products": "Grid de productos con hover y boton agregar"
        },
        "blog": {
            "estructura": ["header", "posts", "sidebar", "footer"],
            "archivos": ["index.html", "style.css", "posts.js"],
            "descripcion": "Blog personal o tecnico",
            "ejemplo_posts": "Cards de posts con imagen, titulo, excerpt"
        },
        "saas": {
            "estructura": ["navbar", "hero", "pricing", "features", "testimonials", "cta", "footer"],
            "archivos": ["index.html", "style.css", "main.js"],
            "descripcion": "Landing page para producto SaaS",
            "ejemplo_pricing": "3 columnas de precios con destacado"
        },
        "restaurant": {
            "estructura": ["hero", "menu", "about", "gallery", "reservation", "footer"],
            "archivos": ["index.html", "style.css", "menu.js"],
            "descripcion": "Pagina de restaurante",
            "ejemplo_menu": "Grid de platos con imagen, nombre, precio"
        },
        "agency": {
            "estructura": ["navbar", "hero", "services", "team", "portfolio", "contact", "footer"],
            "archivos": ["index.html", "style.css", "main.js"],
            "descripcion": "Pagina de agencia digital",
            "ejemplo_services": "Cards con iconos y animaciones"
        }
    },
    
    "quality_checklist": [
        "Responsive en mobile, tablet y desktop",
        "Hover effects en botones y cards",
        "Gradientes o colores modernos",
        "Tipografia clara con jerarquia",
        "Espaciado generoso entre secciones",
        "Animaciones suaves al scroll",
        "Footer con informacion relevante",
        "Navbar fija o sticky",
        "Imagenes con overlay si son de fondo",
        "Formulario funcional si se necesita",
        "Accesibilidad basica (alt, aria-labels)",
        "Performance optimizada (imagenes comprimidas)",
        "Meta tags para SEO",
        "Favicon configurado"
    ],
    
    "file_structure_examples": {
        "simple_web": {
            "estructura": """
proyecto/
├── index.html
├── style.css
└── script.js
"""
        },
        "organized_web": {
            "estructura": """
proyecto/
├── index.html
├── css/
│   ├── style.css
│   └── responsive.css
├── js/
│   ├── main.js
│   └── utils.js
├── images/
│   └── logo.png
└── README.md
"""
        },
        "fullstack": {
            "estructura": """
proyecto/
├── frontend/
│   ├── index.html
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── app.js
├── backend/
│   ├── server.js
│   ├── routes/
│   └── models/
├── package.json
└── README.md
"""
        }
    },
    
    "triggers": {
        "crear": ["crea", "haz", "genera", "construye", "desarrolla"],
        "web": ["pagina", "web", "sitio", "landing", "blog"],
        "app": ["app", "aplicacion", "programa", "sistema"],
        "api": ["api", "servidor", "backend", "endpoint"],
        "mejorar": ["mejora", "actualiza", "optimiza", "modifica"],
        "estructura": ["estructura", "organiza", "carpeta", "directorio"]
    }
}
