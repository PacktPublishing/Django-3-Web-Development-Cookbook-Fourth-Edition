from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string

from .models import ViralVideo


@receiver(post_save, sender=ViralVideo)
def inform_administrators(sender, **kwargs):
    from django.core.mail import mail_admins

    instance = kwargs["instance"]
    created = kwargs["created"]

    if created:
        context = {
            "title": instance.title,
            "link": instance.get_url(),
        }
        plain_text_message = render_to_string(
            'viral_videos/email/administrator/message.txt',
            context)
        html_message = render_to_string(
            'viral_videos/email/administrator/message.html',
            context)
        subject = render_to_string(
            'viral_videos/email/administrator/subject.txt',
            context)

        mail_admins(
            subject=subject.strip(),
            message=plain_text_message,
            html_message=html_message,
            fail_silently=True)
