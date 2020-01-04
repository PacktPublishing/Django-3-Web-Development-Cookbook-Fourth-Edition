from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import ReadOnlyAuthorization
from tastypie.resources import (ModelResource, ALL)

from .models import Song


class SongResource(ModelResource):
    class Meta:
        queryset = Song.objects.all()
        resource_name = "songs"
        fields = [
            "artist", "title", "url", "image"
        ]
        allowed_methods = ["get"]
        authentication = ApiKeyAuthentication()
        authorization = ReadOnlyAuthorization()
        filtering = {
            "artist": ALL,
            "created": ["gt", "gte", "exact", "lte", "lt"],
        }
