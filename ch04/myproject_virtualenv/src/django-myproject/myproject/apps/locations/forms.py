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
    latitude = forms.FloatField(
        label=_("Latitude"),
        help_text=_("Latitude (Lat.) is the angle between any point and the equator (north pole is at 90; south pole is at -90)."),
        required=False,
    )
    longitude = forms.FloatField(
        label=_("Longitude"),
        help_text=_("Longitude (Long.) is the angle east or west of an arbitrary point on Earth from Greenwich (UK), which is the international zero-longitude point (longitude=0 degrees). The anti-meridian of Greenwich is both 180 (direction to east) and -180 (direction to west)."),
        required=False,
    )
    class Meta:
        model = Location
        exclude = ["geoposition", "rating"]

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)
        geoposition = self.instance.get_geoposition()
        if geoposition:
            self.fields["latitude"].initial = geoposition.latitude
            self.fields["longitude"].initial = geoposition.longitude

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

        street_address_field = layout.Field(
            "street_address", css_class="input-block-level"
        )
        street_address2_field = layout.Field(
            "street_address2", css_class="input-block-level"
        )
        postal_code_field = layout.Field("postal_code", css_class="input-block-level")
        city_field = layout.Field("city", css_class="input-block-level")
        country_field = layout.Field("country", css_class="input-block-level")
        latitude_field = layout.Field("latitude", css_class="input-block-level")
        longitude_field = layout.Field("longitude", css_class="input-block-level")
        address_fieldset = layout.Fieldset(
            _("Address"),
            street_address_field,
            street_address2_field,
            postal_code_field,
            city_field,
            country_field,
            latitude_field,
            longitude_field,
        )

        submit_button = layout.Submit("save", _("Save"))
        actions = bootstrap.FormActions(layout.Div(submit_button, css_class="col"))

        self.helper = helper.FormHelper()
        self.helper.form_action = self.request.path
        self.helper.form_method = "POST"
        self.helper.attrs = {"noValidate": "noValidate"}
        self.helper.layout = layout.Layout(main_fieldset, picture_fieldset, address_fieldset, actions)

    def clean(self):
        cleaned_data = super().clean()
        picture_path = cleaned_data["picture_path"]
        if not self.instance.pk and not self.files.get("picture") and not picture_path:
            raise forms.ValidationError(_("Please choose an image."))

    def save(self, commit=True):
        instance = super().save(commit=False)
        picture_path = self.cleaned_data["picture_path"]
        if picture_path:
            temporary_image_path = os.path.join("temporary-uploads", picture_path)
            file_obj = default_storage.open(temporary_image_path)
            instance.picture.save(picture_path, file_obj, save=False)
            default_storage.delete(temporary_image_path)
        latitude = self.cleaned_data["latitude"]
        longitude = self.cleaned_data["longitude"]
        if latitude is not None and longitude is not None:
            instance.set_geoposition(longitude=longitude, latitude=latitude)
        if commit:
            instance.save()
            self.save_m2m()
        return instance
