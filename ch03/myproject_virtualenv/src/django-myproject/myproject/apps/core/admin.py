from django import forms
from django.conf import settings
from django.utils.translation import gettext_lazy as _


def get_multilingual_field_names(field_name):
    lang_code_underscored = settings.LANGUAGE_CODE.replace("-", "_")
    field_names = [f"{field_name}_{lang_code_underscored}"]
    for lang_code, lang_name in settings.LANGUAGES:
        if lang_code != settings.LANGUAGE_CODE:
            lang_code_underscored = lang_code.replace("-", "_")
            field_names.append(f"{field_name}_{lang_code_underscored}")
    return field_names


class LanguageChoicesForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        LANGUAGES_EXCEPT_THE_DEFAULT = [
            (lang_code, lang_name)
            for lang_code, lang_name in settings.LANGUAGES
            if lang_code != settings.LANGUAGE_CODE
        ]
        super().__init__(*args, **kwargs)
        self.fields["language"] = forms.ChoiceField(
            label=_("Language"),
            choices=LANGUAGES_EXCEPT_THE_DEFAULT,
            required=True,
        )