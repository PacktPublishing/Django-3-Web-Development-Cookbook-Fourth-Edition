from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils.html import mark_safe
from crispy_forms.helper import FormHelper
from crispy_forms import layout, bootstrap
from mptt.forms import TreeNodeChoiceField

from utils.fields import MultipleChoiceTreeField
from .models import Category, Genre, Director, Actor, Movie, RATING_CHOICES


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ["categories", "title", "release_year"]

    categories = MultipleChoiceTreeField(
        label=_("Categories"),
        required=False,
        queryset=Category.objects.all())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"
        self.helper.layout = layout.Layout(
            layout.Field("title"),
            layout.Field(
                "categories",
                template="utils/checkbox_multi_select_tree.html"),
            bootstrap.FormActions(
                layout.Submit("submit", _("Save")),
            )
        )


class MovieFilterForm(forms.Form):
    genre = forms.ModelChoiceField(
        label=_("Genre"),
        required=False,
        queryset=Genre.objects.all())
    director = forms.ModelChoiceField(
        label=_("Director"),
        required=False,
        queryset=Director.objects.all())
    actor = forms.ModelChoiceField(
        label=_("Actor"),
        required=False,
        queryset=Actor.objects.all())
    rating = forms.ChoiceField(
        label=_("Rating"),
        required=False,
        choices=RATING_CHOICES)
    category = TreeNodeChoiceField(
        label=_("Category"),
        queryset=Category.objects.all(),
        required=False,
        level_indicator=mark_safe("&nbsp;&nbsp;&nbsp;&nbsp;"))


