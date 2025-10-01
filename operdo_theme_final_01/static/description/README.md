# operdo_theme_final_01

**Unified Operdo theme**: gradient navbar, logo badge (high contrast), consistent secondary menu colors, app switcher styling, and PWA assets (manifest + icons).

## Install
1) Copy to addons: `/odoo/custom/addons/operdo_theme_final_01`
2) Restart Odoo → Update Apps → Install **operdo_theme_final_01**
3) Hard refresh browser (Ctrl+F5)

## Favicon & Manifest
- Nginx:
```
location = /favicon.ico { alias /odoo/custom/addons/operdo_theme_final_01/static/description/icon_32.png; }
location = /apple-touch-icon.png { alias /odoo/custom/addons/operdo_theme_final_01/static/description/icon_180.png; }
location = /manifest.webmanifest { alias /odoo/custom/addons/operdo_theme_final_01/static/description/manifest.webmanifest; }
```
- Or Odoo Website → Settings → Favicon (upload `icon_180.png`) + HTML Head Snippet:
```
<link rel="manifest" href="/operdo_theme_final_01/static/description/manifest.webmanifest">
<link rel="icon" sizes="32x32" href="/operdo_theme_final_01/static/description/icon_32.png">
```