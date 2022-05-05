'use strict';

const body = document.getElementById('body');
const containerLoader = document.getElementById('container-loader');

window.addEventListener('load', () => {
    containerLoader.classList.toggle('container-loader--show');
    body.classList.toggle('body');
});