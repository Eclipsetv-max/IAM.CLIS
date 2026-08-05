// ChatApp - JavaScript
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
});