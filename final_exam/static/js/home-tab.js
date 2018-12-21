$(function () {
    $('.my-nav-item a').on('show.bs.tab', function (e) {
        let related_tab = $(this).data("relatedtab");
        $(related_tab.toString()).tab('show')
    });

});

let url = '/get-history-msg';

function listItemClick(e) {
    let id = e.getAttribute('data-userid');
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
             var ele = document.getElementById('msg-show');
             ele.scrollTop = ele.scrollHeight;
        },
        error: function (error) {

        }
    })
}

function groupChat(e) {
    document.getElementById('nav-info-tab').click();
    let id = e.getAttribute('data-id');
    document.getElementById("chatTitle").innerText = e.getAttribute('data-name');
    currentChat = id;
    // clear message area
    $('#msg-show').empty();
}

$('#gChatLi').click();