/** @odoo-module **/
import { Component, onMounted, onWillUnmount, useState, onWillUpdateProps, useRef } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { registry } from "@web/core/registry";
import { loadJS, loadCSS } from "@web/core/assets";
import { rpc } from "@web/core/network/rpc";
import { session } from "@web/session";
import { CompanySelector  } from "@web/webclient/switch_company_menu/switch_company_menu";

export class DashboardPlannedExpenditure extends Component {
    static props = ["filter", "resetFilter"];
    setup() {
        this.myGridRef = useRef("myGrid");
        this.companyService = useService("company");
        this.state = useState({
            inflow: 0,
            inflow_from_first_m: 0,
            dif: 0,
        });
        onMounted(async () => {
            await loadJS("https://cdn.jsdelivr.net/npm/echarts/dist/echarts.min.js");
            await loadCSS("https://cdn.jsdelivr.net/npm/gridjs/dist/theme/mermaid.min.css");
            await loadJS("https://cdn.jsdelivr.net/npm/gridjs/dist/gridjs.umd.js");
            const inflow = await rpc("/overview/get_planned_current_week", {
                active_company: this.companyService.activeCompanyIds,
            });
            this.state.inflow = inflow.amount.toLocaleString("vi-VN");
            const inflow_from_first_m = await rpc("/overview/get_planned_next_week", {
                active_company: this.companyService.activeCompanyIds,
            });
            this.state.inflow_from_first_m = inflow_from_first_m.amount.toLocaleString("vi-VN");
            const dif = await rpc("/overview/get_dif_filter_expense", {
                active_company: this.companyService.activeCompanyIds,
            });
            this.state.dif = dif.amount.toLocaleString("vi-VN");
            const in_out_year_by_m = await rpc("/overview/get_in_out_year_by_m_expense", {
                active_company: this.companyService.activeCompanyIds,
            });
            //Line chart
            const lineChartInflowDom = document.getElementById("lineChartInflow");
            if (lineChartInflowDom) {
                this.lineChartInflow = echarts.init(lineChartInflowDom, null, { renderer: "svg" });
                this.lineChartInflow.setOption({
                    title: {
                        text: "Tiền chi theo tháng",
                        left: 10,
                        top: 10,
                        textStyle: {
                            fontFamily: "Lexend Deca, sans-serif",
                            fontWeight: 600,
                            fontSize: 20,
                            color: "#323232"
                        }
                    },
                    tooltip: { trigger: "axis" },
                    legend: {
                        show: true,
                        orient: "horizontal",
                        bottom: 0,
                        left: "center",
                        icon: "circle",
                        itemWidth: 10,
                        itemHeight: 10,
                        textStyle: {
                            fontFamily: "Lexend Deca, sans-serif",
                            fontSize: 16,
                            color: "#323232",
                            fontWeight: 500,
                        },
                    },
                    xAxis: { type: "category", data: in_out_year_by_m.labels },
                    yAxis: { type: "value" },
                    series: [
                        {
                            name: "Tiền chi",
                            type: "bar",
                            data: in_out_year_by_m.outflow,
                            itemStyle: { color: "#3941AB" },
                        },
                        {
                            name: "Tiền dự chi",
                            type: "bar",
                            data: in_out_year_by_m.planned,
                            itemStyle: { color: "#A4BCFD" },
                        },
                    ],
                });
            }
            const data = await rpc("/overview/get_planned_table",{
                active_company: this.companyService.activeCompanyIds,
            });
            this.grid = new gridjs.Grid({
                columns: ["Ngày", "Công ty", "Nội dung", "Tiểu mục", "Tiền chi"],
                data: data.map(r => [
                    r.date_entry,
                    r.company_name,
                    r.partner_name,
                    r.category_name,
                    r.amount.toLocaleString("vi-VN"),
                ]),
                pagination: {
                    enabled: true,
                    limit: 5,
                },
                search: false,
                sort: true,
                className: {
                    table: "table table-striped table-hover",
                },
            });

            if (this.myGridRef.el) {
                this.grid.render(this.myGridRef.el);
            }
            this._resizeHandler = () => {
                this.lineChartInflow?.resize();
                this.donutChart?.resize();
            };
            window.addEventListener("resize", this._resizeHandler);
        })
        onWillUpdateProps((newProps) => {
            try {
                document.body.style.cursor = "wait";
                if (newProps.filter.date_from != null && newProps.filter.date_to != null) {
                    this.loadData(newProps.filter).then(() => {
                        if (this.props.resetFilter) {
                            this.props.resetFilter();
                        }
                    });
                }
            } finally {
                document.body.style.cursor = "default";
            }
        });
        onWillUnmount(() => {
            if (this.lineChart) {
                this.lineChart.dispose();
                this.lineChart = null;
            }
            if (this.lineBarChart) {
                this.lineBarChart.dispose();
                this.lineBarChart = null;
            }
            if (this._resizeHandler) {
                window.removeEventListener("resize", this._resizeHandler);
            }
        });
        onWillUnmount(() => {
            if (this.lineChartInflow) {
                this.lineChartInflow.dispose();
                this.lineChartInflow = null;
            }
            if (this.grid) {
                if (this.myGridRef.el) {
                    this.myGridRef.el.innerHTML = "";
                }
                this.grid = null;
            }
            if (this._resizeHandler) {
                window.removeEventListener("resize", this._resizeHandler);
            }
        });
   }
    async loadData(filter) {
        const dif_new = await rpc("/overview/get_dif_filter_expense", {
            filter,
            active_company: this.companyService.activeCompanyIds,
        });
        this.state.dif = dif_new.amount.toLocaleString("vi-VN");
        const in_out_year_by_m_new = await rpc("/overview/get_in_out_year_by_m_expense", {
            filter,
            active_company: this.companyService.activeCompanyIds,
        });
        const data_new = await rpc("/overview/get_planned_table",{
            filter,
            active_company: this.companyService.activeCompanyIds,
        });
        if (this.lineChartInflow) {
            this.lineChartInflow.setOption({
                xAxis: { type: "category", data: in_out_year_by_m_new.labels },
                series: [
                        {
                            name: "Tiền chi",
                            type: "bar",
                            data: in_out_year_by_m_new.outflow,
                            itemStyle: { color: "#3941AB" },
                        },
                        {
                            name: "Tiền dự chi",
                            type: "bar",
                            data: in_out_year_by_m_new.planned,
                            itemStyle: { color: "#A4BCFD" },
                        },
                    ],
            })
        }
        if (this.grid) {
            this.grid.updateConfig({
                data: data_new.map(r => [
                    r.date_entry,
                    r.company_name,
                    r.partner_name,
                    r.category_name,
                    r.amount.toLocaleString("vi-VN"),
                ]),
            }).forceRender();
        }
    }
}

DashboardPlannedExpenditure.template = "cash.DashboardPlannedExpenditureTemplate";
