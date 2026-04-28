$(document).ready(function () {
    setDeletePk = (pk) => $('#modal_delete_pk').val(pk);
    clear_datetimes = () => {
        const details = getUrlDetails();
        const fields = [
            {id: '#daterangepickerranges_create', param: 'date_range_create'},
            {id: '#daterangepickerranges_update', param: 'date_range_update'},
            {id: '#daterangepickerranges_delete', param: 'date_range_delete'}
        ];

        fields.forEach(field => {
            const value = details.params[field.param] || "";
            $(field.id).val(decodeURIComponent(value).replace(/\+/g, ' '));
        });
    };
});