from urllib.parse import urlparse, urlunparse
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now as timezone_now
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.exceptions import FieldError


class UrlBase(models.Model):
    """
    A replacement for get_absolute_url()
    Models extending this mixin should have either get_url or get_url_path implemented.
    http://code.djangoproject.com/wiki/ReplacingGetAbsoluteUrl
    """
    class Meta:
        abstract = True

    def get_url(self):
        if hasattr(self.get_url_path, "dont_recurse"):
            raise NotImplementedError
        try:
            path = self.get_url_path()
        except NotImplementedError:
            raise
        return settings.WEBSITE_URL + path
    get_url.dont_recurse = True

    def get_url_path(self):
        if hasattr(self.get_url, "dont_recurse"):
            raise NotImplementedError
        try:
            url = self.get_url()
        except NotImplementedError:
            raise
        bits = urlparse(url)
        return urlunparse(("", "") + bits[2:])
    get_url_path.dont_recurse = True

    def get_absolute_url(self):
        return self.get_url()


class CreationModificationDateBase(models.Model):
    """
    Abstract base class with a creation and modification date and time
    """

    created = models.DateTimeField(
        _("Creation Date and Time"),
        editable=False,
    )

    modified = models.DateTimeField(
        _("Modification Date and Time"),
        editable=False,
    )

    def save(self, *args, **kwargs):
        if not self.created:
            self.created = timezone_now()
        self.modified = timezone_now()
        super().save(*args, **kwargs)
    save.alters_data = True

    class Meta:
        abstract = True


class MetaTagsBase(models.Model):
    """
    Abstract base class for generating meta tags
    """
    class Meta:
        abstract = True

    meta_keywords = models.CharField(
        _("Keywords"),
        max_length=255,
        blank=True,
        help_text=_("Separate keywords with commas."))
    meta_description = models.CharField(
        _("Description"),
        max_length=255,
        blank=True)
    meta_author = models.CharField(
        _("Author"),
        max_length=255,
        blank=True)
    meta_copyright = models.CharField(
        _("Copyright"),
        max_length=255,
        blank=True)

    def get_meta(self, name, content):
        tag = ""
        if name and content:
            tag = render_to_string("utils/meta.html", {
                "name": name,
                "content": content,
            })
        return mark_safe(tag)

    def get_meta_keywords(self):
        return self.get_meta("keywords", self.meta_keywords)

    def get_meta_description(self):
        return self.get_meta("description", self.meta_description)

    def get_meta_author(self):
        return self.get_meta("author", self.meta_author)

    def get_meta_copyright(self):
        return self.get_meta("copyright", self.meta_copyright)

    def get_meta_tags(self):
        return mark_safe("\n".join((
            self.get_meta_keywords(),
            self.get_meta_description(),
            self.get_meta_author(),
            self.get_meta_copyright(),
        )))


def object_relation_base_factory(
        prefix=None,
        prefix_verbose=None,
        add_related_name=False,
        limit_content_type_choices_to=None,
        limit_object_choices_to=None,
        is_required=False):
    """
    Returns a mixin class for generic foreign keys using
    "Content type - object ID" with dynamic field names.
    This function is just a class generator.

    Parameters:
    prefix:           a prefix, which is added in front of
                      the fields
    prefix_verbose:   a verbose name of the prefix, used to
                      generate a title for the field column
                      of the content object in the Admin
    add_related_name: a boolean value indicating, that a
                      related name for the generated content
                      type foreign key should be added. This
                      value should be true, if you use more
                      than one ObjectRelationMixin in your
                      model.

    The model fields are created using this naming scheme:
        <<prefix>>_content_type
        <<prefix>>_object_id
        <<prefix>>_content_object
    """
    p = ""
    if prefix:
        p = f"{prefix}_"

    prefix_verbose = prefix_verbose or _("Related object")
    limit_content_type_choices_to = limit_content_type_choices_to or {}
    limit_object_choices_to = limit_object_choices_to or {}

    content_type_field = f"{p}content_type"
    object_id_field = f"{p}object_id"
    content_object_field = f"{p}content_object"

    class TheClass(models.Model):
        class Meta:
            abstract = True

    if add_related_name:
        if not prefix:
            raise FieldError("if add_related_name is set to "
                             "True, a prefix must be given")
        related_name = prefix
    else:
        related_name = None

    optional = not is_required

    ct_verbose_name = _(f"{prefix_verbose}'s type (model)")

    content_type = models.ForeignKey(
        ContentType,
        verbose_name=ct_verbose_name,
        related_name=related_name,
        blank=optional,
        null=optional,
        help_text=_("Please select the type (model) "
                    "for the relation, you want to build."),
        limit_choices_to=limit_content_type_choices_to,
        on_delete=models.CASCADE)

    fk_verbose_name = prefix_verbose

    object_id = models.CharField(
        fk_verbose_name,
        blank=optional,
        null=False,
        help_text=_("Please enter the ID of the related object."),
        max_length=255,
        default="")  # for migrations
    object_id.limit_choices_to = limit_object_choices_to
    # can be retrieved by
    # MyModel._meta.get_field("object_id").limit_choices_to

    content_object = GenericForeignKey(
        ct_field=content_type_field,
        fk_field=object_id_field)

    TheClass.add_to_class(content_type_field, content_type)
    TheClass.add_to_class(object_id_field, object_id)
    TheClass.add_to_class(content_object_field,
                          content_object)

    return TheClass
