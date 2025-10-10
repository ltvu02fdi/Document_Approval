/** @odoo-module **/
import { Component, onMounted, onWillUnmount, useState, onWillUpdateProps, useRef } from "@odoo/owl";
import { isMobileOS } from "@web/core/browser/feature_detection";
import { useService } from "@web/core/utils/hooks";
import { registry } from "@web/core/registry";
import { loadJS, loadCSS } from "@web/core/assets";
import { rpc } from "@web/core/network/rpc";
import { session } from "@web/session";
import { CompanySelector  } from "@web/webclient/switch_company_menu/switch_company_menu";

export class DashboardOutflow extends Component {
    static props = ["filter", "resetFilter"];
    setup() {
        this.isMobileOS = isMobileOS();
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
            const inflow = await rpc("/overview/get_cash_outflow_current_week", {
                active_company: this.companyService.activeCompanyIds,
            });
            this.state.inflow = inflow.amount.toLocaleString("vi-VN");
            const inflow_from_first_m = await rpc("/overview/get_cash_outflow_last_week", {
                active_company: this.companyService.activeCompanyIds,
            });
            this.state.inflow_from_first_m = inflow_from_first_m.amount.toLocaleString("vi-VN");
            const dif = await rpc("/overview/get_dif_filter", {
                active_company: this.companyService.activeCompanyIds,
            });
            this.state.dif = dif.amount.toLocaleString("vi-VN");
            const in_out_year_by_m = await rpc("/overview/get_in_out_year_by_m", {
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
                            fontSize: !this.isMobileOS ? 20 : 16,
                            color: "#323232"
                        }
                    },
                    tooltip: { trigger: "axis" },
                    legend: {
                        show: false,
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
                    ],
                });
            }
            const top_5_inflow = await rpc("/overview/get_top5_outflow", {
                active_company: this.companyService.activeCompanyIds,
            });
            const labels = top_5_inflow.map(item => item.partner_name);
            const amounts = top_5_inflow.map(item => item.amount);
            // Donut chart
            const donutDom = document.getElementById("donutTop5Inflow");
            if (donutDom) {
                this.donutChart = echarts.init(donutDom, null, { renderer: "svg" });
                this.donutChart.setOption({
                    title: {
                        text: "Top 5 tiền chi theo danh  mục",
                        left: 10,
                        top: 10,
                        textStyle: {
                            fontFamily: "Lexend Deca, sans-serif",
                            fontWeight: 600,
                            fontSize: !this.isMobileOS ? 20 : 16,
                            color: "#323232",
                        },
                    },
                    tooltip: {
                        trigger: "item",
                        formatter: params => {
                            return `${params.value.toLocaleString("vi-VN")}`;
                        },
                        backgroundColor: "rgba(255,255,255,0.95)",
                        borderColor: "#ccc",
                        borderWidth: 1,
                        padding: 10,
                        textStyle: {
                            color: "#333",
                            fontSize: 14,
                            fontFamily: "Lexend Deca, sans-serif",
                            fontWeight: 500,
                        },
                    },
                    legend: this.isMobileOS
                        ? {
                            orient: "horizontal",
                            bottom: 0,
                            data: labels,
                            icon: "circle",
                            itemWidth: 10,
                            itemHeight: 10,
                            textStyle: {
                                fontFamily: "Lexend Deca, sans-serif",
                                fontWeight: 600,
                                fontSize: 12,
                                color: "#333",
                            },
                        }
                        : [
                            {
                                orient: "vertical",
                                left: "30%",
                                bottom: -4,
                                data: labels.slice(0, 3),
                                icon: "circle",
                                itemWidth: 10,
                                itemHeight: 10,
                                textStyle: {
                                    fontFamily: "Lexend Deca, sans-serif",
                                    fontWeight: 600,
                                    fontSize: 12,
                                    color: "#333",
                                },
                            },
                            {
                                orient: "vertical",
                                left: "60%",
                                bottom: -4,
                                data: labels.slice(3),
                                icon: "circle",
                                itemWidth: 10,
                                itemHeight: 10,
                                textStyle: {
                                    fontFamily: "Lexend Deca, sans-serif",
                                    fontWeight: 600,
                                    fontSize: 12,
                                    color: "#333",
                                },
                            },
                        ],
                    color: ["#9B51E0", "#56CA00", "#16B1FF", "#FF4C51", "#FFB400"],
                    series: [
                        {
                            name: "Top 5 Inflow",
                            type: "pie",
                            radius: ["40%", "70%"],
                            avoidLabelOverlap: false,
                            label: {
                                show: false,
                                position: "center"
                            },
                            emphasis: {
                            label: {
                                    show: false,
                                  }
                            },
                            labelLine: { show: false },
                            data: labels.map((label, i) => ({
                                name: label,
                                value: amounts[i],
                            })),
                        }
                    ]
                });
            }
            const data = await rpc("/overview/get_inflow_table",{
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
            if (this.lineChartInflow) {
                this.lineChartInflow.dispose();
                this.lineChartInflow = null;
            }
            if (this.donutChart) {
                this.donutChart.dispose();
                this.donutChart = null;
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
        const dif_new = await rpc("/overview/get_dif_filter", {
            filter,
            active_company: this.companyService.activeCompanyIds,
        });
        this.state.dif = dif_new.amount.toLocaleString("vi-VN");
        const in_out_year_by_m_new = await rpc("/overview/get_in_out_year_by_m", {
            filter,
            active_company: this.companyService.activeCompanyIds,
        });
        const top_5_inflow_new = await rpc("/overview/get_top5_inflow", {
            filter,
            active_company: this.companyService.activeCompanyIds,
        });
        const labels_new = top_5_inflow_new.map(item => item.partner_name);
        const amounts_new = top_5_inflow_new.map(item => item.amount);
        const data_new = await rpc("/overview/get_inflow_table",{
            filter,
            active_company: this.companyService.activeCompanyIds,
        });
        if (this.lineChartInflow) {
            this.lineChartInflow.setOption({
                xAxis: { type: "category", data: in_out_year_by_m_new.labels },
                series: [
                        {
                            name: "Tiền Thu",
                            type: "bar",
                            data: in_out_year_by_m_new.inflow,
                            itemStyle: { color: "#3941AB" },
                        },
                    ],
            })
        }
        if(this.donutChart){
            this.donutChart.setOption({
                tooltip: {
                    trigger: "item",
                    formatter: params => {
                        return `${params.name}: ${params.value.toLocaleString("vi-VN")}`;
                    },
                    backgroundColor: "rgba(255,255,255,0.95)",
                    borderColor: "#ccc",
                    borderWidth: 1,
                    padding: 10,
                    textStyle: {
                        color: "#333",
                        fontSize: 14,
                        fontFamily: "Lexend Deca, sans-serif",
                        fontWeight: 500,
                    },
                },
                legend: [
                    {
                        orient: "vertical",
                        left: "30%",
                        bottom: -4,
                        data: labels_new.slice(0, 3),
                        icon: "circle",
                        itemWidth: 10,
                        itemHeight: 10,
                        textStyle: {
                            fontFamily: "Lexend Deca, sans-serif",
                            fontWeight: 600,
                            fontSize: 12,
                            color: "#333",
                        }
                    },
                    {
                        orient: "vertical",
                        left: "60%",
                        bottom: -4,
                        data: labels_new.slice(3),
                        icon: "circle",
                        itemWidth: 10,
                        itemHeight: 10,
                        textStyle: {
                            fontFamily: "Lexend Deca, sans-serif",
                            fontWeight: 600,
                            fontSize: 12,
                            color: "#333",
                        }
                    }
                ],
                series: [
                    {
                        name: "Top 5 Inflow",
                        type: "pie",
                        radius: ["40%", "70%"],
                        avoidLabelOverlap: false,
                        label: {
                            show: false,
                            position: "center"
                        },
                        emphasis: {
                        label: {
                                show: false,
                              }
                        },
                        labelLine: { show: false },
                        data: labels_new.map((label, i) => ({
                            name: label,
                            value: amounts_new[i],
                        })),
                    }
                ]
            });
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

DashboardOutflow.template = "cash.DashboardOutflowTemplate";
