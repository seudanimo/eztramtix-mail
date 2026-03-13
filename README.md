# pretix_custommail

Plugin de pretix para renderizar emails HTML con branding completo y una plantilla moderna, elegante y altamente editable.

## Caracteristicas

- Renderer HTML basado en `TemplateBasedMailRenderer`.
- Plantilla responsive con tarjeta central, boton CTA, cabecera, pie y caja de resumen.
- Logo, colores y textos configurables desde un solo lugar.
- Placeholders personalizados para branding y datos clave.
- Compatible con la arquitectura oficial de plugins de pretix.

## Estructura

- Renderer: `pretix_custommail/mail.py`
- Placeholders: `pretix_custommail/placeholders.py`
- Plantilla: `pretix_custommail/templates/pretix_custommail/email/custommail.html`
- Thumbnail: `pretix_custommail/static/pretix_custommail/email/thumb.svg`

## Instalacion (desarrollo o produccion)

1. Clona el repo:

```bash
git clone https://github.com/tu-org/pretix_custommail.git
cd pretix_custommail
```

2. Instala el plugin en el entorno de pretix:

```bash
pip install -e .
```

3. Reinicia pretix (web y worker) para que cargue el plugin.

## Habilitar el plugin

1. En el panel de pretix, ve a **Ajustes del evento** o **Ajustes del organizador** -> **Plugins**.
2. Activa **Custom HTML email renderer**.

## Seleccionar el renderer

1. En el panel del evento, ve a **Ajustes** -> **Emails**.
2. En **HTML email renderer**, selecciona **Custom branded**.
3. Guarda.

## Configuracion rapida (sin UI)

Este MVP usa un diccionario central en Django settings. Agrega en tu configuracion de pretix:

```python
PRETIX_CUSTOMMAIL_SETTINGS = {
    "brand_name": "Tu Marca",
    "support_email": "soporte@tu-marca.com",
    "logo_url": "https://tu-marca.com/logo.png",
    "primary_color": "#1E2A32",
    "secondary_color": "#F2F3F5",
    "cta_text": "Ver pedido",
    "footer_text": "Gracias por confiar en {brand_name}.",
    "footer_links": [
        {"label": "Ayuda", "url": "https://tu-marca.com/ayuda"},
        {"label": "Politica", "url": "https://tu-marca.com/legal"},
    ],
}
```

Opcionalmente, puedes sobreescribir por organizador o evento usando el settings store de pretix:

```
custommail_brand_name
custommail_support_email
custommail_logo_url
custommail_primary_color
custommail_secondary_color
custommail_cta_text
custommail_footer_text
custommail_footer_links
```

Nota: no hay interfaz grafica incluida para estos campos en este MVP. Puedes agregarla luego via un formulario de settings del plugin.

## Placeholders

### Nuevos placeholders del plugin

- `{order_code}`: alias del codigo de pedido.
- `{event_name}`: nombre del evento o subevento.
- `{event_date}`: fecha mostrada por pretix (`get_date_from_display`).
- `{custom_support_email}`: email de soporte del branding.
- `{custom_brand_name}`: nombre de marca del branding.

### Placeholders ya existentes en pretix (no duplicados)

- `{code}`: codigo de pedido (nativo).
- `{event}` / `{event_or_subevent}`: nombre del evento (nativo).
- `{event_location}`: ubicacion del evento (nativo).
- `{url}` / `{url_button}`: enlace y boton a detalles del pedido (nativo).

Si prefieres evitar aliases, puedes usar directamente los placeholders nativos.

## Editar HTML y estilos

La plantilla principal esta en:

- `pretix_custommail/templates/pretix_custommail/email/custommail.html`

Todo el CSS esta en linea o en un bloque `@media` para que el inliner de pretix lo convierta a estilos compatibles con clientes de email.
Puedes modificar colores, tipografias y estructura sin tocar el renderer.

## Notas de compatibilidad

- El renderer usa `css_inline` igual que los renderers oficiales de pretix.
- El HTML esta optimizado para clientes de correo comunes (tables + inline styles).
- El CTA se genera automaticamente si hay `order` en el contexto.

## Como evolucionar a UI en el panel

Para convertir la configuracion en UI:

1. Define campos en `pretix.base.settings` (via `register_global_settings` o settings de evento).
2. Crea un formulario y vista en el plugin.
3. Lee esos valores desde `event.settings` u `organizer.settings`.

El codigo ya tiene hooks para leer estos valores si existen.

## Desarrollo

```bash
pip install -e .
```

## Licencia

MIT
