/** @odoo-module **/
import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { SidePanel } from "./side_panel";
import { Dashboard } from "./dashboard";

export class MainLayout extends Component {
    static components = { SidePanel, Dashboard };
    static template = "my_module.MainLayoutTemplate";
    setup() {
        this.state = useState({
            filter: { date_from: null, date_to: null }
        });
        this.updateFilter = (newFilter) => {
            this.state.filter = newFilter;
        };
        this.resetFilter = () => {
            this.state.filter = { date_from: null, date_to: null };
        };
    }
}

registry.category("actions").add("my_module.main_layout_action", MainLayout);
