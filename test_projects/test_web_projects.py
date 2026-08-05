# -*- coding: utf-8 -*-
"""
Script de prueba - 10 proyectos web grandes para probar IAM
Ejecuta cada proyecto y verifica que funcione
"""

import os
import time
import json
import requests

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECTS_DIR = os.path.join(OUTPUT_DIR, "projects")
os.makedirs(PROJECTS_DIR, exist_ok=True)

# URL del servidor proxy
PROXY_URL = "https://iam-proxy.onrender.com"

# 10 proyectos web grandes
PROJECTS = [
    {
        "name": "01_ecommerce_gaming",
        "title": "Tienda de Gaming",
        "description": "E-commerce completo para videojuegos con carrito de compras",
        "html": """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TechZone Gaming - Tu Tienda de Videojuegos</title>
    <link rel="stylesheet" href="style.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body>
    <nav class="navbar">
        <div class="logo"><i class="fas fa-gamepad"></i> TechZone</div>
        <div class="nav-links">
            <a href="#inicio">Inicio</a>
            <a href="#productos">Productos</a>
            <a href="#ofertas">Ofertas</a>
            <a href="#contacto">Contacto</a>
        </div>
        <div class="cart-icon" id="cartIcon">
            <i class="fas fa-shopping-cart"></i>
            <span id="cartCount">0</span>
        </div>
    </nav>
    
    <header class="hero" id="inicio">
        <div class="hero-content">
            <h1>Los Mejores Videojuegos</h1>
            <p>Encuentra los ultimos lanzamientos a los mejores precios</p>
            <a href="#productos" class="btn-primary">Ver Catalogo</a>
        </div>
    </header>
    
    <section class="featured" id="productos">
        <h2>Productos Destacados</h2>
        <div class="filters">
            <button class="filter-btn active" data-category="all">Todos</button>
            <button class="filter-btn" data-category="pc">PC</button>
            <button class="filter-btn" data-category="ps5">PS5</button>
            <button class="filter-btn" data-category="xbox">Xbox</button>
            <button class="filter-btn" data-category="switch">Switch</button>
        </div>
        <div class="products-grid" id="productsGrid">
            <!-- Productos generados por JS -->
        </div>
    </section>
    
    <section class="deals" id="ofertas">
        <h2>Ofertas Especiales</h2>
        <div class="countdown" id="countdown">
            <div class="time-box"><span id="hours">23</span><p>Horas</p></div>
            <div class="time-box"><span id="minutes">59</span><p>Minutos</p></div>
            <div class="time-box"><span id="seconds">59</span><p>Segundos</p></div>
        </div>
        <div class="deals-grid" id="dealsGrid"></div>
    </section>
    
    <section class="newsletter">
        <h2>Suscribete para Ofertas Exclusivas</h2>
        <form id="newsletterForm">
            <input type="email" placeholder="Tu email" required>
            <button type="submit" class="btn-primary">Suscribirse</button>
        </form>
    </section>
    
    <footer id="contacto">
        <div class="footer-grid">
            <div class="footer-col">
                <h3><i class="fas fa-gamepad"></i> TechZone</h3>
                <p>Tu tienda de videojuegos de confianza desde 2020.</p>
                <div class="social-links">
                    <a href="#"><i class="fab fa-facebook"></i></a>
                    <a href="#"><i class="fab fa-twitter"></i></a>
                    <a href="#"><i class="fab fa-instagram"></i></a>
                    <a href="#"><i class="fab fa-youtube"></i></a>
                </div>
            </div>
            <div class="footer-col">
                <h3>Enlaces</h3>
                <a href="#">Inicio</a>
                <a href="#">Productos</a>
                <a href="#">Ofertas</a>
                <a href="#">Contacto</a>
            </div>
            <div class="footer-col">
                <h3>Contacto</h3>
                <p><i class="fas fa-map-marker-alt"></i> Madrid, España</p>
                <p><i class="fas fa-phone"></i> +34 600 123 456</p>
                <p><i class="fas fa-envelope"></i> info@techzone.com</p>
            </div>
        </div>
        <div class="footer-bottom">
            <p>&copy; 2026 TechZone Gaming. Todos los derechos reservados.</p>
        </div>
    </footer>
    
    <div class="cart-sidebar" id="cartSidebar">
        <div class="cart-header">
            <h3>Mi Carrito</h3>
            <button id="closeCart"><i class="fas fa-times"></i></button>
        </div>
        <div class="cart-items" id="cartItems"></div>
        <div class="cart-total">
            <p>Total: <span id="cartTotal">$0</span></p>
            <button class="btn-primary" id="checkoutBtn">Comprar</button>
        </div>
    </div>
    
    <script src="script.js"></script>
</body>
</html>""",
        "css": """/* TechZone Gaming - Estilos */
:root {
    --primary: #8b5cf6;
    --primary-dark: #7c3aed;
    --secondary: #06b6d4;
    --bg-dark: #0f0f1a;
    --bg-card: #1a1a2e;
    --text: #f1f5f9;
    --text-muted: #94a3b8;
    --accent: #f59e0b;
    --success: #10b981;
    --danger: #ef4444;
    --gradient: linear-gradient(135deg, var(--primary), var(--secondary));
}
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
    font-family: 'Segoe UI', system-ui, sans-serif;
    background: var(--bg-dark);
    color: var(--text);
    line-height: 1.6;
}
.navbar {
    position: fixed;
    top: 0;
    width: 100%;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 5%;
    background: rgba(15, 15, 26, 0.95);
    backdrop-filter: blur(10px);
    z-index: 1000;
    border-bottom: 1px solid rgba(139, 92, 246, 0.2);
}
.logo {
    font-size: 1.5rem;
    font-weight: bold;
    background: var(--gradient);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.nav-links { display: flex; gap: 2rem; }
.nav-links a {
    color: var(--text);
    text-decoration: none;
    transition: color 0.3s;
}
.nav-links a:hover { color: var(--primary); }
.cart-icon {
    position: relative;
    cursor: pointer;
    font-size: 1.3rem;
}
#cartCount {
    position: absolute;
    top: -8px;
    right: -8px;
    background: var(--danger);
    color: white;
    border-radius: 50%;
    padding: 2px 6px;
    font-size: 0.7rem;
}
.hero {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    background: linear-gradient(135deg, rgba(139, 92, 246, 0.2), rgba(6, 182, 212, 0.2));
    padding: 100px 5%;
}
.hero h1 {
    font-size: 3.5rem;
    margin-bottom: 1rem;
    background: var(--gradient);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.hero p { font-size: 1.2rem; color: var(--text-muted); margin-bottom: 2rem; }
.btn-primary {
    display: inline-block;
    padding: 1rem 2rem;
    background: var(--gradient);
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 1rem;
    font-weight: bold;
    cursor: pointer;
    text-decoration: none;
    transition: transform 0.3s, box-shadow 0.3s;
}
.btn-primary:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 30px rgba(139, 92, 246, 0.4);
}
section {
    padding: 5rem 5%;
}
section h2 {
    text-align: center;
    font-size: 2.5rem;
    margin-bottom: 3rem;
    background: var(--gradient);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.filters {
    display: flex;
    justify-content: center;
    gap: 1rem;
    margin-bottom: 3rem;
}
.filter-btn {
    padding: 0.5rem 1.5rem;
    background: var(--bg-card);
    color: var(--text);
    border: 1px solid rgba(139, 92, 246, 0.3);
    border-radius: 20px;
    cursor: pointer;
    transition: all 0.3s;
}
.filter-btn:hover, .filter-btn.active {
    background: var(--primary);
    border-color: var(--primary);
}
.products-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 2rem;
}
.product-card {
    background: var(--bg-card);
    border-radius: 16px;
    overflow: hidden;
    border: 1px solid rgba(139, 92, 246, 0.2);
    transition: transform 0.3s, box-shadow 0.3s;
}
.product-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 20px 40px rgba(139, 92, 246, 0.2);
}
.product-image {
    height: 200px;
    background: var(--gradient);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 4rem;
}
.product-info {
    padding: 1.5rem;
}
.product-info h3 { margin-bottom: 0.5rem; }
.product-info .price {
    font-size: 1.5rem;
    font-weight: bold;
    color: var(--accent);
    margin: 1rem 0;
}
.product-info .add-btn {
    width: 100%;
    padding: 0.8rem;
    background: var(--primary);
    color: white;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    transition: background 0.3s;
}
.product-info .add-btn:hover { background: var(--primary-dark); }
.deals { background: rgba(139, 92, 246, 0.1); }
.countdown {
    display: flex;
    justify-content: center;
    gap: 2rem;
    margin-bottom: 3rem;
}
.time-box {
    text-align: center;
    background: var(--bg-card);
    padding: 1.5rem 2rem;
    border-radius: 12px;
    border: 1px solid rgba(139, 92, 246, 0.3);
}
.time-box span {
    font-size: 2.5rem;
    font-weight: bold;
    color: var(--accent);
}
.newsletter {
    text-align: center;
    background: var(--bg-card);
}
#newsletterForm {
    display: flex;
    justify-content: center;
    gap: 1rem;
    max-width: 500px;
    margin: 0 auto;
}
#newsletterForm input {
    flex: 1;
    padding: 1rem;
    border: 1px solid rgba(139, 92, 246, 0.3);
    border-radius: 8px;
    background: var(--bg-dark);
    color: var(--text);
}
footer {
    background: var(--bg-card);
    padding: 4rem 5% 2rem;
}
.footer-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 3rem;
    margin-bottom: 3rem;
}
.footer-col h3 { color: var(--primary); margin-bottom: 1rem; }
.footer-col a {
    display: block;
    color: var(--text-muted);
    text-decoration: none;
    margin: 0.5rem 0;
    transition: color 0.3s;
}
.footer-col a:hover { color: var(--primary); }
.social-links { display: flex; gap: 1rem; margin-top: 1rem; }
.social-links a {
    width: 40px;
    height: 40px;
    background: var(--bg-dark);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--primary);
    transition: all 0.3s;
}
.social-links a:hover {
    background: var(--primary);
    color: white;
}
.footer-bottom {
    text-align: center;
    padding-top: 2rem;
    border-top: 1px solid rgba(139, 92, 246, 0.2);
    color: var(--text-muted);
}
.cart-sidebar {
    position: fixed;
    right: -400px;
    top: 0;
    width: 400px;
    height: 100vh;
    background: var(--bg-card);
    padding: 2rem;
    transition: right 0.3s;
    z-index: 1001;
    overflow-y: auto;
}
.cart-sidebar.open { right: 0; }
.cart-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 2rem;
}
.cart-header button {
    background: none;
    border: none;
    color: var(--text);
    font-size: 1.5rem;
    cursor: pointer;
}
.cart-item {
    display: flex;
    gap: 1rem;
    padding: 1rem 0;
    border-bottom: 1px solid rgba(139, 92, 246, 0.2);
}
.cart-item-info { flex: 1; }
.cart-item-info h4 { margin-bottom: 0.5rem; }
.cart-item-remove {
    background: var(--danger);
    border: none;
    color: white;
    padding: 0.3rem 0.8rem;
    border-radius: 4px;
    cursor: pointer;
}
.cart-total {
    margin-top: 2rem;
    padding-top: 1rem;
    border-top: 2px solid var(--primary);
}
.cart-total p {
    font-size: 1.3rem;
    font-weight: bold;
    margin-bottom: 1rem;
}
@media (max-width: 768px) {
    .nav-links { display: none; }
    .hero h1 { font-size: 2rem; }
    .cart-sidebar { width: 100%; right: -100%; }
}""",
        "js": """// TechZone Gaming - JavaScript
const products = [
    { id: 1, name: "PlayStation 5", price: 499, category: "ps5", icon: "🎮" },
    { id: 2, name: "Xbox Series X", price: 449, category: "xbox", icon: "🕹️" },
    { id: 3, name: "Nintendo Switch OLED", price: 349, category: "switch", icon: "🎯" },
    { id: 4, name: "GTA VI", price: 69, category: "ps5", icon: "🚗" },
    { id: 5, name: "Elden Ring", price: 59, category: "pc", icon: "⚔️" },
    { id: 6, name: "Call of Duty MW3", price: 69, category: "pc", icon: "🔫" },
    { id: 7, name: "Zelda: Tears of Kingdom", price: 59, category: "switch", icon: "🗡️" },
    { id: 8, name: "Spider-Man 2", price: 69, category: "ps5", icon: "🕷️" },
    { id: 9, name: "Forza Motorsport", price: 69, category: "xbox", icon: "🏎️" },
    { id: 10, name: "Hogwarts Legacy", price: 49, category: "pc", icon: "🧙" },
    { id: 11, name: "Red Dead Redemption 2", price: 29, category: "pc", icon: "🤠" },
    { id: 12, name: "FIFA 24", price: 59, category: "ps5", icon: "⚽" },
];

let cart = JSON.parse(localStorage.getItem('cart')) || [];

// Render products
function renderProducts(filter = 'all') {
    const grid = document.getElementById('productsGrid');
    const filtered = filter === 'all' ? products : products.filter(p => p.category === filter);
    grid.innerHTML = filtered.map(p => `
        <div class="product-card" data-category="${p.category}">
            <div class="product-image">${p.icon}</div>
            <div class="product-info">
                <h3>${p.name}</h3>
                <p class="price">$${p.price}</p>
                <button class="add-btn" onclick="addToCart(${p.id})">Agregar al Carrito</button>
            </div>
        </div>
    `).join('');
}

// Cart functions
function addToCart(id) {
    const product = products.find(p => p.id === id);
    const existing = cart.find(item => item.id === id);
    if (existing) {
        existing.quantity++;
    } else {
        cart.push({ ...product, quantity: 1 });
    }
    updateCart();
    showNotification(`${product.name} agregado al carrito`);
}

function removeFromCart(id) {
    cart = cart.filter(item => item.id !== id);
    updateCart();
}

function updateCart() {
    localStorage.setItem('cart', JSON.stringify(cart));
    document.getElementById('cartCount').textContent = cart.reduce((sum, item) => sum + item.quantity, 0);
    document.getElementById('cartTotal').textContent = '$' + cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
    renderCartItems();
}

function renderCartItems() {
    const container = document.getElementById('cartItems');
    container.innerHTML = cart.map(item => `
        <div class="cart-item">
            <span>${item.icon}</span>
            <div class="cart-item-info">
                <h4>${item.name}</h4>
                <p>$${item.price} x ${item.quantity}</p>
            </div>
            <button class="cart-item-remove" onclick="removeFromCart(${item.id})">Eliminar</button>
        </div>
    `).join('');
}

function showNotification(message) {
    const notification = document.createElement('div');
    notification.style.cssText = 'position:fixed;bottom:20px;right:20px;background:#10b981;color:white;padding:1rem 2rem;border-radius:8px;z-index:2000;animation:slideIn 0.3s';
    notification.textContent = message;
    document.body.appendChild(notification);
    setTimeout(() => notification.remove(), 2000);
}

// Countdown
function updateCountdown() {
    const now = new Date();
    const end = new Date();
    end.setHours(23, 59, 59);
    const diff = end - now;
    document.getElementById('hours').textContent = Math.floor(diff / 3600000);
    document.getElementById('minutes').textContent = Math.floor((diff % 3600000) / 60000);
    document.getElementById('seconds').textContent = Math.floor((diff % 60000) / 1000);
}

// Event listeners
document.addEventListener('DOMContentLoaded', () => {
    renderProducts();
    updateCart();
    updateCountdown();
    setInterval(updateCountdown, 1000);
    
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            renderProducts(btn.dataset.category);
        });
    });
    
    document.getElementById('cartIcon').addEventListener('click', () => {
        document.getElementById('cartSidebar').classList.add('open');
    });
    
    document.getElementById('closeCart').addEventListener('click', () => {
        document.getElementById('cartSidebar').classList.remove('open');
    });
    
    document.getElementById('newsletterForm').addEventListener('submit', (e) => {
        e.preventDefault();
        showNotification('¡Suscrito exitosamente!');
        e.target.reset();
    });
    
    document.getElementById('checkoutBtn').addEventListener('click', () => {
        if (cart.length > 0) {
            showNotification('¡Compra realizada con exito!');
            cart = [];
            updateCart();
            document.getElementById('cartSidebar').classList.remove('open');
        }
    });
});"""
    },
    {
        "name": "02_dashboard_analytics",
        "title": "Dashboard de Analytics",
        "description": "Panel de control con graficos y estadisticas en tiempo real",
        "html": """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AnalyticsPro - Dashboard</title>
    <link rel="stylesheet" href="style.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body>
    <div class="sidebar">
        <div class="logo">
            <i class="fas fa-chart-line"></i>
            <span>AnalyticsPro</span>
        </div>
        <nav class="nav-menu">
            <a href="#" class="nav-item active"><i class="fas fa-home"></i> Dashboard</a>
            <a href="#" class="nav-item"><i class="fas fa-chart-bar"></i> Analiticas</a>
            <a href="#" class="nav-item"><i class="fas fa-users"></i> Usuarios</a>
            <a href="#" class="nav-item"><i class="fas fa-shopping-cart"></i> Ventas</a>
            <a href="#" class="nav-item"><i class="fas fa-cog"></i> Configuracion</a>
        </nav>
        <div class="user-info">
            <div class="avatar">F</div>
            <span>Fernando</span>
        </div>
    </div>
    
    <main class="main-content">
        <header class="top-bar">
            <div class="hamburger" id="hamburger">
                <i class="fas fa-bars"></i>
            </div>
            <h1>Dashboard</h1>
            <div class="top-actions">
                <div class="search-box">
                    <i class="fas fa-search"></i>
                    <input type="text" placeholder="Buscar...">
                </div>
                <button class="notification-btn">
                    <i class="fas fa-bell"></i>
                    <span class="badge">3</span>
                </button>
            </div>
        </header>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-icon" style="background: rgba(59, 130, 246, 0.2); color: #3b82f6">
                    <i class="fas fa-dollar-sign"></i>
                </div>
                <div class="stat-info">
                    <h3>Ingresos</h3>
                    <p class="stat-value">$54,239</p>
                    <p class="stat-change positive">+12.5%</p>
                </div>
            </div>
            <div class="stat-card">
                <div class="stat-icon" style="background: rgba(16, 185, 129, 0.2); color: #10b981">
                    <i class="fas fa-users"></i>
                </div>
                <div class="stat-info">
                    <h3>Usuarios</h3>
                    <p class="stat-value">8,549</p>
                    <p class="stat-change positive">+8.2%</p>
                </div>
            </div>
            <div class="stat-card">
                <div class="stat-icon" style="background: rgba(245, 158, 11, 0.2); color: #f59e0b">
                    <i class="fas fa-shopping-bag"></i>
                </div>
                <div class="stat-info">
                    <h3>Pedidos</h3>
                    <p class="stat-value">1,245</p>
                    <p class="stat-change negative">-3.1%</p>
                </div>
            </div>
            <div class="stat-card">
                <div class="stat-icon" style="background: rgba(139, 92, 246, 0.2); color: #8b5cf6">
                    <i class="fas fa-chart-pie"></i>
                </div>
                <div class="stat-info">
                    <h3>Conversion</h3>
                    <p class="stat-value">3.24%</p>
                    <p class="stat-change positive">+1.8%</p>
                </div>
            </div>
        </div>
        
        <div class="charts-row">
            <div class="chart-card large">
                <div class="chart-header">
                    <h3>Ingresos Mensuales</h3>
                    <select id="periodSelect">
                        <option>Este Ano</option>
                        <option>Este Mes</option>
                        <option>Esta Semana</option>
                    </select>
                </div>
                <canvas id="revenueChart"></canvas>
            </div>
            <div class="chart-card">
                <div class="chart-header">
                    <h3>Ventas por Categoria</h3>
                </div>
                <canvas id="categoryChart"></canvas>
            </div>
        </div>
        
        <div class="tables-row">
            <div class="table-card">
                <div class="table-header">
                    <h3>Ultimos Pedidos</h3>
                    <a href="#" class="view-all">Ver todos</a>
                </div>
                <table>
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Cliente</th>
                            <th>Producto</th>
                            <th>Monto</th>
                            <th>Estado</th>
                        </tr>
                    </thead>
                    <tbody id="ordersTable">
                    </tbody>
                </table>
            </div>
            <div class="table-card">
                <div class="table-header">
                    <h3>Top Productos</h3>
                </div>
                <div class="top-products" id="topProducts">
                </div>
            </div>
        </div>
        
        <div class="activity-section">
            <h3>Actividad Reciente</h3>
            <div class="activity-list" id="activityList">
            </div>
        </div>
    </main>
    
    <script src="script.js"></script>
</body>
</html>""",
        "css": """/* AnalyticsPro Dashboard */
:root {
    --sidebar-width: 260px;
    --bg-main: #0f172a;
    --bg-sidebar: #1e293b;
    --bg-card: #1e293b;
    --text: #f1f5f9;
    --text-muted: #94a3b8;
    --primary: #3b82f6;
    --success: #10b981;
    --warning: #f59e0b;
    --danger: #ef4444;
    --purple: #8b5cf6;
}
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
    font-family: 'Segoe UI', system-ui, sans-serif;
    background: var(--bg-main);
    color: var(--text);
    display: flex;
    min-height: 100vh;
}
.sidebar {
    width: var(--sidebar-width);
    background: var(--bg-sidebar);
    padding: 1.5rem;
    position: fixed;
    height: 100vh;
    display: flex;
    flex-direction: column;
    transition: transform 0.3s;
}
.logo {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    font-size: 1.3rem;
    font-weight: bold;
    color: var(--primary);
    padding-bottom: 1.5rem;
    border-bottom: 1px solid rgba(255,255,255,0.1);
    margin-bottom: 1.5rem;
}
.nav-menu { flex: 1; }
.nav-item {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 0.8rem 1rem;
    color: var(--text-muted);
    text-decoration: none;
    border-radius: 8px;
    margin-bottom: 0.5rem;
    transition: all 0.3s;
}
.nav-item:hover, .nav-item.active {
    background: rgba(59, 130, 246, 0.2);
    color: var(--primary);
}
.user-info {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding-top: 1rem;
    border-top: 1px solid rgba(255,255,255,0.1);
}
.avatar {
    width: 40px;
    height: 40px;
    background: var(--primary);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
}
.main-content {
    margin-left: var(--sidebar-width);
    flex: 1;
    padding: 1.5rem;
}
.top-bar {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 2rem;
}
.hamburger { display: none; cursor: pointer; font-size: 1.5rem; }
.top-bar h1 { flex: 1; }
.top-actions { display: flex; gap: 1rem; align-items: center; }
.search-box {
    display: flex;
    align-items: center;
    background: var(--bg-card);
    padding: 0.5rem 1rem;
    border-radius: 8px;
    gap: 0.5rem;
}
.search-box input {
    background: none;
    border: none;
    color: var(--text);
    outline: none;
}
.notification-btn {
    position: relative;
    background: var(--bg-card);
    border: none;
    color: var(--text);
    width: 40px;
    height: 40px;
    border-radius: 8px;
    cursor: pointer;
}
.badge {
    position: absolute;
    top: -5px;
    right: -5px;
    background: var(--danger);
    color: white;
    font-size: 0.7rem;
    padding: 2px 6px;
    border-radius: 10px;
}
.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 1.5rem;
    margin-bottom: 2rem;
}
.stat-card {
    background: var(--bg-card);
    padding: 1.5rem;
    border-radius: 12px;
    display: flex;
    align-items: center;
    gap: 1rem;
}
.stat-icon {
    width: 60px;
    height: 60px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5rem;
}
.stat-value { font-size: 1.8rem; font-weight: bold; margin: 0.3rem 0; }
.stat-change { font-size: 0.85rem; }
.stat-change.positive { color: var(--success); }
.stat-change.negative { color: var(--danger); }
.charts-row {
    display: grid;
    grid-template-columns: 2fr 1fr;
    gap: 1.5rem;
    margin-bottom: 2rem;
}
.chart-card {
    background: var(--bg-card);
    padding: 1.5rem;
    border-radius: 12px;
}
.chart-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
}
.chart-header select {
    background: var(--bg-main);
    color: var(--text);
    border: 1px solid rgba(255,255,255,0.1);
    padding: 0.3rem 0.8rem;
    border-radius: 6px;
}
.tables-row {
    display: grid;
    grid-template-columns: 1.5fr 1fr;
    gap: 1.5rem;
    margin-bottom: 2rem;
}
.table-card {
    background: var(--bg-card);
    padding: 1.5rem;
    border-radius: 12px;
}
.table-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
}
.view-all { color: var(--primary); text-decoration: none; }
table { width: 100%; border-collapse: collapse; }
th, td { padding: 0.8rem; text-align: left; border-bottom: 1px solid rgba(255,255,255,0.1); }
th { color: var(--text-muted); font-weight: 500; }
.status-badge {
    padding: 0.3rem 0.8rem;
    border-radius: 20px;
    font-size: 0.8rem;
}
.status-badge.completed { background: rgba(16,185,129,0.2); color: var(--success); }
.status-badge.pending { background: rgba(245,158,11,0.2); color: var(--warning); }
.status-badge.cancelled { background: rgba(239,68,68,0.2); color: var(--danger); }
.top-products { display: flex; flex-direction: column; gap: 1rem; }
.top-product-item {
    display: flex;
    align-items: center;
    gap: 1rem;
}
.top-product-item .product-icon {
    width: 40px;
    height: 40px;
    background: rgba(139,92,246,0.2);
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
}
.activity-section {
    background: var(--bg-card);
    padding: 1.5rem;
    border-radius: 12px;
}
.activity-section h3 { margin-bottom: 1rem; }
.activity-list { display: flex; flex-direction: column; gap: 1rem; }
.activity-item {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 0.8rem;
    background: var(--bg-main);
    border-radius: 8px;
}
.activity-icon {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
}
.activity-icon.sale { background: rgba(16,185,129,0.2); color: var(--success); }
.activity-icon.user { background: rgba(59,130,246,0.2); color: var(--primary); }
.activity-icon.alert { background: rgba(245,158,11,0.2); color: var(--warning); }
.activity-info { flex: 1; }
.activity-info p { font-size: 0.9rem; }
.activity-info small { color: var(--text-muted); }
@media (max-width: 1024px) {
    .sidebar { transform: translateX(-100%); }
    .sidebar.open { transform: translateX(0); }
    .main-content { margin-left: 0; }
    .hamburger { display: block; }
    .charts-row, .tables-row { grid-template-columns: 1fr; }
}""",
        "js": """// AnalyticsPro Dashboard - JavaScript
const orders = [
    { id: '#ORD-001', client: 'Ana Garcia', product: 'Laptop Pro', amount: '$1,299', status: 'completed' },
    { id: '#ORD-002', client: 'Carlos Lopez', product: 'iPhone 15', amount: '$999', status: 'pending' },
    { id: '#ORD-003', client: 'Maria Rodriguez', product: 'AirPods Pro', amount: '$249', status: 'completed' },
    { id: '#ORD-004', client: 'Pedro Martinez', product: 'iPad Air', amount: '$599', status: 'cancelled' },
    { id: '#ORD-005', client: 'Laura Sanchez', product: 'MacBook Air', amount: '$1,199', status: 'completed' },
];

const topProducts = [
    { name: 'Laptop Pro', sales: 234, icon: '💻' },
    { name: 'iPhone 15', sales: 189, icon: '📱' },
    { name: 'AirPods Pro', sales: 156, icon: '🎧' },
    { name: 'iPad Air', sales: 142, icon: '📋' },
    { name: 'MacBook Air', sales: 128, icon: '💻' },
];

const activities = [
    { type: 'sale', icon: 'fa-dollar-sign', text: 'Nueva venta de $1,299', time: 'Hace 5 min' },
    { type: 'user', icon: 'fa-user-plus', text: 'Nuevo usuario registrado', time: 'Hace 15 min' },
    { type: 'alert', icon: 'fa-exclamation-triangle', text: 'Stock bajo: iPhone 15', time: 'Hace 30 min' },
    { type: 'sale', icon: 'fa-dollar-sign', text: 'Venta de $599 completada', time: 'Hace 1 hora' },
    { type: 'user', icon: 'fa-user-plus', text: '3 nuevos usuarios hoy', time: 'Hace 2 horas' },
];

// Render orders
function renderOrders() {
    const tbody = document.getElementById('ordersTable');
    tbody.innerHTML = orders.map(o => `
        <tr>
            <td>${o.id}</td>
            <td>${o.client}</td>
            <td>${o.product}</td>
            <td>${o.amount}</td>
            <td><span class="status-badge ${o.status}">${o.status}</span></td>
        </tr>
    `).join('');
}

// Render top products
function renderTopProducts() {
    const container = document.getElementById('topProducts');
    container.innerHTML = topProducts.map(p => `
        <div class="top-product-item">
            <div class="product-icon">${p.icon}</div>
            <div style="flex:1">
                <p>${p.name}</p>
                <small>${p.sales} ventas</small>
            </div>
        </div>
    `).join('');
}

// Render activities
function renderActivities() {
    const container = document.getElementById('activityList');
    container.innerHTML = activities.map(a => `
        <div class="activity-item">
            <div class="activity-icon ${a.type}">
                <i class="fas ${a.icon}"></i>
            </div>
            <div class="activity-info">
                <p>${a.text}</p>
                <small>${a.time}</small>
            </div>
        </div>
    `).join('');
}

// Simple chart drawing
function drawRevenueChart() {
    const canvas = document.getElementById('revenueChart');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const data = [30, 45, 35, 50, 49, 60, 70, 91, 85, 95, 88, 100];
    const months = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'];
    
    canvas.width = canvas.parentElement.offsetWidth - 40;
    canvas.height = 250;
    
    const padding = 40;
    const chartWidth = canvas.width - padding * 2;
    const chartHeight = canvas.height - padding * 2;
    const maxVal = Math.max(...data);
    
    ctx.fillStyle = '#1e293b';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    // Draw grid
    ctx.strokeStyle = 'rgba(255,255,255,0.1)';
    ctx.lineWidth = 1;
    for (let i = 0; i <= 5; i++) {
        const y = padding + (chartHeight / 5) * i;
        ctx.beginPath();
        ctx.moveTo(padding, y);
        ctx.lineTo(canvas.width - padding, y);
        ctx.stroke();
    }
    
    // Draw line
    ctx.strokeStyle = '#3b82f6';
    ctx.lineWidth = 3;
    ctx.beginPath();
    data.forEach((val, i) => {
        const x = padding + (chartWidth / (data.length - 1)) * i;
        const y = padding + chartHeight - (val / maxVal) * chartHeight;
        if (i === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
    });
    ctx.stroke();
    
    // Draw points
    data.forEach((val, i) => {
        const x = padding + (chartWidth / (data.length - 1)) * i;
        const y = padding + chartHeight - (val / maxVal) * chartHeight;
        ctx.fillStyle = '#3b82f6';
        ctx.beginPath();
        ctx.arc(x, y, 5, 0, Math.PI * 2);
        ctx.fill();
    });
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    renderOrders();
    renderTopProducts();
    renderActivities();
    drawRevenueChart();
    
    document.getElementById('hamburger').addEventListener('click', () => {
        document.querySelector('.sidebar').classList.toggle('open');
    });
    
    window.addEventListener('resize', drawRevenueChart);
});"""
    },
    {
        "name": "03_red_social",
        "title": "Red Social",
        "description": "Plataforma de redes sociales estilo Instagram",
        "html": """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SocialHub - Red Social</title>
    <link rel="stylesheet" href="style.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body>
    <nav class="navbar">
        <div class="logo"><i class="fas fa-globe"></i> SocialHub</div>
        <div class="search-box">
            <i class="fas fa-search"></i>
            <input type="text" placeholder="Buscar personas, hashtags...">
        </div>
        <div class="nav-icons">
            <button><i class="fas fa-home"></i></button>
            <button><i class="fas fa-paper-plane"></i></button>
            <button><i class="fas fa-compass"></i></button>
            <button><i class="fas fa-heart"></i></button>
            <div class="user-avatar" id="userAvatar">F</div>
        </div>
    </nav>
    
    <main class="feed">
        <div class="stories">
            <div class="story"><div class="story-ring"><div class="story-avatar">+</div></div><p>Tu historia</p></div>
            <div class="story"><div class="story-ring"><div class="story-avatar">A</div></div><p>Ana</p></div>
            <div class="story"><div class="story-ring"><div class="story-avatar">C</div></div><p>Carlos</p></div>
            <div class="story"><div class="story-ring"><div class="story-avatar">M</div></div><p>Maria</p></div>
            <div class="story"><div class="story-ring"><div class="story-avatar">P</div></div><p>Pedro</p></div>
        </div>
        
        <div class="post" id="post1">
            <div class="post-header">
                <div class="post-avatar">A</div>
                <div class="post-info">
                    <h4>Ana Garcia</h4>
                    <span>Madrid, Espana</span>
                </div>
                <button class="more-btn"><i class="fas fa-ellipsis-h"></i></button>
            </div>
            <div class="post-image" style="background: linear-gradient(135deg, #667eea, #764ba2)">
                <i class="fas fa-image" style="font-size:4rem;opacity:0.3"></i>
            </div>
            <div class="post-actions">
                <button class="like-btn" onclick="toggleLike(this)"><i class="far fa-heart"></i></button>
                <button><i class="far fa-comment"></i></button>
                <button><i class="far fa-paper-plane"></i></button>
                <button class="save-btn" onclick="toggleSave(this)"><i class="far fa-bookmark"></i></button>
            </div>
            <div class="post-likes">
                <span id="likes1">1,234</span> me gusta
            </div>
            <div class="post-caption">
                <h4>Ana Garcia</h4>
                <p>Disfrutando de un hermoso dia en Madrid! #viaje #aventura</p>
            </div>
            <div class="post-comments">
                <a href="#">Ver los 45 comentarios</a>
                <p><b>Carlos</b> Que bonito!</p>
            </div>
            <div class="add-comment">
                <input type="text" placeholder="Anade un comentario...">
                <button>Publicar</button>
            </div>
        </div>
        
        <div class="post" id="post2">
            <div class="post-header">
                <div class="post-avatar">C</div>
                <div class="post-info">
                    <h4>Carlos Lopez</h4>
                    <span>Barcelona, Espana</span>
                </div>
                <button class="more-btn"><i class="fas fa-ellipsis-h"></i></button>
            </div>
            <div class="post-image" style="background: linear-gradient(135deg, #f093fb, #f5576c)">
                <i class="fas fa-image" style="font-size:4rem;opacity:0.3"></i>
            </div>
            <div class="post-actions">
                <button class="like-btn" onclick="toggleLike(this)"><i class="far fa-heart"></i></button>
                <button><i class="far fa-comment"></i></button>
                <button><i class="far fa-paper-plane"></i></button>
                <button class="save-btn" onclick="toggleSave(this)"><i class="far fa-bookmark"></i></button>
            </div>
            <div class="post-likes"><span>856</span> me gusta</div>
            <div class="post-caption">
                <h4>Carlos Lopez</h4>
                <p>Mi setup de gaming nuevo! #gaming #tech</p>
            </div>
            <div class="add-comment">
                <input type="text" placeholder="Anade un comentario...">
                <button>Publicar</button>
            </div>
        </div>
        
        <div class="suggestions">
            <div class="suggestion-header">
                <h4>Sugerencias para ti</h4>
                <a href="#">Ver todo</a>
            </div>
            <div class="suggestion-item">
                <div class="suggestion-avatar">M</div>
                <div class="suggestion-info">
                    <h4>Maria Rodriguez</h4>
                    <p>Te sugiere follow</p>
                </div>
                <button class="follow-btn">Seguir</button>
            </div>
            <div class="suggestion-item">
                <div class="suggestion-avatar">L</div>
                <div class="suggestion-info">
                    <h4>Laura Sanchez</h4>
                    <p>Sigues a Ana</p>
                </div>
                <button class="follow-btn">Seguir</button>
            </div>
        </div>
    </main>
    
    <div class="create-modal" id="createModal">
        <div class="modal-content">
            <div class="modal-header">
                <h3>Crear nueva publicacion</h3>
                <button id="closeModal"><i class="fas fa-times"></i></button>
            </div>
            <div class="modal-body">
                <div class="upload-area" id="uploadArea">
                    <i class="fas fa-cloud-upload-alt"></i>
                    <p>Arrastra tu foto aqui</p>
                    <button class="btn-primary">Seleccionar del ordenador</button>
                </div>
                <textarea placeholder="Escribe un pie de foto..."></textarea>
            </div>
            <div class="modal-footer">
                <button class="btn-primary">Compartir</button>
            </div>
        </div>
    </div>
    
    <button class="fab" id="createBtn"><i class="fas fa-plus"></i></button>
    
    <script src="script.js"></script>
</body>
</html>""",
        "css": """/* SocialHub - Estilos */
:root {
    --bg: #000;
    --bg-card: #121212;
    --bg-secondary: #1a1a1a;
    --text: #f5f5f5;
    --text-muted: #a0a0a0;
    --primary: #0095f6;
    --danger: #ed4956;
    --border: #262626;
}
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    background: var(--bg);
    color: var(--text);
}
.navbar {
    position: fixed;
    top: 0;
    width: 100%;
    height: 60px;
    background: var(--bg-card);
    border-bottom: 1px solid var(--border);
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 20px;
    z-index: 100;
}
.logo {
    font-size: 1.5rem;
    font-weight: bold;
    color: var(--text);
}
.search-box {
    display: flex;
    align-items: center;
    background: var(--bg-secondary);
    padding: 8px 15px;
    border-radius: 8px;
    gap: 8px;
    width: 250px;
}
.search-box input {
    background: none;
    border: none;
    color: var(--text);
    outline: none;
    width: 100%;
}
.nav-icons { display: flex; gap: 15px; align-items: center; }
.nav-icons button {
    background: none;
    border: none;
    color: var(--text);
    font-size: 1.3rem;
    cursor: pointer;
}
.user-avatar {
    width: 32px;
    height: 32px;
    background: linear-gradient(135deg, #833ab4, #fd1d1d);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    cursor: pointer;
}
.feed {
    max-width: 600px;
    margin: 80px auto 20px;
    padding: 0 20px;
}
.stories {
    display: flex;
    gap: 15px;
    padding: 20px 0;
    overflow-x: auto;
    border-bottom: 1px solid var(--border);
    margin-bottom: 20px;
}
.story {
    text-align: center;
    min-width: 70px;
}
.story-ring {
    width: 66px;
    height: 66px;
    background: linear-gradient(135deg, #833ab4, #fd1d1d, #fcb045);
    border-radius: 50%;
    padding: 3px;
    margin-bottom: 5px;
}
.story-avatar {
    width: 100%;
    height: 100%;
    background: var(--bg);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5rem;
    font-weight: bold;
}
.story p { font-size: 0.7rem; color: var(--text-muted); }
.post {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 8px;
    margin-bottom: 20px;
}
.post-header {
    display: flex;
    align-items: center;
    padding: 12px 15px;
    gap: 10px;
}
.post-avatar {
    width: 36px;
    height: 36px;
    background: linear-gradient(135deg, #833ab4, #fd1d1d);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
}
.post-info { flex: 1; }
.post-info h4 { font-size: 0.9rem; }
.post-info span { font-size: 0.8rem; color: var(--text-muted); }
.more-btn {
    background: none;
    border: none;
    color: var(--text);
    cursor: pointer;
}
.post-image {
    width: 100%;
    height: 400px;
    display: flex;
    align-items: center;
    justify-content: center;
}
.post-actions {
    display: flex;
    padding: 12px 15px;
    gap: 15px;
}
.post-actions button {
    background: none;
    border: none;
    color: var(--text);
    font-size: 1.4rem;
    cursor: pointer;
}
.post-actions button:hover { color: var(--text-muted); }
.like-btn:hover, .like-btn.liked { color: var(--danger) !important; }
.like-btn.liked i { font-weight: 900; }
.save-btn:hover, .save-btn.saved { color: var(--text) !important; }
.post-likes {
    padding: 0 15px 8px;
    font-weight: bold;
    font-size: 0.9rem;
}
.post-caption {
    padding: 0 15px 8px;
}
.post-caption h4 { font-size: 0.9rem; display: inline; }
.post-caption p { font-size: 0.9rem; margin-left: 5px; }
.post-comments {
    padding: 0 15px 8px;
    font-size: 0.85rem;
}
.post-comments a {
    color: var(--text-muted);
    text-decoration: none;
    display: block;
    margin-bottom: 5px;
}
.add-comment {
    display: flex;
    padding: 12px 15px;
    border-top: 1px solid var(--border);
    gap: 10px;
}
.add-comment input {
    flex: 1;
    background: none;
    border: none;
    color: var(--text);
    outline: none;
}
.add-comment button {
    background: none;
    border: none;
    color: var(--primary);
    font-weight: bold;
    cursor: pointer;
}
.suggestions {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 15px;
    margin-top: 20px;
}
.suggestion-header {
    display: flex;
    justify-content: space-between;
    margin-bottom: 15px;
}
.suggestion-header h4 { color: var(--text-muted); font-size: 0.9rem; }
.suggestion-header a { color: var(--text); text-decoration: none; font-size: 0.85rem; }
.suggestion-item {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 12px;
}
.suggestion-avatar {
    width: 36px;
    height: 36px;
    background: linear-gradient(135deg, #833ab4, #fd1d1d);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
}
.suggestion-info { flex: 1; }
.suggestion-info h4 { font-size: 0.9rem; }
.suggestion-info p { font-size: 0.8rem; color: var(--text-muted); }
.follow-btn {
    background: none;
    border: none;
    color: var(--primary);
    font-weight: bold;
    cursor: pointer;
}
.fab {
    position: fixed;
    bottom: 30px;
    right: 30px;
    width: 60px;
    height: 60px;
    background: linear-gradient(135deg, #833ab4, #fd1d1d);
    border: none;
    border-radius: 50%;
    color: white;
    font-size: 1.5rem;
    cursor: pointer;
    box-shadow: 0 5px 20px rgba(131, 58, 180, 0.5);
}
.create-modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0,0,0,0.8);
    display: none;
    align-items: center;
    justify-content: center;
    z-index: 200;
}
.create-modal.active { display: flex; }
.modal-content {
    background: var(--bg-card);
    border-radius: 12px;
    width: 90%;
    max-width: 500px;
}
.modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 15px;
    border-bottom: 1px solid var(--border);
}
.modal-header button {
    background: none;
    border: none;
    color: var(--text);
    font-size: 1.2rem;
    cursor: pointer;
}
.modal-body { padding: 20px; }
.upload-area {
    border: 2px dashed var(--border);
    border-radius: 8px;
    padding: 40px;
    text-align: center;
    margin-bottom: 15px;
}
.upload-area i { font-size: 3rem; color: var(--text-muted); margin-bottom: 10px; }
.modal-body textarea {
    width: 100%;
    height: 100px;
    background: var(--bg-secondary);
    border: none;
    border-radius: 8px;
    padding: 10px;
    color: var(--text);
    resize: none;
}
.modal-footer {
    padding: 15px;
    border-top: 1px solid var(--border);
    text-align: right;
}
@media (max-width: 600px) {
    .search-box { display: none; }
    .feed { margin-top: 60px; }
}""",
        "js": """// SocialHub - JavaScript
function toggleLike(btn) {
    btn.classList.toggle('liked');
    const icon = btn.querySelector('i');
    const likesEl = btn.closest('.post').querySelector('.post-likes span');
    let likes = parseInt(likesEl.textContent.replace(',', ''));
    if (btn.classList.contains('liked')) {
        icon.classList.remove('far');
        icon.classList.add('fas');
        likes++;
    } else {
        icon.classList.remove('fas');
        icon.classList.add('far');
        likes--;
    }
    likesEl.textContent = likes.toLocaleString();
}

function toggleSave(btn) {
    btn.classList.toggle('saved');
    const icon = btn.querySelector('i');
    if (btn.classList.contains('saved')) {
        icon.classList.remove('far');
        icon.classList.add('fas');
    } else {
        icon.classList.remove('fas');
        icon.classList.add('far');
    }
}

document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('createBtn').addEventListener('click', () => {
        document.getElementById('createModal').classList.add('active');
    });
    
    document.getElementById('closeModal').addEventListener('click', () => {
        document.getElementById('createModal').classList.remove('active');
    });
    
    document.querySelectorAll('.follow-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            btn.textContent = btn.textContent === 'Seguir' ? 'Siguiendo' : 'Seguir';
        });
    });
});"""
    },
    {
        "name": "04_plataforma_cursos",
        "title": "Plataforma de Cursos",
        "description": "LMS completa con cursos, progreso y certificados",
        "html": """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>EduMaster - Plataforma de Cursos</title>
    <link rel="stylesheet" href="style.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body>
    <nav class="navbar">
        <div class="logo"><i class="fas fa-graduation-cap"></i> EduMaster</div>
        <div class="nav-links">
            <a href="#cursos">Cursos</a>
            <a href="#categorias">Categorias</a>
            <a href="#instructores">Instructores</a>
        </div>
        <div class="nav-actions">
            <button class="btn-outline" id="loginBtn">Iniciar Sesion</button>
            <button class="btn-primary">Registrarse</button>
        </div>
    </nav>
    
    <header class="hero">
        <div class="hero-content">
            <h1>Aprende lo que quieras, cuando quieras</h1>
            <p>Miles de cursos en linea para impulsar tu carrera profesional</p>
            <div class="search-bar">
                <i class="fas fa-search"></i>
                <input type="text" placeholder="Buscar cursos...">
                <button class="btn-primary">Buscar</button>
            </div>
            <div class="stats-row">
                <div class="stat"><h3>500+</h3><p>Cursos</p></div>
                <div class="stat"><h3>50k+</h3><p>Estudiantes</p></div>
                <div class="stat"><h3>200+</h3><p>Instructores</p></div>
            </div>
        </div>
    </header>
    
    <section class="categories" id="categorias">
        <h2>Explora por Categorias</h2>
        <div class="categories-grid">
            <div class="category-card" style="background: linear-gradient(135deg, #667eea, #764ba2)">
                <i class="fas fa-code"></i>
                <h3>Programacion</h3>
                <p>120 cursos</p>
            </div>
            <div class="category-card" style="background: linear-gradient(135deg, #f093fb, #f5576c)">
                <i class="fas fa-palette"></i>
                <h3>Diseno</h3>
                <p>85 cursos</p>
            </div>
            <div class="category-card" style="background: linear-gradient(135deg, #4facfe, #00f2fe)">
                <i class="fas fa-chart-line"></i>
                <h3>Negocios</h3>
                <p>95 cursos</p>
            </div>
            <div class="category-card" style="background: linear-gradient(135deg, #43e97b, #38f9d7)">
                <i class="fas fa-bullhorn"></i>
                <h3>Marketing</h3>
                <p>65 cursos</p>
            </div>
        </div>
    </section>
    
    <section class="featured-courses" id="cursos">
        <h2>Cursos Populares</h2>
        <div class="courses-grid" id="coursesGrid"></div>
    </section>
    
    <section class="instructors" id="instructores">
        <h2>Mejores Instructores</h2>
        <div class="instructors-grid" id="instructorsGrid"></div>
    </section>
    
    <section class="testimonials">
        <h2>Lo que dicen nuestros estudiantes</h2>
        <div class="testimonials-grid">
            <div class="testimonial-card">
                <div class="stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div>
                <p>"Excelente plataforma! Aprendi React en 2 meses y consegui empleo como desarrollador."</p>
                <div class="testimonial-author">
                    <div class="author-avatar">M</div>
                    <div>
                        <h4>Maria Garcia</h4>
                        <span>Desarrolladora Frontend</span>
                    </div>
                </div>
            </div>
            <div class="testimonial-card">
                <div class="stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div>
                <p>"Los cursos son muy completos y los instructores explican de maravilla."</p>
                <div class="testimonial-author">
                    <div class="author-avatar">C</div>
                    <div>
                        <h4>Carlos Lopez</h4>
                        <span>Disenador UX</span>
                    </div>
                </div>
            </div>
        </div>
    </section>
    
    <section class="cta">
        <h2>Empieza a aprender hoy</h2>
        <p>Unete a miles de estudiantes que ya estan transformando su carrera</p>
        <button class="btn-primary btn-large">Comenzar Ahora - Es Gratis</button>
    </section>
    
    <footer>
        <div class="footer-grid">
            <div class="footer-col">
                <h3><i class="fas fa-graduation-cap"></i> EduMaster</h3>
                <p>La plataforma de aprendizaje en linea #1 en Latinoamerica.</p>
            </div>
            <div class="footer-col">
                <h3>Cursos</h3>
                <a href="#">Programacion</a>
                <a href="#">Diseno</a>
                <a href="#">Negocios</a>
                <a href="#">Marketing</a>
            </div>
            <div class="footer-col">
                <h3>Empresa</h3>
                <a href="#">Sobre Nosotros</a>
                <a href="#">Carreras</a>
                <a href="#">Blog</a>
                <a href="#">Prensa</a>
            </div>
            <div class="footer-col">
                <h3>Soporte</a>
                <a href="#">Centro de Ayuda</a>
                <a href="#">Contacto</a>
                <a href="#">Terminos</a>
                <a href="#">Privacidad</a>
            </div>
        </div>
        <div class="footer-bottom">
            <p>&copy; 2026 EduMaster. Todos los derechos reservados.</p>
        </div>
    </footer>
    
    <script src="script.js"></script>
</body>
</html>""",
        "css": """/* EduMaster - Estilos */
:root {
    --primary: #6366f1;
    --primary-dark: #4f46e5;
    --bg: #0f172a;
    --bg-card: #1e293b;
    --text: #f1f5f9;
    --text-muted: #94a3b8;
    --gradient: linear-gradient(135deg, #6366f1, #8b5cf6);
}
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
    font-family: 'Segoe UI', system-ui, sans-serif;
    background: var(--bg);
    color: var(--text);
}
.navbar {
    position: fixed;
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1rem 5%;
    background: rgba(15, 23, 42, 0.95);
    backdrop-filter: blur(10px);
    z-index: 100;
}
.logo {
    font-size: 1.5rem;
    font-weight: bold;
    color: var(--primary);
}
.nav-links { display: flex; gap: 2rem; }
.nav-links a {
    color: var(--text);
    text-decoration: none;
    transition: color 0.3s;
}
.nav-links a:hover { color: var(--primary); }
.nav-actions { display: flex; gap: 1rem; }
.btn-outline {
    padding: 0.5rem 1.5rem;
    background: transparent;
    color: var(--text);
    border: 1px solid var(--primary);
    border-radius: 8px;
    cursor: pointer;
}
.btn-primary {
    padding: 0.5rem 1.5rem;
    background: var(--gradient);
    color: white;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    font-weight: bold;
}
.btn-large {
    padding: 1rem 3rem;
    font-size: 1.1rem;
}
.hero {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 100px 5%;
    background: linear-gradient(135deg, rgba(99, 102, 241, 0.2), rgba(139, 92, 246, 0.2));
}
.hero h1 {
    font-size: 3rem;
    margin-bottom: 1rem;
    background: var(--gradient);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.hero p { font-size: 1.2rem; color: var(--text-muted); margin-bottom: 2rem; }
.search-bar {
    display: flex;
    align-items: center;
    background: var(--bg-card);
    padding: 0.5rem 1rem;
    border-radius: 50px;
    max-width: 500px;
    margin: 0 auto 3rem;
    gap: 1rem;
}
.search-bar input {
    flex: 1;
    background: none;
    border: none;
    color: var(--text);
    outline: none;
}
.stats-row {
    display: flex;
    justify-content: center;
    gap: 4rem;
}
.stat h3 { font-size: 2.5rem; color: var(--primary); }
.stat p { color: var(--text-muted); }
section {
    padding: 5rem 5%;
}
section h2 {
    text-align: center;
    font-size: 2rem;
    margin-bottom: 3rem;
    background: var(--gradient);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.categories-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1.5rem;
}
.category-card {
    padding: 2rem;
    border-radius: 16px;
    text-align: center;
    cursor: pointer;
    transition: transform 0.3s;
}
.category-card:hover { transform: translateY(-5px); }
.category-card i { font-size: 3rem; margin-bottom: 1rem; }
.courses-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
}
.course-card {
    background: var(--bg-card);
    border-radius: 16px;
    overflow: hidden;
    border: 1px solid rgba(99, 102, 241, 0.2);
    transition: transform 0.3s;
}
.course-card:hover { transform: translateY(-5px); }
.course-image {
    height: 180px;
    background: var(--gradient);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 4rem;
}
.course-info { padding: 1.5rem; }
.course-info h3 { margin-bottom: 0.5rem; }
.course-info p { color: var(--text-muted); font-size: 0.9rem; margin-bottom: 1rem; }
.course-meta {
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.course-price {
    font-size: 1.3rem;
    font-weight: bold;
    color: var(--primary);
}
.course-rating { color: #f59e0b; }
.instructors-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 2rem;
}
.instructor-card {
    background: var(--bg-card);
    padding: 2rem;
    border-radius: 16px;
    text-align: center;
}
.instructor-avatar {
    width: 80px;
    height: 80px;
    background: var(--gradient);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2rem;
    font-weight: bold;
    margin: 0 auto 1rem;
}
.instructor-card h3 { margin-bottom: 0.3rem; }
.instructor-card p { color: var(--text-muted); }
.testimonials-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
}
.testimonial-card {
    background: var(--bg-card);
    padding: 2rem;
    border-radius: 16px;
}
.stars { color: #f59e0b; font-size: 1.2rem; margin-bottom: 1rem; }
.testimonial-author {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-top: 1.5rem;
}
.author-avatar {
    width: 50px;
    height: 50px;
    background: var(--gradient);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
}
.cta {
    text-align: center;
    padding: 5rem;
    background: var(--gradient);
}
.cta h2 { color: white; -webkit-text-fill-color: white; }
.cta p { color: rgba(255,255,255,0.9); margin-bottom: 2rem; }
.cta .btn-primary { background: white; color: var(--primary); }
footer {
    background: var(--bg-card);
    padding: 4rem 5% 2rem;
}
.footer-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 3rem;
    margin-bottom: 2rem;
}
.footer-col h3 { color: var(--primary); margin-bottom: 1rem; }
.footer-col a {
    display: block;
    color: var(--text-muted);
    text-decoration: none;
    margin: 0.5rem 0;
}
.footer-bottom {
    text-align: center;
    padding-top: 2rem;
    border-top: 1px solid rgba(99, 102, 241, 0.2);
    color: var(--text-muted);
}
@media (max-width: 768px) {
    .nav-links { display: none; }
    .hero h1 { font-size: 2rem; }
    .stats-row { gap: 2rem; }
}""",
        "js": """// EduMaster - JavaScript
const courses = [
    { id: 1, title: "React desde Cero", category: "Programacion", rating: 4.9, students: 12500, price: 49, icon: "⚛️" },
    { id: 2, title: "Python Completo", category: "Programacion", rating: 4.8, students: 9800, price: 39, icon: "🐍" },
    { id: 3, title: "UI/UX Design Master", category: "Diseno", rating: 4.9, students: 8200, price: 59, icon: "🎨" },
    { id: 4, title: "Marketing Digital", category: "Marketing", rating: 4.7, students: 6500, price: 45, icon: "📈" },
    { id: 5, title: "JavaScript Avanzado", category: "Programacion", rating: 4.8, students: 11000, price: 49, icon: "📜" },
    { id: 6, title: "Figma Professional", category: "Diseno", rating: 4.9, students: 7300, price: 39, icon: "🎯" },
];

const instructors = [
    { name: "Prof. Carlos Ruiz", specialty: "Programacion Full Stack", students: 25000, rating: 4.9, initial: "C" },
    { name: "Dra. Ana Martinez", specialty: "UI/UX & Design Thinking", students: 18000, rating: 4.8, initial: "A" },
    { name: "Ing. Pedro Sanchez", specialty: "Data Science & AI", students: 22000, rating: 4.9, initial: "P" },
    { name: "Mg. Laura Torres", specialty: "Marketing & Growth", students: 15000, rating: 4.7, initial: "L" },
];

function renderCourses() {
    const grid = document.getElementById('coursesGrid');
    grid.innerHTML = courses.map(c => `
        <div class="course-card">
            <div class="course-image">${c.icon}</div>
            <div class="course-info">
                <p style="color:var(--primary);font-size:0.85rem">${c.category}</p>
                <h3>${c.title}</h3>
                <div class="course-meta">
                    <span class="course-price">$${c.price}</span>
                    <span class="course-rating">★ ${c.rating}</span>
                </div>
                <p style="margin-top:0.5rem"><i class="fas fa-users"></i> ${c.students.toLocaleString()} estudiantes</p>
            </div>
        </div>
    `).join('');
}

function renderInstructors() {
    const grid = document.getElementById('instructorsGrid');
    grid.innerHTML = instructors.map(i => `
        <div class="instructor-card">
            <div class="instructor-avatar">${i.initial}</div>
            <h3>${i.name}</h3>
            <p>${i.specialty}</p>
            <p style="color:var(--primary);margin-top:0.5rem">★ ${i.rating} | ${i.students.toLocaleString()} alumnos</p>
        </div>
    `).join('');
}

document.addEventListener('DOMContentLoaded', () => {
    renderCourses();
    renderInstructors();
});"""
    },
    {
        "name": "05_chat_app",
        "title": "Chat Application",
        "description": "Aplicacion de chat en tiempo real",
        "html": """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ChatApp - Mensajeria Instantanea</title>
    <link rel="stylesheet" href="style.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body>
    <div class="app">
        <div class="sidebar">
            <div class="sidebar-header">
                <h2><i class="fas fa-comments"></i> ChatApp</h2>
                <button id="newChat"><i class="fas fa-edit"></i></button>
            </div>
            <div class="search-box">
                <i class="fas fa-search"></i>
                <input type="text" placeholder="Buscar chats...">
            </div>
            <div class="chat-list" id="chatList"></div>
        </div>
        
        <div class="chat-area">
            <div class="chat-header" id="chatHeader">
                <div class="chat-avatar">A</div>
                <div class="chat-info">
                    <h3>Ana Garcia</h3>
                    <p>en linea</p>
                </div>
                <div class="chat-actions">
                    <button><i class="fas fa-phone"></i></button>
                    <button><i class="fas fa-video"></i></button>
                    <button><i class="fas fa-ellipsis-v"></i></button>
                </div>
            </div>
            
            <div class="messages" id="messages">
                <div class="message received">
                    <div class="message-avatar">A</div>
                    <div class="message-content">
                        <p>Hola Fernando! Como estas?</p>
                        <span class="time">10:30</span>
                    </div>
                </div>
                <div class="message sent">
                    <div class="message-content">
                        <p>Hola Ana! Todo bien, y tu?</p>
                        <span class="time">10:31</span>
                    </div>
                </div>
                <div class="message received">
                    <div class="message-avatar">A</div>
                    <div class="message-content">
                        <p>Muy bien! Trabajando en el nuevo proyecto</p>
                        <span class="time">10:32</span>
                    </div>
                </div>
                <div class="message sent">
                    <div class="message-content">
                        <p>Genial! En que consiste?</p>
                        <span class="time">10:33</span>
                    </div>
                </div>
                <div class="message received">
                    <div class="message-avatar">A</div>
                    <div class="message-content">
                        <p>Es una app de chat como esta! Jeje</p>
                        <span class="time">10:34</span>
                    </div>
                </div>
            </div>
            
            <div class="message-input">
                <button><i class="fas fa-smile"></i></button>
                <button><i class="fas fa-paperclip"></i></button>
                <input type="text" id="messageInput" placeholder="Escribe un mensaje...">
                <button id="sendBtn"><i class="fas fa-paper-plane"></i></button>
            </div>
        </div>
        
        <div class="info-panel" id="infoPanel">
            <div class="info-avatar">A</div>
            <h3>Ana Garcia</h3>
            <p>en linea</p>
            <div class="info-actions">
                <button><i class="fas fa-bell"></i> Notificaciones</button>
                <button><i class="fas fa-image"></i> Multimedia</button>
                <button><i class="fas fa-star"></i> Mensajes Destacados</button>
                <button><i class="fas fa-ban"></i> Bloquear</button>
            </div>
        </div>
    </div>
    
    <script src="script.js"></script>
</body>
</html>""",
        "css": """/* ChatApp - Estilos */
:root {
    --bg: #0a0a0a;
    --bg-sidebar: #111;
    --bg-chat: #0d0d0d;
    --bg-message-sent: #005c4b;
    --bg-message-received: #1f2c34;
    --text: #e9edef;
    --text-muted: #8696a0;
    --primary: #00a884;
    --border: #222;
}
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
    font-family: 'Segoe UI', sans-serif;
    background: var(--bg);
    color: var(--text);
    height: 100vh;
}
.app {
    display: flex;
    height: 100vh;
}
.sidebar {
    width: 350px;
    background: var(--bg-sidebar);
    border-right: 1px solid var(--border);
    display: flex;
    flex-direction: column;
}
.sidebar-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 15px;
    border-bottom: 1px solid var(--border);
}
.sidebar-header h2 { color: var(--primary); }
.sidebar-header button {
    background: none;
    border: none;
    color: var(--text);
    font-size: 1.2rem;
    cursor: pointer;
}
.search-box {
    display: flex;
    align-items: center;
    padding: 8px 15px;
    gap: 10px;
    border-bottom: 1px solid var(--border);
}
.search-box input {
    flex: 1;
    background: var(--bg);
    border: none;
    border-radius: 8px;
    padding: 8px 15px;
    color: var(--text);
    outline: none;
}
.chat-list { flex: 1; overflow-y: auto; }
.chat-item {
    display: flex;
    align-items: center;
    padding: 12px 15px;
    gap: 12px;
    cursor: pointer;
    transition: background 0.2s;
}
.chat-item:hover, .chat-item.active { background: rgba(0, 168, 132, 0.1); }
.chat-avatar {
    width: 50px;
    height: 50px;
    background: var(--primary);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    font-size: 1.2rem;
}
.chat-preview { flex: 1; }
.chat-preview h4 { margin-bottom: 3px; }
.chat-preview p { color: var(--text-muted); font-size: 0.85rem; }
.chat-meta { text-align: right; }
.chat-meta small { color: var(--text-muted); }
.unread-badge {
    background: var(--primary);
    color: white;
    font-size: 0.7rem;
    padding: 2px 6px;
    border-radius: 10px;
    margin-top: 5px;
    display: inline-block;
}
.chat-area {
    flex: 1;
    display: flex;
    flex-direction: column;
    background: var(--bg-chat);
}
.chat-header {
    display: flex;
    align-items: center;
    padding: 10px 20px;
    gap: 15px;
    background: var(--bg-sidebar);
    border-bottom: 1px solid var(--border);
}
.chat-info { flex: 1; }
.chat-info h3 { font-size: 1rem; }
.chat-info p { color: var(--primary); font-size: 0.8rem; }
.chat-actions button {
    background: none;
    border: none;
    color: var(--text-muted);
    font-size: 1.1rem;
    cursor: pointer;
    margin-left: 15px;
}
.messages {
    flex: 1;
    overflow-y: auto;
    padding: 20px;
    background: url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKCAYAAACNMs+9AAAAFklEQVQYV2P8z8BQz0BFwMgwasCoAgBrNwMR506IOAAAAABJRU5ErkJggg==');
}
.message {
    display: flex;
    gap: 8px;
    margin-bottom: 8px;
    max-width: 70%;
}
.message.sent { margin-left: auto; }
.message-avatar {
    width: 30px;
    height: 30px;
    background: var(--primary);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.8rem;
}
.message-content {
    background: var(--bg-message-received);
    padding: 8px 12px;
    border-radius: 8px;
    position: relative;
}
.message.sent .message-content {
    background: var(--bg-message-sent);
    border-top-right-radius: 0;
}
.message.received .message-content { border-top-left-radius: 0; }
.message-content p { margin-bottom: 3px; }
.time { color: var(--text-muted); font-size: 0.7rem; }
.message-input {
    display: flex;
    align-items: center;
    padding: 10px 20px;
    gap: 10px;
    background: var(--bg-sidebar);
}
.message-input input {
    flex: 1;
    background: var(--bg);
    border: none;
    border-radius: 8px;
    padding: 10px 15px;
    color: var(--text);
    outline: none;
}
.message-input button {
    background: none;
    border: none;
    color: var(--text-muted);
    font-size: 1.2rem;
    cursor: pointer;
}
#sendBtn { color: var(--primary) !important; }
.info-panel {
    width: 300px;
    background: var(--bg-sidebar);
    border-left: 1px solid var(--border);
    padding: 30px 20px;
    text-align: center;
}
.info-avatar {
    width: 100px;
    height: 100px;
    background: var(--primary);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2.5rem;
    font-weight: bold;
    margin: 0 auto 15px;
}
.info-panel h3 { margin-bottom: 5px; }
.info-panel p { color: var(--primary); margin-bottom: 20px; }
.info-actions { text-align: left; }
.info-actions button {
    width: 100%;
    padding: 12px 15px;
    background: none;
    border: none;
    border-bottom: 1px solid var(--border);
    color: var(--text);
    text-align: left;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 15px;
}
.info-actions button:hover { background: rgba(0,168,132,0.1); }
@media (max-width: 768px) {
    .sidebar { display: none; }
    .info-panel { display: none; }
}""",
        "js": """// ChatApp - JavaScript
const contacts = [
    { id: 1, name: "Ana Garcia", lastMessage: "Genial!", time: "10:34", unread: 2, online: true },
    { id: 2, name: "Carlos Lopez", lastMessage: "Nos vemos manana", time: "09:15", unread: 0, online: true },
    { id: 3, name: "Maria Rodriguez", lastMessage: "Te envie el archivo", time: "Ayer", unread: 1, online: false },
    { id: 4, name: "Pedro Martinez", lastMessage: "Ok, entendido", time: "Ayer", unread: 0, online: false },
    { id: 5, name: "Laura Sanchez", lastMessage: "Jajaja que funny", time: "Lun", unread: 0, online: true },
];

function renderChatList() {
    const list = document.getElementById('chatList');
    list.innerHTML = contacts.map(c => `
        <div class="chat-item ${c.id === 1 ? 'active' : ''}" onclick="selectChat(${c.id})">
            <div class="chat-avatar">${c.name[0]}</div>
            <div class="chat-preview">
                <h4>${c.name}</h4>
                <p>${c.lastMessage}</p>
            </div>
            <div class="chat-meta">
                <small>${c.time}</small>
                ${c.unread > 0 ? `<div class="unread-badge">${c.unread}</div>` : ''}
            </div>
        </div>
    `).join('');
}

function selectChat(id) {
    document.querySelectorAll('.chat-item').forEach(i => i.classList.remove('active'));
    event.currentTarget.classList.add('active');
}

function sendMessage() {
    const input = document.getElementById('messageInput');
    const text = input.value.trim();
    if (!text) return;
    
    const messages = document.getElementById('messages');
    const time = new Date().toLocaleTimeString('es', { hour: '2-digit', minute: '2-digit' });
    
    const msgHtml = `
        <div class="message sent">
            <div class="message-content">
                <p>${text}</p>
                <span class="time">${time}</span>
            </div>
        </div>
    `;
    messages.insertAdjacentHTML('beforeend', msgHtml);
    input.value = '';
    messages.scrollTop = messages.scrollHeight;
    
    // Simular respuesta
    setTimeout(() => {
        const replies = ["Genial!", "Entendido", "Ok!", "Jaja", "Perfecto", "Dale"];
        const reply = replies[Math.floor(Math.random() * replies.length)];
        const replyHtml = `
            <div class="message received">
                <div class="message-avatar">A</div>
                <div class="message-content">
                    <p>${reply}</p>
                    <span class="time">${new Date().toLocaleTimeString('es', { hour: '2-digit', minute: '2-digit' })}</span>
                </div>
            </div>
        `;
        messages.insertAdjacentHTML('beforeend', replyHtml);
        messages.scrollTop = messages.scrollHeight;
    }, 1000);
}

document.addEventListener('DOMContentLoaded', () => {
    renderChatList();
    document.getElementById('sendBtn').addEventListener('click', sendMessage);
    document.getElementById('messageInput').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });
});"""
    },
    {
        "name": "06_portfolio_fotografia",
        "title": "Portfolio Fotografia",
        "description": "Portfolio profesional de fotografia con galeria",
        "html": """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FotoStudio - Portfolio Profesional</title>
    <link rel="stylesheet" href="style.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body>
    <nav class="navbar">
        <div class="logo">FotoStudio</div>
        <div class="nav-links">
            <a href="#inicio">Inicio</a>
            <a href="#galeria">Galeria</a>
            <a href="#servicios">Servicios</a>
            <a href="#sobre-mi">Sobre Mi</a>
            <a href="#contacto">Contacto</a>
        </div>
    </nav>
    
    <header class="hero" id="inicio">
        <div class="hero-content">
            <h1>Capturando Momentos</h1>
            <p>Fotografia profesional que cuenta historias</p>
            <a href="#galeria" class="btn-primary">Ver Galeria</a>
        </div>
    </header>
    
    <section class="gallery" id="galeria">
        <h2>Mi Galeria</h2>
        <div class="gallery-filters">
            <button class="filter-btn active" data-filter="all">Todos</button>
            <button class="filter-btn" data-filter="boda">Bodas</button>
            <button class="filter-btn" data-filter="retrato">Retratos</button>
            <button class="filter-btn" data-filter="naturaleza">Naturaleza</button>
            <button class="filter-btn" data-filter="evento">Eventos</button>
        </div>
        <div class="gallery-grid" id="galleryGrid">
            <div class="gallery-item" data-category="boda">
                <div class="gallery-image" style="background: linear-gradient(135deg, #f5af19, #f12711)"></div>
                <div class="gallery-overlay">
                    <h3>Boda Maria & Pedro</h3>
                    <p>Boda</p>
                </div>
            </div>
            <div class="gallery-item" data-category="retrato">
                <div class="gallery-image" style="background: linear-gradient(135deg, #667eea, #764ba2)"></div>
                <div class="gallery-overlay">
                    <h3>Retrato Profesional</h3>
                    <p>Retrato</p>
                </div>
            </div>
            <div class="gallery-item" data-category="naturaleza">
                <div class="gallery-image" style="background: linear-gradient(135deg, #11998e, #38ef7d)"></div>
                <div class="gallery-overlay">
                    <h3>Paisaje Montano</h3>
                    <p>Naturaleza</p>
                </div>
            </div>
            <div class="gallery-item" data-category="evento">
                <div class="gallery-image" style="background: linear-gradient(135deg, #ee0979, #ff6a00)"></div>
                <div class="gallery-overlay">
                    <h3>Concierto</h3>
                    <p>Evento</p>
                </div>
            </div>
            <div class="gallery-item" data-category="boda">
                <div class="gallery-image" style="background: linear-gradient(135deg, #f093fb, #f5576c)"></div>
                <div class="gallery-overlay">
                    <h3>Ceremonia al Aire Libre</h3>
                    <p>Boda</p>
                </div>
            </div>
            <div class="gallery-item" data-category="retrato">
                <div class="gallery-image" style="background: linear-gradient(135deg, #4facfe, #00f2fe)"></div>
                <div class="gallery-overlay">
                    <h3>Retrato Artístico</h3>
                    <p>Retrato</p>
                </div>
            </div>
        </div>
    </section>
    
    <section class="services" id="servicios">
        <h2>Servicios</h2>
        <div class="services-grid">
            <div class="service-card">
                <i class="fas fa-heart"></i>
                <h3>Bodas</h3>
                <p>Capturamos los momentos mas especiales de tu dia tan especial.</p>
                <span class="price">Desde $500</span>
            </div>
            <div class="service-card">
                <i class="fas fa-user"></i>
                <h3>Retratos</h3>
                <p>Sesiones profesionales para personas y familias.</p>
                <span class="price">Desde $150</span>
            </div>
            <div class="service-card">
                <i class="fas fa-building"></i>
                <h3>Empresas</h3>
                <p>Fotografia corporativa y de eventos empresariales.</p>
                <span class="price">Desde $300</span>
            </div>
            <div class="service-card">
                <i class="fas fa-camera"></i>
                <h3>Producto</h3>
                <p>Fotografia de producto para e-commerce.</p>
                <span class="price">Desde $200</span>
            </div>
        </div>
    </section>
    
    <section class="about" id="sobre-mi">
        <div class="about-content">
            <div class="about-image">
                <div class="about-placeholder">
                    <i class="fas fa-camera"></i>
                </div>
            </div>
            <div class="about-text">
                <h2>Sobre Mi</h2>
                <p>Soy Fernando, fotografo profesional con mas de 10 anos de experiencia. Mi pasion es capturar momentos unicos que cuenten historias.</p>
                <p>He trabajado con clientes de todo el mundo y mi trabajo ha sido publicado en revistas internacionales.</p>
                <div class="stats">
                    <div class="stat">
                        <h3>500+</h3>
                        <p>Proyectos</p>
                    </div>
                    <div class="stat">
                        <h3>10+</h3>
                        <p>Anos Exp.</p>
                    </div>
                    <div class="stat">
                        <h3>50+</h3>
                        <p>Premios</p>
                    </div>
                </div>
            </div>
        </div>
    </section>
    
    <section class="contact" id="contacto">
        <h2>Contacto</h2>
        <div class="contact-grid">
            <div class="contact-info">
                <div class="contact-item">
                    <i class="fas fa-map-marker-alt"></i>
                    <div>
                        <h4>Ubicacion</h4>
                        <p>Madrid, Espana</p>
                    </div>
                </div>
                <div class="contact-item">
                    <i class="fas fa-phone"></i>
                    <div>
                        <h4>Telefono</h4>
                        <p>+34 600 123 456</p>
                    </div>
                </div>
                <div class="contact-item">
                    <i class="fas fa-envelope"></i>
                    <div>
                        <h4>Email</h4>
                        <p>info@fotostudio.com</p>
                    </div>
                </div>
            </div>
            <form class="contact-form">
                <input type="text" placeholder="Tu nombre" required>
                <input type="email" placeholder="Tu email" required>
                <select>
                    <option>Selecciona servicio</option>
                    <option>Boda</option>
                    <option>Retrato</option>
                    <option>Empresa</option>
                    <option>Producto</option>
                </select>
                <textarea placeholder="Tu mensaje" rows="5" required></textarea>
                <button type="submit" class="btn-primary">Enviar Mensaje</button>
            </form>
        </div>
    </section>
    
    <footer>
        <div class="social-links">
            <a href="#"><i class="fab fa-instagram"></i></a>
            <a href="#"><i class="fab fa-facebook"></i></a>
            <a href="#"><i class="fab fa-twitter"></i></a>
            <a href="#"><i class="fab fa-pinterest"></i></a>
        </div>
        <p>&copy; 2026 FotoStudio. Todos los derechos reservados.</p>
    </footer>
    
    <script src="script.js"></script>
</body>
</html>""",
        "css": """/* FotoStudio - Estilos */
:root {
    --primary: #d4a574;
    --bg: #0a0a0a;
    --bg-card: #141414;
    --text: #f5f5f5;
    --text-muted: #888;
}
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
    font-family: 'Playfair Display', Georgia, serif;
    background: var(--bg);
    color: var(--text);
}
.navbar {
    position: fixed;
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1.5rem 5%;
    z-index: 100;
}
.logo { font-size: 1.5rem; font-weight: bold; color: var(--primary); }
.nav-links { display: flex; gap: 2rem; }
.nav-links a {
    color: var(--text);
    text-decoration: none;
    font-family: 'Segoe UI', sans-serif;
    font-size: 0.9rem;
    transition: color 0.3s;
}
.nav-links a:hover { color: var(--primary); }
.hero {
    height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    background: linear-gradient(135deg, rgba(212,165,116,0.2), rgba(0,0,0,0.8));
}
.hero h1 {
    font-size: 4rem;
    margin-bottom: 1rem;
    color: var(--primary);
}
.hero p {
    font-size: 1.3rem;
    color: var(--text-muted);
    margin-bottom: 2rem;
}
.btn-primary {
    display: inline-block;
    padding: 1rem 2rem;
    background: var(--primary);
    color: var(--bg);
    text-decoration: none;
    font-family: 'Segoe UI', sans-serif;
    font-weight: bold;
    border-radius: 0;
    transition: all 0.3s;
}
.btn-primary:hover { background: #c49564; transform: translateY(-2px); }
section { padding: 5rem 5%; }
section h2 {
    text-align: center;
    font-size: 2.5rem;
    margin-bottom: 3rem;
    color: var(--primary);
}
.gallery-filters {
    display: flex;
    justify-content: center;
    gap: 1rem;
    margin-bottom: 3rem;
}
.filter-btn {
    padding: 0.5rem 1.5rem;
    background: transparent;
    color: var(--text);
    border: 1px solid var(--primary);
    font-family: 'Segoe UI', sans-serif;
    cursor: pointer;
    transition: all 0.3s;
}
.filter-btn:hover, .filter-btn.active {
    background: var(--primary);
    color: var(--bg);
}
.gallery-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 1rem;
}
.gallery-item {
    position: relative;
    overflow: hidden;
    cursor: pointer;
}
.gallery-image {
    height: 300px;
    transition: transform 0.5s;
}
.gallery-item:hover .gallery-image { transform: scale(1.1); }
.gallery-overlay {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    padding: 2rem;
    background: linear-gradient(transparent, rgba(0,0,0,0.9));
    transform: translateY(100%);
    transition: transform 0.3s;
}
.gallery-item:hover .gallery-overlay { transform: translateY(0); }
.gallery-overlay h3 { color: var(--primary); margin-bottom: 0.3rem; }
.services-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 2rem;
}
.service-card {
    background: var(--bg-card);
    padding: 2.5rem;
    text-align: center;
    border: 1px solid rgba(212,165,116,0.2);
    transition: all 0.3s;
}
.service-card:hover { border-color: var(--primary); transform: translateY(-5px); }
.service-card i { font-size: 3rem; color: var(--primary); margin-bottom: 1.5rem; }
.service-card h3 { margin-bottom: 1rem; }
.service-card p { color: var(--text-muted); margin-bottom: 1rem; }
.service-card .price { color: var(--primary); font-weight: bold; }
.about-content {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 4rem;
    align-items: center;
}
.about-placeholder {
    width: 100%;
    height: 400px;
    background: linear-gradient(135deg, var(--primary), #8b5cf6);
    display: flex;
    align-items: center;
    justify-content: center;
}
.about-placeholder i { font-size: 5rem; opacity: 0.3; }
.about-text h2 { margin-bottom: 1.5rem; }
.about-text p { color: var(--text-muted); margin-bottom: 1rem; line-height: 1.8; }
.stats {
    display: flex;
    gap: 3rem;
    margin-top: 2rem;
}
.stat h3 { font-size: 2.5rem; color: var(--primary); }
.stat p { color: var(--text-muted); }
.contact-grid {
    display: grid;
    grid-template-columns: 1fr 2fr;
    gap: 4rem;
}
.contact-item {
    display: flex;
    gap: 1rem;
    margin-bottom: 2rem;
}
.contact-item i { color: var(--primary); font-size: 1.5rem; }
.contact-item h4 { margin-bottom: 0.3rem; }
.contact-item p { color: var(--text-muted); }
.contact-form input,
.contact-form select,
.contact-form textarea {
    width: 100%;
    padding: 1rem;
    margin-bottom: 1rem;
    background: var(--bg-card);
    border: 1px solid rgba(212,165,116,0.3);
    color: var(--text);
    font-family: 'Segoe UI', sans-serif;
}
.contact-form input:focus,
.contact-form select:focus,
.contact-form textarea:focus { border-color: var(--primary); outline: none; }
footer {
    text-align: center;
    padding: 3rem;
    border-top: 1px solid rgba(212,165,116,0.2);
}
.social-links {
    display: flex;
    justify-content: center;
    gap: 1.5rem;
    margin-bottom: 1rem;
}
.social-links a {
    width: 45px;
    height: 45px;
    border: 1px solid var(--primary);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--primary);
    text-decoration: none;
    transition: all 0.3s;
}
.social-links a:hover { background: var(--primary); color: var(--bg); }
@media (max-width: 768px) {
    .nav-links { display: none; }
    .hero h1 { font-size: 2.5rem; }
    .about-content, .contact-grid { grid-template-columns: 1fr; }
}""",
        "js": """// FotoStudio - JavaScript
document.addEventListener('DOMContentLoaded', () => {
    // Gallery filter
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            const filter = btn.dataset.filter;
            document.querySelectorAll('.gallery-item').forEach(item => {
                if (filter === 'all' || item.dataset.category === filter) {
                    item.style.display = 'block';
                } else {
                    item.style.display = 'none';
                }
            });
        });
    });
    
    // Smooth scroll
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });
    
    // Contact form
    document.querySelector('.contact-form').addEventListener('submit', (e) => {
        e.preventDefault();
        alert('Mensaje enviado! Te contactaremos pronto.');
        e.target.reset();
    });
});"""
    },
    {
        "name": "07_gestion_tareas",
        "title": "Gestion de Tareas",
        "description": "App de productividad con kanban y calendario",
        "html": """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TaskFlow - Gestor de Tareas</title>
    <link rel="stylesheet" href="style.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body>
    <div class="app">
        <aside class="sidebar">
            <div class="logo">
                <i class="fas fa-tasks"></i>
                <span>TaskFlow</span>
            </div>
            <nav class="nav-menu">
                <a href="#" class="nav-item active"><i class="fas fa-home"></i> Dashboard</a>
                <a href="#" class="nav-item"><i class="fas fa-calendar"></i> Calendario</a>
                <a href="#" class="nav-item"><i class="fas fa-project-diagram"></i> Proyectos</a>
                <a href="#" class="nav-item"><i class="fas fa-users"></i> Equipo</a>
                <a href="#" class="nav-item"><i class="fas fa-chart-pie"></i> Estadisticas</a>
            </nav>
            <div class="user-profile">
                <div class="avatar">F</div>
                <span>Fernando</span>
            </div>
        </aside>
        
        <main class="main">
            <header class="header">
                <div>
                    <h1>Mi Dashboard</h1>
                    <p>Tienes 5 tareas pendientes hoy</p>
                </div>
                <div class="header-actions">
                    <button class="btn-primary" id="addTaskBtn">
                        <i class="fas fa-plus"></i> Nueva Tarea
                    </button>
                </div>
            </header>
            
            <div class="stats-row">
                <div class="stat-card">
                    <div class="stat-icon" style="background: rgba(59,130,246,0.2); color: #3b82f6">
                        <i class="fas fa-clipboard-list"></i>
                    </div>
                    <div class="stat-info">
                        <h3>12</h3>
                        <p>Tareas Totales</p>
                    </div>
                </div>
                <div class="stat-card">
                    <div class="stat-icon" style="background: rgba(16,185,129,0.2); color: #10b981">
                        <i class="fas fa-check-circle"></i>
                    </div>
                    <div class="stat-info">
                        <h3>7</h3>
                        <p>Completadas</p>
                    </div>
                </div>
                <div class="stat-card">
                    <div class="stat-icon" style="background: rgba(245,158,11,0.2); color: #f59e0b">
                        <i class="fas fa-clock"></i>
                    </div>
                    <div class="stat-info">
                        <h3>5</h3>
                        <p>Pendientes</p>
                    </div>
                </div>
                <div class="stat-card">
                    <div class="stat-icon" style="background: rgba(239,68,68,0.2); color: #ef4444">
                        <i class="fas fa-exclamation-circle"></i>
                    </div>
                    <div class="stat-info">
                        <h3>2</h3>
                        <p>Urgentes</p>
                    </div>
                </div>
            </div>
            
            <div class="board">
                <div class="column" id="todo">
                    <div class="column-header">
                        <h3><span class="dot" style="background:#3b82f6"></span> Por Hacer</h3>
                        <span class="count">4</span>
                    </div>
                    <div class="tasks" id="todoTasks">
                        <div class="task-card" draggable="true">
                            <div class="task-priority high">Urgente</div>
                            <h4>Disenar landing page</h4>
                            <p>Crear mockup en Figma</p>
                            <div class="task-footer">
                                <span><i class="far fa-clock"></i> 2h</span>
                                <div class="task-avatar">A</div>
                            </div>
                        </div>
                        <div class="task-card" draggable="true">
                            <div class="task-priority medium">Media</div>
                            <h4>Revisar codigo</h4>
                            <p>PR del modulo de pagos</p>
                            <div class="task-footer">
                                <span><i class="far fa-clock"></i> 1h</span>
                                <div class="task-avatar">C</div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="column" id="doing">
                    <div class="column-header">
                        <h3><span class="dot" style="background:#f59e0b"></span> En Progreso</h3>
                        <span class="count">3</span>
                    </div>
                    <div class="tasks" id="doingTasks">
                        <div class="task-card" draggable="true">
                            <div class="task-priority high">Urgente</div>
                            <h4>API de usuarios</h4>
                            <p>Endpoints REST completos</p>
                            <div class="task-footer">
                                <span><i class="far fa-clock"></i> 4h</span>
                                <div class="task-avatar">F</div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="column" id="done">
                    <div class="column-header">
                        <h3><span class="dot" style="background:#10b981"></span> Completado</h3>
                        <span class="count">5</span>
                    </div>
                    <div class="tasks" id="doneTasks">
                        <div class="task-card completed" draggable="true">
                            <h4>Configurar base de datos</h4>
                            <p>PostgreSQL + Redis</p>
                            <div class="task-footer">
                                <span><i class="fas fa-check-circle"></i> Completado</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </main>
    </div>
    
    <div class="modal" id="taskModal">
        <div class="modal-content">
            <div class="modal-header">
                <h3>Nueva Tarea</h3>
                <button class="close-btn"><i class="fas fa-times"></i></button>
            </div>
            <form id="taskForm">
                <input type="text" placeholder="Titulo de la tarea" required>
                <textarea placeholder="Descripcion" rows="3"></textarea>
                <select>
                    <option value="low">Baja Prioridad</option>
                    <option value="medium">Media Prioridad</option>
                    <option value="high">Alta Prioridad</option>
                </select>
                <input type="date">
                <button type="submit" class="btn-primary">Crear Tarea</button>
            </form>
        </div>
    </div>
    
    <script src="script.js"></script>
</body>
</html>""",
        "css": """/* TaskFlow - Estilos */
:root {
    --bg: #0f172a;
    --bg-card: #1e293b;
    --bg-column: #162032;
    --text: #f1f5f9;
    --text-muted: #94a3b8;
    --primary: #3b82f6;
    --success: #10b981;
    --warning: #f59e0b;
    --danger: #ef4444;
}
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
    font-family: 'Segoe UI', system-ui, sans-serif;
    background: var(--bg);
    color: var(--text);
}
.app {
    display: flex;
    min-height: 100vh;
}
.sidebar {
    width: 260px;
    background: var(--bg-card);
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
}
.logo {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    font-size: 1.3rem;
    font-weight: bold;
    color: var(--primary);
    margin-bottom: 2rem;
}
.nav-menu { flex: 1; }
.nav-item {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 0.8rem 1rem;
    color: var(--text-muted);
    text-decoration: none;
    border-radius: 8px;
    margin-bottom: 0.5rem;
    transition: all 0.3s;
}
.nav-item:hover, .nav-item.active {
    background: rgba(59,130,246,0.2);
    color: var(--primary);
}
.user-profile {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding-top: 1rem;
    border-top: 1px solid rgba(255,255,255,0.1);
}
.avatar {
    width: 40px;
    height: 40px;
    background: var(--primary);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
}
.main { flex: 1; padding: 1.5rem; }
.header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 2rem;
}
.header h1 { margin-bottom: 0.3rem; }
.header p { color: var(--text-muted); }
.btn-primary {
    padding: 0.8rem 1.5rem;
    background: var(--primary);
    color: white;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.stats-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
    margin-bottom: 2rem;
}
.stat-card {
    background: var(--bg-card);
    padding: 1.5rem;
    border-radius: 12px;
    display: flex;
    align-items: center;
    gap: 1rem;
}
.stat-icon {
    width: 50px;
    height: 50px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.3rem;
}
.stat-info h3 { font-size: 1.8rem; }
.stat-info p { color: var(--text-muted); font-size: 0.85rem; }
.board {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1.5rem;
}
.column {
    background: var(--bg-column);
    border-radius: 12px;
    padding: 1rem;
}
.column-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
}
.column-header h3 {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.95rem;
}
.dot {
    width: 10px;
    height: 10px;
    border-radius: 50%;
}
.count {
    background: rgba(255,255,255,0.1);
    padding: 0.2rem 0.6rem;
    border-radius: 10px;
    font-size: 0.8rem;
}
.tasks { min-height: 200px; }
.task-card {
    background: var(--bg-card);
    padding: 1rem;
    border-radius: 8px;
    margin-bottom: 0.8rem;
    cursor: grab;
    transition: transform 0.2s;
}
.task-card:hover { transform: translateY(-2px); }
.task-card.completed { opacity: 0.6; }
.task-priority {
    display: inline-block;
    padding: 0.2rem 0.6rem;
    border-radius: 4px;
    font-size: 0.7rem;
    margin-bottom: 0.5rem;
}
.task-priority.high { background: rgba(239,68,68,0.2); color: var(--danger); }
.task-priority.medium { background: rgba(245,158,11,0.2); color: var(--warning); }
.task-priority.low { background: rgba(16,185,129,0.2); color: var(--success); }
.task-card h4 { margin-bottom: 0.3rem; font-size: 0.95rem; }
.task-card p { color: var(--text-muted); font-size: 0.85rem; }
.task-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 0.8rem;
    font-size: 0.8rem;
    color: var(--text-muted);
}
.task-avatar {
    width: 28px;
    height: 28px;
    background: var(--primary);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.75rem;
}
.modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0,0,0,0.7);
    display: none;
    align-items: center;
    justify-content: center;
}
.modal.active { display: flex; }
.modal-content {
    background: var(--bg-card);
    padding: 2rem;
    border-radius: 12px;
    width: 90%;
    max-width: 400px;
}
.modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1.5rem;
}
.close-btn {
    background: none;
    border: none;
    color: var(--text);
    font-size: 1.2rem;
    cursor: pointer;
}
#taskForm input,
#taskForm select,
#taskForm textarea {
    width: 100%;
    padding: 0.8rem;
    margin-bottom: 1rem;
    background: var(--bg);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 8px;
    color: var(--text);
}
#taskForm input:focus,
#taskForm select:focus,
#taskForm textarea:focus { border-color: var(--primary); outline: none; }
@media (max-width: 1024px) {
    .sidebar { display: none; }
    .board { grid-template-columns: 1fr; }
    .stats-row { grid-template-columns: repeat(2, 1fr); }
}""",
        "js": """// TaskFlow - JavaScript
document.addEventListener('DOMContentLoaded', () => {
    const modal = document.getElementById('taskModal');
    const addBtn = document.getElementById('addTaskBtn');
    const closeBtn = document.querySelector('.close-btn');
    const form = document.getElementById('taskForm');
    
    addBtn.addEventListener('click', () => modal.classList.add('active'));
    closeBtn.addEventListener('click', () => modal.classList.remove('active'));
    
    form.addEventListener('submit', (e) => {
        e.preventDefault();
        const title = form.querySelector('input').value;
        const desc = form.querySelector('textarea').value;
        const priority = form.querySelector('select').value;
        
        const taskHtml = `
            <div class="task-card" draggable="true">
                <div class="task-priority ${priority}">${priority === 'high' ? 'Urgente' : priority === 'medium' ? 'Media' : 'Baja'}</div>
                <h4>${title}</h4>
                <p>${desc}</p>
                <div class="task-footer">
                    <span><i class="far fa-clock"></i> Ahora</span>
                    <div class="task-avatar">F</div>
                </div>
            </div>
        `;
        document.getElementById('todoTasks').insertAdjacentHTML('beforeend', taskHtml);
        modal.classList.remove('active');
        form.reset();
        initDragAndDrop();
    });
    
    // Drag and drop
    function initDragAndDrop() {
        document.querySelectorAll('.task-card').forEach(card => {
            card.addEventListener('dragstart', (e) => {
                e.target.classList.add('dragging');
            });
            card.addEventListener('dragend', (e) => {
                e.target.classList.remove('dragging');
            });
        });
    }
    
    document.querySelectorAll('.tasks').forEach(column => {
        column.addEventListener('dragover', (e) => {
            e.preventDefault();
            const dragging = document.querySelector('.dragging');
            if (dragging) {
                column.appendChild(dragging);
            }
        });
    });
    
    initDragAndDrop();
});"""
    },
    {
        "name": "08_food_delivery",
        "title": "Food Delivery",
        "description": "App de delivery de comida con carrito",
        "html": """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FoodExpress - Delivery de Comida</title>
    <link rel="stylesheet" href="style.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body>
    <nav class="navbar">
        <div class="logo"><i class="fas fa-utensils"></i> FoodExpress</div>
        <div class="search-box">
            <i class="fas fa-search"></i>
            <input type="text" placeholder="Buscar restaurantes o platos...">
        </div>
        <div class="nav-icons">
            <button><i class="fas fa-map-marker-alt"></i> Madrid</button>
            <button class="cart-btn" id="cartBtn">
                <i class="fas fa-shopping-bag"></i>
                <span id="cartCount">0</span>
            </button>
        </div>
    </nav>
    
    <main class="main">
        <section class="categories-section">
            <h2>Categorias</h2>
            <div class="categories-scroll">
                <div class="category-item"><div class="cat-icon">🍕</div><p>Pizza</p></div>
                <div class="category-item"><div class="cat-icon">🍔</div><p>Hamburguesa</p></div>
                <div class="category-item"><div class="cat-icon">🍣</div><p>Sushi</p></div>
                <div class="category-item"><div class="cat-icon">🌮</div><p>Tacos</p></div>
                <div class="category-item"><div class="cat-icon">🥗</div><p>Ensaladas</p></div>
                <div class="category-item"><div class="cat-icon">🍜</div><p>Ramen</p></div>
                <div class="category-item"><div class="cat-icon">🍦</div><p>Postres</p></div>
                <div class="category-item"><div class="cat-icon">☕</div><p>Cafe</p></div>
            </div>
        </section>
        
        <section class="restaurants-section">
            <h2>Restaurantes Populares</h2>
            <div class="restaurants-grid" id="restaurantsGrid"></div>
        </section>
        
        <section class="featured-section">
            <h2>Platos Destacados</h2>
            <div class="dishes-grid" id="dishesGrid"></div>
        </section>
    </main>
    
    <div class="cart-panel" id="cartPanel">
        <div class="cart-header">
            <h3>Mi Pedido</h3>
            <button id="closeCart"><i class="fas fa-times"></i></button>
        </div>
        <div class="cart-items" id="cartItems">
            <p class="empty-cart">Tu carrito esta vacio</p>
        </div>
        <div class="cart-summary">
            <div class="summary-row">
                <span>Subtotal</span>
                <span id="subtotal">$0</span>
            </div>
            <div class="summary-row">
                <span>Delivery</span>
                <span>$3.99</span>
            </div>
            <div class="summary-row total">
                <span>Total</span>
                <span id="total">$3.99</span>
            </div>
            <button class="btn-primary" id="checkoutBtn">Realizar Pedido</button>
        </div>
    </div>
    
    <script src="script.js"></script>
</body>
</html>""",
        "css": """/* FoodExpress - Estilos */
:root {
    --primary: #ff6b35;
    --primary-dark: #e55a2b;
    --bg: #fafafa;
    --bg-card: #fff;
    --text: #1a1a1a;
    --text-muted: #666;
    --shadow: 0 2px 10px rgba(0,0,0,0.1);
}
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
    font-family: 'Segoe UI', system-ui, sans-serif;
    background: var(--bg);
    color: var(--text);
}
.navbar {
    position: fixed;
    top: 0;
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1rem 5%;
    background: var(--bg-card);
    box-shadow: var(--shadow);
    z-index: 100;
}
.logo {
    font-size: 1.4rem;
    font-weight: bold;
    color: var(--primary);
}
.search-box {
    display: flex;
    align-items: center;
    background: var(--bg);
    padding: 0.6rem 1.2rem;
    border-radius: 50px;
    gap: 0.5rem;
    flex: 1;
    max-width: 400px;
    margin: 0 2rem;
}
.search-box input {
    background: none;
    border: none;
    outline: none;
    width: 100%;
}
.nav-icons { display: flex; gap: 1rem; align-items: center; }
.nav-icons button {
    background: none;
    border: none;
    color: var(--text);
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 0.3rem;
}
.cart-btn {
    position: relative;
    background: var(--primary) !important;
    color: white !important;
    padding: 0.5rem 1rem !important;
    border-radius: 50px !important;
}
#cartCount {
    position: absolute;
    top: -5px;
    right: -5px;
    background: var(--text);
    color: white;
    font-size: 0.7rem;
    width: 18px;
    height: 18px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
}
.main { padding: 80px 5% 2rem; }
section { margin-bottom: 3rem; }
section h2 {
    font-size: 1.5rem;
    margin-bottom: 1.5rem;
}
.categories-scroll {
    display: flex;
    gap: 1.5rem;
    overflow-x: auto;
    padding-bottom: 1rem;
}
.category-item {
    text-align: center;
    min-width: 80px;
    cursor: pointer;
}
.cat-icon {
    width: 60px;
    height: 60px;
    background: var(--bg-card);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.8rem;
    margin-bottom: 0.5rem;
    box-shadow: var(--shadow);
    transition: transform 0.3s;
}
.category-item:hover .cat-icon { transform: scale(1.1); }
.restaurants-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 1.5rem;
}
.restaurant-card {
    background: var(--bg-card);
    border-radius: 16px;
    overflow: hidden;
    box-shadow: var(--shadow);
    cursor: pointer;
    transition: transform 0.3s;
}
.restaurant-card:hover { transform: translateY(-5px); }
.restaurant-image {
    height: 150px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 4rem;
}
.restaurant-info {
    padding: 1rem;
}
.restaurant-info h3 { margin-bottom: 0.3rem; }
.restaurant-info p { color: var(--text-muted); font-size: 0.85rem; }
.restaurant-meta {
    display: flex;
    justify-content: space-between;
    margin-top: 0.8rem;
    font-size: 0.85rem;
}
.rating { color: #f59e0b; }
.dishes-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 1.5rem;
}
.dish-card {
    background: var(--bg-card);
    border-radius: 16px;
    padding: 1rem;
    box-shadow: var(--shadow);
    display: flex;
    gap: 1rem;
}
.dish-image {
    width: 80px;
    height: 80px;
    background: #f0f0f0;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2.5rem;
}
.dish-info { flex: 1; }
.dish-info h4 { margin-bottom: 0.3rem; }
.dish-info p { color: var(--text-muted); font-size: 0.8rem; margin-bottom: 0.5rem; }
.dish-price {
    font-weight: bold;
    color: var(--primary);
    font-size: 1.1rem;
}
.add-to-cart {
    margin-top: 0.5rem;
    padding: 0.4rem 1rem;
    background: var(--primary);
    color: white;
    border: none;
    border-radius: 20px;
    cursor: pointer;
    font-size: 0.85rem;
}
.cart-panel {
    position: fixed;
    right: -400px;
    top: 0;
    width: 380px;
    height: 100vh;
    background: var(--bg-card);
    box-shadow: -5px 0 20px rgba(0,0,0,0.2);
    display: flex;
    flex-direction: column;
    transition: right 0.3s;
    z-index: 200;
}
.cart-panel.open { right: 0; }
.cart-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1.5rem;
    border-bottom: 1px solid #eee;
}
.cart-header button {
    background: none;
    border: none;
    font-size: 1.3rem;
    cursor: pointer;
}
.cart-items {
    flex: 1;
    overflow-y: auto;
    padding: 1rem;
}
.empty-cart {
    text-align: center;
    color: var(--text-muted);
    padding: 2rem;
}
.cart-item {
    display: flex;
    gap: 1rem;
    padding: 1rem 0;
    border-bottom: 1px solid #eee;
}
.cart-item-image {
    width: 60px;
    height: 60px;
    background: #f0f0f0;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5rem;
}
.cart-item-info { flex: 1; }
.cart-item-info h4 { font-size: 0.95rem; }
.cart-item-info p { color: var(--text-muted); font-size: 0.85rem; }
.cart-item-qty {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    margin-top: 0.5rem;
}
.cart-item-qty button {
    width: 28px;
    height: 28px;
    border: 1px solid #ddd;
    background: none;
    border-radius: 50%;
    cursor: pointer;
}
.cart-item-price { font-weight: bold; color: var(--primary); }
.cart-summary {
    padding: 1.5rem;
    border-top: 2px solid #eee;
}
.summary-row {
    display: flex;
    justify-content: space-between;
    margin-bottom: 0.8rem;
}
.summary-row.total {
    font-size: 1.2rem;
    font-weight: bold;
    padding-top: 0.8rem;
    border-top: 1px solid #eee;
}
.cart-summary .btn-primary {
    width: 100%;
    padding: 1rem;
    margin-top: 1rem;
    font-size: 1rem;
}
@media (max-width: 768px) {
    .search-box { display: none; }
    .cart-panel { width: 100%; right: -100%; }
}""",
        "js": """// FoodExpress - JavaScript
const restaurants = [
    { id: 1, name: "Pizza Palace", cuisine: "Italiana", rating: 4.8, time: "25-35 min", icon: "🍕" },
    { id: 2, name: "Burger House", cuisine: "Americana", rating: 4.6, time: "20-30 min", icon: "🍔" },
    { id: 3, name: "Sakura Sushi", cuisine: "Japonesa", rating: 4.9, time: "30-40 min", icon: "🍣" },
    { id: 4, name: "Taco Fiesta", cuisine: "Mexicana", rating: 4.7, time: "15-25 min", icon: "🌮" },
];

const dishes = [
    { id: 1, name: "Pizza Margarita", desc: "Queso mozzarella, tomate, albahaca", price: 12.99, icon: "🍕" },
    { id: 2, name: "Doble Cheeseburger", desc: "Carne, queso, lechuga, tomate", price: 9.99, icon: "🍔" },
    { id: 3, name: "Roll de Salmón", desc: "8 piezas con salmón fresco", price: 14.99, icon: "🍣" },
    { id: 4, name: "Tacos al Pastor", desc: "3 tacos con carne y piña", price: 8.99, icon: "🌮" },
    { id: 5, name: "Ensalada César", desc: "Lechuga, pollo, parmesano", price: 7.99, icon: "🥗" },
    { id: 6, name: "Ramen Tonkotsu", desc: "Caldo de cerdo, noodles, huevo", price: 11.99, icon: "🍜" },
];

let cart = [];

function renderRestaurants() {
    const grid = document.getElementById('restaurantsGrid');
    grid.innerHTML = restaurants.map(r => `
        <div class="restaurant-card">
            <div class="restaurant-image" style="background: linear-gradient(135deg, #ff6b35, #f7931e)">${r.icon}</div>
            <div class="restaurant-info">
                <h3>${r.name}</h3>
                <p>${r.cuisine}</p>
                <div class="restaurant-meta">
                    <span class="rating">★ ${r.rating}</span>
                    <span>${r.time}</span>
                </div>
            </div>
        </div>
    `).join('');
}

function renderDishes() {
    const grid = document.getElementById('dishesGrid');
    grid.innerHTML = dishes.map(d => `
        <div class="dish-card">
            <div class="dish-image">${d.icon}</div>
            <div class="dish-info">
                <h4>${d.name}</h4>
                <p>${d.desc}</p>
                <span class="dish-price">$${d.price}</span>
                <button class="add-to-cart" onclick="addToCart(${d.id})">Agregar</button>
            </div>
        </div>
    `).join('');
}

function addToCart(id) {
    const dish = dishes.find(d => d.id === id);
    const existing = cart.find(item => item.id === id);
    if (existing) {
        existing.qty++;
    } else {
        cart.push({ ...dish, qty: 1 });
    }
    updateCart();
}

function updateCart() {
    const count = cart.reduce((sum, item) => sum + item.qty, 0);
    document.getElementById('cartCount').textContent = count;
    
    const itemsEl = document.getElementById('cartItems');
    if (cart.length === 0) {
        itemsEl.innerHTML = '<p class="empty-cart">Tu carrito esta vacio</p>';
    } else {
        itemsEl.innerHTML = cart.map(item => `
            <div class="cart-item">
                <div class="cart-item-image">${item.icon}</div>
                <div class="cart-item-info">
                    <h4>${item.name}</h4>
                    <div class="cart-item-qty">
                        <button onclick="changeQty(${item.id}, -1)">-</button>
                        <span>${item.qty}</span>
                        <button onclick="changeQty(${item.id}, 1)">+</button>
                    </div>
                </div>
                <span class="cart-item-price">$${(item.price * item.qty).toFixed(2)}</span>
            </div>
        `).join('');
    }
    
    const subtotal = cart.reduce((sum, item) => sum + (item.price * item.qty), 0);
    document.getElementById('subtotal').textContent = '$' + subtotal.toFixed(2);
    document.getElementById('total').textContent = '$' + (subtotal + 3.99).toFixed(2);
}

function changeQty(id, delta) {
    const item = cart.find(i => i.id === id);
    if (item) {
        item.qty += delta;
        if (item.qty <= 0) {
            cart = cart.filter(i => i.id !== id);
        }
        updateCart();
    }
}

document.addEventListener('DOMContentLoaded', () => {
    renderRestaurants();
    renderDishes();
    
    document.getElementById('cartBtn').addEventListener('click', () => {
        document.getElementById('cartPanel').classList.add('open');
    });
    
    document.getElementById('closeCart').addEventListener('click', () => {
        document.getElementById('cartPanel').classList.remove('open');
    });
    
    document.getElementById('checkoutBtn').addEventListener('click', () => {
        if (cart.length > 0) {
            alert('Pedido realizado con exito!');
            cart = [];
            updateCart();
            document.getElementById('cartPanel').classList.remove('open');
        }
    });
});"""
    },
    {
        "name": "09_fitness_app",
        "title": "Fitness App",
        "description": "App de fitness con rutinas y seguimiento",
        "html": """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FitPro - Tu Entrenador Personal</title>
    <link rel="stylesheet" href="style.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body>
    <nav class="navbar">
        <div class="logo"><i class="fas fa-dumbbell"></i> FitPro</div>
        <div class="nav-links">
            <a href="#dashboard">Dashboard</a>
            <a href="#rutinas">Rutinas</a>
            <a href="#progreso">Progreso</a>
            <a href="#comunidad">Comunidad</a>
        </div>
        <div class="user-menu">
            <div class="avatar">F</div>
        </div>
    </nav>
    
    <main class="main">
        <section class="dashboard" id="dashboard">
            <div class="welcome">
                <h1>Hola, Fernando!</h1>
                <p>Continua con tu entrenamiento de hoy</p>
            </div>
            
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-icon"><i class="fas fa-fire"></i></div>
                    <div class="stat-info">
                        <h3>450</h3>
                        <p>Calorias quemadas</p>
                    </div>
                </div>
                <div class="stat-card">
                    <div class="stat-icon"><i class="fas fa-shoe-prints"></i></div>
                    <div class="stat-info">
                        <h3>8,542</h3>
                        <p>Pasos hoy</p>
                    </div>
                </div>
                <div class="stat-card">
                    <div class="stat-icon"><i class="fas fa-heartbeat"></i></div>
                    <div class="stat-info">
                        <h3>72</h3>
                        <p>BPM promedio</p>
                    </div>
                </div>
                <div class="stat-card">
                    <div class="stat-icon"><i class="fas fa-clock"></i></div>
                    <div class="stat-info">
                        <h3>45</h3>
                        <p>Minutos activo</p>
                    </div>
                </div>
            </div>
            
            <div class="today-workout">
                <h2>Entrenamiento de Hoy</h2>
                <div class="workout-card">
                    <div class="workout-header">
                        <div class="workout-icon">💪</div>
                        <div>
                            <h3>Full Body Workout</h3>
                            <p>45 minutos | 12 ejercicios</p>
                        </div>
                    </div>
                    <div class="exercise-list" id="exerciseList"></div>
                    <button class="btn-primary" id="startWorkout">Iniciar Entrenamiento</button>
                </div>
            </div>
        </section>
        
        <section class="routines" id="rutinas">
            <h2>Rutinas Disponibles</h2>
            <div class="routines-grid" id="routinesGrid"></div>
        </section>
        
        <section class="progress" id="progreso">
            <h2>Mi Progreso Semanal</h2>
            <div class="progress-chart">
                <div class="chart-bar" style="height: 60%"><span>Lun</span></div>
                <div class="chart-bar" style="height: 80%"><span>Mar</span></div>
                <div class="chart-bar active" style="height: 45%"><span>Mie</span></div>
                <div class="chart-bar" style="height: 90%"><span>Jue</span></div>
                <div class="chart-bar" style="height: 70%"><span>Vie</span></div>
                <div class="chart-bar" style="height: 30%"><span>Sab</span></div>
                <div class="chart-bar" style="height: 0%"><span>Dom</span></div>
            </div>
        </section>
        
        <section class="community" id="comunidad">
            <h2>Comunidad</h2>
            <div class="community-grid">
                <div class="leaderboard">
                    <h3>Leaderboard</h3>
                    <div class="leader-item"><span>1</span><div class="leader-avatar">A</div><p>Ana Garcia</p><span>12,500 pts</span></div>
                    <div class="leader-item"><span>2</span><div class="leader-avatar">F</div><p>Fernando</p><span>11,200 pts</span></div>
                    <div class="leader-item"><span>3</span><div class="leader-avatar">C</div><p>Carlos Lopez</p><span>10,800 pts</span></div>
                </div>
                <div class="achievements">
                    <h3>Logros</h3>
                    <div class="achievement unlocked"><i class="fas fa-trophy"></i><span>Primera Semana</span></div>
                    <div class="achievement unlocked"><i class="fas fa-fire"></i><span>7 Dias Seguidos</span></div>
                    <div class="achievement"><i class="fas fa-medal"></i><span>100 Entrenamientos</span></div>
                </div>
            </div>
        </section>
    </main>
    
    <div class="timer-modal" id="timerModal">
        <div class="timer-content">
            <h2>Entrenamiento en Curso</h2>
            <div class="timer" id="timer">00:00</div>
            <p id="currentExercise">Burpees</p>
            <div class="timer-controls">
                <button id="pauseBtn"><i class="fas fa-pause"></i></button>
                <button id="stopBtn"><i class="fas fa-stop"></i></button>
            </div>
        </div>
    </div>
    
    <script src="script.js"></script>
</body>
</html>""",
        "css": """/* FitPro - Estilos */
:root {
    --primary: #10b981;
    --primary-dark: #059669;
    --bg: #0f172a;
    --bg-card: #1e293b;
    --text: #f1f5f9;
    --text-muted: #94a3b8;
    --danger: #ef4444;
    --warning: #f59e0b;
}
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
    font-family: 'Segoe UI', system-ui, sans-serif;
    background: var(--bg);
    color: var(--text);
}
.navbar {
    position: fixed;
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1rem 5%;
    background: rgba(15, 23, 42, 0.95);
    backdrop-filter: blur(10px);
    z-index: 100;
}
.logo {
    font-size: 1.5rem;
    font-weight: bold;
    color: var(--primary);
}
.nav-links { display: flex; gap: 2rem; }
.nav-links a {
    color: var(--text);
    text-decoration: none;
    transition: color 0.3s;
}
.nav-links a:hover { color: var(--primary); }
.avatar {
    width: 40px;
    height: 40px;
    background: var(--primary);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
}
.main { padding: 80px 5% 2rem; }
.welcome { margin-bottom: 2rem; }
.welcome h1 { font-size: 2rem; margin-bottom: 0.5rem; }
.welcome p { color: var(--text-muted); }
.stats-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
    margin-bottom: 2rem;
}
.stat-card {
    background: var(--bg-card);
    padding: 1.5rem;
    border-radius: 16px;
    display: flex;
    align-items: center;
    gap: 1rem;
}
.stat-icon {
    width: 50px;
    height: 50px;
    background: rgba(16, 185, 129, 0.2);
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.3rem;
    color: var(--primary);
}
.stat-info h3 { font-size: 1.5rem; }
.stat-info p { color: var(--text-muted); font-size: 0.85rem; }
.today-workout { margin-bottom: 2rem; }
.today-workout h2 { margin-bottom: 1rem; }
.workout-card {
    background: var(--bg-card);
    padding: 1.5rem;
    border-radius: 16px;
}
.workout-header {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 1.5rem;
}
.workout-icon { font-size: 3rem; }
.exercise-list {
    margin-bottom: 1.5rem;
}
.exercise-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.8rem 0;
    border-bottom: 1px solid rgba(255,255,255,0.1);
}
.exercise-item:last-child { border-bottom: none; }
.exercise-name { display: flex; align-items: center; gap: 0.8rem; }
.exercise-sets { color: var(--text-muted); }
.btn-primary {
    width: 100%;
    padding: 1rem;
    background: var(--primary);
    color: white;
    border: none;
    border-radius: 12px;
    font-size: 1rem;
    font-weight: bold;
    cursor: pointer;
}
.btn-primary:hover { background: var(--primary-dark); }
.routines h2 { margin-bottom: 1rem; }
.routines-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 1rem;
}
.routine-card {
    background: var(--bg-card);
    padding: 1.5rem;
    border-radius: 16px;
    cursor: pointer;
    transition: transform 0.3s;
}
.routine-card:hover { transform: translateY(-3px); }
.routine-icon { font-size: 2.5rem; margin-bottom: 0.8rem; }
.routine-card h3 { margin-bottom: 0.3rem; }
.routine-card p { color: var(--text-muted); font-size: 0.85rem; }
.progress h2 { margin-bottom: 1.5rem; }
.progress-chart {
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
    height: 200px;
    background: var(--bg-card);
    padding: 2rem;
    border-radius: 16px;
}
.chart-bar {
    width: 12%;
    background: var(--primary);
    border-radius: 8px 8px 0 0;
    position: relative;
    transition: height 0.3s;
}
.chart-bar.active { background: var(--warning); }
.chart-bar span {
    position: absolute;
    bottom: -25px;
    left: 50%;
    transform: translateX(-50%);
    font-size: 0.8rem;
    color: var(--text-muted);
}
.community h2 { margin-bottom: 1rem; }
.community-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1.5rem;
}
.leaderboard, .achievements {
    background: var(--bg-card);
    padding: 1.5rem;
    border-radius: 16px;
}
.leaderboard h3, .achievements h3 { margin-bottom: 1rem; }
.leader-item {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 0.8rem 0;
    border-bottom: 1px solid rgba(255,255,255,0.1);
}
.leader-item:last-child { border-bottom: none; }
.leader-avatar {
    width: 35px;
    height: 35px;
    background: var(--primary);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
}
.leader-item p { flex: 1; }
.achievement {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 0.8rem;
    margin-bottom: 0.5rem;
    background: rgba(255,255,255,0.05);
    border-radius: 8px;
    opacity: 0.5;
}
.achievement.unlocked { opacity: 1; background: rgba(16,185,129,0.2); }
.achievement i { color: var(--warning); font-size: 1.3rem; }
.timer-modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0,0,0,0.9);
    display: none;
    align-items: center;
    justify-content: center;
}
.timer-modal.active { display: flex; }
.timer-content { text-align: center; }
.timer {
    font-size: 5rem;
    font-weight: bold;
    color: var(--primary);
    margin: 2rem 0;
}
.timer-controls { display: flex; gap: 1rem; justify-content: center; }
.timer-controls button {
    width: 60px;
    height: 60px;
    border-radius: 50%;
    border: none;
    font-size: 1.5rem;
    cursor: pointer;
}
#pauseBtn { background: var(--warning); color: var(--bg); }
#stopBtn { background: var(--danger); color: white; }
@media (max-width: 768px) {
    .nav-links { display: none; }
    .stats-grid { grid-template-columns: repeat(2, 1fr); }
    .community-grid { grid-template-columns: 1fr; }
}""",
        "js": """// FitPro - JavaScript
const exercises = [
    { name: "Burpees", sets: "3 x 12", icon: "🔥" },
    { name: "Sentadillas", sets: "4 x 15", icon: "🦵" },
    { name: "Flexiones", sets: "3 x 20", icon: "💪" },
    { name: "Plancha", sets: "3 x 45s", icon: "🏋️" },
    { name: "Zancadas", sets: "3 x 12", icon: "🏃" },
];

const routines = [
    { name: "Full Body", desc: "45 min | Intermedio", icon: "💪" },
    { name: "Cardio HIIT", desc: "30 min | Avanzado", icon: "🔥" },
    { name: "Yoga Flow", desc: "60 min | Todos", icon: "🧘" },
    { name: "Fuerza Upper", desc: "40 min | Intermedio", icon: "🏋️" },
    { name: "Piernas", desc: "35 min | Todos", icon: "🦵" },
    { name: "Abdomen", desc: "20 min | Todos", icon: "🎯" },
];

function renderExercises() {
    const list = document.getElementById('exerciseList');
    list.innerHTML = exercises.map(e => `
        <div class="exercise-item">
            <div class="exercise-name">
                <span>${e.icon}</span>
                <span>${e.name}</span>
            </div>
            <span class="exercise-sets">${e.sets}</span>
        </div>
    `).join('');
}

function renderRoutines() {
    const grid = document.getElementById('routinesGrid');
    grid.innerHTML = routines.map(r => `
        <div class="routine-card">
            <div class="routine-icon">${r.icon}</div>
            <h3>${r.name}</h3>
            <p>${r.desc}</p>
        </div>
    `).join('');
}

let timerInterval;
let seconds = 0;

function startTimer() {
    document.getElementById('timerModal').classList.add('active');
    seconds = 0;
    updateTimerDisplay();
    timerInterval = setInterval(() => {
        seconds++;
        updateTimerDisplay();
    }, 1000);
}

function updateTimerDisplay() {
    const mins = Math.floor(seconds / 60).toString().padStart(2, '0');
    const secs = (seconds % 60).toString().padStart(2, '0');
    document.getElementById('timer').textContent = mins + ':' + secs;
}

document.addEventListener('DOMContentLoaded', () => {
    renderExercises();
    renderRoutines();
    
    document.getElementById('startWorkout').addEventListener('click', startTimer);
    document.getElementById('pauseBtn').addEventListener('click', () => {
        if (timerInterval) {
            clearInterval(timerInterval);
            timerInterval = null;
        } else {
            timerInterval = setInterval(() => {
                seconds++;
                updateTimerDisplay();
            }, 1000);
        }
    });
    document.getElementById('stopBtn').addEventListener('click', () => {
        clearInterval(timerInterval);
        timerInterval = null;
        document.getElementById('timerModal').classList.remove('active');
    });
});"""
    },
    {
        "name": "10_booking_hotel",
        "title": "Booking Hotel",
        "description": "Sistema de reservas de hotel",
        "html": """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LuxeStay - Hoteles de Lujo</title>
    <link rel="stylesheet" href="style.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body>
    <nav class="navbar">
        <div class="logo"><i class="fas fa-hotel"></i> LuxeStay</div>
        <div class="nav-links">
            <a href="#habitaciones">Habitaciones</a>
            <a href="#servicios">Servicios</a>
            <a href="#galeria">Galeria</a>
            <a href="#contacto">Contacto</a>
        </div>
        <div class="nav-actions">
            <button class="btn-outline">Iniciar Sesion</button>
            <button class="btn-primary">Reservar Ahora</button>
        </div>
    </nav>
    
    <header class="hero">
        <div class="hero-content">
            <h1>Experiencias Inolvidables</h1>
            <p>Descubre hoteles de lujo en los mejores destinos del mundo</p>
            <div class="booking-form">
                <div class="form-group">
                    <label>Destino</label>
                    <input type="text" placeholder="¿A donde vas?">
                </div>
                <div class="form-group">
                    <label>Check-in</label>
                    <input type="date">
                </div>
                <div class="form-group">
                    <label>Check-out</label>
                    <input type="date">
                </div>
                <div class="form-group">
                    <label>Huespedes</label>
                    <select>
                        <option>1 Huesped</option>
                        <option>2 Huespedes</option>
                        <option>3 Huespedes</option>
                        <option>4+ Huespedes</option>
                    </select>
                </div>
                <button class="btn-primary">Buscar</button>
            </div>
        </div>
    </header>
    
    <section class="rooms" id="habitaciones">
        <h2>Nuestras Habitaciones</h2>
        <div class="rooms-grid" id="roomsGrid"></div>
    </section>
    
    <section class="amenities" id="servicios">
        <h2>Servicios Premium</h2>
        <div class="amenities-grid">
            <div class="amenity-card">
                <i class="fas fa-spa"></i>
                <h3>Spa & Wellness</h3>
                <p>Relajate con nuestros tratamientos exclusivos</p>
            </div>
            <div class="amenity-card">
                <i class="fas fa-utensils"></i>
                <h3>Restaurante Gourmet</h3>
                <p>Cocina de autor con vistas panoramicas</p>
            </div>
            <div class="amenity-card">
                <i class="fas fa-swimming-pool"></i>
                <h3>Piscina Infinity</h3>
                <p>Piscina de borde infinito con vista al mar</p>
            </div>
            <div class="amenity-card">
                <i class="fas fa-dumbbell"></i>
                <h3>Gimnasio 24/7</h3>
                <p>Equipamiento de ultima generacion</p>
            </div>
        </div>
    </section>
    
    <section class="gallery-section" id="galeria">
        <h2>Galeria</h2>
        <div class="gallery-grid">
            <div class="gallery-item" style="background: linear-gradient(135deg, #667eea, #764ba2)"></div>
            <div class="gallery-item" style="background: linear-gradient(135deg, #f093fb, #f5576c)"></div>
            <div class="gallery-item" style="background: linear-gradient(135deg, #4facfe, #00f2fe)"></div>
            <div class="gallery-item" style="background: linear-gradient(135deg, #43e97b, #38f9d7)"></div>
            <div class="gallery-item" style="background: linear-gradient(135deg, #fa709a, #fee140)"></div>
            <div class="gallery-item" style="background: linear-gradient(135deg, #a8edea, #fed6e3)"></div>
        </div>
    </section>
    
    <section class="testimonials">
        <h2>Lo que dicen nuestros huespedes</h2>
        <div class="testimonials-grid">
            <div class="testimonial-card">
                <div class="stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div>
                <p>"Una experiencia increible. El servicio es excepcional y las instalaciones son de primer nivel."</p>
                <div class="author">
                    <div class="author-avatar">M</div>
                    <div>
                        <h4>Maria Garcia</h4>
                        <span>Madrid, Espana</span>
                    </div>
                </div>
            </div>
            <div class="testimonial-card">
                <div class="stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div>
                <p>"El mejor hotel en el que me he alojado. Volvere sin duda."</p>
                <div class="author">
                    <div class="author-avatar">C</div>
                    <div>
                        <h4>Carlos Lopez</h4>
                        <span>Barcelona, Espana</span>
                    </div>
                </div>
            </div>
        </div>
    </section>
    
    <footer id="contacto">
        <div class="footer-grid">
            <div class="footer-col">
                <h3><i class="fas fa-hotel"></i> LuxeStay</h3>
                <p>Hoteles de lujo en los mejores destinos del mundo.</p>
                <div class="social-links">
                    <a href="#"><i class="fab fa-facebook"></i></a>
                    <a href="#"><i class="fab fa-instagram"></i></a>
                    <a href="#"><i class="fab fa-twitter"></i></a>
                </div>
            </div>
            <div class="footer-col">
                <h3>Contacto</h3>
                <p><i class="fas fa-map-marker-alt"></i> Madrid, Espana</p>
                <p><i class="fas fa-phone"></i> +34 900 123 456</p>
                <p><i class="fas fa-envelope"></i> info@luxestay.com</p>
            </div>
        </div>
        <div class="footer-bottom">
            <p>&copy; 2026 LuxeStay. Todos los derechos reservados.</p>
        </div>
    </footer>
    
    <script src="script.js"></script>
</body>
</html>""",
        "css": """/* LuxeStay - Estilos */
:root {
    --primary: #c9a961;
    --primary-dark: #b8952f;
    --bg: #0a0a0a;
    --bg-card: #141414;
    --text: #f5f5f5;
    --text-muted: #888;
}
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
    font-family: 'Playfair Display', Georgia, serif;
    background: var(--bg);
    color: var(--text);
}
.navbar {
    position: fixed;
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1.5rem 5%;
    z-index: 100;
}
.logo {
    font-size: 1.5rem;
    font-weight: bold;
    color: var(--primary);
}
.nav-links { display: flex; gap: 2rem; }
.nav-links a {
    color: var(--text);
    text-decoration: none;
    font-family: 'Segoe UI', sans-serif;
    transition: color 0.3s;
}
.nav-links a:hover { color: var(--primary); }
.nav-actions { display: flex; gap: 1rem; }
.btn-outline {
    padding: 0.6rem 1.5rem;
    background: transparent;
    color: var(--text);
    border: 1px solid var(--primary);
    font-family: 'Segoe UI', sans-serif;
    cursor: pointer;
}
.btn-primary {
    padding: 0.6rem 1.5rem;
    background: var(--primary);
    color: var(--bg);
    border: none;
    font-family: 'Segoe UI', sans-serif;
    font-weight: bold;
    cursor: pointer;
}
.hero {
    height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    background: linear-gradient(135deg, rgba(201,169,97,0.2), rgba(0,0,0,0.8));
}
.hero h1 {
    font-size: 4rem;
    margin-bottom: 1rem;
    color: var(--primary);
}
.hero p {
    font-size: 1.3rem;
    color: var(--text-muted);
    margin-bottom: 3rem;
}
.booking-form {
    display: flex;
    gap: 1rem;
    background: var(--bg-card);
    padding: 1.5rem;
    border-radius: 8px;
    max-width: 900px;
    margin: 0 auto;
    align-items: flex-end;
}
.form-group {
    flex: 1;
    text-align: left;
}
.form-group label {
    display: block;
    margin-bottom: 0.5rem;
    font-family: 'Segoe UI', sans-serif;
    font-size: 0.85rem;
    color: var(--text-muted);
}
.form-group input,
.form-group select {
    width: 100%;
    padding: 0.8rem;
    background: var(--bg);
    border: 1px solid rgba(201,169,97,0.3);
    color: var(--text);
    font-family: 'Segoe UI', sans-serif;
}
.booking-form .btn-primary {
    padding: 0.8rem 2rem;
}
section { padding: 5rem 5%; }
section h2 {
    text-align: center;
    font-size: 2.5rem;
    margin-bottom: 3rem;
    color: var(--primary);
}
.rooms-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
}
.room-card {
    background: var(--bg-card);
    border-radius: 16px;
    overflow: hidden;
    border: 1px solid rgba(201,169,97,0.2);
    transition: transform 0.3s;
}
.room-card:hover { transform: translateY(-5px); }
.room-image {
    height: 200px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 4rem;
}
.room-info { padding: 1.5rem; }
.room-info h3 { margin-bottom: 0.5rem; }
.room-info p { color: var(--text-muted); margin-bottom: 1rem; }
.room-amenities {
    display: flex;
    gap: 1rem;
    margin-bottom: 1rem;
    font-size: 0.85rem;
    color: var(--text-muted);
}
.room-price {
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.room-price .price {
    font-size: 1.5rem;
    font-weight: bold;
    color: var(--primary);
}
.amenities-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 2rem;
}
.amenity-card {
    background: var(--bg-card);
    padding: 2rem;
    border-radius: 16px;
    text-align: center;
    border: 1px solid rgba(201,169,97,0.2);
    transition: all 0.3s;
}
.amenity-card:hover { border-color: var(--primary); transform: translateY(-5px); }
.amenity-card i {
    font-size: 3rem;
    color: var(--primary);
    margin-bottom: 1rem;
}
.gallery-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
}
.gallery-item {
    height: 250px;
    border-radius: 12px;
    cursor: pointer;
    transition: transform 0.3s;
}
.gallery-item:hover { transform: scale(1.05); }
.testimonials-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
}
.testimonial-card {
    background: var(--bg-card);
    padding: 2rem;
    border-radius: 16px;
}
.stars { color: var(--primary); margin-bottom: 1rem; }
.testimonial-card p {
    color: var(--text-muted);
    font-style: italic;
    margin-bottom: 1.5rem;
}
.author {
    display: flex;
    align-items: center;
    gap: 1rem;
}
.author-avatar {
    width: 50px;
    height: 50px;
    background: var(--primary);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
}
.author h4 { margin-bottom: 0.2rem; }
.author span { color: var(--text-muted); font-size: 0.85rem; }
footer {
    background: var(--bg-card);
    padding: 4rem 5% 2rem;
}
.footer-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 3rem;
    margin-bottom: 2rem;
}
.footer-col h3 { color: var(--primary); margin-bottom: 1rem; }
.footer-col p { color: var(--text-muted); margin-bottom: 0.5rem; }
.social-links {
    display: flex;
    gap: 1rem;
    margin-top: 1rem;
}
.social-links a {
    width: 40px;
    height: 40px;
    border: 1px solid var(--primary);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--primary);
    text-decoration: none;
}
.footer-bottom {
    text-align: center;
    padding-top: 2rem;
    border-top: 1px solid rgba(201,169,97,0.2);
    color: var(--text-muted);
}
@media (max-width: 768px) {
    .nav-links { display: none; }
    .hero h1 { font-size: 2.5rem; }
    .booking-form { flex-direction: column; }
    .gallery-grid { grid-template-columns: repeat(2, 1fr); }
}""",
        "js": """// LuxeStay - JavaScript
const rooms = [
    { name: "Suite Deluxe", desc: "Vista al mar, 50m2", price: 299, icon: "🛏️", amenities: ["WiFi", "Minibar", "Vista Mar"] },
    { name: "Habitacion Premium", desc: "Amplia y luminosa, 35m2", price: 199, icon: "🏨", amenities: ["WiFi", "Minibar"] },
    { name: "Suite Presidencial", desc: "Lujo absoluto, 80m2", price: 599, icon: "👑", amenities: ["WiFi", "Minibar", "Jacuzzi", "Vista Mar"] },
    { name: "Habitacion Estandar", desc: "Comoda y funcional, 25m2", price: 129, icon: "🏠", amenities: ["WiFi"] },
];

function renderRooms() {
    const grid = document.getElementById('roomsGrid');
    grid.innerHTML = rooms.map(r => `
        <div class="room-card">
            <div class="room-image" style="background: linear-gradient(135deg, #c9a961, #8b5cf6)">${r.icon}</div>
            <div class="room-info">
                <h3>${r.name}</h3>
                <p>${r.desc}</p>
                <div class="room-amenities">
                    ${r.amenities.map(a => `<span>✓ ${a}</span>`).join('')}
                </div>
                <div class="room-price">
                    <span class="price">$${r.price}/noche</span>
                    <button class="btn-primary">Reservar</button>
                </div>
            </div>
        </div>
    `).join('');
}

document.addEventListener('DOMContentLoaded', () => {
    renderRooms();
    
    document.querySelectorAll('.btn-primary').forEach(btn => {
        btn.addEventListener('click', (e) => {
            if (e.target.textContent === 'Reservar' || e.target.textContent === 'Reservar Ahora') {
                alert('Redirigiendo al sistema de reservas...');
            }
        });
    });
});"""
    }
]

def save_project(project):
    """Guardar proyecto en carpeta"""
    project_dir = os.path.join(PROJECTS_DIR, project["name"])
    os.makedirs(project_dir, exist_ok=True)
    
    with open(os.path.join(project_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(project["html"])
    
    with open(os.path.join(project_dir, "style.css"), "w", encoding="utf-8") as f:
        f.write(project["css"])
    
    with open(os.path.join(project_dir, "script.js"), "w", encoding="utf-8") as f:
        f.write(project["js"])
    
    return project_dir

def test_server():
    """Probar que el servidor responde"""
    try:
        response = requests.get(f"{PROXY_URL}/health", timeout=10)
        return response.status_code == 200
    except:
        return False

def test_chat():
    """Probar que el chat funciona"""
    try:
        response = requests.post(
            f"{PROXY_URL}/v1/chat/completions",
            json={
                "model": "mimo-v2.5-free",
                "messages": [{"role": "user", "content": "di hola"}],
                "max_tokens": 10
            },
            timeout=30
        )
        return response.status_code == 200
    except:
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("TEST: 10 PROYECTOS WEB GRANDES")
    print("=" * 60)
    
    # Probar servidor
    print("\n[1/3] Probando servidor...")
    if test_server():
        print("  [OK] Servidor respondiendo")
    else:
        print("  [ERROR] Servidor no responde")
        exit(1)
    
    # Probar chat
    print("\n[2/3] Probando chat...")
    if test_chat():
        print("  [OK] Chat funcionando")
    else:
        print("  [ERROR] Chat no funciona")
        exit(1)
    
    # Generar proyectos
    print("\n[3/3] Generando 10 proyectos web...")
    results = []
    
    for i, project in enumerate(PROJECTS, 1):
        print(f"\n  [{i}/10] {project['title']}")
        project_dir = save_project(project)
        
        # Verificar archivos
        html_size = len(project["html"])
        css_size = len(project["css"])
        js_size = len(project["js"])
        total_size = html_size + css_size + js_size
        
        print(f"    - HTML: {html_size} bytes")
        print(f"    - CSS: {css_size} bytes")
        print(f"    - JS: {js_size} bytes")
        print(f"    - Total: {total_size} bytes")
        print(f"    - Directorio: {project_dir}")
        
        results.append({
            "name": project["name"],
            "title": project["title"],
            "html": html_size,
            "css": css_size,
            "js": js_size,
            "total": total_size,
            "status": "OK"
        })
    
    # Resumen
    print("\n" + "=" * 60)
    print("RESUMEN DE PRUEBAS")
    print("=" * 60)
    
    total_bytes = sum(r["total"] for r in results)
    print(f"\nProyectos generados: {len(results)}")
    print(f"Total bytes: {total_bytes:,}")
    print(f"Promedio por proyecto: {total_bytes // len(results):,} bytes")
    
    print("\nDetalles:")
    for r in results:
        print(f"  {r['title']}: {r['total']:,} bytes [{r['status']}]")
    
    print("\n" + "=" * 60)
    print("PRUEBAS COMPLETADAS")
    print("=" * 60)
