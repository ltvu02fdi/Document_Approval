/** @odoo-module **/
import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { SidePanel } from "./side_panel";
import { Dashboard } from "./dashboard";
import { DashboardInflow } from "./dashboard_inflow";

export class MainLayout extends Component {
    static components = { SidePanel, Dashboard, DashboardInflow };
    static template = "my_module.MainLayoutTemplate";
    setup() {
        this.state = useState({
            filter: { date_from: null, date_to: null },
            type_dboard: this.props.action.context.type_dashboard,
        });
        this.updateFilter = (newFilter) => {
            this.state.filter = newFilter;
        };
        this.resetFilter = () => {
            this.state.filter = { date_from: null, date_to: null };
        };
    }
}

registry.category("actions").add("cash.main_layout_action", MainLayout);
