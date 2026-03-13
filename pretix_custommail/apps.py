from django.utils.translation import gettext_lazy

from pretix.base.plugins import PluginConfig
from pretix.base.plugins import PLUGIN_LEVEL_EVENT

from . import __version__


class PluginApp(PluginConfig):
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
        compatibility = "2026.2.0"
        level = PLUGIN_LEVEL_EVENT

    def ready(self):
        from . import signals  # NOQA
