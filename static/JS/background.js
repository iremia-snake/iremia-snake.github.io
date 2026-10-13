        function getCookie(name) {
        let cookies = document.cookie.split("; ");
        for (let cookie of cookies) {
            let [cookieName, ...rest] = cookie.split("=");
            if (cookieName === name) {
                return decodeURIComponent(rest.join("="));
            }
        }
        return null; // Cookie not found
    }

    bgUrl = getCookie('background');
    if (bgUrl && bgUrl != ''){
        setBg(bgUrl);
        document.body.querySelector('main').classList.add('bg-mobile-set');
    }

    function setBg(url){
        if(url){
            document.body.querySelector('main').classList.add('bg-mobile-set');
        }else{
            document.body.querySelector('main').classList.remove('bg-mobile-set');
        }
        document.body.style.backgroundImage = "url("+url+")";
    }

    Array.from(document.body.querySelectorAll('.select-background')).forEach(element => {
        element.onclick = ()=>{
            let url = element.querySelector('img').getAttribute('src');
            setBg(url);
            document.cookie = `background=${url}; path=/`;
        }
    });