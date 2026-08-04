// iam-proxy-worker.js
// Proxy para IAM - Sin cold start en Cloudflare Workers

function getDashboard() {
  return `<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>IAM Proxy - Dashboard</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', sans-serif; 
            background: #0a0a0a; 
            color: #fff;
            min-height: 100vh;
        }
        .container { max-width: 900px; margin: 0 auto; padding: 30px; }
        .header { 
            background: linear-gradient(135deg, #1a1a2e, #16213e);
            padding: 40px;
            border-radius: 20px;
            margin-bottom: 30px;
            border: 1px solid #00d4aa;
            text-align: center;
        }
        .header h1 { color: #00d4aa; font-size: 2.5em; margin-bottom: 10px; }
        .header p { color: #888; font-size: 1.1em; }
        .status-badge {
            display: inline-block;
            padding: 10px 25px;
            border-radius: 25px;
            font-weight: bold;
            font-size: 1em;
            margin-top: 20px;
            background: #00ff88;
            color: #000;
        }
        .cards { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; }
        .card {
            background: #1a1a2e;
            padding: 25px;
            border-radius: 15px;
            border: 1px solid #333;
        }
        .card h3 { color: #00d4aa; margin-bottom: 20px; font-size: 1.2em; }
        .endpoint {
            background: #0a0a0a;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 10px;
            font-family: monospace;
            word-break: break-all;
        }
        .endpoint a { color: #00d4aa; text-decoration: none; }
        .endpoint a:hover { text-decoration: underline; }
        .method {
            display: inline-block;
            padding: 3px 8px;
            border-radius: 5px;
            font-size: 0.8em;
            font-weight: bold;
            margin-right: 8px;
        }
        .get { background: #00ff88; color: #000; }
        .post { background: #00aaff; color: #000; }
        .stat { 
            display: flex; 
            justify-content: space-between; 
            padding: 12px 0;
            border-bottom: 1px solid #333;
        }
        .stat:last-child { border-bottom: none; }
        .stat-label { color: #888; }
        .stat-value { color: #fff; font-weight: bold; }
        .footer {
            text-align: center;
            margin-top: 40px;
            padding: 20px;
            color: #555;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>IAM Proxy Server</h1>
            <p>Cloudflare Worker - Sin cold start</p>
            <div class="status-badge">ACTIVO</div>
        </div>
        
        <div class="cards">
            <div class="card">
                <h3>Endpoints</h3>
                <div class="endpoint">
                    <span class="method get">GET</span>
                    <a href="/health">/health</a>
                </div>
                <div class="endpoint">
                    <span class="method get">GET</span>
                    <a href="/v1/models">/v1/models</a>
                </div>
                <div class="endpoint">
                    <span class="method post">POST</span>
                    <a href="/v1/chat/completions">/v1/chat/completions</a>
                </div>
                <div class="endpoint">
                    <span class="method post">POST</span>
                    <a href="/v1/gemini">/v1/gemini</a>
                </div>
            </div>
            
            <div class="card">
                <h3>APIs Configuradas</h3>
                <div class="stat">
                    <span class="stat-label">FreeTheAi</span>
                    <span class="stat-value" style="color:#00ff88">Activa</span>
                </div>
                <div class="stat">
                    <span class="stat-label">Gemini</span>
                    <span class="stat-value" style="color:#00ff88">Activa</span>
                </div>
                <div class="stat">
                    <span class="stat-label">OpenCode/MiMo</span>
                    <span class="stat-value" style="color:#00ff88">Activa</span>
                </div>
            </div>
            
            <div class="card">
                <h3>Info</h3>
                <div class="stat">
                    <span class="stat-label">Servidor</span>
                    <span class="stat-value">Cloudflare Worker</span>
                </div>
                <div class="stat">
                    <span class="stat-label">Latencia</span>
                    <span class="stat-value">~0ms cold start</span>
                </div>
                <div class="stat">
                    <span class="stat-label">Version</span>
                    <span class="stat-value">2.0</span>
                </div>
            </div>
        </div>
        
        <div class="footer">
            IAM Proxy Server 2026 | Powered by Cloudflare Workers
        </div>
    </div>
</body>
</html>`;
}

export default {
  async fetch(request, env) {
    const corsHeaders = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    };

    if (request.method === 'OPTIONS') {
      return new Response(null, { headers: corsHeaders });
    }

    const url = new URL(request.url);

    // Dashboard
    if (url.pathname === '/dashboard' || url.pathname === '/app') {
      return new Response(getDashboard(), {
        headers: { ...corsHeaders, 'Content-Type': 'text/html;charset=UTF-8' }
      });
    }

    // Health check
    if (url.pathname === '/' || url.pathname === '/health') {
      return new Response(JSON.stringify({
        status: 'ok',
        service: 'IAM Proxy',
        version: '2.0',
        dashboard: url.origin + '/dashboard',
        endpoints: ['/v1/chat/completions', '/v1/models', '/v1/gemini'],
        debug: {
          hasOpenCodeKey: !!env.OPENCODE_API_KEY,
          hasFreeTheAiKey: !!env.FREETHEAI_API_KEY,
          openCodeKeyPrefix: env.OPENCODE_API_KEY ? env.OPENCODE_API_KEY.substring(0, 10) + '...' : 'none'
        }
      }), {
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }
      });
    }

    // List models
    if (url.pathname === '/v1/models') {
      try {
        const response = await fetch('https://api.freetheai.xyz/v1/models', {
          headers: {
            'Authorization': 'Bearer ' + env.FREETHEAI_API_KEY,
          }
        });
        const data = await response.json();
        return new Response(JSON.stringify(data), {
          headers: { ...corsHeaders, 'Content-Type': 'application/json' }
        });
      } catch (error) {
        return new Response(JSON.stringify({ error: error.message }), {
          status: 500,
          headers: { ...corsHeaders, 'Content-Type': 'application/json' }
        });
      }
    }

    // Chat completions
    if (url.pathname === '/v1/chat/completions' && request.method === 'POST') {
      try {
        const body = await request.json();

        if (!body.messages || !Array.isArray(body.messages)) {
          return new Response(JSON.stringify({
            error: 'Invalid request: messages array required'
          }), {
            status: 400,
            headers: { ...corsHeaders, 'Content-Type': 'application/json' }
          });
        }

        const model = body.model || 'mimo-v2.5-free';
        let apiUrl;
        let headers = { 'Content-Type': 'application/json' };

        if (model.startsWith('mimo')) {
          apiUrl = 'https://opencode.ai/zen/v1/chat/completions';
          headers['Authorization'] = 'Bearer ' + env.OPENCODE_API_KEY;
          headers['HTTP-Referer'] = 'https://iam-ai.local';
          headers['X-Title'] = 'IAM AI Assistant';
        } else {
          apiUrl = 'https://api.freetheai.xyz/v1/chat/completions';
          headers['Authorization'] = 'Bearer ' + env.FREETHEAI_API_KEY;
        }

        const response = await fetch(apiUrl, {
          method: 'POST',
          headers,
          body: JSON.stringify({
            model,
            messages: body.messages,
            temperature: body.temperature || 0.7,
            max_tokens: body.max_tokens || 4096,
          })
        });

        const data = await response.json();
        return new Response(JSON.stringify(data), {
          status: response.status,
          headers: { ...corsHeaders, 'Content-Type': 'application/json' }
        });

      } catch (error) {
        return new Response(JSON.stringify({
          error: 'Proxy error',
          message: error.message
        }), {
          status: 500,
          headers: { ...corsHeaders, 'Content-Type': 'application/json' }
        });
      }
    }

    // Gemini
    if (url.pathname === '/v1/gemini' && request.method === 'POST') {
      try {
        const body = await request.json();
        const apiKey = env.GEMINI_API_KEY;
        const model = body.model || 'gemini-2.0-flash';
        
        const response = await fetch(
          'https://generativelanguage.googleapis.com/v1beta/models/' + model + ':generateContent?key=' + apiKey,
          {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              contents: [{ parts: [{ text: body.prompt }] }],
              generationConfig: {
                temperature: body.temperature || 0.7,
                maxOutputTokens: body.max_tokens || 2048,
              }
            })
          }
        );

        const data = await response.json();
        const text = data.candidates && data.candidates[0] && data.candidates[0].content && data.candidates[0].content.parts && data.candidates[0].content.parts[0] ? data.candidates[0].content.parts[0].text : '';
        return new Response(JSON.stringify({ response: text }), {
          headers: { ...corsHeaders, 'Content-Type': 'application/json' }
        });

      } catch (error) {
        return new Response(JSON.stringify({ error: error.message }), {
          status: 500,
          headers: { ...corsHeaders, 'Content-Type': 'application/json' }
        });
      }
    }

    return new Response(JSON.stringify({
      error: 'Not found',
      dashboard: url.origin + '/dashboard',
      endpoints: ['GET /health', 'GET /v1/models', 'POST /v1/chat/completions', 'POST /v1/gemini']
    }), {
      status: 404,
      headers: { ...corsHeaders, 'Content-Type': 'application/json' }
    });
  }
};