$(function () {
    $('.my-nav-item a').on('show.bs.tab', function (e) {
        let related_tab = $(this).data("relatedtab");
        $(related_tab.toString()).tab('show')
    });


});

function listItemClick(e) {
    let name = e.getAttribute('data-name');
    var e1 = document.getElementById("chatTitle");
    e1.innerText = name;

}

let uid = '1';

function append_msg(msg) {
    let from = msg["from"];
    //let msg_show = document.getElementById("msg-show");
    var html_div_content;

    if (msg['from'] == uid) {
        html_div_content = '<div class="media text-muted py-2 msg-item msg-mine" data-userid="' + from + '"><div class="d-flex msg-container"><img data-src="" alt="32x32" class="rounded img-face-msg" src="" data-holder-rendered="true"><p class="media-body mb-0 small lh-125 p-2 msg-content">' + msg["content"] + '</p></div></div>'
    }else{
        html_div_content = '<div class="media text-muted py-2 msg-item msg-other" data-userid="' + from + '"><div class="d-flex msg-container"><img data-src="" alt="32x32" class="rounded img-face-msg" src="" data-holder-rendered="true"><p class="media-body mb-0 small lh-125 p-2 msg-content">' + msg["content"] + '</p></div></div>'
    }
    $('#msg-show').append(html_div_content)
}