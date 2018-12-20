let e = $('#user');
var uid = e.data("id");
var username = e.data("username");
var currentChat = null;
var totalOnline = 1;


function appendMsg(data) {
    let from = data["from"];
    let to = data["to"];
    //let msg_show = document.getElementById("msg-show");
    let html_div_content;

    if (from == uid && to == currentChat) {
        html_div_content = '<div class="media text-muted py-2 msg-item msg-mine" data-userid="' + from + '"><div class="d-flex msg-container"><img data-src="" alt="32x32" class="rounded img-face-msg" src="/static/img/face.jpg" data-holder-rendered="true"><p class="media-body mb-0 small lh-125 p-2 msg-content">' + data.msg + '</p></div></div>'
    } else if (from == currentChat && to == uid) {
        html_div_content = '<div class="media text-muted py-2 msg-item msg-other" data-userid="' + from + '"><div class="d-flex msg-container"><img data-src="" alt="32x32" class="rounded img-face-msg" src="/static/img/face.jpg" data-holder-rendered="true"><p class="media-body mb-0 small lh-125 p-2 msg-content">' + data.msg + '</p></div></div>'
    } else {
        return
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
        let type = data['type'];
        console.log('message: ' + data);//打印出服务端返回过来的数据

        if (type == 'msg') {
            if (data.from == currentChat || data.to == currentChat) {
                appendMsg(data);
                /*if (isNewInWindow()) {
                    scrollToEnd()
                }*/
            }
        }else if (type == 'broadcast') {
            let t_id = data['id'];
            if (t_id == uid){

            } else if (data['msg'] == 'on') {
                let html = '<div class="media text-muted my-tab-item" id="g' + data['id'] + '" ><img alt="32x32" class="mr-2 rounded img-face" src="/static/img/face.jpg" data-holder-rendered="true"><p class="media-body mb-0 small lh-125"><strong class="d-block text-gray-dark">' + data['username'] + '</strong></p></div>'
                $('#friends').append(html);
            } else if (data['msg'] == 'off') {
                $('#g' + t_id).remove()
            }
        }

    };
    // Call onopen directly if socket is already open
    if (socket.readyState === WebSocket.OPEN) socket.onopen();
    window.s = socket;


    function keep_up() {
        //用户上线时发送type 以及自己的uid
        let data = {'uid': uid, 'username':username,'type': 1};
        window.s.send(JSON.stringify(data));
    }


    //send message to server
    function sendMsg() {
        //如果未连接到websocket
        if (!window.s) {
            alert("websocket未连接.");
        } else {
            let inputArea = $('#tx-input');
            let content = inputArea.val();
            //if don't choose a user to chat or input is blank
            if (currentChat == null || content.replace(/\s*/g,"") == '') {
                inputArea.val('');
                return
            }

            let data = {'type': 'msg', 'from': uid, 'to': currentChat, 'msg': content};
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
        let e = $('#msg-show');
        e.scrollTop(e.lastElementChild.scrollHeight);
    }

    /*判断当有新信息来时，用户是否在页面底端*/
    function isNewInWindow() {
        let p = $('#msg-show');
        let e = $('#msg-show').last();
        let secondChildTop = e.height();
        let parentBottom = $('#msg-show').height();
        return secondChildTop > parentBottom;
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


    $('#toChat').click(function () {
        if (currentChat == null || currentChat == undefined) {
            return
        }
        $('#f' + currentChat).click();
    })
});

