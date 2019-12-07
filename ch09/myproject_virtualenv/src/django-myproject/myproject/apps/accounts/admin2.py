from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, Group, GroupAdmin
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.encoding import force_bytes
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import UserCreationForm

from .helpers import download_avatar
from .models import User, Role


class MyUserCreationForm(UserCreationForm):
    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = user.email
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


@admin.register(User)
class MyUserAdmin(UserAdmin):
    save_on_top = True
    list_display = [
        "get_avatar",
        "get_full_name",
        "download_gravatar",
        "is_active",
        "is_staff",
        "is_superuser",
    ]
    list_display_links = [
        "get_avatar",
        "get_full_name",
    ]
    search_fields = ["email", "first_name", "last_name", "id", "username"]
    ordering = ["-is_superuser", "-is_staff", "last_name", "first_name"]

    fieldsets = [
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (_("Avatar"), {"fields": ("avatar",)}),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    ]
    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": ("email", "password1", "password2")}),
    )
    add_form = MyUserCreationForm

    def get_full_name(self, obj):
        return obj.get_full_name()

    get_full_name.short_description = _("Full name")

    def get_avatar(self, obj):
        from django.template.loader import render_to_string
        html = render_to_string("admin/accounts/includes/avatar.html", context={
            "obj": obj
        })
        return mark_safe(html)

    get_avatar.short_description = _("Avatar")

    def download_gravatar(self, obj):
        from django.template.loader import render_to_string
        info = self.model._meta.app_label, self.model._meta.model_name
        gravatar_url = reverse("admin:%s_%s_download_gravatar" % info, args=[obj.pk])
        html = render_to_string("admin/accounts/includes/download_gravatar.html", context={
            "url": gravatar_url
        })
        return mark_safe(html)

    download_gravatar.short_description = _("Gravatar")

    def get_urls(self):
        from functools import update_wrapper
        from django.conf.urls import url

        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)

            wrapper.model_admin = self
            return update_wrapper(wrapper, view)

        info = self.model._meta.app_label, self.model._meta.model_name

        urlpatterns = [
            url(
                r"^(.+)/download-gravatar/$",
                wrap(self.download_gravatar_view),
                name="%s_%s_download_gravatar" % info,
            )
        ] + super().get_urls()

        return urlpatterns

    def download_gravatar_view(self, request, object_id):
        if request.method != "POST":
            return HttpResponse(
                "{} method not allowed.".format(request.method), status=405
            )
        from .models import User

        user = get_object_or_404(User, pk=object_id)
        import hashlib

        m = hashlib.md5()
        m.update(force_bytes(user.email))
        md5_hash = m.hexdigest()
        # d=404 ensures that 404 error is raised if gravatar is not found instead of returning default placeholder
        url = "https://www.gravatar.com/avatar/{md5_hash}?s=800&d=404".format(
            md5_hash=md5_hash
        )
        download_avatar(object_id, url)
        return HttpResponse("Gravatar downloaded.", status=200)


admin.site.unregister(Group)


@admin.register(Role)
class RoleAdmin(GroupAdmin):
    list_display = ("__str__", "display_users")
    save_on_top = True

    def display_users(self, obj):
        links = []
        for user in obj.user_set.all():
            ct = ContentType.objects.get_for_model(user)
            url = reverse(
                "admin:{}_{}_change".format(ct.app_label, ct.model), args=(user.pk,)
            )
            links.append(
                """<a href="{}" target="_blank">{}</a>""".format(
                    url,
                    user.get_full_name() or user.username,
                )
            )
        return mark_safe(u"<br />".join(links))

    display_users.short_description = _("Users")
