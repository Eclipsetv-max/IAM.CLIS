// EduMaster - JavaScript
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
});