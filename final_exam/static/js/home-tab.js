$(function () {
    $('.my-nav-item a').on('show.bs.tab', function (e) {
        let related_tab = $(this).data("relatedtab");
        $(related_tab.toString()).tab('show')
    });


});

let url = '/get-history-msg';

function listItemClick(e) {
    let id = e.getAttribute('data-userid');
    if (currentChat == undefined || id != currentChat) {
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
    }
}
