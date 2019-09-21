/* register widget initialization for a formset form */
window.WIDGET_INIT_REGISTER = window.WIDGET_INIT_REGISTER || [];

$(function () {
    function reinit_widgets($formset_form) {
        $(window.WIDGET_INIT_REGISTER).each(function (index, func) {
            func($formset_form);
        });
    }

    function set_index_for_fields($formset_form, index) {
        $formset_form.find(':input').each(function () {
            var $field = $(this);
            if ($field.attr("id")) {
                $field.attr(
                    "id",
                    $field.attr("id").replace(/-__prefix__-/, "-" + index + "-")
                );
            }
            if ($field.attr("name")) {
                $field.attr(
                    "name",
                    $field.attr("name").replace(/-__prefix__-/, "-" + index + "-")
                );
            }
        });
        $formset_form.find('label').each(function () {
            var $field = $(this);
            if ($field.attr("for")) {
                $field.attr(
                    "for",
                    $field.attr("for").replace(/-__prefix__-/, "-" + index + "-")
                );
            }
        });
        $formset_form.find('div').each(function () {
            var $field = $(this);
            if ($field.attr("id")) {
                $field.attr(
                    "id",
                    $field.attr("id").replace(/-__prefix__-/, "-" + index + "-")
                );
            }
        });
    }

    function add_delete_button($formset_form) {
        $formset_form.find('input:checkbox[id$=DELETE]').each(function () {
            var $checkbox = $(this);
            var $deleteLink = $(
                '<button class="delete btn btn-sm btn-danger mb-3">Remove</button>'
            );
            $formset_form.append($deleteLink);
            $checkbox.closest('.form-group').hide();
        });

    }

    $('.add-inline-form').click(function (e) {
        e.preventDefault();
        var $formset = $(this).closest('.formset');
        var $total_forms = $formset.find('[id$="TOTAL_FORMS"]');
        var $new_form = $formset.find('.empty-form').clone(true).attr("id", null);
        $new_form.removeClass('empty-form d-none').addClass('formset-form');
        set_index_for_fields($new_form, parseInt($total_forms.val(), 10));
        $formset.find('.formset-forms').append($new_form);
        add_delete_button($new_form);
        $total_forms.val(parseInt($total_forms.val(), 10) + 1);
        reinit_widgets($new_form);
    });
    $('.formset-form').each(function () {
        $formset_form = $(this);
        add_delete_button($formset_form);
        reinit_widgets($formset_form);
    });
    $(document).on('click', '.delete', function (e) {
        e.preventDefault();
        var $formset = $(this).closest('.formset-form');
        var $checkbox = $formset.find('input:checkbox[id$=DELETE]');
        $checkbox.attr("checked", "checked");
        $formset.hide();
    });
});
