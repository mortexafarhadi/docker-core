toggle_show_password = () => {
    let x = $('#id_password');
    x.attr('type', x.attr('type') === "password" ? 'text' : 'password');
}
toggle_show_confirm_password = () => {
    let x = $('#id_confirm_password');
    x.attr('type', x.attr('type') === "password" ? 'text' : 'password');
}