/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { AppsMenu } from "@web_responsive/components/apps_menu/apps_menu.esm";
import {useState} from "@odoo/owl";
import {session} from "@web/session";
import {useBus, useService} from "@web/core/utils/hooks";
import {browser} from "@web/core/browser/browser";
import {user} from "@web/core/user";


patch(AppsMenu.prototype, {
 setup() {
        super.setup();
        this.state = useState({open: false});
        this.theme = session.apps_menu.theme || "milk";
        this.menuService = useService("menu");
        browser.localStorage.setItem("redirect_menuId", "");
        if (user.context.is_redirect_to_home) {
            this.router = router;
            const menuId = Number(this.router.current.menu_id || 0);
            this.state = useState({open: menuId === 0});
        }
        useBus(this.env.bus, "ACTION_MANAGER:UI-UPDATED", () => {
            this.setOpenState(false);
        });
        useBus(this.env.bus, "APPS_MENU:ON_CLICK", () => {
            this.onMenuClick();
        });
        this._setupKeyNavigation();
    }
});
