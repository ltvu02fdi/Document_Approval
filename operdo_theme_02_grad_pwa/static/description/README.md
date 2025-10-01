# operdo_theme_02_grad_pwa

- Gradient navbar (#3941AB → #8098F9), list header accent #C7D7FE
- Logo on navbar (background of `.o_menu_brand`)
- PWA assets included: `manifest.webmanifest`, `icon_192.png`, `icon_512.png`, `favicon (32/64/180)`

## Install
- Copy to addons: `/odoo/custom/addons/operdo_theme_02_grad_pwa`
- Restart Odoo → Update Apps → Install
- Hard refresh browser (Ctrl+F5)

## Hook up favicon & manifest
### Option A — Nginx (khuyến nghị)
```
location = /favicon.ico { alias /odoo/custom/addons/operdo_theme_02_grad_pwa/static/description/icon_32.png; }
location = /apple-touch-icon.png { alias /odoo/custom/addons/operdo_theme_02_grad_pwa/static/description/icon_180.png; }
location = /manifest.webmanifest { alias /odoo/custom/addons/operdo_theme_02_grad_pwa/static/description/manifest.webmanifest; }
```
### Option B — Odoo Website
Website → Configuration → Settings → Website Logo & Favicon (upload `icon_180.png`).  
Để manifest: thêm thẻ trong Website → HTML Head Snippets:
```
<link rel="manifest" href="/operdo_theme_02_grad_pwa/static/description/manifest.webmanifest">
<link rel="icon" sizes="32x32" href="/operdo_theme_02_grad_pwa/static/description/icon_32.png">
```