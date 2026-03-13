from pretix.base.services.placeholders import SimpleFunctionalTextPlaceholder

from .settings import get_custommail_settings


def _event_date(value):
    if hasattr(value, "get_date_from_display"):
        return value.get_date_from_display()
    return ""


def get_placeholders(event):
    return [
        SimpleFunctionalTextPlaceholder(
            "order_code",
            ["order"],
            lambda order: order.code,
            "F8VVL",
        ),
        SimpleFunctionalTextPlaceholder(
            "event_name",
            ["event_or_subevent"],
            lambda event_or_subevent: event_or_subevent.name,
            lambda event: event.name,
        ),
        SimpleFunctionalTextPlaceholder(
            "event_date",
            ["event_or_subevent"],
            lambda event_or_subevent: _event_date(event_or_subevent),
            lambda event: _event_date(event),
        ),
        SimpleFunctionalTextPlaceholder(
            "custom_support_email",
            ["event"],
            lambda event: get_custommail_settings(event=event).get("support_email"),
            lambda event: get_custommail_settings(event=event).get("support_email"),
        ),
        SimpleFunctionalTextPlaceholder(
            "custom_brand_name",
            ["event"],
            lambda event: get_custommail_settings(event=event).get("brand_name"),
            lambda event: get_custommail_settings(event=event).get("brand_name"),
        ),
    ]
