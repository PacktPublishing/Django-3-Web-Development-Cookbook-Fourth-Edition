import os
from django import forms
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.core.files.storage import default_storage

from crispy_forms import bootstrap, helper, layout

from .models import Location


class LocationForm(forms.ModelForm):
    picture = forms.ImageField(
        label=_("Picture"), max_length=255, widget=forms.FileInput(), required=False
    )
    picture_path = forms.CharField(
        max_length=255, widget=forms.HiddenInput(), required=False
    )

    class Meta:
        model = Location
        fields = "__all__"

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)

        name_field = layout.Field("name", css_class="input-block-level")
        description_field = layout.Field(
            "description", css_class="input-block-level", rows="3"
        )
        main_fieldset = layout.Fieldset(_("Main data"), name_field, description_field)

        picture_preview_html = layout.HTML(
            """{% include "core/includes/picture_preview.html" %}"""
        )
        picture_field = layout.Field(
            "picture",
            data_url=reverse("upload_file"),
            template="core/includes/file_upload_field.html",
        )
        picture_path_field = layout.Field("picture_path")

        picture_fieldset = layout.Fieldset(
            _("Picture"),
            picture_preview_html,
            picture_field,
            picture_path_field,
            title=_("Picture upload"),
            css_id="picture_fieldset",
        )

        submit_button = layout.Submit("save", _("Save"))
        actions = bootstrap.FormActions(layout.Div(submit_button, css_class="col"))

        self.helper = helper.FormHelper()
        self.helper.form_action = self.request.path
        self.helper.form_method = "POST"
        self.helper.attrs = {"noValidate": "noValidate"}
        self.helper.layout = layout.Layout(main_fieldset, picture_fieldset, actions)

    def clean(self):
        cleaned_data = super().clean()
        picture_path = cleaned_data["picture_path"]
        if not self.instance.pk and not self.files.get("picture") and not picture_path:
            raise forms.ValidationError(_("Please choose an image."))

    def save(self, commit=True):
        instance = super().save(commit=False)
        picture_path = self.cleaned_data["picture_path"]
        if picture_path:
            temporary_image_path = os.path.join(
                "temporary-uploads", picture_path
            )
            file_obj = default_storage.open(temporary_image_path)
            instance.picture.save(
                picture_path, file_obj, save=False
            )
            default_storage.delete(temporary_image_path)
        if commit:
            instance.save()
            self.save_m2m()
        return instance
