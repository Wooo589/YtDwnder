const drop_button = document.getElementById('dropdown');
const nav_list = document.getElementById('nav-opt');


drop_button.addEventListener('click', () => {
    nav_list.classList.toggle('active');
})


