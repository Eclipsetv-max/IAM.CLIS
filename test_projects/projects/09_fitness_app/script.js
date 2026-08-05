// FitPro - JavaScript
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
});