let e = $('#user');
var uid = e.data("id");
var username = e.data("username");
var currentChat = null;


function appendMsg(data) {
    let from = data["from"];
    let to = data["to"];
    //let msg_show = document.getElementById("msg-show");
    let html_div_content;

    if (data['from'] == uid) {
        html_div_content = '<div class="media text-muted py-2 msg-item msg-mine" data-userid="' + from + '"><div class="d-flex msg-container"><img data-src="" alt="32x32" class="rounded img-face-msg" src="/static/img/face.jpg" data-holder-rendered="true"><p class="media-body mb-0 small lh-125 p-2 msg-content">' + data.msg + '</p></div></div>'
    } else {
        if (currentChat == to || to == uid) {
            html_div_content = '<div class="media text-muted py-2 msg-item msg-other" data-userid="' + from + '"><div class="d-flex msg-container"><img data-src="" alt="32x32" class="rounded img-face-msg" src="/static/img/face.jpg" data-holder-rendered="true"><p class="media-body mb-0 small lh-125 p-2 msg-content">' + data.msg + '</p></div></div>'
            //然后把数据存在数据库里
        } else {
            //先把数据存在数据库里
        }
    }
    $('#msg-show').append(html_div_content)
}


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
        let data = JSON.parse(e.data);
        console.log('message: ' + data);//打印出服务端返回过来的数据
        if (data.from == currentChat || data.to == currentChat) {
            appendMsg(data);
            /*if (isNewInWindow()) {
                scrollToEnd()
            }*/
        }
    };
    // Call onopen directly if socket is already open
    if (socket.readyState === WebSocket.OPEN) socket.onopen();
    window.s = socket;

    //send message to server
    function sendMsg() {
        //如果未连接到websocket
        if (!window.s) {
            alert("websocket未连接.");
        } else {
            let inputArea = $('#tx-input');
            let content = inputArea.val();
            //if don't choose a user to chat or input is blank
            if (currentChat == null || content == '') {
                return
            }

            let data = {'from': uid, 'to': currentChat, 'msg': content};
            window.s.send(JSON.stringify(data));//通过websocket发送数据

            //clear input area
            inputArea.val('')
        }
    }

    $('#close_websocket').click(function () {
        if (window.s) {
            window.s.close();//关闭websocket
            console.log('websocket已关闭');
        }
    });

    // send button
    $('#bt-send').click(function () {
        sendMsg()
    });

    //listen to the Enter key
    $(document).keydown(function (event) {
        if (event.keyCode == 13) {
            sendMsg();
        }
    });


    /*将页面下拉到最新消息处*/
    function scrollToEnd() {
        let div = document.getElementById("msg-show");
        let len = div.length;
        let hei = div.height;
        let div_length = len - 6;
        div[div_length].scrollIntoView({behavior: "smooth"});	   //平滑滚动，提高了用户体验

    }

    /*判断当有新信息来时，用户是否在页面底端*/
    function isNewInWindow() {
        let msgShowDiv = document.getElementById("msg-show");
        let last = msgShowDiv.lastElementChild;
        return true;
    }

    /*判定元素是否在界面内*/
    function isInWindow(x) {
        if (x.getBoundingClientRect().top > window.innerHeight) {
            // 元素低于当前界面
            return false;
        } else if (x.getBoundingClientRect().bottom < 0) {
            // 元素高于当前界面
            return false;
        }
        return true;
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

