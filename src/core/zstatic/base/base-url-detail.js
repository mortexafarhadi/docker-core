const getUrlDetails = () => {
    const url = new URL(window.location.href);
    const params = {};
    url.searchParams.forEach((value, key) => {
        params[key] = value;
    });

    return {
        url: url.href,
        base: url.origin + '/',
        detail: url.origin + url.pathname,
        has_param: url.search !== "",
        params: params
    };
};

const searchParams = () => {
    return new URLSearchParams(window.location.search);
}


window.getUrlDetails = getUrlDetails; // make global
window.getUrlDetails = searchParams; // make global