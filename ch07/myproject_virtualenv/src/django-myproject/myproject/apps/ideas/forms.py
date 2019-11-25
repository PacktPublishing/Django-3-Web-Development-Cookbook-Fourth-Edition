from django import forms
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.contrib.auth import get_user_model

from crispy_forms import bootstrap, helper, layout

from .models import Idea, IdeaTranslations

User = get_user_model()


class IdeaForm(forms.ModelForm):
    class Meta:
        model = Idea
        exclude = ["author"]

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)

        title_field = layout.Field("title", css_class="input-block-level")
        content_field = layout.Field("content", css_class="input-block-level", rows="3")
        main_fieldset = layout.Fieldset(_("Main data"), title_field, content_field)

        picture_field = layout.Field("picture", css_class="input-block-level")
        format_html = layout.HTML(
            """{% include "ideas/includes/picture_guidelines.html" %}"""
        )

        picture_fieldset = layout.Fieldset(
            _("Picture"),
            picture_field,
            format_html,
            title=_("Image upload"),
            css_id="picture_fieldset",
        )

        inline_translations = layout.HTML(
            """{% include "ideas/forms/translations.html" %}"""
        )

        submit_button = layout.Submit("save", _("Save"))
        actions = bootstrap.FormActions(submit_button)

        self.helper = helper.FormHelper()
        self.helper.form_action = self.request.path
        self.helper.form_method = "POST"
        self.helper.layout = layout.Layout(
            main_fieldset,
            inline_translations,
            picture_fieldset,
            actions,
        )

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.author = self.request.user
        if commit:
            instance.save()
            self.save_m2m()
        return instance


class IdeaTranslationsForm(forms.ModelForm):
    language = forms.ChoiceField(
        label=_("Language"),
        choices=settings.LANGUAGES_EXCEPT_THE_DEFAULT,
        required=True,
    )

    class Meta:
        model = IdeaTranslations
        exclude = ["idea"]

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)

        id_field = layout.Field("id")
        language_field = layout.Field("language", css_class="input-block-level")
        title_field = layout.Field("title", css_class="input-block-level")
        content_field = layout.Field("content", css_class="input-block-level", rows="3")
        delete_field = layout.Field("DELETE")
        main_fieldset = layout.Fieldset(
            _("Main data"),
            id_field,
            language_field,
            title_field,
            content_field,
            delete_field,
        )

        self.helper = helper.FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.layout = layout.Layout(main_fieldset)
