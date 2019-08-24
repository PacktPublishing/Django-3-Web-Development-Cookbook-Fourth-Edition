from django.conf import settings
from django.db import models
from django.utils.translation import get_language
from django.utils import translation


class MultilingualField(models.Field):
    SUPPORTED_FIELD_TYPES = [models.CharField, models.TextField]

    def __init__(self, verbose_name=None, **kwargs):
        self.localized_field_model = None
        for model in MultilingualField.SUPPORTED_FIELD_TYPES:
            if issubclass(self.__class__, model):
                self.localized_field_model = model
        self._blank = kwargs.get("blank", False)
        self._editable = kwargs.get("editable", True)
        super().__init__(verbose_name, **kwargs)

    @staticmethod
    def localized_field_name(name, lang_code):
        lang_code_safe = lang_code.replace("-", "_")
        return f"{name}_{lang_code_safe}"

    def get_localized_field(self, lang_code, lang_name):
        _blank = (self._blank
                  if lang_code == settings.LANGUAGE_CODE
                  else True)
        localized_field = self.localized_field_model(
            f"{self.verbose_name} ({lang_name})",
            name=self.name,
            primary_key=self.primary_key,
            max_length=self.max_length,
            unique=self.unique,
            blank=_blank,
            null=False, # we ignore the null argument!
            db_index=self.db_index,
            default=self.default or "",
            editable=self._editable,
            serialize=self.serialize,
            choices=self.choices,
            help_text=self.help_text,
            db_column=None,
            db_tablespace=self.db_tablespace)
        return localized_field

    def contribute_to_class(self, cls, name,
                            private_only=False,
                            virtual_only=False):
        def translated_value(self):
            language = get_language()
            val = self.__dict__.get(
                MultilingualField.localized_field_name(
                        name, language))
            if not val:
                val = self.__dict__.get(
                    MultilingualField.localized_field_name(
                            name, settings.LANGUAGE_CODE))
            return val

        # generate language-specific fields dynamically
        if not cls._meta.abstract:
            if self.localized_field_model:
                for lang_code, lang_name in settings.LANGUAGES:
                    localized_field = self.get_localized_field(
                        lang_code, lang_name)
                    localized_field.contribute_to_class(
                            cls,
                            MultilingualField.localized_field_name(
                                    name, lang_code))

                setattr(cls, name, property(translated_value))
            else:
                super().contribute_to_class(
                    cls, name, private_only, virtual_only)


class MultilingualCharField(models.CharField, MultilingualField):
    pass


class MultilingualTextField(models.TextField, MultilingualField):
    pass


class TranslatedField(object):
    def __init__(self, field_name):
        self.field_name = field_name

    def __get__(self, instance, owner):
        lang_code = translation.get_language()
        if lang_code == settings.LANGUAGE_CODE:
            # The fields of the default language are the main model
            return getattr(instance, self.field_name)
        else:
            # The fields of the other languages are the translation model, but falls back to the main model
            translations = (
                instance.translations.filter(language=lang_code).first() or instance
            )
            return getattr(translations, self.field_name)
