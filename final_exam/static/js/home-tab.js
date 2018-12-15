$(function () {
    $('.my-nav-item a').on('show.bs.tab', function (e) {
        let related_tab = $(this).data("relatedtab");
        $(related_tab.toString()).tab('show')
    })
});