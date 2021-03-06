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
            "first_name": fields.TextField(),
            "last_name": fields.TextField(),
            "username": fields.TextField(),
            "pk": fields.IntegerField(),
        },
        include_in_root=True,
    )
    title_bg = fields.TextField()
    title_hr = fields.TextField()
    title_cs = fields.TextField()
    title_da = fields.TextField()
    title_nl = fields.TextField()
    title_en = fields.TextField()
    title_et = fields.TextField()
    title_fi = fields.TextField()
    title_fr = fields.TextField()
    title_de = fields.TextField()
    title_el = fields.TextField()
    title_hu = fields.TextField()
    title_ga = fields.TextField()
    title_it = fields.TextField()
    title_lv = fields.TextField()
    title_lt = fields.TextField()
    title_mt = fields.TextField()
    title_pl = fields.TextField()
    title_pt = fields.TextField()
    title_ro = fields.TextField()
    title_sk = fields.TextField()
    title_sl = fields.TextField()
    title_es = fields.TextField()
    title_sv = fields.TextField()
    content_bg = fields.TextField()
    content_hr = fields.TextField()
    content_cs = fields.TextField()
    content_da = fields.TextField()
    content_nl = fields.TextField()
    content_en = fields.TextField()
    content_et = fields.TextField()
    content_fi = fields.TextField()
    content_fr = fields.TextField()
    content_de = fields.TextField()
    content_el = fields.TextField()
    content_hu = fields.TextField()
    content_ga = fields.TextField()
    content_it = fields.TextField()
    content_lv = fields.TextField()
    content_lt = fields.TextField()
    content_mt = fields.TextField()
    content_pl = fields.TextField()
    content_pt = fields.TextField()
    content_ro = fields.TextField()
    content_sk = fields.TextField()
    content_sl = fields.TextField()
    content_es = fields.TextField()
    content_sv = fields.TextField()

    picture_thumbnail_url = fields.TextField()

    categories = fields.NestedField(
        properties=dict(
            pk=fields.IntegerField(),
            title_bg=fields.TextField(),
            title_hr=fields.TextField(),
            title_cs=fields.TextField(),
            title_da=fields.TextField(),
            title_nl=fields.TextField(),
            title_en=fields.TextField(),
            title_et=fields.TextField(),
            title_fi=fields.TextField(),
            title_fr=fields.TextField(),
            title_de=fields.TextField(),
            title_el=fields.TextField(),
            title_hu=fields.TextField(),
            title_ga=fields.TextField(),
            title_it=fields.TextField(),
            title_lv=fields.TextField(),
            title_lt=fields.TextField(),
            title_mt=fields.TextField(),
            title_pl=fields.TextField(),
            title_pt=fields.TextField(),
            title_ro=fields.TextField(),
            title_sk=fields.TextField(),
            title_sl=fields.TextField(),
            title_es=fields.TextField(),
            title_sv=fields.TextField(),
        ),
        include_in_root=True,
    )

    url_path_bg = fields.TextField()
    url_path_hr = fields.TextField()
    url_path_cs = fields.TextField()
    url_path_da = fields.TextField()
    url_path_nl = fields.TextField()
    url_path_en = fields.TextField()
    url_path_et = fields.TextField()
    url_path_fi = fields.TextField()
    url_path_fr = fields.TextField()
    url_path_de = fields.TextField()
    url_path_el = fields.TextField()
    url_path_hu = fields.TextField()
    url_path_ga = fields.TextField()
    url_path_it = fields.TextField()
    url_path_lv = fields.TextField()
    url_path_lt = fields.TextField()
    url_path_mt = fields.TextField()
    url_path_pl = fields.TextField()
    url_path_pt = fields.TextField()
    url_path_ro = fields.TextField()
    url_path_sk = fields.TextField()
    url_path_sl = fields.TextField()
    url_path_es = fields.TextField()
    url_path_sv = fields.TextField()

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
