var app_item_click = new Vue({
    el: '.my-tab-item',
    data: {

    },
    methods: {
        tabItemSelect(item){
            var id = item.getAttribute("data-userid");
            alert(id);
        }
    }
});