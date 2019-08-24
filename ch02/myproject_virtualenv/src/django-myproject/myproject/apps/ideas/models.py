from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from myproject.apps.core.model_fields import (
    MultilingualCharField,
    MultilingualTextField,
)
from myproject.apps.core.models import (
    CreationModificationDateBase,
    MetaTagsBase,
    UrlBase,
    object_relation_base_factory as generic_relation,
)


FavoriteObjectBase = generic_relation(is_required=True)


OwnerBase = generic_relation(
    prefix="owner",
    prefix_verbose=_("Owner"),
    is_required=True,
    add_related_name=True,
    limit_content_type_choices_to={
        "model__in": (
            "user",
            "group",
        )
    }
)


class Like(FavoriteObjectBase, OwnerBase):
    class Meta:
        verbose_name = _("Like")
        verbose_name_plural = _("Likes")

    def __str__(self):
        return _("{owner} likes {object}").format(
            owner=self.owner_content_object,
            object=self.content_object
        )


class Idea(CreationModificationDateBase, MetaTagsBase, UrlBase):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("Author"),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="authored_ideas",
    )
    title = MultilingualCharField(
        _("Title"),
        max_length=200,
    )
    content = MultilingualTextField(
        _("Content"),
    )
    category = models.ForeignKey(
        "categories.Category",
        verbose_name=_("Category"),
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="category_ideas",
    )
    #categories = models.ManyToManyField(
    #    "categories.Category",
    #    verbose_name=_("Category"),
    #    blank=True,
    #    related_name="ideas",
    #)

    class Meta:
        verbose_name = _("Idea")
        verbose_name_plural = _("Ideas")

        constraints = [
            models.UniqueConstraint(
                fields=[f"title_{settings.LANGUAGE_CODE}"],
                condition=~models.Q(author=None),
                name="unique_titles_for_each_author",
            ),
            models.CheckConstraint(
                check=models.Q(**{
                    f"title_{settings.LANGUAGE_CODE}__iregex": r"^\S.*\S$"
                    # starts with non-whitespace,
                    # ends with non-whitespace,
                    # anything in the middle
                }),
                name="title_has_no_leading_and_trailing_whitespaces",
            )
        ]

    def __str__(self):
        return self.title

    def get_url_path(self):
        return reverse("idea_details", kwargs={
            "idea_id": str(self.pk),
        })

    def clean(self):
        import re
        lang_code_underscored = settings.LANGUAGE_CODE.replace("-", "_")
        title_field = f"title_{lang_code_underscored}"
        title_value = getattr(self, f"title_{lang_code_underscored}")
        if self.author and Idea.objects.exclude(pk=self.pk).filter(**{
            "author": self.author,
            title_field: title_value,
        }).exists():
            raise ValidationError(_("Each idea of the same user should have a unique title."))
        if not re.match(r"^\S.*\S$", title_value):
            raise ValidationError(_("The title cannot start or end with a whitespace."))
