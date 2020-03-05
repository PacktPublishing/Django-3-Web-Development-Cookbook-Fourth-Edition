import re
from datetime import datetime
from urllib.parse import urlencode

from django import template
from django.apps import apps
from django.template.loader import get_template
from django.utils import timezone
from django.utils.encoding import force_str
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

register = template.Library()


""" TAGS """


class IncludeNode(template.Node):
    def __init__(self, template_name):
        self.template_name = template.Variable(template_name)

    def render(self, context):
        try:
            # Loading the template and rendering it
            included_template = self.template_name.resolve(context)
            if isinstance(included_template, str):
                included_template = get_template(included_template)
            rendered_template = included_template.render(context.flatten())
        except (template.TemplateDoesNotExist,
                template.VariableDoesNotExist,
                AttributeError):
            rendered_template = ""
        return rendered_template


@register.tag
def try_to_include(parser, token):
    """
    Usage: {% try_to_include "some_template.html" %}

    This will fail silently if the template doesn't exist.
    If it does exist, it will be rendered with the current context.
    """
    try:
        tag_name, template_name = token.split_contents()
    except ValueError:
        tag_name = token.contents.split()[0]
        raise template.TemplateSyntaxError(
            f"{tag_name} tag requires a single argument")
    return IncludeNode(template_name)


class ObjectsNode(template.Node):
    def __init__(self, model, manager_method, limit, var_name):
        self.model = model
        self.manager_method = manager_method
        self.limit = template.Variable(limit) if limit else None
        self.var_name = var_name

    def render(self, context):
        if "." in self.manager_method:
            manager, method = self.manager_method.split(".")
        else:
            manager = "_default_manager"
            method = self.manager_method

        model_manager = getattr(self.model, manager)
        fallback_method = self.model._default_manager.none
        qs = getattr(model_manager, method, fallback_method)()
        limit = None
        if self.limit:
            try:
                limit = self.limit.resolve(context)
            except template.VariableDoesNotExist:
                limit = None
        context[self.var_name] = qs[:limit] if limit else qs
        return ""


@register.tag
def load_objects(parser, token):
    """
    Gets a queryset of objects of the model specified by app and
    model names

    Usage:
        {% load_objects [<manager>.]<method>
                        from <app_name>.<model_name>
                        [limit <amount>]
                        as <var_name> %}

    Examples:
        {% load_objects latest_published from people.Person
                        limit 3 as people %}
        {% load_objects site_objects.all from news.Article
                        as articles %}
        {% load_objects site_objects.all from news.Article
                        limit 3 as articles %}
    """
    limit_count = None
    try:
        (tag_name, manager_method,
         str_from, app_model,
         str_limit, limit_count,
         str_as, var_name) = token.split_contents()
    except ValueError:
        try:
            (tag_name, manager_method,
             str_from, app_model,
             str_as, var_name) = token.split_contents()
        except ValueError:
            tag_name = token.contents.split()[0]
            raise template.TemplateSyntaxError(
                f"{tag_name} tag requires the following syntax: "
                f"{{% {tag_name} [<manager>.]<method> from "
                "<app_name>.<model_name> [limit <amount>] "
                "as <var_name> %}")
    try:
        app_name, model_name = app_model.split(".")
    except ValueError:
        raise template.TemplateSyntaxError(
            "load_objects tag requires application name "
            "and model name, separated by a dot")
    model = apps.get_model(app_name, model_name)
    return ObjectsNode(model, manager_method, limit_count,
                       var_name)


class ParseNode(template.Node):
    def __init__(self, template_value, var_name):
        self.template_value = template.Variable(template_value)
        self.var_name = var_name

    def render(self, context):
        template_value = self.template_value.resolve(context)
        t = template.Template(template_value)
        context_vars = {}
        for d in list(context):
            for var, val in d.items():
                context_vars[var] = val
        req_context = template.RequestContext(context["request"],
                                              context_vars)
        result = t.render(req_context)
        if self.var_name:
            context[self.var_name] = result
            result = ""
        return result


@register.tag
def parse(parser, token):
    """
    Parses a value as a template and prints or saves to a variable

    Usage:
        {% parse <template_value> [as <variable>] %}

    Examples:
        {% parse object.description %}
        {% parse header as header %}
        {% parse "{{ MEDIA_URL }}js/" as js_url %}
    """
    bits = token.split_contents()
    tag_name = bits.pop(0)
    try:
        template_value = bits.pop(0)
        var_name = None
        if len(bits) >= 2:
            str_as, var_name = bits[:2]
    except ValueError:
        raise template.TemplateSyntaxError(
            f"{tag_name} tag requires the following syntax: "
            f"{{% {tag_name} <template_value> [as <variable>] %}}")
    return ParseNode(template_value, var_name)


def construct_query_string(context, query_params):
    # empty values will be removed
    query_string = context["request"].path
    if len(query_params):
        encoded_params = urlencode([
            (key, force_str(value))
            for (key, value) in query_params if value
        ]).replace("&", "&amp;")
        query_string += f"?{encoded_params}"
    return mark_safe(query_string)


@register.simple_tag(takes_context=True)
def modify_query(context, *params_to_remove, **params_to_change):
    """Renders a link with modified current query parameters"""
    query_params = []
    for key, value_list in context["request"].GET.lists():
        if not key in params_to_remove:
            # don't add key-value pairs for params_to_remove
            if key in params_to_change:
                # update values for keys in params_to_change
                query_params.append((key, params_to_change[key]))
                params_to_change.pop(key)
            else:
                # leave existing parameters as they were
                # if not mentioned in the params_to_change
                for value in value_list:
                    query_params.append((key, value))
                    # attach new params
    for key, value in params_to_change.items():
        query_params.append((key, value))
    return construct_query_string(context, query_params)


@register.simple_tag(takes_context=True)
def add_to_query(context, *params_to_remove, **params_to_add):
    """Renders a link with modified current query parameters"""
    query_params = []
    # go through current query params..
    for key, value_list in context["request"].GET.lists():
        if key not in params_to_remove:
            # don't add key-value pairs which already
            # exist in the query
            if (key in params_to_add
                    and params_to_add[key] in value_list):
                params_to_add.pop(key)
            for value in value_list:
                query_params.append((key, value))
    # add the rest key-value pairs
    for key, value in params_to_add.items():
        query_params.append((key, value))
    return construct_query_string(context, query_params)


@register.simple_tag(takes_context=True)
def remove_from_query(context, *args, **kwargs):
    """Renders a link with modified current query parameters"""
    query_params = []
    # go through current query params..
    for key, value_list in context["request"].GET.lists():
        # skip keys mentioned in the args
        if key not in args:
            for value in value_list:
                # skip key-value pairs mentioned in kwargs
                if not (key in kwargs and
                        str(value) == str(kwargs[key])):
                    query_params.append((key, value))
    return construct_query_string(context, query_params)


""" FILTERS """

DAYS_PER_YEAR = 365
DAYS_PER_MONTH = 30
DAYS_PER_WEEK = 7


@register.filter(is_safe=True)
def date_since(specific_date):
    """
    Returns a human-friendly difference between today and past_date
    (adapted from https://www.djangosnippets.org/snippets/116/)
    """
    today = timezone.now().date()
    if isinstance(specific_date, datetime):
        specific_date = specific_date.date()
    diff = today - specific_date
    diff_years = int(diff.days / DAYS_PER_YEAR)
    diff_months = int(diff.days / DAYS_PER_MONTH)
    diff_weeks = int(diff.days / DAYS_PER_WEEK)
    diff_map = [
        ("year", "years", diff_years,),
        ("month", "months", diff_months,),
        ("week", "weeks", diff_weeks,),
        ("day", "days", diff.days,),
    ]
    for parts in diff_map:
        (interval, intervals, count,) = parts
        if count > 1:
            return _(f"{count} {intervals} ago")
        elif count == 1:
            return _("yesterday") \
                if interval == "day" \
                else _(f"last {interval}")
    if diff.days == 0:
        return _("today")
    else:
        # Date is in the future; return formatted date.
        return f"{specific_date:%B %d, %Y}"


MEDIA_CLOSED_TAGS = "|".join([
    "figure", "object", "video", "audio", "iframe"])
MEDIA_SINGLE_TAGS = "|".join(["img", "embed"])
MEDIA_TAGS_REGEX = re.compile(
    r"<(?P<tag>" + MEDIA_CLOSED_TAGS + ")[\S\s]+?</(?P=tag)>|" +
    r"<(" + MEDIA_SINGLE_TAGS + ")[^>]+>",
    re.MULTILINE)


@register.filter
def first_media(content):
    """
    Returns the chunk of media-related markup from the html content
    """
    tag_match = MEDIA_TAGS_REGEX.search(content)
    media_tag = ""
    if tag_match:
        media_tag = tag_match.group()
    return mark_safe(media_tag)


@register.filter
def humanize_url(url, letter_count=40):
    """
    Returns a shortened human-readable URL
    """
    letter_count = int(letter_count)
    re_start = re.compile(r"^https?://")
    re_end = re.compile(r"/$")
    url = re_end.sub("", re_start.sub("", url))
    if len(url) > letter_count:
        url = f"{url[:letter_count - 1]}…"
    return url

