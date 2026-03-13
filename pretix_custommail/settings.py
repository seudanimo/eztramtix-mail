from copy import deepcopy

from django.conf import settings as django_settings


DEFAULTS = {
    "brand_name": "Your Brand",
    "support_email": "support@example.com",
    "logo_url": "",
    "primary_color": "#1E2A32",
    "secondary_color": "#F2F3F5",
    "cta_text": "Ver pedido",
    "footer_text": "Gracias por confiar en {brand_name}.",
    "footer_links": [],
}


SETTINGS_KEY = "PRETIX_CUSTOMMAIL_SETTINGS"


def _coalesce_setting(store, key):
    if not store:
        return None
    value = store.get(key)
    if value is None:
        return None
    return value


def get_custommail_settings(event=None, organizer=None):
    cfg = deepcopy(DEFAULTS)

    overrides = getattr(django_settings, SETTINGS_KEY, {})
    if isinstance(overrides, dict):
        cfg.update(overrides)

    if organizer is not None:
        cfg.update(
            {
                k: v
                for k, v in {
                    "brand_name": _coalesce_setting(organizer.settings, "custommail_brand_name"),
                    "support_email": _coalesce_setting(organizer.settings, "custommail_support_email"),
                    "logo_url": _coalesce_setting(organizer.settings, "custommail_logo_url"),
                    "primary_color": _coalesce_setting(organizer.settings, "custommail_primary_color"),
                    "secondary_color": _coalesce_setting(organizer.settings, "custommail_secondary_color"),
                    "cta_text": _coalesce_setting(organizer.settings, "custommail_cta_text"),
                    "footer_text": _coalesce_setting(organizer.settings, "custommail_footer_text"),
                    "footer_links": _coalesce_setting(organizer.settings, "custommail_footer_links"),
                }.items()
                if v is not None
            }
        )

    if event is not None:
        cfg.update(
            {
                k: v
                for k, v in {
                    "brand_name": _coalesce_setting(event.settings, "custommail_brand_name"),
                    "support_email": _coalesce_setting(event.settings, "custommail_support_email"),
                    "logo_url": _coalesce_setting(event.settings, "custommail_logo_url"),
                    "primary_color": _coalesce_setting(event.settings, "custommail_primary_color"),
                    "secondary_color": _coalesce_setting(event.settings, "custommail_secondary_color"),
                    "cta_text": _coalesce_setting(event.settings, "custommail_cta_text"),
                    "footer_text": _coalesce_setting(event.settings, "custommail_footer_text"),
                    "footer_links": _coalesce_setting(event.settings, "custommail_footer_links"),
                }.items()
                if v is not None
            }
        )

    return cfg
