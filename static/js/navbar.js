const _button = document.querySelector('.burger')
const _open = document.querySelector('.open-btn')
const _close = document.querySelector('.close-btn')
const _navB = document.querySelector('nav ul')
const _mql = window.matchMedia('(min-width: 768px)');

/* Taking care of burgermenu if its slid in and media queries change */
const retreatBurger = e => {
    if (e.matches && _navB.classList.contains('active'))
        hideBurger()
}

const toggleBurger = () => {
    _navB.classList.toggle('active')
    _open.classList.toggle('invisible')
    _close.classList.toggle('invisible')
}

const hideBurger = () => {
    _navB.classList.remove('active')
    _open.classList.toggle('invisible')
    _close.classList.toggle('invisible')
}

_button.addEventListener('click', toggleBurger)
_mql.addEventListener('change', retreatBurger);