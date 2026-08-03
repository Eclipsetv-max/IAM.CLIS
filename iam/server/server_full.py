# -*- coding: utf-8 -*-
"""
IAM Proxy Server - Con Dashboard Web
Control total: activar/desactivar, ver estado, gestionar APIs
"""

import os
import json
import time
import requests
from pathlib import Path
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
from functools import wraps

app = Flask(__name__)
CORS(app)

# ============ ESTADO DEL SERVIDOR ============
# False = Mantenimiento, True = Activo
SERVER_ACTIVE = True
START_TIME = time.time()

# ============ API KEYS ============
API_KEYS = {
    'FREETHEAI_API_KEY': os.environ.get('FREETHEAI_API_KEY', ''),
    'GEMINI_API_KEY': os.environ.get('GEMINI_API_KEY', ''),
    'OPENCODE_API_KEY': os.environ.get('OPENCODE_API_KEY', ''),
}

# Password del dashboard (cambiar en produccion)
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'iam2026')

# ============ DECORADOR DE SEGURIDAD ============
def check_maintenance(f):
    """Verificar si el servidor esta activo"""
    @wraps(f)
    def decorated(*args, **kwargs):
        if not SERVER_ACTIVE and request.endpoint not in ['dashboard', 'login', 'toggle_server', 'status_page']:
            return jsonify({
                "error": "Servidor en mantenimiento",
                "status": "maintenance",
                "message": "El servidor esta temporalmente desactivado. Intenta de nuevo mas tarde."
            }), 503
        return f(*args, **kwargs)
    return decorated

# ============ HTML TEMPLATES ============

DASHBOARD_HTML = """
<!DOCTYPE html>
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
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        .header { 
            background: linear-gradient(135deg, #1a1a2e, #16213e);
            padding: 30px;
            border-radius: 15px;
            margin-bottom: 20px;
            border: 1px solid #00d4aa;
        }
        .header h1 { color: #00d4aa; font-size: 2.5em; }
        .header p { color: #888; margin-top: 10px; }
        .status-badge {
            display: inline-block;
            padding: 8px 20px;
            border-radius: 20px;
            font-weight: bold;
            font-size: 1.1em;
            margin-top: 15px;
        }
        .status-active { background: #00ff88; color: #000; }
        .status-maintenance { background: #ff4444; color: #fff; }
        .cards { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }
        .card {
            background: #1a1a2e;
            padding: 25px;
            border-radius: 12px;
            border: 1px solid #333;
        }
        .card h3 { color: #00d4aa; margin-bottom: 15px; }
        .stat { 
            display: flex; 
            justify-content: space-between; 
            padding: 10px 0;
            border-bottom: 1px solid #333;
        }
        .stat:last-child { border-bottom: none; }
        .stat-label { color: #888; }
        .stat-value { color: #fff; font-weight: bold; }
        .btn {
            padding: 12px 30px;
            border: none;
            border-radius: 8px;
            font-size: 1em;
            cursor: pointer;
            font-weight: bold;
            transition: all 0.3s;
        }
        .btn-activate { background: #00ff88; color: #000; }
        .btn-activate:hover { background: #00cc6a; }
        .btn-deactivate { background: #ff4444; color: #fff; }
        .btn-deactivate:hover { background: #cc0000; }
        .btn-secondary { background: #333; color: #fff; }
        .btn-secondary:hover { background: #444; }
        .actions { display: flex; gap: 15px; margin-top: 20px; }
        .api-status { 
            display: flex; 
            align-items: center; 
            gap: 10px;
            padding: 10px;
            background: #0a0a0a;
            border-radius: 8px;
            margin-bottom: 10px;
        }
        .api-dot {
            width: 12px;
            height: 12px;
            border-radius: 50%;
        }
        .api-dot.active { background: #00ff88; }
        .api-dot.inactive { background: #ff4444; }
        .url-box {
            background: #0a0a0a;
            padding: 15px;
            border-radius: 8px;
            font-family: monospace;
            word-break: break-all;
            margin-top: 10px;
        }
        .url-box a { color: #00d4aa; text-decoration: none; }
        .url-box a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>IAM Proxy Server</h1>
            <p>Dashboard de control del servidor proxy</p>
            <div class="status-badge {{ 'status-active' if active else 'status-maintenance' }}">
                {{ 'ACTIVO' if active else 'MANTENIMIENTO' }}
            </div>
        </div>
        
        <div class="cards">
            <div class="card">
                <h3>Estado del Servidor</h3>
                <div class="stat">
                    <span class="stat-label">Estado</span>
                    <span class="stat-value" style="color: {{ '#00ff88' if active else '#ff4444' }}">
                        {{ 'Activo' if active else 'Mantenimiento' }}
                    </span>
                </div>
                <div class="stat">
                    <span class="stat-label">Tiempo activo</span>
                    <span class="stat-value">{{ uptime }}</span>
                </div>
                <div class="stat">
                    <span class="stat-label">URL del servidor</span>
                    <span class="stat-value" style="font-size: 0.8em;">{{ server_url }}</span>
                </div>
                <div class="actions">
                    {% if active %}
                    <button class="btn btn-deactivate" onclick="toggleServer()">
                        Desactivar Servidor
                    </button>
                    {% else %}
                    <button class="btn btn-activate" onclick="toggleServer()">
                        Activar Servidor
                    </button>
                    {% endif %}
                </div>
            </div>
            
            <div class="card">
                <h3>APIs Configuradas</h3>
                <div class="api-status">
                    <div class="api-dot {{ 'active' if freetheai else 'inactive' }}"></div>
                    <span>FreeTheAi</span>
                    <span style="margin-left: auto; color: #888;">{{ 'Configurada' if freetheai else 'No configurada' }}</span>
                </div>
                <div class="api-status">
                    <div class="api-dot {{ 'active' if gemini else 'inactive' }}"></div>
                    <span>Gemini</span>
                    <span style="margin-left: auto; color: #888;">{{ 'Configurada' if gemini else 'No configurada' }}</span>
                </div>
                <div class="api-status">
                    <div class="api-dot {{ 'active' if opencode else 'inactive' }}"></div>
                    <span>OpenCode/Mimo</span>
                    <span style="margin-left: auto; color: #888;">{{ 'Configurada' if opencode else 'No configurada' }}</span>
                </div>
            </div>
            
            <div class="card">
                <h3>Endpoints</h3>
                <div class="url-box">
                    <a href="{{ server_url }}/v1/chat/completions" target="_blank">
                        POST /v1/chat/completions
                    </a>
                </div>
                <div class="url-box">
                    <a href="{{ server_url }}/v1/models" target="_blank">
                        GET /v1/models
                    </a>
                </div>
                <div class="url-box">
                    <a href="{{ server_url }}/v1/gemini" target="_blank">
                        POST /v1/gemini
                    </a>
                </div>
            </div>
            
            <div class="card">
                <h3>Como usar en IAM</h3>
                <div class="url-box" style="font-size: 0.9em;">
                    1. Abre IAM CLI<br>
                    2. Ejecuta: /engine freetheai<br>
                    3. O configura en .env:<br>
                    FREETHEAI_PROXY_URL={{ server_url }}
                </div>
            </div>
        </div>
    </div>
    
    <script>
        async function toggleServer() {
            const password = prompt('Password del admin:');
            if (!password) return;
            
            try {
                const response = await fetch('/admin/toggle', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ password })
                });
                
                const data = await response.json();
                if (data.success) {
                    location.reload();
                } else {
                    alert('Error: ' + (data.error || 'Password incorrecto'));
                }
            } catch (e) {
                alert('Error de conexion');
            }
        }
    </script>
</body>
</html>
"""

STATUS_PAGE_HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>IAM - Mantenimiento</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', sans-serif; 
            background: #0a0a0a; 
            color: #fff;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .maintenance {
            text-align: center;
            padding: 40px;
            max-width: 600px;
        }
        .icon { font-size: 5em; margin-bottom: 20px; }
        h1 { color: #ff4444; margin-bottom: 15px; }
        p { color: #888; line-height: 1.6; }
        .status-box {
            background: #1a1a2e;
            padding: 20px;
            border-radius: 12px;
            margin-top: 30px;
            border: 1px solid #333;
        }
        .status-item {
            display: flex;
            justify-content: space-between;
            padding: 10px 0;
            border-bottom: 1px solid #333;
        }
        .status-item:last-child { border-bottom: none; }
    </style>
</head>
<body>
    <div class="maintenance">
        <div class="icon">🔧</div>
        <h1>En Mantenimiento</h1>
        <p>El servidor esta temporalmente desactivado.<br>Intenta de nuevo mas tarde.</p>
        
        <div class="status-box">
            <div class="status-item">
                <span>Estado</span>
                <span style="color: #ff4444;">Inactivo</span>
            </div>
            <div class="status-item">
                <span>Servidor</span>
                <span>{{ server_name }}</span>
            </div>
        </div>
    </div>
</body>
</html>
"""

# ============ RUTAS DEL DASHBOARD ============

@app.route('/dashboard')
def dashboard():
    """Dashboard de administracion"""
    uptime_seconds = int(time.time() - START_TIME)
    hours = uptime_seconds // 3600
    minutes = (uptime_seconds % 3600) // 60
    
    server_url = os.environ.get('SERVER_URL', 'http://localhost:5000')
    
    return render_template_string(
        DASHBOARD_HTML,
        active=SERVER_ACTIVE,
        uptime=f"{hours}h {minutes}m",
        server_url=server_url,
        freetheai=bool(API_KEYS.get('FREETHEAI_API_KEY')),
        gemini=bool(API_KEYS.get('GEMINI_API_KEY')),
        opencode=bool(API_KEYS.get('OPENCODE_API_KEY'))
    )

@app.route('/admin/toggle', methods=['POST'])
def toggle_server():
    """Activar/desactivar servidor"""
    global SERVER_ACTIVE
    
    data = request.json
    password = data.get('password', '')
    
    if password != ADMIN_PASSWORD:
        return jsonify({"error": "Password incorrecto", "success": False}), 401
    
    SERVER_ACTIVE = not SERVER_ACTIVE
    return jsonify({
        "success": True,
        "new_state": "active" if SERVER_ACTIVE else "maintenance"
    })

# ============ API ENDPOINTS ============

@app.route('/')
def index():
    """Info del servidor"""
    if not SERVER_ACTIVE:
        return jsonify({
            "status": "maintenance",
            "message": "Servidor en mantenimiento"
        }), 503
    
    return jsonify({
        "name": "IAM Proxy Server",
        "version": "1.0",
        "status": "active",
        "dashboard": "/dashboard"
    })

@app.route('/health')
def health():
    """Health check"""
    return jsonify({
        "status": "active" if SERVER_ACTIVE else "maintenance"
    })

@app.route('/status')
def status_page():
    """Pagina de estado para usuarios"""
    if SERVER_ACTIVE:
        return jsonify({"status": "active"})
    else:
        return render_template_string(
            STATUS_PAGE_HTML,
            server_name="IAM Proxy"
        ), 503

@app.route('/v1/models')
@check_maintenance
def list_models():
    """Listar modelos"""
    api_key = API_KEYS.get('FREETHEAI_API_KEY', '')
    if not api_key:
        return jsonify({"error": "FreeTheAi API key not configured"}), 500
    
    try:
        response = requests.get(
            "https://api.freetheai.xyz/v1/models",
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=10
        )
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/v1/chat/completions', methods=['POST'])
@check_maintenance
def chat_completions():
    """Proxy para chat"""
    data = request.json
    
    if not data or 'messages' not in data:
        return jsonify({"error": "Invalid request"}), 400
    
    model = data.get('model', 'opc/deepseek-v4-flash-free')
    
    if any(model.startswith(p) for p in ['opc/', 'glm/', 'bbl/', 'rev/', 'olm/', 'min/', 'mim/']):
        api_key = API_KEYS.get('FREETHEAI_API_KEY', '')
        base_url = "https://api.freetheai.xyz/v1"
    elif model.startswith('mimo'):
        api_key = API_KEYS.get('OPENCODE_API_KEY', '')
        base_url = "https://opencode.ai/zen/v1"
    else:
        api_key = API_KEYS.get('FREETHEAI_API_KEY', '')
        base_url = "https://api.freetheai.xyz/v1"
    
    if not api_key:
        return jsonify({"error": "API key not configured"}), 500
    
    try:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        if "opencode.ai" in base_url:
            headers["HTTP-Referer"] = "https://iam-ai.local"
            headers["X-Title"] = "IAM AI Assistant"
        
        response = requests.post(
            f"{base_url}/chat/completions",
            headers=headers,
            json=data,
            timeout=120
        )
        
        return jsonify(response.json())
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/v1/gemini', methods=['POST'])
@check_maintenance
def gemini_chat():
    """Proxy para Gemini"""
    data = request.json
    
    api_key = API_KEYS.get('GEMINI_API_KEY', '')
    if not api_key:
        return jsonify({"error": "Gemini API key not configured"}), 500
    
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        
        model = genai.GenerativeModel(data.get('model', 'gemini-2.0-flash'))
        
        prompt = data.get('prompt', '')
        system = data.get('system_prompt', '')
        
        if system:
            prompt = f"[System]: {system}\n\n[User]: {prompt}"
        
        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": data.get('temperature', 0.7),
                "max_output_tokens": data.get('max_tokens', 2048),
            }
        )
        
        return jsonify({"response": response.text})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    
    print("=" * 50)
    print("IAM Proxy Server v2.0")
    print("=" * 50)
    print(f"Puerto: {port}")
    print(f"Dashboard: http://localhost:{port}/dashboard")
    print(f"Password: {ADMIN_PASSWORD}")
    print("=" * 50)
    
    app.run(host='0.0.0.0', port=port, debug=False)
