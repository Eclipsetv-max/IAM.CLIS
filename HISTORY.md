# IAM v4.1 - Historial de Cambios

## Que es IAM?

IAM (Inteligencia Artificial Multitarea) es un asistente de IA que funciona **sin necesidad de API keys**. Solo instalas y listo.

## Como funciona?

```
Tu PC (sin keys) → Servidor Proxy (tiene las keys) → APIs de IA
```

**El servidor proxy** (`https://iam-proxy.onrender.com`) maneja todas las API keys. Tu solo instalas IAM y usas las IAs sin configurar nada.

## IAs Disponibles

| IA | Estado | Requiere Key |
|----|--------|--------------|
| OpenCode/MiMo v2.5-free | ✅ Activo | No (proxy) |
| FreeTheAi | ⚠️ Pendiente | No (proxy) |
| Gemini | ⚠️ Pendiente | No (proxy) |

## Instalacion

```bash
git clone https://github.com/Eclipsetv-max/IAM.CLIS.git
cd IAM.CLIS
pip install -r requirements.txt
python main.py
```

**No necesitas configurar API keys.** El servidor proxy ya las tiene.

## Comandos

- `/engine opencode` - Usar OpenCode/MiMo (default)
- `/engine freetheai` - Usar FreeTheAi
- `/engine gemini` - Usar Gemini
- `/project` - Seleccionar proyecto
- `/help` - Ver ayuda

## Dashboard del Servidor

- URL: `https://iam-proxy.onrender.com/dashboard`
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

## Arquitectura

```
IAM CLI (Python)
    ↓
Render Server (https://iam-proxy.onrender.com)
    ↓
OpenCode/MiMo API
FreeTheAi API
Gemini API
```

## Servidores

| Servidor | URL | Estado |
|----------|-----|--------|
| Render (Produccion) | https://iam-proxy.onrender.com | ✅ Activo |
| Cloudflare Worker | https://iam-proxy.feabpemu12345.workers.dev | ✅ Activo |
| Fly.io (Backup) | https://iam-ai-proxy.fly.dev | ✅ Activo |

**UptimeRobot** mantiene el servidor de Render siempre despierto (ping cada 5 min).

## Cambios Recientes (4 Agosto 2026)

### v4.1 - Migracion a Cloudflare/Fly.io/Render
- ✅ Cloudflare Worker desplegado con dashboard web
- ✅ Fly.io desplegado con servidor completo
- ✅ Render configurado con UptimeRobot
- ✅ API keys configuradas en todos los servidores
- ✅ Motor por defecto: OpenCode/MiMo v2.5-free
- ✅ Quitado "OpenCode-Inspired" del titulo
- ✅ VERSION actualizada a v4.1

### API Keys Configuradas
- `OPENCODE_API_KEY` - OpenCode/MiMo
- `FREETHEAI_API_KEY` - FreeTheAi
- `GEMINI_API_KEY` - Google Gemini

### Archivos Importantes

| Archivo | Descripcion |
|---------|-------------|
| `main.py` | Punto de entrada |
| `iam/config/settings.py` | Configuracion global |
| `iam/core/agent.py` | Motor Multi-AI |
| `iam/core/freetheai.py` | Cliente FreeTheAi |
| `iam/core/gemini.py` | Cliente Gemini |
| `iam/server/server_full.py` | Servidor Proxy |
| `proxy/worker.js` | Cloudflare Worker |
| `.env.example` | Ejemplo de configuracion |

## Proximos Pasos

- [ ] Configurar FreeTheAi (check-in diario en Discord)
- [ ] Configurar Gemini
- [ ] Agregar mas modos de IA
- [ ] Mejorar dashboard con estadisticas de uso
