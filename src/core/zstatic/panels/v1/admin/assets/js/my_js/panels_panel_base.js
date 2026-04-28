function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(";").shift();
}

function getCsrfToken() {
    return getCookie("csrftoken");
}

click_link = (e) => e.children[0].click();
set_language = (language, direction) => {
    let l = $("#setting_language")
    l.val(language)
    let d = $("#setting_direction")
    d.val(direction)
    l.parent().submit()
}
set_hide_sidebar = () => {
    const hide_sidebar = localStorage.getItem('hide_sidebar')
    localStorage.setItem('hide_sidebar', (hide_sidebar === 'true') ? 'false' : 'true')
}

async function toggle_dark_mode() {
    await fetch("/set-user-setting/toggle-dark-mode/", {
        method: "POST", headers: {
            "Content-Type": "application/json", "X-CSRFToken": getCsrfToken(),
        }
    });
}

async function change_background_mode() {
    await fetch("/set-user-setting/change-background-mode/", {
        method: "POST", headers: {
            "Content-Type": "application/json", "X-CSRFToken": getCsrfToken(),
        }
    });
}

async function change_color_mode() {
    await fetch("/set-user-setting/change-color-mode/", {
        method: "POST", headers: {
            "Content-Type": "application/json", "X-CSRFToken": getCsrfToken(),
        }
    });
}
async function change_sidebar_mode() {
    await fetch("/set-user-setting/change-sidebar-mode/", {
        method: "POST", headers: {
            "Content-Type": "application/json", "X-CSRFToken": getCsrfToken(),
        }
    });
}

setTimeout(function () {
    const e = document.querySelector("html");
    e.setAttribute("dir", e.getAttribute("my-dir"));
    const hide_sidebar = localStorage.getItem('hide_sidebar')
    if (hide_sidebar == null) {
        localStorage.setItem('hide_sidebar', 'false')
    } else if (hide_sidebar === 'true') {
        $("#checker_hide_sidebar").click()
    }
}, 100);
