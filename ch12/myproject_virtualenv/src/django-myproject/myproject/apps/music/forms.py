from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Song


class SongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = "__all__"


class SongFilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        artist_choices = [
            (artist, artist)
            for artist in sorted(
                Song.objects.values_list("artist", flat=True).distinct(),
                key=str.casefold
            )
        ]
        self.fields['artist'] = forms.ChoiceField(
            label=_("Artist"),
            choices=artist_choices,
            required=False,
        )