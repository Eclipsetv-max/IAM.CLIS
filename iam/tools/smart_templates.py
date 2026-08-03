# -*- coding: utf-8 -*-
"""
IAM Smart Templates - Templates inteligentes para proyectos web
Genera HTML, CSS y JS profesionales automaticamente
"""

from typing import Dict, Any, Optional


class SmartTemplates:
    """Templates inteligentes para diferentes tipos de proyectos web"""
    
    # Variables CSS por defecto
    DEFAULT_VARS = """/* ========================================
   VARIABLES
   ======================================== */
:root {
    --primary: #6366f1;
    --primary-dark: #4f46e5;
    --primary-light: #818cf8;
    --secondary: #ec4899;
    --secondary-dark: #db2777;
    --accent: #06b6d4;
    --dark: #0f172a;
    --darker: #020617;
    --dark-light: #1e293b;
    --light: #f8fafc;
    --gray: #94a3b8;
    --gray-dark: #334155;
    --success: #22c55e;
    --warning: #f59e0b;
    --error: #ef4444;
    --gradient: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
    --gradient-dark: linear-gradient(135deg, var(--dark) 0%, var(--darker) 100%);
    --shadow-sm: 0 1px 2px rgba(0,0,0,0.3);
    --shadow: 0 4px 6px -1px rgba(0,0,0,0.3);
    --shadow-lg: 0 20px 40px rgba(0,0,0,0.4);
    --shadow-glow: 0 0 30px rgba(99, 102, 241, 0.3);
    --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    --transition-fast: all 0.15s ease;
    --radius-sm: 8px;
    --radius: 12px;
    --radius-lg: 20px;
    --radius-full: 50px;
}"""
    
    # Reset CSS base
    BASE_RESET = """/* ========================================
   RESET
   ======================================== */
*, *::before, *::after {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

html {
    scroll-behavior: smooth;
    font-size: 16px;
}

body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background: var(--dark);
    color: var(--light);
    line-height: 1.6;
    overflow-x: hidden;
    -webkit-font-smoothing: antialiased;
}

img {
    max-width: 100%;
    height: auto;
    display: block;
}

a {
    text-decoration: none;
    color: inherit;
    transition: var(--transition);
}

ul, ol {
    list-style: none;
}

button {
    cursor: pointer;
    border: none;
    background: none;
    font-family: inherit;
}

input, textarea, select {
    font-family: inherit;
    font-size: inherit;
}"""
    
    # Navbar base
    NAVBAR_TEMPLATE = """/* ========================================
   NAVBAR
   ======================================== */
.navbar {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 1000;
    padding: 1rem 5%;
    transition: var(--transition);
    background: transparent;
}

.navbar.scrolled {
    background: rgba(15, 23, 42, 0.95);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    box-shadow: var(--shadow);
    padding: 0.7rem 5%;
}

.nav-container {
    max-width: 1200px;
    margin: 0 auto;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.logo {
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--light);
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.logo-icon {
    font-size: 1.8rem;
}

.logo-text {
    background: var(--gradient);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.nav-links {
    display: flex;
    gap: 2rem;
}

.nav-links a {
    color: var(--light);
    font-weight: 500;
    position: relative;
    padding: 0.5rem 0;
}

.nav-links a::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    width: 0;
    height: 2px;
    background: var(--gradient);
    transition: var(--transition);
}

.nav-links a:hover::after,
.nav-links a.active::after {
    width: 100%;
}

.nav-links a:hover,
.nav-links a.active {
    color: var(--primary-light);
}

.hamburger {
    display: none;
    flex-direction: column;
    gap: 5px;
    cursor: pointer;
    z-index: 1001;
}

.hamburger span {
    width: 25px;
    height: 3px;
    background: var(--light);
    border-radius: 2px;
    transition: var(--transition);
}

.hamburger.active span:nth-child(1) {
    transform: rotate(45deg) translate(5px, 5px);
}

.hamburger.active span:nth-child(2) {
    opacity: 0;
}

.hamburger.active span:nth-child(3) {
    transform: rotate(-45deg) translate(7px, -6px);
}"""
    
    # Hero base
    HERO_TEMPLATE = """/* ========================================
   HERO
   ======================================== */
.hero {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 2rem 5%;
    position: relative;
    overflow: hidden;
}

.hero::before {
    content: '';
    position: absolute;
    inset: 0;
    background: var(--gradient);
    opacity: 0.9;
}

.hero-bg {
    position: absolute;
    inset: 0;
    background-size: cover;
    background-position: center;
    opacity: 0.15;
}

.hero-content {
    position: relative;
    z-index: 1;
    max-width: 900px;
}

.hero-badge {
    display: inline-block;
    padding: 0.5rem 1.5rem;
    background: rgba(255,255,255,0.1);
    border: 1px solid rgba(255,255,255,0.2);
    border-radius: var(--radius-full);
    font-size: 0.9rem;
    margin-bottom: 1.5rem;
    backdrop-filter: blur(10px);
}

.hero h1 {
    font-size: clamp(2.5rem, 8vw, 5rem);
    font-weight: 700;
    line-height: 1.1;
    margin-bottom: 1.5rem;
}

.hero-subtitle {
    font-size: clamp(1rem, 2.5vw, 1.3rem);
    opacity: 0.9;
    margin-bottom: 2rem;
    max-width: 600px;
    margin-left: auto;
    margin-right: auto;
}

.hero-buttons {
    display: flex;
    gap: 1rem;
    justify-content: center;
    flex-wrap: wrap;
}"""
    
    # Buttons
    BUTTONS_TEMPLATE = """/* ========================================
   BUTTONS
   ======================================== */
.btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    padding: 1rem 2rem;
    border-radius: var(--radius-full);
    font-weight: 600;
    font-size: 1rem;
    transition: var(--transition);
    cursor: pointer;
    border: none;
    white-space: nowrap;
}

.btn-primary {
    background: var(--gradient);
    color: var(--light);
    box-shadow: 0 4px 20px rgba(99, 102, 241, 0.4);
}

.btn-primary:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 30px rgba(99, 102, 241, 0.5);
}

.btn-secondary {
    background: rgba(255,255,255,0.1);
    color: var(--light);
    border: 2px solid rgba(255,255,255,0.3);
    backdrop-filter: blur(10px);
}

.btn-secondary:hover {
    background: rgba(255,255,255,0.2);
    transform: translateY(-3px);
}

.btn-outline {
    background: transparent;
    color: var(--light);
    border: 2px solid var(--light);
}

.btn-outline:hover {
    background: var(--light);
    color: var(--dark);
}

.btn-lg {
    padding: 1.2rem 3rem;
    font-size: 1.1rem;
}

.btn-sm {
    padding: 0.7rem 1.5rem;
    font-size: 0.9rem;
}"""
    
    # Sections
    SECTIONS_TEMPLATE = """/* ========================================
   SECTIONS
   ======================================== */
.section {
    padding: clamp(4rem, 10vw, 8rem) 5%;
}

.section-dark {
    background: var(--darker);
}

.section-header {
    text-align: center;
    margin-bottom: 4rem;
}

.section-header h2 {
    font-size: clamp(2rem, 5vw, 3rem);
    font-weight: 700;
    margin-bottom: 1rem;
}

.section-header p {
    color: var(--gray);
    max-width: 600px;
    margin: 0 auto;
    font-size: 1.1rem;
}

.section-line {
    width: 80px;
    height: 4px;
    background: var(--gradient);
    margin: 1.5rem auto;
    border-radius: 2px;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 clamp(1rem, 5vw, 2rem);
}"""
    
    # Cards
    CARDS_TEMPLATE = """/* ========================================
   CARDS
   ======================================== */
.cards-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
}

.card {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: var(--radius-lg);
    padding: 2rem;
    transition: var(--transition);
    position: relative;
    overflow: hidden;
}

.card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: var(--gradient);
    transform: scaleX(0);
    transition: var(--transition);
}

.card:hover {
    transform: translateY(-10px);
    border-color: rgba(99, 102, 241, 0.3);
    box-shadow: var(--shadow-lg);
}

.card:hover::before {
    transform: scaleX(1);
}

.card-icon {
    width: 70px;
    height: 70px;
    background: var(--gradient);
    border-radius: var(--radius);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2rem;
    margin-bottom: 1.5rem;
}

.card h3 {
    font-size: 1.3rem;
    font-weight: 600;
    margin-bottom: 0.75rem;
}

.card p {
    color: var(--gray);
    line-height: 1.7;
}"""
    
    # Stats
    STATS_TEMPLATE = """/* ========================================
   STATS
   ======================================== */
.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 2rem;
}

.stat-card {
    text-align: center;
    padding: 2rem;
}

.stat-icon {
    font-size: 2.5rem;
    margin-bottom: 1rem;
}

.stat-number {
    font-size: clamp(2.5rem, 5vw, 3.5rem);
    font-weight: 700;
    background: var(--gradient);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1;
}

.stat-label {
    color: var(--gray);
    margin-top: 0.5rem;
    font-size: 1rem;
}"""
    
    # Footer
    FOOTER_TEMPLATE = """/* ========================================
   FOOTER
   ======================================== */
.footer {
    background: var(--darker);
    padding: 4rem 5% 2rem;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.footer-content {
    max-width: 1200px;
    margin: 0 auto;
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 3rem;
    margin-bottom: 3rem;
}

.footer-section h4 {
    font-size: 1.2rem;
    margin-bottom: 1.5rem;
    background: var(--gradient);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.footer-section p {
    color: var(--gray);
    margin-bottom: 1rem;
}

.footer-links {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
}

.footer-links a {
    color: var(--gray);
    transition: var(--transition);
}

.footer-links a:hover {
    color: var(--primary-light);
    padding-left: 5px;
}

.footer-bottom {
    text-align: center;
    padding-top: 2rem;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    color: var(--gray);
}

.social-links {
    display: flex;
    gap: 1rem;
    margin-top: 1rem;
}

.social-link {
    width: 45px;
    height: 45px;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: var(--transition);
}

.social-link:hover {
    background: var(--gradient);
    transform: translateY(-3px);
}"""
    
    # Animations
    ANIMATIONS_TEMPLATE = """/* ========================================
   ANIMATIONS
   ======================================== */
@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

@keyframes slideInLeft {
    from {
        opacity: 0;
        transform: translateX(-30px);
    }
    to {
        opacity: 1;
        transform: translateX(0);
    }
}

@keyframes slideInRight {
    from {
        opacity: 0;
        transform: translateX(30px);
    }
    to {
        opacity: 1;
        transform: translateX(0);
    }
}

@keyframes pulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.05); }
}

@keyframes float {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-10px); }
}

.animate-fadeInUp {
    animation: fadeInUp 0.6s ease forwards;
}

.animate-fadeIn {
    animation: fadeIn 0.6s ease forwards;
}

.animate-slideInLeft {
    animation: slideInLeft 0.6s ease forwards;
}

.animate-slideInRight {
    animation: slideInRight 0.6s ease forwards;
}

/* Scroll reveal */
.reveal {
    opacity: 0;
    transform: translateY(30px);
    transition: all 0.6s ease;
}

.reveal.active {
    opacity: 1;
    transform: translateY(0);
}"""
    
    # Responsive
    RESPONSIVE_TEMPLATE = """/* ========================================
   RESPONSIVE
   ======================================== */
@media (max-width: 1200px) {
    .container {
        max-width: 1000px;
    }
}

@media (max-width: 1024px) {
    .nav-links {
        gap: 1.5rem;
    }
}

@media (max-width: 768px) {
    .nav-links {
        position: fixed;
        top: 0;
        right: -100%;
        width: 70%;
        max-width: 300px;
        height: 100vh;
        background: var(--darker);
        flex-direction: column;
        justify-content: center;
        align-items: center;
        gap: 2rem;
        transition: var(--transition);
        box-shadow: -10px 0 30px rgba(0,0,0,0.3);
    }

    .nav-links.active {
        right: 0;
    }

    .hamburger {
        display: flex;
    }

    .hero h1 {
        font-size: clamp(2rem, 10vw, 3rem);
    }

    .hero-buttons {
        flex-direction: column;
        align-items: center;
    }

    .cards-grid {
        grid-template-columns: 1fr;
    }

    .footer-content {
        grid-template-columns: 1fr;
        text-align: center;
    }

    .social-links {
        justify-content: center;
    }
}

@media (max-width: 480px) {
    html {
        font-size: 14px;
    }

    .section {
        padding: 3rem 5%;
    }

    .btn {
        padding: 0.8rem 1.5rem;
    }

    .btn-lg {
        padding: 1rem 2rem;
    }
}"""
    
    # Utilities
    UTILITIES_TEMPLATE = """/* ========================================
   UTILITIES
   ======================================== */
.text-gradient {
    background: var(--gradient);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.text-center { text-align: center; }
.text-left { text-align: left; }
.text-right { text-align: right; }

.mb-0 { margin-bottom: 0; }
.mb-1 { margin-bottom: 0.5rem; }
.mb-2 { margin-bottom: 1rem; }
.mb-3 { margin-bottom: 1.5rem; }
.mb-4 { margin-bottom: 2rem; }
.mb-5 { margin-bottom: 3rem; }

.mt-0 { margin-top: 0; }
.mt-1 { margin-top: 0.5rem; }
.mt-2 { margin-top: 1rem; }
.mt-3 { margin-top: 1.5rem; }
.mt-4 { margin-top: 2rem; }
.mt-5 { margin-top: 3rem; }

.hidden { display: none !important; }
.visible { visibility: visible; }
.invisible { visibility: hidden; }

.overflow-hidden { overflow: hidden; }
.relative { position: relative; }
.absolute { position: absolute; }

.flex { display: flex; }
.flex-col { flex-direction: column; }
.flex-wrap { flex-wrap: wrap; }
.items-center { align-items: center; }
.justify-center { justify-content: center; }
.justify-between { justify-content: space-between; }
.gap-1 { gap: 0.5rem; }
.gap-2 { gap: 1rem; }
.gap-3 { gap: 1.5rem; }
.gap-4 { gap: 2rem; }

.w-full { width: 100%; }
.h-full { height: 100%; }
.min-h-screen { min-height: 100vh; }

.rounded-sm { border-radius: var(--radius-sm); }
.rounded { border-radius: var(--radius); }
.rounded-lg { border-radius: var(--radius-lg); }
.rounded-full { border-radius: 50%; }

.shadow-sm { box-shadow: var(--shadow-sm); }
.shadow { box-shadow: var(--shadow); }
.shadow-lg { box-shadow: var(--shadow-lg); }

.transition { transition: var(--transition); }
.transition-fast { transition: var(--transition-fast); }

/* Scrollbar personalizado */
::-webkit-scrollbar {
    width: 10px;
}

::-webkit-scrollbar-track {
    background: var(--darker);
}

::-webkit-scrollbar-thumb {
    background: var(--primary);
    border-radius: 5px;
}

::-webkit-scrollbar-thumb:hover {
    background: var(--primary-dark);
}"""
    
    @classmethod
    def get_full_css(cls) -> str:
        """Obtener CSS completo con todos los templates"""
        return "\n\n".join([
            cls.DEFAULT_VARS,
            cls.BASE_RESET,
            cls.NAVBAR_TEMPLATE,
            cls.HERO_TEMPLATE,
            cls.BUTTONS_TEMPLATE,
            cls.SECTIONS_TEMPLATE,
            cls.CARDS_TEMPLATE,
            cls.STATS_TEMPLATE,
            cls.FOOTER_TEMPLATE,
            cls.ANIMATIONS_TEMPLATE,
            cls.RESPONSIVE_TEMPLATE,
            cls.UTILITIES_TEMPLATE
        ])
    
    @classmethod
    def get_base_html(cls, title: str = "Mi Proyecto", description: str = "") -> str:
        """Obtener HTML base estructurado"""
        return f'''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{description}">
    <title>{title}</title>
    <link rel="stylesheet" href="style.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body>
    <!-- Navbar -->
    <nav class="navbar" id="navbar">
        <div class="nav-container">
            <a href="#" class="logo">
                <span class="logo-icon">⚡</span>
                <span class="logo-text">MiProyecto</span>
            </a>
            <ul class="nav-links" id="navLinks">
                <li><a href="#inicio" class="active">Inicio</a></li>
                <li><a href="#servicios">Servicios</a></li>
                <li><a href="#about">Nosotros</a></li>
                <li><a href="#contacto">Contacto</a></li>
            </ul>
            <div class="hamburger" id="hamburger">
                <span></span>
                <span></span>
                <span></span>
            </div>
        </div>
    </nav>

    <!-- Hero -->
    <section class="hero" id="inicio">
        <div class="hero-content">
            <span class="hero-badge">✨ Bienvenido</span>
            <h1>Titulo <span class="text-gradient">Principal</span></h1>
            <p class="hero-subtitle">Subtitulo descriptivo de tu proyecto aqui</p>
            <div class="hero-buttons">
                <a href="#servicios" class="btn btn-primary btn-lg">
                    <i class="fas fa-arrow-right"></i> Empezar
                </a>
                <a href="#about" class="btn btn-secondary btn-lg">
                    <i class="fas fa-info-circle"></i> Saber Mas
                </a>
            </div>
        </div>
    </section>

    <!-- Stats -->
    <section class="section section-dark" id="stats">
        <div class="container">
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-icon">🎯</div>
                    <div class="stat-number" data-target="150">0</div>
                    <div class="stat-label">Proyectos</div>
                </div>
                <div class="stat-card">
                    <div class="stat-icon">😊</div>
                    <div class="stat-number" data-target="100">0</div>
                    <div class="stat-label">Clientes</div>
                </div>
                <div class="stat-card">
                    <div class="stat-icon">⭐</div>
                    <div class="stat-number" data-target="99">0</div>
                    <div class="stat-label">% Satisfaccion</div>
                </div>
            </div>
        </div>
    </section>

    <!-- Servicios -->
    <section class="section" id="servicios">
        <div class="container">
            <div class="section-header">
                <h2>Nuestros <span class="text-gradient">Servicios</span></h2>
                <div class="section-line"></div>
                <p>Ofrecemos las mejores soluciones para tu negocio</p>
            </div>
            <div class="cards-grid">
                <div class="card">
                    <div class="card-icon">🚀</div>
                    <h3>Servicio 1</h3>
                    <p>Descripcion del primer servicio que ofreces</p>
                </div>
                <div class="card">
                    <div class="card-icon">💡</div>
                    <h3>Servicio 2</h3>
                    <p>Descripcion del segundo servicio que ofreces</p>
                </div>
                <div class="card">
                    <div class="card-icon">🛡️</div>
                    <h3>Servicio 3</h3>
                    <p>Descripcion del tercer servicio que ofreces</p>
                </div>
            </div>
        </div>
    </section>

    <!-- About -->
    <section class="section section-dark" id="about">
        <div class="container">
            <div class="section-header">
                <h2>Sobre <span class="text-gradient">Nosotros</span></h2>
                <div class="section-line"></div>
                <p>Conoce mas sobre nuestra empresa</p>
            </div>
        </div>
    </section>

    <!-- Contacto -->
    <section class="section" id="contacto">
        <div class="container">
            <div class="section-header">
                <h2>Contacto</h2>
                <div class="section-line"></div>
                <p>Envianos un mensaje</p>
            </div>
        </div>
    </section>

    <!-- Footer -->
    <footer class="footer">
        <div class="footer-content">
            <div class="footer-section">
                <h4>MiProyecto</h4>
                <p>Tu descripcion aqui</p>
                <div class="social-links">
                    <a href="#" class="social-link"><i class="fab fa-facebook-f"></i></a>
                    <a href="#" class="social-link"><i class="fab fa-twitter"></i></a>
                    <a href="#" class="social-link"><i class="fab fa-instagram"></i></a>
                </div>
            </div>
            <div class="footer-section">
                <h4>Links</h4>
                <div class="footer-links">
                    <a href="#inicio">Inicio</a>
                    <a href="#servicios">Servicios</a>
                    <a href="#about">Nosotros</a>
                    <a href="#contacto">Contacto</a>
                </div>
            </div>
            <div class="footer-section">
                <h4>Contacto</h4>
                <div class="footer-links">
                    <a href="mailto:info@proyecto.com"><i class="fas fa-envelope"></i> info@proyecto.com</a>
                    <a href="tel:+123456789"><i class="fas fa-phone"></i> +1 234 567 89</a>
                </div>
            </div>
        </div>
        <div class="footer-bottom">
            <p>&copy; 2026 MiProyecto. Todos los derechos reservados.</p>
        </div>
    </footer>

    <script src="script.js"></script>
</body>
</html>'''
    
    @classmethod
    def get_base_js(cls) -> str:
        """Obtener JavaScript base funcional"""
        return '''// ========================================
// INICIALIZACION
// ========================================
document.addEventListener('DOMContentLoaded', () => {
    initNavbar();
    initMobileMenu();
    initScrollAnimations();
    initCounters();
    initSmoothScroll();
});

// ========================================
// NAVBAR SCROLL
// ========================================
function initNavbar() {
    const navbar = document.getElementById('navbar');
    if (!navbar) return;

    const handleScroll = () => {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    };

    window.addEventListener('scroll', handleScroll);
    handleScroll(); // Ejecutar una vez al cargar
}

// ========================================
// MENU MOBILE
// ========================================
function initMobileMenu() {
    const hamburger = document.getElementById('hamburger');
    const navLinks = document.getElementById('navLinks');
    if (!hamburger || !navLinks) return;

    hamburger.addEventListener('click', () => {
        hamburger.classList.toggle('active');
        navLinks.classList.toggle('active');
    });

    // Cerrar al hacer click en un link
    navLinks.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', () => {
            hamburger.classList.remove('active');
            navLinks.classList.remove('active');
        });
    });

    // Cerrar al hacer click fuera
    document.addEventListener('click', (e) => {
        if (!hamburger.contains(e.target) && !navLinks.contains(e.target)) {
            hamburger.classList.remove('active');
            navLinks.classList.remove('active');
        }
    });
}

// ========================================
// SCROLL REVEAL ANIMATIONS
// ========================================
function initScrollAnimations() {
    const elements = document.querySelectorAll('.reveal, .card, .stat-card');
    if (!elements.length) return;

    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                setTimeout(() => {
                    entry.target.classList.add('active');
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }, index * 100);
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });

    elements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'all 0.6s ease';
        observer.observe(el);
    });
}

// ========================================
// COUNTER ANIMATION
// ========================================
function initCounters() {
    const counters = document.querySelectorAll('.stat-number[data-target]');
    if (!counters.length) return;

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                animateCounter(entry.target);
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });

    counters.forEach(counter => observer.observe(counter));
}

function animateCounter(element) {
    const target = parseInt(element.getAttribute('data-target')) || 0;
    const duration = 2000;
    const increment = target / (duration / 16);
    let current = 0;

    const updateCounter = () => {
        current += increment;
        if (current < target) {
            element.textContent = Math.floor(current);
            requestAnimationFrame(updateCounter);
        } else {
            element.textContent = target + '+';
        }
    };

    updateCounter();
}

// ========================================
// SMOOTH SCROLL
// ========================================
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                const headerOffset = 80;
                const elementPosition = target.getBoundingClientRect().top;
                const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

                window.scrollTo({
                    top: offsetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });

    // Active link highlight
    const sections = document.querySelectorAll('section[id]');
    window.addEventListener('scroll', () => {
        let current = '';
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            if (window.pageYOffset >= sectionTop - 200) {
                current = section.getAttribute('id');
            }
        });

        document.querySelectorAll('.nav-links a').forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === `#${current}`) {
                link.classList.add('active');
            }
        });
    });
}

// ========================================
// UTILIDADES
// ========================================
function debounce(func, wait = 20) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

function throttle(func, limit) {
    let inThrottle;
    return function(...args) {
        if (!inThrottle) {
            func.apply(this, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// Lazy loading para imagenes
if ('IntersectionObserver' in window) {
    const imageObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                if (img.dataset.src) {
                    img.src = img.dataset.src;
                    img.removeAttribute('data-src');
                }
                imageObserver.unobserve(img);
            }
        });
    });

    document.querySelectorAll('img[data-src]').forEach(img => {
        imageObserver.observe(img);
    });
}'''


# Instancia global
smart_templates = SmartTemplates()
