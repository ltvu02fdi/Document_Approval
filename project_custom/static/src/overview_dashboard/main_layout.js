/** @odoo-module **/
import { Component, useState } from "@odoo/owl";
import { isMobileOS } from "@web/core/browser/feature_detection";
import { registry } from "@web/core/registry";
import { SidePanel } from "./side_panel";
import { Dashboard } from "./dashboard";
import { DashboardInflow } from "./dashboard_inflow";
import { DashboardOutflow } from "./dashboard_outflow";
import { DashboardPlannedExpenditure } from "./dashboard_planned_expenditure";

export class MainLayout extends Component {
    static components = { SidePanel, Dashboard, DashboardInflow, DashboardOutflow, DashboardPlannedExpenditure };
    static template = "my_module.MainLayoutTemplate";
    setup() {
        this.isMobileOS = isMobileOS();
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
