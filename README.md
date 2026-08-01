# IAM CLI

> Asistente de IA multi-modos con ejecucion directa de codigo

## Descripcion

IAM CLI es un asistente de inteligencia artificial que ejecuta codigo directamente en lugar de solo describirlo. Cuenta con 5 modos especializados, animaciones de carga en tiempo real, y un parser TOOL_CALL que genera archivos automaticamente.

## Caracteristicas

- **5 Modos Especializados:**
  - `general` - Asistente general con analisis profundo
  - `builder` - Constructor de proyectos web completos
  - `debug` - Detective de bugs con analisis paso a paso
  - `security` - Auditor de seguridad y vulnerabilidades
  - `reader` - Lector y analizador de archivos

- **Ejecucion Directa:** La IA crea archivos reales, no describe lo que haria

- **TOOL_CALL Parser:** Detecta HTML, CSS, JS y genera archivos automaticamente

- **Loading Animations:** Animaciones en tiempo real con `sys.stdout.buffer.write`

- **Tab Mode Switching:** Cambia entre modos con la tecla Tab

## Instalacion

```bash
# Clonar repositorio
git clone https://github.com/TU_USUARIO/iam-cli.git
cd iam-cli

# Instalar dependencias
pip install -r requirements.txt

# Configurar API keys
cp .env.example .env
# Editar .env con tus API keys
```

## Configuracion

Crear archivo `.env` con:

```env
OPENCODE_API_KEY=tu-api-key-aqui
GROQ_API_KEY=tu-api-key-aqui
```

## Uso

```bash
# Ejecutar IAM
python main.py

# Comandos disponibles:
# /general  - Modo general (por defecto)
# /build    - Modo constructor
# /debug    - Modo depuracion
# /security - Modo seguridad
# /reader   - Modo lectura
# /project  - Seleccionar proyecto
# /help     - Ayuda
# /clear    - Limpiar pantalla
# /exit     - Salir
```

## Ejemplo

```
> /build crea una web de camiones

[iam] Modo: [construyendo]...
[iam] Proyecto: C:\Users\usuario\mi-proyecto

> Hazme una web moderna de camiones con navbar, hero, cards y footer

[construyendo] Creando proyecto...
[OK] Archivo creado: index.html
[OK] Archivo creado: style.css
[OK] Archivo creado: script.js
[OK] Verificado: index.html (2847 bytes)
[OK] Verificado: style.css (1523 bytes)
[OK] Verificado: script.js (892 bytes)

Cree index.html, style.css y script.js. Abrilo en tu navegador.
```

## Estructura del Proyecto

```
iam-cli/
├── main.py                 # Punto de entrada
├── requirements.txt        # Dependencias
├── .env.example           # Ejemplo de configuracion
├── iam/
│   ├── core/
│   │   ├── agent.py       # Motor principal de IA
│   │   ├── enhanced_cli.py # CLI mejorado
│   │   ├── loading.py     # Animaciones de carga
│   │   ├── memory.py      # Sistema de memoria
│   │   ├── reasoning.py   # Motor de razonamiento
│   │   └── session.py     # Manejo de sesiones
│   ├── config/
│   │   ├── prompts.py     # Prompts de cada modo
│   │   └── settings.py    # Configuracion global
│   ├── modes/
│   │   ├── loader.py      # Cargador de modos
│   │   ├── general/       # Modo general
│   │   ├── builder/       # Modo constructor
│   │   ├── debug/         # Modo depuracion
│   │   ├── security/      # Modo seguridad
│   │   └── reader/        # Modo lectura
│   └── tools/             # Herramientas del sistema
└── pruebas/               # Suite de tests
    └── test_completo.py   # 154 tests
```

## Tests

```bash
# Ejecutar todos los tests
python pruebas/test_completo.py

# Ejecutar un test especifico
python -c "from pruebas.test_completo import *; test_load_modes()"
```

## Tecnologias

- Python 3.12+
- OpenCode API (MiMo v2.5)
- Groq API (Llama 3.3)
- Rich (UI en terminal)
- psutil (monitoreo del sistema)

## Licencia

MIT

## Autor

IAM - Intencional Artificial Multitarea
