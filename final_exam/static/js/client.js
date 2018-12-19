document.getElementById("setname").onclick = function(){
        var name = document.getElementById('name').value;
        if (name =='')return console.log('名字为空');
        ws = new WebSocket('ws://localhost:1000');

        ws.onopen = function () {
            ws.send(JSON.stringify({name:name,type:'setname'}));
        };

               document.getElementById('btn').onclick=function () {

            ws.send(JSON.stringify({text:document.getElementById('text').value,
                type:"chat"}));
        };

        //获取消息
        ws.onmessage =function (e) {
            JA = JSON.parse(e.data);
            text = JA.text
            document.getElementById('container').appendChild(createChatPanel(JSON.parse(e.data).text));
        };

        //防止点击两次
        document.getElementById('setname').setAttribute('disabled',true);


    };