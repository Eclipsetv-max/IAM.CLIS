// LuxeStay - JavaScript
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
});