# IAM v3.4 - Multi-AI Assistant

## Que es IAM?

IAM (Inteligencia Artificial Multitarea) es un asistente de IA que funciona **sin necesidad de API keys**. Solo instalas y listo.

## Como funciona?

```
Tu PC (sin keys) → Servidor Proxy (tiene las keys) → APIs de IA
```

**El servidor proxy** (`https://iam-proxy.feabpemu12345.workers.dev`) maneja todas las API keys. Tu solo instalas IAM y usas las IAs sin configurar nada.

## IAs Disponibles

| IA | Estado | Requiere Key |
|----|--------|--------------|
| FreeTheAi | ✅ Activo | No (proxy) |
| Gemini | ✅ Activo | No (proxy) |
| OpenCode/MiMo | ⚠️ Pendiente | Si (key del usuario) |

## Instalacion

```bash
git clone https://github.com/Eclipsetv-max/IAM.CLIS.git
cd IAM.CLIS
pip install -r requirements.txt
python main.py
```

**No necesitas configurar API keys.** El servidor proxy ya las tiene.

## Comandos

- `/engine multi` - Usar todas las IAs juntas (default)
- `/engine freetheai` - Solo FreeTheAi
- `/engine gemini` - Solo Gemini
- `/engine opencode` - Solo OpenCode (requiere key)

## Dashboard del Servidor

- URL: `https://iam-proxy.feabpemu12345.workers.dev/dashboard`
- Password: Configurado como variable de entorno `ADMIN_PASSWORD`
- Funciones:
  - Activar/desactivar servidor
  - Ver estado de las APIs
  - Modo mantenimiento

## Seguridad

- **API keys NUNCA** se exponen a los usuarios
- Las keys estan en el servidor como variables de entorno
- Los usuarios solo ven la URL del proxy
- Puedes desactivar el servidor desde el dashboard

## Cambios recientes (v3.4)

### Multi-AI Engine
- Todas las IAs trabajan en paralelo
- Si una falla, las otras siguen funcionando
- Respuesta de la IA mas completa

### Proxy Server
- Servidor en Render.com (gratis)
- Dashboard con control total
- Modo mantenimiento
- Endpoints: `/v1/chat/completions`, `/v1/gemini`, `/health`

### Seguridad
- API keys en variables de entorno del servidor
- `.env` en `.gitignore` (no se sube a GitHub)
- Solo placeholders en `.env.example`

## Arquitectura

```
IAM CLI (Python)
    ↓
Proxy Server (Flask en Render)
    ↓
FreeTheAi API
Gemini API
OpenCode API
```

## Archivos importantes

- `iam/core/freetheai.py` - Cliente FreeTheAi
- `iam/core/gemini.py` - Cliente Gemini
- `iam/core/agent.py` - Motor Multi-AI
- `iam/server/server_full.py` - Servidor Proxy
- `.env.example` - Ejemplo de configuracion
