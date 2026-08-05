// FoodExpress - JavaScript
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
});