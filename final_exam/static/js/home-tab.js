$(function () {
    $('.my-nav-item a').on('show.bs.tab', function (e) {
        let related_tab = $(this).data("relatedtab");
        $(related_tab.toString()).tab('show')
    });


});

function listItemClick(e) {
    let name = e.getAttribute('data-name');
    let e1 = $('#chatName');
    let t = e1.innerText;
};