/** @odoo-module **/
import { Component, onMounted, onWillUnmount, useState, onWillUpdateProps } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { registry } from "@web/core/registry";
import { loadJS } from "@web/core/assets";
import { rpc } from "@web/core/network/rpc";
import { session } from "@web/session";
import { CompanySelector  } from "@web/webclient/switch_company_menu/switch_company_menu";

export class Dashboard extends Component {
    static props = ["filter", "resetFilter"];
    setup() {
        debugger
        this.companyService = useService("company");
        this.state = useState({
            inflow: 0,
            outflow: 0,
            dif: 0,
        });
        this.lineChart = null;
        this.lineBarChart = null;

        onMounted(async () => {
            const inflow = await rpc("/overview/get_cash_inflow", {
                active_company: this.companyService.activeCompanyIds,
            });
            this.state.inflow = inflow.amount.toLocaleString("vi-VN");
            const outflow = await rpc("/overview/get_cash_outflow", {
                active_company: this.companyService.activeCompanyIds,
            });
            this.state.outflow = outflow.amount.toLocaleString("vi-VN");
            const dif = inflow.amount - outflow.amount;
            this.state.dif = dif.toLocaleString("vi-VN");
            await loadJS("https://cdn.jsdelivr.net/npm/echarts/dist/echarts.min.js");
            const in_out_year = await rpc("/overview/get_in_out_year", {
                active_company: this.companyService.activeCompanyIds,
            });
            const lineDom = document.getElementById("lineChart");
            if (lineDom) {
                this.lineChart = echarts.init(lineDom, null, { renderer: "svg" });
                this.lineChart.setOption({
                    title: {
                        text: "Thu - Chi lũy kế năm",
                        left: 10,
                        top: 10,
                        textStyle: {
                            fontFamily: "Lexend Deca, sans-serif",
                            fontWeight: 600,
                            fontSize: 20,
                        }
                    },
                    tooltip: { trigger: "axis" },
                    legend: {
                        data: [
                            { name: "Tiền Thu", icon: "circle" },
                            { name: "Tiền Chi", icon: "circle" }
                        ],
                        itemWidth: 12,
                        itemHeight: 12,
                        itemGap: 20,
                        textStyle: {
                            fontSize: 16,
                            color: "#323232",
                            fontWeight: 500,
                            fontFamily: "Lexend Deca, sans-serif",
                        }
                    },
                    xAxis: {
                        type: "category",
                        data: in_out_year.labels
                    },
                    yAxis: {
                        type: "value",
                        min: 0
                    },
                    series: [
                        {
                            name: "Tiền Thu",
                            type: "line",
                            data: in_out_year.inflow,
                            showSymbol: false,
                            lineStyle: { color: "#3941AB", width: 2 },
                            itemStyle: { color: "#3941AB" },
                            areaStyle: {
                                color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                                    { offset: 0, color: "rgba(57, 65, 171, 0.2)" },
                                    { offset: 1, color: "rgba(57, 65, 171, 0)" }
                                ])
                            }
                        },
                        {
                            name: "Tiền Chi",
                            type: "line",
                            data: in_out_year.outflow,
                            showSymbol: false,
                            lineStyle: { color: "#E83E3C", width: 2 },
                            itemStyle: { color: "#E83E3C" },
                            areaStyle: {
                                color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                                    { offset: 0, color: "rgba(232, 62, 60, 0.2)" },
                                    { offset: 1, color: "rgba(232, 62, 60, 0)" }
                                ])
                            }
                        }
                    ],
                });
            }
            const in_out_year_by_m = await rpc("/overview/get_in_out_year_by_m", {
                active_company: this.companyService.activeCompanyIds,
            });
            const lineBarChartDom = document.getElementById("lineBarChart");
            if (lineBarChartDom) {
                this.lineBarChart = echarts.init(lineBarChartDom, null, { renderer: "svg" });
                this.lineBarChart.setOption({
                    title: {
                        text: "Tiền thu và tiền chi theo tháng",
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
                        data: [
                            {
                                name: 'Tiền Thu',
                                icon:'circle'
                            },
                            {
                                name: 'Tiền Chi',
                                icon: 'path://M2 5H18 M10 10C8.67413 10 7.40255 9.47339 6.46491 8.53598C5.52726 7.59856 5.00033 6.32712 5 5.00125C4.99967 3.67538 5.52596 2.40367 6.46314 1.46579C7.40032 0.527912 8.67163 0.000663559 9.9975 0 C11.3234 -0.000662307 12.5952 0.525314 13.5333 1.46226C14.4714 2.3992 14.999 3.67038 15 4.99625C15.001 6.32212 14.4753 7.59409 13.5386 8.53244C12.6019 9.47079 11.3309 9.99867 10.005 10L10 10Z'
                            }
                        ],
                        itemWidth: 12,
                        itemHeight: 12,
                        itemGap: 20,
                        textStyle: {
                            fontSize: 16,
                            color: "#323232",
                            fontWeight: 500,
                            fontFamily: "Lexend Deca, sans-serif",
                        }
                    },
                    xAxis: { type: "category", data: in_out_year_by_m.labels },
                    yAxis: { type: "value" },
                    series: [
                        {
                            name: "Tiền Thu",
                            type: "bar",
                            data: in_out_year_by_m.inflow,
                            itemStyle: { color: "#3941AB" },
                        },
                        {
                            name: "Tiền Chi",
                            type: "line",
                            smooth: true,
                            showSymbol: true,
                            symbol: 'circle',
                            symbolSize: 8,
                            data: in_out_year_by_m.outflow,
                            lineStyle: { color: "#E83E3C", width: 2 },
                            itemStyle: {
                                color: "#E83E3C",    // fill màu tròn
                                borderColor: "#E83E3C", // viền tròn
                                borderWidth: 1
                            },
                        },
                    ],
                });
            }
            this._resizeHandler = () => {
                this.lineChart?.resize();
                this.lineBarChart?.resize();
            };
            window.addEventListener("resize", this._resizeHandler);
        });
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
            // cleanup charts
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
    }
    async loadData(filter) {
        debugger
        const rawInflow = await rpc("/overview/get_cash_inflow", {
            filter,
            active_company: this.companyService.activeCompanyIds,
        });
        const rawOutflow = await rpc("/overview/get_cash_outflow", {
            filter,
            active_company: this.companyService.activeCompanyIds,
        });

        const rawInOutYearByM = await rpc("/overview/get_in_out_year_by_m", {
            filter,
            active_company: this.companyService.activeCompanyIds,
        });

        this.state.inflow = rawInflow.amount.toLocaleString("vi-VN");
        this.state.outflow = rawOutflow.amount.toLocaleString("vi-VN");
        if (this.lineBarChart) {
            this.lineBarChart.setOption({
                xAxis: { data: rawInOutYearByM.labels },
                series: [
                    { name: "Tiền Thu", data: rawInOutYearByM.inflow },
                    { name: "Tiền Chi", data: rawInOutYearByM.outflow },
                ],
            });
        }
    }
}

Dashboard.template = "cash.DashboardTemplate";
