/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { NavBar } from "@web/webclient/navbar/navbar";

patch(NavBar.prototype, {
    logoClick() {
        this.env.bus.trigger("APPS_MENU:ON_CLICK");
    },
});
