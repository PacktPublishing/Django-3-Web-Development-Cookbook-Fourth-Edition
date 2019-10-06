from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.conf import settings

from .forms import LocationForm
from .models import Location, RATING_CHOICES


class LocationList(ListView):
    model = Location
    paginate_by = 10

class LocationDetail(DetailView):
    model = Location
    context_object_name = "location"


@login_required
def add_or_change_location(request, pk=None):
    location = None
    if pk:
        location = get_object_or_404(Location, pk=pk)
    if request.method == "POST":
        form = LocationForm(request, data=request.POST, files=request.FILES, instance=location)
        if form.is_valid():
            location = form.save()
            return redirect("locations:location_detail", pk=location.pk)
    else:
        form = LocationForm(request, instance=location)

    context = {"location": location, "form": form}
    return render(request, "locations/location_form.html", context)


@login_required
def delete_location(request, pk):
    location = get_object_or_404(Location, pk=pk)
    if request.method == "POST":
        location.delete()
        return redirect("locations:location_list")
    context = {"location": location}
    return render(request, "locations/location_deleting_confirmation.html", context)


PAGE_SIZE = getattr(settings, "PAGE_SIZE", 24)
