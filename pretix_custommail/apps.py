from django.apps import AppConfig
from django.utils.translation import gettext_lazy

from . import __version__


class CustomMailApp(AppConfig):
    name = "pretix_custommail"
    verbose_name = "Pretix Custom Mail"

    class PretixPluginMeta:
        name = gettext_lazy("Custom HTML email renderer")
        author = "Pretix Custom Mail Contributors"
        category = "CUSTOMIZATION"
        description = gettext_lazy(
            "Provide a modern, branded HTML email renderer for pretix."
        )
        visible = True
        version = __version__
        compatibility = "2025.7.0"

    def ready(self):
        from . import signals  # NOQA
