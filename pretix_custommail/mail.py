import bleach
import css_inline
from django.conf import settings
from django.template.loader import get_template
from django.utils.translation import get_language, gettext_lazy as _

from pretix.base.email import TemplateBasedMailRenderer
from pretix.base.templatetags.rich_text import (
    DEFAULT_CALLBACKS,
    EMAIL_RE,
    URL_RE,
    abslink_callback,
    markdown_compile_email,
    truelink_callback,
)
from pretix.helpers.format import FormattedString, SafeFormatter, format_map
from pretix.multidomain.urlreverse import build_absolute_uri

from .settings import get_custommail_settings


class CustomMailRenderer(TemplateBasedMailRenderer):
    verbose_name = _("Custom branded")
    identifier = "pretix_custommail"
    thumbnail_filename = "pretix_custommail/email/thumb.svg"
    template_name = "pretix_custommail/email/custommail.html"

    def compile_markdown(self, plaintext, context=None):
        return markdown_compile_email(plaintext, context=context)

    def _cta_for_order(self, order):
        if not order or not self.event:
            return None
        return build_absolute_uri(
            self.event,
            "presale:event.order.open",
            kwargs={
                "order": order.code,
                "secret": order.secret,
                "hash": order.email_confirm_secret(),
            },
        )

    def render(self, plain_body, plain_signature, subject, order=None, position=None, context=None):
        apply_format_map = not isinstance(plain_body, FormattedString)
        body_md = self.compile_markdown(plain_body, context)
        if context:
            linker = bleach.Linker(
                url_re=URL_RE,
                email_re=EMAIL_RE,
                callbacks=DEFAULT_CALLBACKS + [truelink_callback, abslink_callback],
                parse_email=True,
            )
            if apply_format_map:
                body_md = format_map(
                    body_md,
                    context=context,
                    mode=SafeFormatter.MODE_RICH_TO_HTML,
                    linkifier=linker,
                )

        htmlctx = {
            "site": settings.PRETIX_INSTANCE_NAME,
            "site_url": settings.SITE_URL,
            "body": body_md,
            "subject": str(subject),
            "rtl": get_language() in settings.LANGUAGES_RTL
            or get_language().split("-")[0] in settings.LANGUAGES_RTL,
        }

        if self.organizer:
            htmlctx["organizer"] = self.organizer

        if self.event:
            htmlctx["event"] = self.event

        if plain_signature:
            signature_md = plain_signature.replace("\n", "<br>\n")
            signature_md = self.compile_markdown(signature_md)
            htmlctx["signature"] = signature_md

        if order:
            htmlctx["order"] = order

        if position:
            htmlctx["position"] = position

        event_or_subevent = None
        if position and getattr(position, "subevent", None):
            event_or_subevent = position.subevent
        elif self.event:
            event_or_subevent = self.event

        if event_or_subevent:
            htmlctx["event_or_subevent"] = event_or_subevent
            htmlctx["event_date"] = (
                event_or_subevent.get_date_from_display()
                if hasattr(event_or_subevent, "get_date_from_display")
                else ""
            )
            htmlctx["event_location"] = str(event_or_subevent.location or "")

        brand = get_custommail_settings(event=self.event, organizer=self.organizer)
        htmlctx.update(
            {
                "brand_name": brand.get("brand_name"),
                "support_email": brand.get("support_email"),
                "logo_url": brand.get("logo_url"),
                "primary_color": brand.get("primary_color"),
                "secondary_color": brand.get("secondary_color"),
                "cta_text": brand.get("cta_text"),
                "footer_text": brand.get("footer_text", "").format(
                    brand_name=brand.get("brand_name")
                ),
                "footer_links": brand.get("footer_links", []),
                "cta_url": self._cta_for_order(order),
            }
        )

        highlight_items = []
        if order:
            highlight_items.append({"label": _("Order code"), "value": order.code})
        if event_or_subevent:
            highlight_items.append(
                {"label": _("Event"), "value": event_or_subevent.name}
            )
        if htmlctx.get("event_date"):
            highlight_items.append(
                {"label": _("Date"), "value": htmlctx["event_date"]}
            )
        if htmlctx.get("event_location"):
            highlight_items.append(
                {"label": _("Location"), "value": htmlctx["event_location"]}
            )
        htmlctx["highlight_items"] = highlight_items

        tpl = get_template(self.template_name)
        body_html = tpl.render(htmlctx)

        inliner = css_inline.CSSInliner(keep_style_tags=False)
        body_html = inliner.inline(body_html)

        return body_html
