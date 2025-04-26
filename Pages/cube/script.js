window.onload = Main;
        function Main(){
            RotateCube(document.getElementById("cube"),90*4);
            InputBool(document.getElementById("cube"),"--bool",document.getElementsByName("mouse_control")[0],"");
            SetStyle(document.body,"perspective",document.getElementsByName("input_perspective")[0],"px");
            SetStyle(document.getElementById("cube"),"--size",document.getElementsByName("input_size")[0],"px");
            SetStyle(document.getElementById("cube"),"--border",document.getElementsByName("input_border_width")[0],"px");
            SetStyle(document.getElementById("cube").children,"opacity",document.getElementsByName("input_opacity")[0],"");
        }
        function RotateCube(elem,sensivity){
            let window_width = window.getComputedStyle(document.body).width.slice(0,-2);
            let window_height = window.getComputedStyle(document.body).height.slice(0,-2);
            // console.log(window_width,window_height);
            document.body.addEventListener("mousemove",(event)=>{
                if(document.getElementsByName("mouse_control")[0].checked){
                    let x = event.pageX;
                    let y = event.pageY;
                    // let sensivity = 90*4;
                    let rotX = x/window_width*sensivity - sensivity/2;
                    let rotY = y/window_height*sensivity - sensivity/2;
                    elem.style.transform = `rotateX(${-rotY}deg) rotateY(${rotX}deg)`;
                }
            });
        }
        function SetStyle(elem,style,input,measurement){
            if(elem[0]){
                setInterval(()=>{
                    let value = input.value;
                    if (last_value != value){
                        last_value = value;
                        for (i of elem){
                            i.style.cssText += `${style}:${value}${measurement};`;
                        }
                        // console.log();
                    }
                },250);
            }
            let last_value;
            setInterval(()=>{
                let value = input.value;
                if (last_value != value){
                    last_value = value;
                    elem.style.cssText += `${style}:${value}${measurement};`;
                    // console.log();
                }
            },250);
        }
        function InputBool(elem,style,input,measurement){
            let last_value;
            setInterval(()=>{
                let value = input.checked;
                if (last_value != value){
                    last_value = value;
                    elem.style.cssText += `${style}:${!value*1}${measurement};`;
                    // console.log(value);
                }
            },250);
        }