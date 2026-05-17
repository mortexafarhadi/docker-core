toggle_show_password = (e) => {
    let icon = e.firstElementChild;
    let parent = e.parentNode;
    const input = parent.querySelector('input');
    input.setAttribute('type', input.getAttribute('type') === 'password' ? 'text' : 'password');
    icon.classList.toggle('bi-eye');
    icon.classList.toggle('bi-eye-slash');
}