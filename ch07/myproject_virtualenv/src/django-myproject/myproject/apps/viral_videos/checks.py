from django.core.checks import Warning, register, Tags


@register(Tags.compatibility)
def settings_check(app_configs, **kwargs):
    from django.conf import settings

    errors = []

    if not settings.ADMINS:
        errors.append(Warning(
            """
The system admins are not set in the project settings
""",
            obj=settings,
            hint="""
            In order to receive notifications when new videos are
            created, define system admins in your settings, like:

            ADMINS = (
                ("Admin", "administrator@example.com"),
            )
""",
            id="viral_videos.W001"))

    return errors
