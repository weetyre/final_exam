var ws = require('nodejs-websocket');

var server = ws.createServer(function (req,res) {
    console.log("new connection");
    //接收来自客户端的消息
    req.on('text',function (str) {
        console.log(str);

        var data = JSON.parse(str);

        switch (data.type) {
            case "setname":
                req.nickname = data.name;
                boardcast(JSON.stringify(
                    {
                       name:"server",
                       text: data.name+"加入了房间"
                    }
                ));
                break;
            case "chat":
                boardcast(JSON.stringify(
                    {
                        name:req.nickname,
                        text:data.text
                    }
                ));
                break;
            default:
        }

    });

    req.on('error',function (err) {
        console.log(err);
    });


    req.on('close',function () {
        boardcast(JSON.stringify(
            {
                name:"server",
                text: data.name+"离开了房间"
            }
        ));
    });

}).listen(1000);


//广播包多发
function boardcast(str) {
    server.connections.forEach(function (req) {
        req.sendText(str);
    })

};