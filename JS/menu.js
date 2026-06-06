function changwNavSubmenuSide(event){
            element = event.srcElement.parentElement;
            var el_rect = element.getBoundingClientRect()
            var width = window.innerWidth;
            if (el_rect.x + el_rect.width*2 > width){
                element.classList.add("left");
            }
            else{
                element.classList.remove("left");
            }
        }


function main(){
    document.body.className += " loaded";

    Array.from(document.body.getElementsByClassName("submenu")).forEach(element => {
        element.onclick = changwNavSubmenuSide;
        element.onmouseover = changwNavSubmenuSide;
    });
}


document.addEventListener('DOMContentLoaded', () => {
    main();
});
