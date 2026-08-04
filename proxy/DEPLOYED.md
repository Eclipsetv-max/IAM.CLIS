# IAM Proxy - Cloudflare Worker

## URL del Worker
```
https://iam-proxy.feabpemu12345.workers.dev
```

## Endpoints disponibles

### Health Check
```bash
GET https://iam-proxy.feabpemu12345.workers.dev/health
```

### Chat Completions (proxy a OpenCode/MiMo)
```bash
POST https://iam-proxy.feabpemu12345.workers.dev/v1/chat/completions
Content-Type: application/json

{
  "model": "mimo-v2.5-free",
  "messages": [
    {"role": "user", "content": "Hola"}
  ],
  "max_tokens": 1024
}
```

## Configurar en IAM CLI

Editar `.env` y cambiar:
```env
OPENCODE_PROXY_URL=https://iam-proxy.feabpemu12345.workers.dev
```

## Variables de entorno

La API key de OpenCode ya está configurada como secret en Cloudflare:
- `OPENCODE_API_KEY` - Configurada vía `wrangler secret`

## Comandos útiles

```bash
# Ver logs en tiempo real
wrangler tail

# Redesplegar después de cambios
wrangler deploy

# Ver estado
wrangler whoami
```