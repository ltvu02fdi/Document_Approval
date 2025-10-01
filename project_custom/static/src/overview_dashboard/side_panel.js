/** @odoo-module **/

import { Component, useState, onMounted, useRef, onWillUnmount, onWillUpdateProps } from "@odoo/owl";
import { useBus } from "@web/core/utils/hooks";
import { loadJS, loadCSS } from "@web/core/assets";
import { CompanySelector  } from "@web/webclient/switch_company_menu/switch_company_menu";


export class SidePanel extends Component {
    static template = "my_module.SidePanelTemplate";
    static props = ["filter", "onApply"];
    convertDateFormat(dateStr) {
        if (!dateStr) return null;
        const parts = dateStr.split("/");
        if (parts.length === 3) {
            const [day, month, year] = parts;
            return `${year}-${month.padStart(2, "0")}-${day.padStart(2, "0")}`;
        }
        return null;
    }
    setup() {
        this.state = useState({
            selected: {
                date_from: null,
                date_to: null,
            },
        });

        this.dateFromRef = useRef("dateFrom");
        this.dateToRef = useRef("dateTo");
        this.fpInstances = {};

        onMounted(async () => {
            await loadCSS("https://cdn.jsdelivr.net/npm/flatpickr/dist/flatpickr.min.css");
            await loadJS("https://cdn.jsdelivr.net/npm/flatpickr");
            flatpickr(this.dateFromRef.el, {
                dateFormat: "d/m/Y",
                allowInput: true,
                onChange: (selectedDates, dateStr) => {
                    this.state.selected.date_from = dateStr;
                },
            });
            this.dateFromRef.el.addEventListener("input", (ev) => {
                this.state.selected.date_from = ev.target.value || null;
            });
            flatpickr(this.dateToRef.el, {
                dateFormat: "d/m/Y",
                allowInput: true,
                onChange: (selectedDates, dateStr) => {
                    this.state.selected.date_to = dateStr;
                },
            });
            this.dateToRef.el.addEventListener("input", (ev) => {
                this.state.selected.date_to = ev.target.value || null;
            });
        });
        onWillUnmount(() => {
            if (this.fpInstances.dateFrom) {
                this.fpInstances.dateFrom.destroy();
            }
            if (this.fpInstances.dateTo) {
                this.fpInstances.dateTo.destroy();
            }
        });
        onWillUpdateProps((newProps) => {
            if (!newProps.filter?.date_from && !newProps.filter?.date_to) {
                this.state.selected.date_from = null;
                this.state.selected.date_to = null;
                if (this.fpInstances.dateFrom) {
                    this.fpInstances.dateFrom.clear();
                }
                if (this.fpInstances.dateTo) {
                    this.fpInstances.dateTo.clear();
                }
                this.dateFromRef.el.value = "";
                this.dateToRef.el.value = "";
            }
        });
    }
    onClickCalendar(){
        this.dateFromRef.el.click();
    }
    onClickCalendarDateTo(){
        this.dateToRef.el.click();
    }
    applyFilter() {
        const { date_from, date_to } = this.state.selected;
        this.props.onApply({
            date_from: this.convertDateFormat(date_from),
            date_to: this.convertDateFormat(date_to),
        });
    }
}
