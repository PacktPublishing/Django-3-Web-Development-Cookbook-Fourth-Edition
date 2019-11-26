from django.contrib import admin

from admin_honeypot.admin import LoginAttemptAdmin
from admin_honeypot.models import LoginAttempt
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

admin.site.unregister(LoginAttempt)


@admin.register(LoginAttempt)
class FixedLoginAttemptAdmin(LoginAttemptAdmin):
    def get_session_key(self, instance):
        return mark_safe('<a href="?session_key=%(key)s">%(key)s</a>' % {'key': instance.session_key})
    get_session_key.short_description = _('Session')

    def get_ip_address(self, instance):
        return mark_safe('<a href="?ip_address=%(ip)s">%(ip)s</a>' % {'ip': instance.ip_address})
    get_ip_address.short_description = _('IP Address')

    def get_path(self, instance):
        return mark_safe('<a href="?path=%(path)s">%(path)s</a>' % {'path': instance.path})
    get_path.short_description = _('URL')
