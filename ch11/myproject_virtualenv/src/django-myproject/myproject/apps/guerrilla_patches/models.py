from django.utils import text
from transliterate import slugify


text.slugify = slugify
