// Функция для отображения и скрытия модального меню
// Получаем элементы меню и кнопки
const menuBtn = document.getElementById('menu-btn');
const modalMenu = document.getElementById('modal-menu');
const closeBtn = document.getElementById('close-btn');

// Открытие меню при клике на сэндвич-иконку
menuBtn.addEventListener('click', function() {
    modalMenu.style.display = 'block'; // Открываем меню
});

// Закрытие меню при клике на кнопку "Закрыть"
closeBtn.addEventListener('click', function() {
    modalMenu.style.display = 'none'; // Закрываем меню
});

// Закрытие меню при клике вне его области
document.addEventListener('click', function(event) {
    const isClickInsideMenu = modalMenu.contains(event.target);
    const isClickOnMenuBtn = menuBtn.contains(event.target);

    // Закрываем меню, если клик был вне меню и не по кнопке сэндвич
    if (!isClickInsideMenu && !isClickOnMenuBtn) {
        modalMenu.style.display = 'none';
    }
});

// Таймер для закрытия меню через небольшую задержку
function startCloseMenuTimer() {
    menuTimeout = setTimeout(() => {
        closeMenu();
    }, 500); // Задержка 500 мс перед закрытием меню
}