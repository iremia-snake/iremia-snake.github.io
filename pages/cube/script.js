'use strict'

const mainCube = document.getElementById('cube');
let parametrs = {};
const controlsForm = document.getElementById('controls-form');
const cubeSize = controlsForm.querySelector('input[name="input_size"]');
const cubePerspective = controlsForm.querySelector('input[name="input_perspective"]');
const cubeBorderWidth = controlsForm.querySelector('input[name="input_border_width"]');
const cubeOpacity= controlsForm.querySelector('input[name="input_opacity"]');
const cubeMouseControlOn= controlsForm.querySelector('input[name="mouse_control"]');

function throttle(func, limit){
    let inThrottle = false;
    return function(...args){
    if(!inThrottle){
        func.apply(this, args);
        inThrottle = true;
        setTimeout(() => {inThrottle = false}, limit);
        }
    }
}
function updateStyle(){
    let str = '';
    for(let key in parametrs){
        str += `--${key}:${parametrs[key]};`;
    }
    mainCube.style.cssText = str.slice(0, str.length-1);
}

function setCubeSize(event){
    parametrs['size'] = event.target.value + 'px';
    updateStyle();
}
function setCubePerspective(event){
    document.body.style.perspective = event.target.value + 'px';
}
function setCubeBorder(event){
    parametrs['border'] = event.target.value + 'px';
    updateStyle();
}

function rotateCube(event){
    mainCube.style.transform = `rotateX(${-event.pageY/window.innerHeight*360}deg) rotateY(${-event.pageX/window.innerWidth*360}deg)`;
}
function touchTotateCube(event){
    mainCube.style.transform = `rotateX(${-event.touches[0].clientY/window.innerHeight*360}deg) rotateY(${-event.touches[0].clientX/window.innerWidth*360}deg)`;
}

function setCubeMouseControl(event){
    if(event.target.checked){
        parametrs['auto'] = 0;
        document.body.addEventListener('mousemove', rotateCube);
        document.body.addEventListener('touchmove', touchTotateCube);
    }else{
        parametrs['auto'] = 1;
        document.body.removeEventListener('mousemove', rotateCube);
        document.body.removeEventListener('touchmove', touchTotateCube);
    }
    updateStyle();
}

function setCubeOpacity(event){
    Array.from(mainCube.getElementsByClassName('side')).forEach(element => {
        element.style.opacity = event.target.value;
    });
}

cubeSize.addEventListener('input', throttle(setCubeSize, 30)); 
cubePerspective.addEventListener('input', throttle(setCubePerspective, 30)); 
cubeBorderWidth.addEventListener('input', throttle(setCubeBorder, 30));
cubeOpacity.addEventListener('input', throttle(setCubeOpacity, 30));
cubeMouseControlOn.addEventListener('click', setCubeMouseControl);

/// механизм работы - по событию изменить параметр, собрать в строку настроек, применить
