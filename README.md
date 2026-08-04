# IAM CLI v3.4

> Asistente de IA multi-modos que funciona **sin API keys**

## Que es IAM?

IAM (Inteligencia Artificial Multitarea) es un asistente de IA que ejecuta codigo directamente. **No necesitas configurar API keys** - el servidor proxy ya las tiene.

## Como funciona?

```
Tu PC (sin keys) → Servidor Proxy (tiene las keys) → APIs de IA
```

## Instalacion

```bash
git clone https://github.com/Eclipsetv-max/IAM.CLIS.git
cd IAM.CLIS
pip install -r requirements.txt
python main.py
```

**No necesitas configurar API keys.** Solo instalas y usas.

## Caracteristicas

- **Multi-AI Engine:** FreeTheAi, Gemini y OpenCode trabajan juntas
- **5 Modos Especializados:** general, builder, debug, security, reader
- **Ejecucion Directa:** La IA crea archivos reales
- **TOOL_CALL Parser:** Genera HTML, CSS, JS automaticamente
- **Loading Animations:** Animaciones en tiempo real

## Comandos

| Comando | Descripcion |
|---------|-------------|
| `/engine multi` | Usar todas las IAs (default) |
| `/engine freetheai` | Solo FreeTheAi |
| `/engine gemini` | Solo Gemini |
| `/general` | Modo general |
| `/build` | Modo constructor |
| `/debug` | Modo depuracion |
| `/security` | Modo seguridad |
| `/project` | Seleccionar proyecto |
| `/help` | Ayuda |

## Ejemplo

```
> hola que puedes hacer?

[MULTI-AI: FreeTheAi, Gemini] (2.3s)
--- Respuesta de FreeTheAi ---
Hola! Soy IAM, puedo ayudarte con:
- Crear paginas web completas
- Programar en cualquier lenguaje
- Depurar errores
- Y mucho mas!

> crea una web de camiones

[construyendo] Creando proyecto...
[OK] Archivo creado: index.html
[OK] Archivo creado: style.css
[OK] Archivo creado: script.js
```

## Arquitectura

```
IAM CLI (Python)
    ↓
Render Server (https://iam-proxy.onrender.com)
    ↓
FreeTheAi API
Gemini API
OpenCode/MiMo API
```

**Las API keys ya estan configuradas.** No necesitas nada mas.

## Seguridad

- **API keys NUNCA** se exponen a los usuarios
- Las keys estan en el servidor como variables de entorno
- Los usuarios solo ven la URL del proxy
- Puedes desactivar el servidor desde el dashboard

## Dashboard del Servidor

- URL: `https://iam-proxy.onrender.com/dashboard`
- Estado del servidor en tiempo real

## Archivos importantes

| Archivo | Descripcion |
|---------|-------------|
| `main.py` | Punto de entrada |
| `iam/core/agent.py` | Motor Multi-AI |
| `iam/core/freetheai.py` | Cliente FreeTheAi |
| `iam/core/gemini.py` | Cliente Gemini |
| `iam/server/server_full.py` | Servidor Proxy |
| `.env.example` | Ejemplo de configuracion |
| `HISTORY.md` | Historial de cambios |

## Cambios recientes

- **v3.5:** Cloudflare Worker - sin cold start, acceso global
- **v3.4:** Multi-AI engine, proxy server auto-conectado
- **v3.1:** Animaciones mejoradas, loading indicators
- **v3.0:** Sistema de modos, TOOL_CALL parser

## Soporte

- GitHub: https://github.com/Eclipsetv-max/IAM.CLIS
- Issues: https://github.com/Eclipsetv-max/IAM.CLIS/issues
