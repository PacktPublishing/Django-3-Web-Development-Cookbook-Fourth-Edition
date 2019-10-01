from django import template
from django.contrib.contenttypes.models import ContentType
from django.template.loader import render_to_string

from likes.models import Like

register = template.Library()


class ObjectLikeWidget(template.Node):
    def __init__(self, var):
        self.var = var

    def render(self, context):
        liked_object = self.var.resolve(context)
        ct = ContentType.objects.get_for_model(liked_object)
        user = context["request"].user

        if not user.is_authenticated:
            return ""

        context.push(object=liked_object,
                     content_type_id=ct.pk)
        #              is_liked_by_user=liked_by(liked_object,
        #                                        user),
        #              count=liked_count(liked_object))
        output = render_to_string("likes/includes/widget.html",
                                  context.flatten())
        context.pop()
        return output


# TAGS

@register.tag
def like_widget(parser, token):
    try:
        tag_name, for_str, var_name = token.split_contents()
    except ValueError:
        tag_name = "%r" % token.contents.split()[0]
        raise template.TemplateSyntaxError(
            f"{tag_name} tag requires a following syntax: "
            f"{{% {tag_name} for <object> %}}")
    var = template.Variable(var_name)
    return ObjectLikeWidget(var)


# FILTERS

@register.filter
def liked_by(obj, user):
    ct = ContentType.objects.get_for_model(obj)
    liked = Like.objects.filter(user=user,
                                content_type=ct,
                                object_id=obj.pk)
    return liked.count() > 0


@register.filter
def liked_count(obj):
    ct = ContentType.objects.get_for_model(obj)
    likes = Like.objects.filter(content_type=ct,
                                object_id=obj.pk)
    return likes.count()
