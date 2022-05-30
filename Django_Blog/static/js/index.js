'use strict';

const $buttonNav = document.getElementById('button-nav-main');
const $menu = document.getElementById('options-account');

if ($buttonNav) {
    $buttonNav.addEventListener('click', () => {
        $menu.classList.toggle('container-nav-options-user-account--show');
    });
}

function editCommentary(button, article) {
    article.childNodes[7].classList.toggle('container-form-edit-commentary--show');
    article.childNodes[3].classList.toggle('container-commentary__paragraph--hidden');
    article.childNodes[5].classList.toggle('container-commentary__paragraph--hidden');
    article.childNodes[9].classList.toggle('container-actions-commentary--hidden');
    button.classList.toggle('container-actions-commentary__link--hidden');
}

function cancelEditCommentary(button, article) {
    article.childNodes[7].classList.toggle('container-form-edit-commentary--show');
    article.childNodes[3].classList.toggle('container-commentary__paragraph--hidden');
    article.childNodes[5].classList.toggle('container-commentary__paragraph--hidden');
    article.childNodes[9].classList.toggle('container-actions-commentary--hidden');
    button.classList.toggle('container-actions-commentary__link--hidden');
}