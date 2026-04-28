(() => {
    var c = document.querySelector("#flatpickr-range-create");
    var u = document.querySelector("#flatpickr-range-update");
    var d = document.querySelector("#flatpickr-range-delete");
    null != typeof c && c.flatpickr({mode: "range", static: !0}),
    u && u.flatpickr({mode: "range", static: !0}),
    d && d.flatpickr({mode: "range", static: !0})
})();
const set_page_size = (e) => {
    let input_page_size = $("#id__page_size");
    input_page_size.val(e.selectedOptions[0].value);
    input_page_size.parent().submit();
}
const change_text_in_search = (e) => {
    let input_search_content = $("#id__q");
    input_search_content.val(e.value);
    input_search_content.parent().submit();
};

setDeletePk = (pk) => $('#modal_delete_pk').val(pk);