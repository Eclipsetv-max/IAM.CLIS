// TechZone Gaming - JavaScript
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
});