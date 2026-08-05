// TaskFlow - JavaScript
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
});