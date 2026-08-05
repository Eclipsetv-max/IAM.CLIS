// SocialHub - JavaScript
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
});