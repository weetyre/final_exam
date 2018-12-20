$(function () {
    $('.my-nav-item a').on('show.bs.tab', function (e) {
        let related_tab = $(this).data("relatedtab");
        $(related_tab.toString()).tab('show')
    });


});

let url = '/get-history-msg';

function listItemClick(e) {
    let id = e.getAttribute('data-userid');
    //if (currentChat == undefined || id != currentChat) {
        let name = e.getAttribute('data-name');
        document.getElementById("chatTitle").innerText = name;
        currentChat = id;
        // clear message area
        $('#msg-show').empty();

        $.ajax({
            url: url + "?uid=" + id,
            type: "GET",
            dataType: 'json',
            success: function (datas) {
                for (let i = 0; i < datas.length; i++) {
                    appendMsg(datas[i]);
                }
            },
            error: function (error) {

            }
        })
    //}
}

function listItemClick2(e) {
    let id = e.getAttribute('data-userid');
    let name = e.getAttribute('data-name');
    currentChat = id;
    let html = '<div id="userInfoBox" class="row profile_1"><img data-src="" alt="32x32" class="rounded img-face-msg img_size" src="/static/img/face.jpg"></div><div class="row profile_2"><h1 id="userInfo">' + name + '</h1></div><div class="row profile_3"><button id="toChat" onclick="onToChat()" class="btn btn-success btn-lg">发消息</button></div>'
    document.getElementById('nav-info-tab').click();
    document.getElementById("friendsInfoBox").innerHTML = html;
}

function onToChat() {
    if (currentChat == null || currentChat == undefined) {
        return
    }
    let id = 'f' + currentChat;
    document.getElementById('nav-chat-tab').click();
    listItemClick(document.getElementById(id));
}