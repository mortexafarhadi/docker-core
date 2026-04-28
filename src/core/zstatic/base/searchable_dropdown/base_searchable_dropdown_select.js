let selectedOptions = {};

const capitalizeFirstLetter = str => str.charAt(0).toUpperCase() + str.slice(1);

function toggleDropdown(item) {
    if (document.getElementById(`id_${item}`).getAttribute('disabled') == null) {
        document.getElementsByClassName(`searchable-dropdown-menu ${item}`)[0].classList.toggle("show");
    }
}

function setSelectedOptions() {
    const selected_options_containers = document.getElementsByClassName("searchable-selected-options");
    for (let container of selected_options_containers) {
        let class_list = [...container.classList];
        class_list = class_list.filter(cls => cls !== 'searchable-selected-options' && cls !== 'overflow-hidden');
        let class_name = class_list[0]
        let my_list = container.getElementsByTagName("span");
        let value_list = []
        for (let item of my_list) {
            value_list.push(item.innerText)
        }
        selectedOptions[class_name] = value_list;
        updateSelectedDisplay(class_name);
    }
}

function selectOption(option, title, class_name) {
    document.getElementsByClassName(`searchable-selected ${class_name}`)[0].innerText = title;
    document.getElementsByClassName(`searchable-option-selected ${class_name}`)[0].value = option;
    document.getElementsByClassName(`searchable-dropdown-menu ${class_name}`)[0].classList.remove("show");
    let my_list = document.getElementsByClassName(`searchable-options-list ${class_name}`)[0].getElementsByTagName("li");

    for (let item of my_list) {
        if (item.innerText === title) {
            item.classList.add("bg-primary-subtle");
        } else {
            item.classList.remove("bg-primary-subtle");
        }
    }
}

function filterOptions(class_name) {
    let input = document.getElementsByClassName(`searchable-search ${class_name}`)[0].value.toLowerCase();
    let items = document.getElementsByClassName(`searchable-options-list ${class_name}`)[0].getElementsByTagName("li");
    for (let item of items) {
        if (item.innerText.toLowerCase().includes(input)) {
            item.style.display = "block";
        } else {
            item.style.display = "none";
        }
    }
}

function selectManyOption(option, title, class_name) {
    let my_list = selectedOptions[class_name];
    let added_item = false;
    if (my_list === undefined) {
        my_list = [title]
        selectedOptions[class_name] = my_list
        added_item = true
    } else {
        if (!my_list.includes(title)) {
            selectedOptions[class_name].push(title);
            added_item = true
        }
    }
    if (added_item) {
        updateSelectedDisplay(class_name);
        const container = document.getElementById(`id_${class_name}`);
        const mode = container.getAttribute("key");
        let option_list = (mode === "choice") ? container.querySelectorAll("input[type='checkbox']") : container.options;
        for (let i = 0; i < option_list.length; i++) {
            if (option_list[i].value === option) {
                (mode === "choice") ? option_list[i].checked = true : option_list[i].selected = true;
                break;
            }
        }
    }
}

function updateSelectedDisplay(class_name) {
    const selectedContainer = document.getElementsByClassName(`searchable-selected-options ${class_name}`)[0];
    selectedContainer.innerHTML = "";
    let my_list = selectedOptions[class_name];
    if (my_list.length === 0) {
        selectedContainer.innerHTML = "Select " + capitalizeFirstLetter(class_name);
    } else {
        my_list.forEach(option => {
            let span = document.createElement("span");
            span.innerText = option;
            span.onclick = () => removeOption(option, class_name);
            selectedContainer.appendChild(span);
        });
    }
    const optionListContainer = document.getElementsByClassName(`searchable-options-list ${class_name}`)[0];
    const option_list = optionListContainer.getElementsByTagName("li");
    for (let item of option_list) {
        if (my_list.includes(item.innerText)) {
            item.classList.add("bg-primary-subtle");
        } else {
            item.classList.remove("bg-primary-subtle");
        }
    }
}

function removeOption(option, class_name) {
    selectedOptions[class_name] = selectedOptions[class_name].filter(item => item !== option);
    updateSelectedDisplay(class_name);
    const container = document.getElementById(`id_${class_name}`);
    const mode = container.getAttribute("key");
    let option_list = (mode === "choice") ? container.querySelectorAll("input[type='checkbox']") : container.options;
    for (let i = 0; i < option_list.length; i++) {
        if (mode === "choice") {
            if (option_list[i].parentElement.innerText.trim() === option) {
                option_list[i].checked = false;
                break;
            }
        } else {
            if (option_list[i].value === option) {
                option_list[i].selected = false;
                break;
            }
        }
    }
}

document.addEventListener("click", function (event) {
    Object.keys(selectedOptions).length === 0 ? setSelectedOptions() : null;

    let dropdowns = document.querySelectorAll(".searchable-dropdown");
    dropdowns.forEach(dropdown => {
        if (!dropdown.contains(event.target)) {
            dropdown.querySelector(".searchable-dropdown-menu").classList.remove("show");
        }
    })
});