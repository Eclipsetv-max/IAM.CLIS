// AnalyticsPro Dashboard - JavaScript
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
});