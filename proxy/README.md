# IAM Proxy - Cloudflare Worker

## Pasos para deploy:

### 1. Instalar Wrangler CLI
```bash
npm install -g wrangler
```

### 2. Login en Cloudflare
```bash
wrangler login
```

### 3. Ir a la carpeta del proxy
```bash
cd "C:\Users\casa\Desktop\Yo ia para github\proxy"
```

### 4. Agregar API key de OpenCode
```bash
wrangler secret put OPENCODE_API_KEY
# Pegar tu API key cuando te lo pida
```

### 5. Deploy
```bash
wrangler deploy
```

### 6. Copiar la URL del worker
Te mostrara algo como:
```
https://iam-proxy.abc123.workers.dev
```

### 7. Actualizar IAM
Copiar la URL en `iam/core/agent.py` linea 1770:
```python
proxy_url = "https://iam-proxy.TU-ID.workers.dev"
```

## Testing
```bash
curl https://iam-proxy.TU-ID.workers.dev/health
curl -X POST https://iam-proxy.TU-ID.workers.dev/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"mimo-v2.5-free","messages":[{"role":"user","content":"Hola"}]}'
```

## Ventajas
- Cold start: 0ms (siempre listo)
- Gratis: 100,000 requests/dia
- CORS habilitado por defecto
- HTTPS automatico
