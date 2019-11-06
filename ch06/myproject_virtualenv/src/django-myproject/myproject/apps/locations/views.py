from pprint import pprint

from django.conf import settings
from django.views.generic import ListView, DetailView

from django.utils.decorators import classonlymethod

from .models import Location


class LocationList(ListView):
    model = Location


class LocationDetail(DetailView):
    model = Location
    template_name = "locations/location_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["MAPS_API_KEY"] = settings.MAPS_API_KEY
        return context
