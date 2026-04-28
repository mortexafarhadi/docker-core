$(document).ready(function () {
    set_page = (page) => {
        const url_params = searchParams();
        url_params.set("page", page);
        window.location.href = window.location.pathname + "?" + url_params.toString();
    };
});