'use strict';

function editCommentary(button, article) {
    article.childNodes[3].classList.toggle('container-form-edit-commentary--show');
    button.classList.toggle('container-actions-commentary__link--hidden');
}