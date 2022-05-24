'use strict';

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