from django import forms
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.db import models

from crispy_forms import bootstrap, helper, layout


from django.contrib.auth import get_user_model

User = get_user_model()

from myproject.apps.categories.models import Category

from .models import Idea, IdeaTranslations, RATING_CHOICES


class IdeaForm(forms.ModelForm):
    class Meta:
        model = Idea
        exclude = ["author"]

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)

        self.fields["categories"].widget = forms.CheckboxSelectMultiple()

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

        categories_field = layout.Field("categories", css_class="input-block-level")
        categories_fieldset = layout.Fieldset(
            _("Categories"), categories_field, css_id="categories_fieldset"
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
            categories_fieldset,
            actions,
        )

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.author = self.request.user
        instance.save()
        if commit:
            self.save_m2m()
        return instance


class IdeaTranslationsForm(forms.ModelForm):
    language = forms.ChoiceField(
        label=_("Language"),
        choices=settings.LANGUAGES_EXCEPT_THE_DEFAULT,
        required=True,
    )

    class Meta:
        model = Idea
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


class IdeaFilterForm(forms.Form):
    author = forms.ModelChoiceField(
        label=_("Author"),
        required=False,
        queryset=User.objects.annotate(
            idea_count=models.Count("authored_ideas")
        ).filter(idea_count__gt=0),
    )
    category = forms.ModelChoiceField(
        label=_("Category"),
        required=False,
        queryset=Category.objects.annotate(
            idea_count=models.Count("category_ideas")
        ).filter(idea_count__gt=0),
    )
    rating = forms.ChoiceField(
        label=_("Rating"), required=False, choices=RATING_CHOICES
    )
