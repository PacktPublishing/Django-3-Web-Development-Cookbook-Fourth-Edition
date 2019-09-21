from django.conf import settings
from django.utils.translation import get_language, activate
from django.db import models

from django_elasticsearch_dsl import fields
from django_elasticsearch_dsl.documents import (
    Document,
    model_field_class_to_field_class,
)
from django_elasticsearch_dsl.registries import registry

from myproject.apps.categories.models import Category
from .models import Idea

# monkey patching the mapper of Django model fields to ElasticSearch fields
model_field_class_to_field_class[models.UUIDField] = fields.TextField


def _get_url_path(instance, language):
    current_language = get_language()
    activate(language)
    url_path = instance.get_url_path()
    activate(current_language)
    return url_path


@registry.register_document
class IdeaDocument(Document):
    author = fields.NestedField(
        properties={
            "first_name": fields.StringField(),
            "last_name": fields.StringField(),
            "username": fields.StringField(),
            "pk": fields.IntegerField(),
        },
        include_in_root=True,
    )
    title_bg = fields.StringField()
    title_hr = fields.StringField()
    title_cs = fields.StringField()
    title_da = fields.StringField()
    title_nl = fields.StringField()
    title_en = fields.StringField()
    title_et = fields.StringField()
    title_fi = fields.StringField()
    title_fr = fields.StringField()
    title_de = fields.StringField()
    title_el = fields.StringField()
    title_hu = fields.StringField()
    title_ga = fields.StringField()
    title_it = fields.StringField()
    title_lv = fields.StringField()
    title_lt = fields.StringField()
    title_mt = fields.StringField()
    title_pl = fields.StringField()
    title_pt = fields.StringField()
    title_ro = fields.StringField()
    title_sk = fields.StringField()
    title_sl = fields.StringField()
    title_es = fields.StringField()
    title_sv = fields.StringField()
    content_bg = fields.StringField()
    content_hr = fields.StringField()
    content_cs = fields.StringField()
    content_da = fields.StringField()
    content_nl = fields.StringField()
    content_en = fields.StringField()
    content_et = fields.StringField()
    content_fi = fields.StringField()
    content_fr = fields.StringField()
    content_de = fields.StringField()
    content_el = fields.StringField()
    content_hu = fields.StringField()
    content_ga = fields.StringField()
    content_it = fields.StringField()
    content_lv = fields.StringField()
    content_lt = fields.StringField()
    content_mt = fields.StringField()
    content_pl = fields.StringField()
    content_pt = fields.StringField()
    content_ro = fields.StringField()
    content_sk = fields.StringField()
    content_sl = fields.StringField()
    content_es = fields.StringField()
    content_sv = fields.StringField()

    picture_thumbnail_url = fields.StringField()

    categories = fields.NestedField(
        properties=dict(
            pk=fields.IntegerField(),
            title_bg=fields.StringField(),
            title_hr=fields.StringField(),
            title_cs=fields.StringField(),
            title_da=fields.StringField(),
            title_nl=fields.StringField(),
            title_en=fields.StringField(),
            title_et=fields.StringField(),
            title_fi=fields.StringField(),
            title_fr=fields.StringField(),
            title_de=fields.StringField(),
            title_el=fields.StringField(),
            title_hu=fields.StringField(),
            title_ga=fields.StringField(),
            title_it=fields.StringField(),
            title_lv=fields.StringField(),
            title_lt=fields.StringField(),
            title_mt=fields.StringField(),
            title_pl=fields.StringField(),
            title_pt=fields.StringField(),
            title_ro=fields.StringField(),
            title_sk=fields.StringField(),
            title_sl=fields.StringField(),
            title_es=fields.StringField(),
            title_sv=fields.StringField(),
        ),
        include_in_root=True,
    )

    url_path_bg = fields.StringField()
    url_path_hr = fields.StringField()
    url_path_cs = fields.StringField()
    url_path_da = fields.StringField()
    url_path_nl = fields.StringField()
    url_path_en = fields.StringField()
    url_path_et = fields.StringField()
    url_path_fi = fields.StringField()
    url_path_fr = fields.StringField()
    url_path_de = fields.StringField()
    url_path_el = fields.StringField()
    url_path_hu = fields.StringField()
    url_path_ga = fields.StringField()
    url_path_it = fields.StringField()
    url_path_lv = fields.StringField()
    url_path_lt = fields.StringField()
    url_path_mt = fields.StringField()
    url_path_pl = fields.StringField()
    url_path_pt = fields.StringField()
    url_path_ro = fields.StringField()
    url_path_sk = fields.StringField()
    url_path_sl = fields.StringField()
    url_path_es = fields.StringField()
    url_path_sv = fields.StringField()

    class Index:
        name = "ideas"
        settings = {"number_of_shards": 1, "number_of_replicas": 0}

    class Django:
        model = Idea
        # The fields of the model you want to be indexed in Elasticsearch
        fields = ["uuid", "rating"]
        related_models = [Category]

    def prepare(self, instance):
        lang_code_underscored = settings.LANGUAGE_CODE.replace("-", "_")
        setattr(instance, f"title_{lang_code_underscored}", instance.title)
        setattr(instance, f"content_{lang_code_underscored}", instance.content)
        setattr(
            instance,
            f"url_path_{lang_code_underscored}",
            _get_url_path(instance=instance, language=settings.LANGUAGE_CODE),
        )
        for lang_code, lang_name in settings.LANGUAGES_EXCEPT_THE_DEFAULT:
            lang_code_underscored = lang_code.replace("-", "_")
            setattr(instance, f"title_{lang_code_underscored}", "")
            setattr(instance, f"content_{lang_code_underscored}", "")
            translations = instance.translations.filter(language=lang_code).first()
            if translations:
                setattr(instance, f"title_{lang_code_underscored}", translations.title)
                setattr(
                    instance, f"content_{lang_code_underscored}", translations.content
                )
            setattr(
                instance,
                f"url_path_{lang_code_underscored}",
                _get_url_path(instance=instance, language=lang_code),
            )
        data = super().prepare(instance=instance)
        return data

    def prepare_picture_thumbnail_url(self, instance):
        if not instance.picture:
            return ""
        return instance.picture_thumbnail.url

    def prepare_author(self, instance):
        author = instance.author
        if not author:
            return []
        author_dict = {
            "pk": author.pk,
            "first_name": author.first_name,
            "last_name": author.last_name,
            "username": author.username,
        }
        return [author_dict]

    def prepare_categories(self, instance):
        categories = []
        for category in instance.categories.all():
            category_dict = {"pk": category.pk}
            lang_code_underscored = settings.LANGUAGE_CODE.replace("-", "_")
            category_dict[f"title_{lang_code_underscored}"] = category.title
            for lang_code, lang_name in settings.LANGUAGES_EXCEPT_THE_DEFAULT:
                lang_code_underscored = lang_code.replace("-", "_")
                category_dict[f"title_{lang_code_underscored}"] = ""
                translations = category.translations.filter(language=lang_code).first()
                if translations:
                    category_dict[f"title_{lang_code_underscored}"] = translations.title
            categories.append(category_dict)
        return categories

    @property
    def translated_title(self):
        lang_code_underscored = get_language().replace("-", "_")
        return getattr(self, f"title_{lang_code_underscored}", "")

    @property
    def translated_content(self):
        lang_code_underscored = get_language().replace("-", "_")
        return getattr(self, f"content_{lang_code_underscored}", "")

    def get_url_path(self):
        lang_code_underscored = get_language().replace("-", "_")
        return getattr(self, f"url_path_{lang_code_underscored}", "")

    def get_categories(self):
        lang_code_underscored = get_language().replace("-", "_")
        return [
            dict(
                translated_title=category_dict[f"title_{lang_code_underscored}"],
                **category_dict,
            )
            for category_dict in self.categories
        ]

    def get_instances_from_related(self, related_instance):
        if isinstance(related_instance, Category):
            category = related_instance
            return category.category_ideas.all()
