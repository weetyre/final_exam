let e = $('#user');
var uid = e.data("id");
var username = e.data("username");
var currentChat = null;

$(function () {


    if (window.s) {
        window.s.close()
    }
    /*创建socket连接*/
    var socket = new WebSocket("ws://" + window.location.host + "/echo/" + uid);
    socket.onopen = function () {
        console.log('WebSocket open');//成功连接上Websocket
    };
    socket.onmessage = function (e) {
        console.log('message: ' + e.data);//打印出服务端返回过来的数据

        append_msg(JSON.parse(e.data));
    };
    // Call onopen directly if socket is already open
    if (socket.readyState === WebSocket.OPEN) socket.onopen();
    window.s = socket;

    // send button
    $('#bt-send').click(function () {
        //如果未连接到websocket
        if (!window.s) {
            alert("websocket未连接.");
        } else {
            let inputArea = $('#tx-input');
            let content = inputArea.val();
            if (currentChat == null || content == '') {
                return
            }

            let data = {'from': uid, 'to': currentChat, 'msg': content};
            window.s.send(JSON.stringify(data));//通过websocket发送数据

            inputArea.val('')
        }
    });
    $('#close_websocket').click(function () {
        if (window.s) {
            window.s.close();//关闭websocket
            console.log('websocket已关闭');
        }
    });

    function append_msg(data) {
        let from = data["from"];
        //let msg_show = document.getElementById("msg-show");
        var html_div_content;

        if (data['from'] == uid) {
            html_div_content = '<div class="media text-muted py-2 msg-item msg-mine" data-userid="' + from + '"><div class="d-flex msg-container"><img data-src="" alt="32x32" class="rounded img-face-msg" src="/static/img/face.jpg" data-holder-rendered="true"><p class="media-body mb-0 small lh-125 p-2 msg-content">' + data.msg + '</p></div></div>'
        } else {
            html_div_content = '<div class="media text-muted py-2 msg-item msg-other" data-userid="' + from + '"><div class="d-flex msg-container"><img data-src="" alt="32x32" class="rounded img-face-msg" src="/static/img/face.jpg" data-holder-rendered="true"><p class="media-body mb-0 small lh-125 p-2 msg-content">' + data.msg + '</p></div></div>'
        }
        $('#msg-show').append(html_div_content)
    }

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

});

