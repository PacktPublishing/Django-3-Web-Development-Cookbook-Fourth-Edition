import json

from django.contrib.contenttypes.models import ContentType
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt

from .models import Like
from .templatetags.likes_tags import liked_count


@never_cache
@csrf_exempt
def json_set_like(request, content_type_id, object_id):
    """
    Sets the object as a favorite for the current user
    """
    result = {
        "success": False,
    }
    if request.user.is_authenticated and request.method == "POST":
        content_type = ContentType.objects.get(id=content_type_id)
        obj = content_type.get_object_for_this_type(pk=object_id)

        like, is_created = Like.objects.get_or_create(
            content_type=ContentType.objects.get_for_model(obj),
            object_id=obj.pk,
            user=request.user)
        if not is_created:
            like.delete()

        result = {
            "success": True,
            "action": "add" if is_created else "remove",
            "count": liked_count(obj),
        }

    return JsonResponse(result)
