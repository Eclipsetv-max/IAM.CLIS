# IAM v4.5 - Documentación Completa de Desarrollo

## Resumen

IAM es un asistente de IA de línea de comandos que funciona como Claude Code. Ofrece múltiples modos de operación, integración con APIs de IA, y generación automática de proyectos web.

**Versión actual:** 4.5  
**Fecha:** Agosto 2026  
**Archivos Python:** 56  
**Líneas de código:** ~23,000  

---

## Historial de Commits (Sesión Actual)

### `1314cd1` - Limpieza de nombres externos
- Eliminados TODOS los rastros de "OpenCode", "FreeTheAi", "Gemini" del código visible
- Renombrado a IAM: engine `"iam"`, campos `API_KEY`, `API_KEY_ALT`, `API_KEY_GEM`
- Clases renombradas: `TertiaryClient`, `SecondaryClient`
- Strings de usuario: "Motor IA" en vez de nombres externos
- 21 archivos modificados

### `a5b3bd4` - Ultra ofuscación de API keys
- 4 capas de protección: Salt + Triple XOR + Shuffle + Checksum + Split
- Keys embebidas en settings.py con decodificación en runtime
- Imposible hacer copy-paste de las keys

### `e5606e1` - Fix placeholder bug
- Renombrado `placeholder` → `fallback_js` en bloque JS fallback
- Fixes NameError que causaba modo offline

### `81807eb` - Fix carga de .env
- Agregado `load_dotenv()` en main.py
- API keys ahora se cargan correctamente desde .env

---

## Arquitectura del Sistema

```
iam/
├── config/
│   ├── settings.py      # Configuración global, API keys ofuscadas
│   └── prompts.py       # System prompts para cada modo
├── core/
│   ├── agent.py         # Router principal de IA (~6500 líneas)
│   ├── memory.py        # Sistema de memoria a largo plazo
│   ├── session.py       # Gestión de sesiones
│   ├── enhanced_cli.py  # Interfaz de línea de comandos
│   ├── loading.py       # Indicadores de progreso
│   ├── permissions.py   # Sistema de permisos y seguridad
│   ├── file_history.py  # Versionado de archivos
│   ├── context_loader.py # Carga de contexto del proyecto
│   ├── auto_compact.py  # Compactación automática de contexto
│   ├── cost_tracking.py # Seguimiento de costos por tokens
│   ├── events.py        # Sistema de eventos
│   ├── persistent_shell.py # Shell persistente
│   ├── sub_agent.py     # Sub-agentes para tareas paralelas
│   ├── patch.py         # Sistema de patches
│   ├── reasoning.py     # Animación de "pensando"
│   ├── gemini.py        # Motor IA terciario (via proxy)
│   └── freetheai.py     # Motor IA secundario (via proxy)
├── modes/
│   ├── __init__.py
│   └── ... (modos eliminados, solo loader.py muerto)
├── tools/
│   ├── filesystem.py    # Operaciones de archivos
│   ├── code.py          # Herramientas de código
│   └── code_validator.py # Validador de código
├── server/
│   └── server_full.py   # Servidor proxy con dashboard
└── training/            # Fine-tuning (opcional)
```

---

## Motor de IA Principal

### API Keys Ultra Ofuscadas

Las 3 API keys están protegidas con 4 capas de ofuscación:

```python
# Capa 1: Salt (8 bytes aleatorios)
# Capa 2: Triple XOR (4 claves diferentes)
# Capa 3: Shuffle de bytes (patrón SHA256)
# Capa 4: Split en 4 partes + checksum MD5
```

**Decodificación en runtime:**
```python
settings.API_KEY      # Key principal (OpenCode/MiMo)
settings.API_KEY_ALT  # Key secundaria (FreeTheAi)
settings.API_KEY_GEM  # Key terciaria (Gemini)
```

### Conexión directa sin proxy

El agente intenta primero conexión directa con la API, luego fallback al proxy:

```python
def _call_iam_fast():
    # Intento 1: Directo (más rápido)
    # Intento 2: Proxy (fallback rápido)
    # Intento 3: Directo final
```

---

## Modos de Operación

| Modo | Descripción |
|------|-------------|
| `general` | Chat general, preguntas y respuestas |
| `builder` | Creación de proyectos web completos |
| `debug` | Depuración de código |
| `security` | Análisis de seguridad |
| `reader` | Solo lectura de archivos |

---

## Comandos Especiales

| Comando | Función |
|---------|---------|
| `/project` | Seleccionar carpeta de proyecto |
| `/engine iam` | Cambiar motor de IA |
| `/think` | Modo pensamiento |
| `/compact` | Modo compacto |
| `/help` | Ayuda completa |
| `/stats` | Estadísticas de uso |
| `/cost` | Costo de tokens |
| `/save` | Guardar respuesta |
| `/history` | Historial de archivos |
| `/rollback` | Deshacer cambios |
| `/tree` | Ver estructura del proyecto |
| `/deps` | Ver dependencias |
| `/run` | Ejecutar comandos |
| `/search` | Buscar en archivos |
| `/grep` | Búsqueda con regex |

---

## Generación de Proyectos Web

### Builder Mode

Cuando el usuario pide crear un sitio web, IAM genera:

1. **HTML** - Estructura completa con semántica
2. **CSS** - ~576 líneas con:
   - Variables CSS
   - Glassmorphism
   - Gradientes complejos
   - 8+ animaciones
   - Responsive design
   - Tabs, accordion, modal, tooltip
   - Skeleton loading
   - Print styles
3. **JavaScript** - ~431 líneas con:
   - Navegación activa al scroll
   - Navbar sticky con efecto glass
   - Animaciones al scroll (IntersectionObserver)
   - Mobile menu toggle
   - Smooth scroll
   - Dark mode toggle
   - Form validation
   - Tabs funcionales
   - Accordion expand/collapse
   - Modal open/close
   - Back to top button
   - Typing animation
   - Counter animation
   - Parallax scrolling
   - Tooltip hover
   - Lazy loading

### Fallback Automático

Si la IA no genera archivos, IAM crea fallbacks automáticamente:

```python
if needs_html:
    # HTML básico con link a CSS y JS
if needs_css:
    # CSS completo de 576 líneas
if needs_js:
    # JS completo de 431 líneas
```

---

## Protección de API Keys

### Niveles de protección

1. **En código fuente:** Keys ofuscadas con XOR + shuffle
2. **En .env:** Variables de entorno (no subido a git)
3. **En proxy:** Cloudflare Worker enmasks keys

### Flujo de autenticación

```
Usuario → IAM CLI → Settings (decode key) → API directa
                                         ↓ (fallback)
                                         → Cloudflare Worker Proxy
```

---

## Infraestructura

### Cloudflare Worker Proxy

- **URL:** `https://iam-proxy.feabpemu12345.workers.dev`
- **Endpoints:**
  - `GET /health` - Health check
  - `GET /v1/models` - Listar modelos
  - `POST /v1/chat/completions` - Chat completions
  - `POST /v1/gemini` - Gemini API
- **Dashboard:** `/dashboard`
- **Sin cold start:** Workers se ejecutan边缘

### Variables de Entorno (.env)

```env
# API Keys (no subir a git)
GEMINI_API_KEY=...
FREETHEAI_API_KEY=...
OPENCODE_API_KEY=...

# Proxy URLs
FREETHEAI_PROXY_URL=https://iam-proxy.feabpemu12345.workers.dev
GEMINI_PROXY_URL=https://iam-proxy.feabpemu12345.workers.dev
OPENCODE_PROXY_URL=https://iam-proxy.feabpemu12345.workers.dev
```

---

## Cambios Recientes Detallados

### Limpieza de Código Muerto (21 items eliminados)

**Archivos eliminados:**
- `test_retry.py` - Test manual obsoleto
- `test_runner.py` - Runner de tests ad-hoc
- `debug_runner.py` - Script de debug
- `test_projects/test_web_projects.py` - 1600+ líneas de tests hardcodeados
- `iam/modes/loader.py` - Functions nunca usadas

**Métodos eliminados:**
- `_call_huggingface()` - Motor eliminado
- `_auto_generate_title()` - Roto (asignaba atributo inexistente)
- `chat_stream()` en gemini.py - Roto (llamaba `_get_model()` inexistente)
- `chat_stream()` en freetheai.py - Nunca llamado
- `list_models()` en freetheai.py - Nunca llamado
- `_fallback_response()` branches groq/huggingface - Muertos

**Constantes eliminadas:**
- `HF_API_KEY` - Solo usada en código muerto
- `LOCAL_MODEL_DIR`, `LOCAL_MODEL_NAME` - Nunca referenciadas
- `FALLBACK_MODELS` - Nunca referenciada
- `get_model()` - Nunca llamado
- `USERNAME`, `USER_ALIAS`, `CODENAME` - Nunca usadas
- `BASE_DIR`, `IAM_DIR` - Nunca referenciadas
- 15 constantes de colores no usadas

**Imports eliminados:**
- `code_validator`, `quality_checker` - No usados en agent.py
- `ThinkingAnimation`, `PhaseAnimation` - No instanciados
- `hashlib`, `Generator` duplicados en múltiples archivos
- `TypeVar`, `Generic`, `Tuple`, `Callable` no usados

**Código muerto en prompts.py:**
- `MODE_CONFIGS` - Dict nunca importado
- `get_agent_by_command()` - Función nunca llamada

---

## Modelo de IA Utilizado

**Modelo principal:** `mimo-v2.5-free`  
**Proveedor:** OpenCode API  
**Costo:** Gratis  
**Contexto:** 128K tokens  

---

## Cómo Ejecutar

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar IAM
python main.py

# Con tema específico
python main.py --theme cyberpunk

# Modo compacto
python main.py --compact

# Modo pensamiento
python main.py --think
```

---

## Estructura de Directorios del Proyecto

```
Yo ia para github/
├── main.py                    # Punto de entrada
├── requirements.txt           # Dependencias
├── .env                       # API keys (no subir a git)
├── .gitignore
├── README.md
├── iam/                       # Código fuente principal
│   ├── config/
│   ├── core/
│   ├── tools/
│   ├── server/
│   ├── training/
│   └── data/
├── iam_real_tests/            # Tests de proyectos web
├── proxy/                     # Cloudflare Worker
│   └── worker.js
└── iam_v45_complete.md        # Este archivo
```

---

## Notas para Desarrolladores

1. **Nunca subir .env a git** - Contiene API keys
2. **Las keys están ofuscadas** - No son visibles en código fuente
3. **El proxy es opcional** - IAM funciona directo con la API
4. **Fallback automático** - Si la IA falla, crea archivos de respaldo
5. **Ultra ofuscación** - 4 capas de protección para keys

---

## Estado Actual

- [x] API keys ofuscadas con 4 capas
- [x] Conexión directa a API sin proxy
- [x] Todos los nombres externos eliminados
- [x] Código muerto limpiado (21 items)
- [x] Builder mode funcional con CSS/JS completos
- [x] Proxy Cloudflare Worker desplegado
- [x] Dashboard con estado del servidor
- [x] 5 tests pasando
- [x] Documentación completa

---

*IAM v4.5 - Asistente de IA de línea de comandos*
*Desarrollado con ❤️*
