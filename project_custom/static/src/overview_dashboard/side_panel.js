/** @odoo-module **/

import { Component, useState, onMounted, useRef, onWillUnmount, onWillUpdateProps } from "@odoo/owl";
import { useBus, useService } from "@web/core/utils/hooks";
import { loadJS, loadCSS } from "@web/core/assets";
import { CompanySelector  } from "@web/webclient/switch_company_menu/switch_company_menu";
import { isMobileOS } from "@web/core/browser/feature_detection";

export class SidePanel extends Component {
    static template = "cash.SidePanelTemplate";
    static props = ["filter", "onApply", "type_dboard"];
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
        this.notification = useService("notification");
        this.isMobileOS = isMobileOS();
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
            let debounceTimer = null;
            await loadCSS("https://cdn.jsdelivr.net/npm/flatpickr/dist/flatpickr.min.css");
            await loadJS("https://cdn.jsdelivr.net/npm/flatpickr");
            flatpickr(this.dateFromRef.el, {
                dateFormat: "d/m/Y",
                allowInput: !this.isMobileOS ? true : false,
                disableMobile: true,
                onChange: (selectedDates, dateStr) => {
                    this.state.selected.date_from = dateStr;
                    if (this.isMobileOS){
                        triggerDebounce();
                    }
                },
            });
            this.dateFromRef.el.addEventListener("input", (ev) => {
                this.state.selected.date_from = ev.target.value || null;
            });
            flatpickr(this.dateToRef.el, {
                dateFormat: "d/m/Y",
                allowInput: !this.isMobileOS ? true : false,
                disableMobile: true,
                onChange: (selectedDates, dateStr) => {
                    this.state.selected.date_to = dateStr;
                    if (this.isMobileOS){
                        triggerDebounce();
                    }
                },
            });
            this.dateToRef.el.addEventListener("input", (ev) => {
                this.state.selected.date_to = ev.target.value || null;
            });
            const triggerDebounce = () => {
                clearTimeout(debounceTimer);
                debounceTimer = setTimeout(() => {
                    const { date_from, date_to } = this.state.selected;
                    if (date_from && date_to) {
                        this.applyFilter();
                    }
                }, 2000);
            };
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

        if (!date_from || !date_to) {
            this.showNotification("Vui lòng chọn đầy đủ ngày bắt đầu và ngày kết thúc!");
            return;
        }
        const formatToMDY = (dateStr) => {
            const [d, m, y] = dateStr.split("/");
            return `${m}/${d}/${y}`;
        };
        const fromDate = new Date(formatToMDY(date_from));
        const toDate = new Date(formatToMDY(date_to));
        if (isNaN(fromDate) || isNaN(toDate)) {
            this.showNotification("Định dạng ngày không hợp lệ!");
            return;
        }
        if (fromDate > toDate) {
            this.showNotification("Ngày bắt đầu không được lớn hơn ngày kết thúc!");
            return;
        }
        this.props.onApply({
            date_from: this.convertDateFormat(date_from),
            date_to: this.convertDateFormat(date_to),
        });
    }
    showNotification(message) {
        if (this.env?.services?.notification) {
            this.env.services.notification.add(message, { type: "danger" });
        } else {
            alert(message);
        }
    }

}
