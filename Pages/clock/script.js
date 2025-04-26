window.onload = Main;

function getPlate(n){
    return document.querySelectorAll('.clock-number')[n];
}
function getSymb(n){
    return getPlate(n).querySelector('.card .front').innerText;
}
function setSymb(n, symbol){
    let clockNumber = getPlate(n);
    while (clockNumber.firstChild) {
        clockNumber.removeChild(clockNumber.firstChild);
    }
    let newCardPair=`
    <div class="card">
        <span class="symbol back"></span>
        <span class="symbol front">${symbol}</span>
    </div>
    <div class="card flip">
        <span class="symbol back">${symbol}</span>
        <span class="symbol front"></span>
    </div>
    `;
    clockNumber.insertAdjacentHTML("beforeend", newCardPair);
}
function changeSymb(n, symb){
    let clockNumber = getPlate(n);
    clockNumber.querySelector('.card .symbol.back').innerText = symb;
    let newCard=`
    <div class="card">
        <span class="symbol back"></span>
        <span class="symbol front">${symb}</span>
    </div>`;
    clockNumber.insertAdjacentHTML('afterbegin',newCard);
    clockNumber.children[1].classList.add('flip');
    setTimeout(()=>{
        clockNumber.lastElementChild.remove();
    }, 650);
}
function flip(n){
    let clockNumber = getPlate(n);
    clockNumber.onmouseenter = ()=>{clockNumber.children[1].classList.add('flip');}
    clockNumber.onmouseleave = ()=>{clockNumber.children[1].classList.remove('flip');}
}
function randInt(min, max){
    return Math.round(Math.random()*(max-min)+min);
}
function symbol(n){
    symbolString = `qwertyuiop[]asdfghjkl;zxcvbnm,./1234567890-=`;
    return symbolString[n%symbolString.length];
}
function clock(){
    let date = new Date();
    let numArr = [];
    numArr[0] = Math.floor(date.getHours()*0.1);
    numArr[1] = date.getHours()%10;
    numArr[2] = Math.floor(date.getMinutes()*0.1);
    numArr[3] = date.getMinutes()%10;
    numArr[4] = Math.floor(date.getSeconds()*0.1);
    numArr[5] = date.getSeconds()%10;

    for(let i = 0; i < numArr.length; i++){
        if(getSymb(i) != numArr[i]) changeSymb(i,numArr[i]);
    }
}
function Main(){
    for(let i = 0; i < document.querySelectorAll('.clock-number').length; i++){
        setSymb(i, '0'); 
    }
    setInterval(clock, 1000);
}