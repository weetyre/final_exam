$(function () {
    $('.my-nav-item a').on('show.bs.tab', function (e) {
        let related_tab = $(this).data("relatedtab");
        $(related_tab.toString()).tab('show')
    });


});

function listItemClick(e) {
    let id = e.getAttribute('data-userid');
    if (id != currentChat) {
        let name = e.getAttribute('data-name');
        document.getElementById("chatTitle").innerText = name;
        currentChat = id;
        // clear message area
        $('#msg-show').empty()
    }
}
