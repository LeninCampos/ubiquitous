// Selección de elementos
const burger = document.querySelector('.burger');
const nav = document.querySelector('.nav-links');
const navLinks = document.querySelectorAll('.nav-links li');

// Función para abrir/cerrar menú móvil
const toggleMenu = () => {
    // Toggle Nav
    nav.classList.toggle('nav-active');

    // Animar enlaces
    navLinks.forEach((link, index) => {
        if (link.style.animation) {
            link.style.animation = '';
        } else {
            link.style.animation = `navLinkFade 0.5s ease forwards ${index / 7 + 0.3}s`;
        }
    });

    // Animación del botón hamburguesa
    burger.classList.toggle('toggle');
}

burger.addEventListener('click', toggleMenu);

// Opcional: Marcar link activo según scroll
window.addEventListener('scroll', () => {
    let current = '';
    const sections = document.querySelectorAll('section, header');
    
    sections.forEach(section => {
        const sectionTop = section.offsetTop;
        const sectionHeight = section.clientHeight;
        if (pageYOffset >= (sectionTop - sectionHeight / 3)) {
            current = section.getAttribute('id');
        }
    });
    
    // Aquí podrías agregar lógica para cambiar la clase 'active' en el nav
});