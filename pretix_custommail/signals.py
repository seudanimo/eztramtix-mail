from django.dispatch import receiver

from pretix.base.signals import register_html_mail_renderers, register_text_placeholders

from .mail import CustomMailRenderer
from .placeholders import get_placeholders


@receiver(register_html_mail_renderers, dispatch_uid="pretix_custommail_renderer")
def register_renderer(sender, **kwargs):
    return [CustomMailRenderer]


@receiver(register_text_placeholders, dispatch_uid="pretix_custommail_placeholders")
def register_placeholders(sender, **kwargs):
    return get_placeholders(sender)
