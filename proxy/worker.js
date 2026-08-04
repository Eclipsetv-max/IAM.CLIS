// iam-proxy-worker.js
// Proxy para IAM - Sin cold start en Cloudflare Workers

export default {
  async fetch(request, env) {
    // CORS headers
    const corsHeaders = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    };

    // Handle CORS preflight
    if (request.method === 'OPTIONS') {
      return new Response(null, { headers: corsHeaders });
    }

    const url = new URL(request.url);

    // Health check
    if (url.pathname === '/' || url.pathname === '/health') {
      return new Response(JSON.stringify({
        status: 'ok',
        service: 'IAM Proxy',
        version: '1.0',
        cold_start: '0ms'
      }), {
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }
      });
    }

    // Chat completions endpoint
    if (url.pathname === '/v1/chat/completions' && request.method === 'POST') {
      try {
        const body = await request.json();

        // Validate request
        if (!body.messages || !Array.isArray(body.messages)) {
          return new Response(JSON.stringify({
            error: 'Invalid request: messages array required'
          }), {
            status: 400,
            headers: { ...corsHeaders, 'Content-Type': 'application/json' }
          });
        }

        // Call OpenCode/MiMo API
        const response = await fetch('https://opencode.ai/zen/v1/chat/completions', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${env.OPENCODE_API_KEY}`,
            'Content-Type': 'application/json',
            'HTTP-Referer': 'https://iam-ai.local',
            'X-Title': 'IAM AI Assistant'
          },
          body: JSON.stringify({
            model: body.model || 'mimo-v2.5-free',
            messages: body.messages,
            temperature: body.temperature || 0.7,
            max_tokens: body.max_tokens || 4096,
            top_p: body.top_p || 0.9
          })
        });

        // Return response
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

    // 404 for unknown routes
    return new Response(JSON.stringify({
      error: 'Not found',
      available_endpoints: [
        'GET /',
        'GET /health',
        'POST /v1/chat/completions'
      ]
    }), {
      status: 404,
      headers: { ...corsHeaders, 'Content-Type': 'application/json' }
    });
  }
};
