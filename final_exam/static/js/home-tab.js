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
    if (msg['from'] == uid) {

    }
}