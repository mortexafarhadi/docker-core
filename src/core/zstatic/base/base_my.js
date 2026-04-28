const isNumberKey = (evt, e, max_length = null, char = ',', dont_start_zero = true) => {
    var charCode = (evt.which) ? evt.which : event.keyCode;
    if (charCode > 31 && (charCode < 48 || charCode > 57)) {
        return false;
    }
    if (e && dont_start_zero) if (e.value.length < 1 && (charCode === 48)) return false;

    if (max_length) {
        let content = e.value.replaceAll(char, '')
        content = content.replaceAll(" ", '')
        if (content.length > max_length - 1)
            return false;
    }
    return true;
}

const setCommaThreeDigit = (e) => {
    let content = e.value.replaceAll(',', '')
    if (content.length > 3) {
        let result = ''
        let z = content;
        let i = content.length;
        let x = 0;
        while (i > 0) {
            let y = z.substring(i - 1, i)
            result = y + result
            if (x === 2) result = ',' + result
            if (x > 2) x = 0
            x += 1;
            i -= 1;
        }
        if (result.startsWith(','))
            result = result.substring(1, result.length);
        content = result;
    }
    e.value = content;
}

const setDashForeDigitCard = (e) => {
    let content = e.value.replaceAll('-', '')
    content = content.replaceAll(' ', '')
    if (content.length > 3) {
        let result = ''
        let z = content;
        let i = 0;
        let x = 0;
        while (i < content.length) {
            let y = z.substring(i, i + 1)
            result += y
            if (x === 3) result += ' - '
            if (x > 3) x = 0
            x += 1;
            i += 1;
        }
        if (result.endsWith(' - '))
            result = result.substring(0, result.length - 3);
        e.value = result;
    }
}

const click_element_with_id = (_id) => document.getElementById(_id).click();

const submit_form_with_id = (_id) => document.getElementById(_id).submit();

const set_value_for_element_with_id = (id_, value_) => document.getElementById(id_).value = value_;

const set_value_for_element_then_submit_form_with_id = (_id, _value, _form_id) => {
    document.getElementById(_id).value = _value;
    submit_form_with_id(_form_id);
}
