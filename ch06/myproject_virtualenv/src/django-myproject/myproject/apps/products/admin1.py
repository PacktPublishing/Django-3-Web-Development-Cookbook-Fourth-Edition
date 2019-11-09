# myproject/apps/products/admin.py
from django.contrib import admin
from django.template.loader import render_to_string
from django.utils.html import mark_safe
from django.utils.translation import ugettext_lazy as _

from .models import Product, ProductPhoto


class ProductPhotoInline(admin.StackedInline):
    model = ProductPhoto
    extra = 0
    fields = ["photo"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["get_first_photo", "title", "has_description", "price"]
    list_display_links = ["get_first_photo", "title"]
    list_editable = ["price"]

    fieldsets = ((_("Product"), {"fields": ("title", "slug", "description", "price")}),)
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ProductPhotoInline]

    def get_first_photo(self, obj):
        project_photos = obj.productphoto_set.all()[:1]
        if project_photos.count() > 0:
            photo_preview = render_to_string(
                "admin/products/includes/photo-preview.html",
                {"photo": project_photos[0], "product": obj},
            )
            return mark_safe(photo_preview)
        return ""

    get_first_photo.short_description = _("Preview")

    def has_description(self, obj):
        return bool(obj.description)

    has_description.short_description = _("Has description?")
    has_description.admin_order_field = "description"
    has_description.boolean = True