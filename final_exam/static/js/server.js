$(document).ready(function () {
    // 获取当前时间的函数
    function getNowFormatDate() {
        var date = new Date();
        var seperator1 = "-";
        var seperator2 = ":";
        var month = date.getMonth() + 1;
        var strDate = date.getDate();
        if (month >= 1 && month <= 9) {
            month = "0" + month;
        }
        if (strDate >= 0 && strDate <= 9) {
            strDate = "0" + strDate;
        }
        var currentdate = date.getFullYear() + seperator1 + month + seperator1 + strDate
            + " " + date.getHours() + seperator2 + date.getMinutes()
            + seperator2 + date.getSeconds();
        return currentdate;
    }


    if (window.s) {
        window.s.close()
    }
    ;
    /*创建socket连接*/
    var socket = new WebSocket("ws://" + window.location.host + "/echo/" + $('#userid').val());
    socket.onopen = function () {
        console.log('WebSocket open');//成功连接上Websocket
    };
    socket.onmessage = function (e) {
        console.log('message: ' + e.data);//打印出服务端返回过来的数据
        $('#messagecontainer').prepend('<p>' + e.data + '</p>');
    };
    // Call onopen directly if socket is already open
    if (socket.readyState === WebSocket.OPEN) socket.onopen();
    window.s = socket;

    $('#send_message').click(function () {
        //如果未连接到websocket
        if (!window.s) {
            alert("websocket未连接.");
        } else {
            window.s.send($('#username').val() + ' ' + getNowFormatDate() + ':<br>' + $('#message').val());//通过websocket发送数据
        }
    });
    $('#close_websocket').click(function () {
        if (window.s) {
            window.s.close();//关闭websocket
            console.log('websocket已关闭');
        }
    });

});