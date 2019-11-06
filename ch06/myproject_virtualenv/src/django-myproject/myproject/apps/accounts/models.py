import os
import uuid

from imagekit.models import ImageSpecField
from pilkit.processors import ResizeToFill

from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone


class Role(Group):
    class Meta:
        proxy = True
        verbose_name = _("Role")
        verbose_name_plural = _("Roles")

    def __str__(self):
        return self.name


class UserManager(BaseUserManager):
    def create_user(self, username="", email="", password="", **extra_fields):
        if not email:
            raise ValueError("Enter an email address")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username="", email="", password=""):
        user = self.create_user(email=email, password=password, username=username)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


def upload_to(instance, filename):
    now = timezone.now()
    filename_base, filename_ext = os.path.splitext(filename)
    return "users/{user_id}/{filename}{ext}".format(
        user_id=instance.pk,
        filename=now.strftime("%Y%m%d%H%M%S"),
        ext=filename_ext.lower(),
    )


class User(AbstractUser):
    uuid = models.UUIDField(primary_key=True, default=None, editable=False)
    # change username to non-editable non-required field
    username = models.CharField(
        _("username"), max_length=150, editable=False, blank=True
    )
    # change email to unique and required field
    email = models.EmailField(_("email address"), unique=True)

    avatar = models.ImageField(_("Avatar"), upload_to=upload_to, blank=True)
    avatar_thumbnail = ImageSpecField(
        source="avatar",
        processors=[ResizeToFill(60, 60)],
        format="JPEG",
        options={"quality": 100},
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.pk = uuid.uuid4()
        super().save(*args, **kwargs)
