from django import forms
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model

from crispy_forms import bootstrap, helper, layout
from mptt.forms import TreeNodeChoiceField

from myproject.apps.categories1.models import Category

from .models import Idea, RATING_CHOICES
from ..core.form_fields import MultipleChoiceTreeField

User = get_user_model()


class IdeaForm(forms.ModelForm):
    categories = MultipleChoiceTreeField(
        label=_("Categories"),
        required=False,
        queryset=Category.objects.all(),
    )

    class Meta:
        model = Idea
        exclude = ["author"]

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)

        title_field = layout.Field("title")
        content_field = layout.Field("content", rows="3")
        main_fieldset = layout.Fieldset(_("Main data"), title_field, content_field)

        picture_field = layout.Field("picture")
        format_html = layout.HTML(
            """{% include "ideas1/includes/picture_guidelines.html" %}"""
        )

        picture_fieldset = layout.Fieldset(
            _("Picture"),
            picture_field,
            format_html,
            title=_("Image upload"),
            css_id="picture_fieldset",
        )

        categories_field = layout.Field(
            "categories",
            template="core/includes/checkboxselectmultiple_tree.html"
        )
        categories_fieldset = layout.Fieldset(
            _("Categories"), categories_field, css_id="categories_fieldset"
        )

        submit_button = layout.Submit("save", _("Save"))
        actions = bootstrap.FormActions(submit_button, css_class="my-4")

        self.helper = helper.FormHelper()
        self.helper.form_action = self.request.path
        self.helper.form_method = "POST"
        self.helper.layout = layout.Layout(
            main_fieldset,
            picture_fieldset,
            categories_fieldset,
            actions,
        )

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.author = self.request.user
        if commit:
            instance.save()
            self.save_m2m()
        return instance


class IdeaFilterForm(forms.Form):
    author = forms.ModelChoiceField(
        label=_("Author"),
        required=False,
        queryset=User.objects.all(),
    )
    category = TreeNodeChoiceField(
        label=_("Category"),
        required=False,
        queryset=Category.objects.all(),
        level_indicator=mark_safe("&nbsp;&nbsp;&nbsp;&nbsp;")
    )
    rating = forms.ChoiceField(
        label=_("Rating"), required=False, choices=RATING_CHOICES
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        author_field = layout.Field("author")
        category_field = layout.Field("category")
        rating_field = layout.Field("rating")
        submit_button = layout.Submit("filter", _("Filter"))
        actions = bootstrap.FormActions(submit_button)

        main_fieldset = layout.Fieldset(
            _("Filter"),
            author_field,
            category_field,
            rating_field,
            actions,
        )

        self.helper = helper.FormHelper()
        self.helper.form_method = "GET"
        self.helper.layout = layout.Layout(main_fieldset)
