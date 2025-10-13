/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

export class AutoPagedSearchableCardList extends Component {
    setup() {
        this.state = useState({
            items: [],
            currentPage: 1,
            searchQuery: "",
        });

        // Dữ liệu demo
        this.state.items = [
            { id: 1, title: "Báo cáo tài chính", description: "Chi tiết báo cáo tháng 9" },
            { id: 2, title: "Tổng hợp thu chi", description: "Dữ liệu 2025" },
            { id: 3, title: "Chi phí văn phòng", description: "Chi tiết hóa đơn" },
            { id: 4, title: "Doanh thu quý 3", description: "Cập nhật mới nhất" },
            { id: 5, title: "Báo cáo tồn kho", description: "Kho hàng chính" },
            { id: 6, title: "Lương nhân viên", description: "Chi tiết tháng 8" },
            { id: 7, title: "Kế hoạch ngân sách", description: "Dự toán 2026" },
        ];

        this.maxPerPage = this.props.max_cards_per_page || 3;
    }

    get filteredItems() {
        debugger
        const query = this.state.searchQuery.toLowerCase().trim();
        if (!query) return this.state.items;
        return this.state.items.filter(item =>
            item.title.toLowerCase().includes(query)
        );
    }
    get paginatedItems() {
        const start = (this.state.currentPage - 1) * this.maxPerPage;
        return this.filteredItems.slice(start, start + this.maxPerPage);
    }
    get totalPages() {
        return Math.ceil(this.filteredItems.length / this.maxPerPage) || 1;
    }

    changePage(page) {
        if (page >= 1 && page <= this.totalPages) {
            this.state.currentPage = page;
        }
    }

    onSearchInput(ev) {
        this.state.searchQuery = ev.target.value;
        this.state.currentPage = 1; // Reset về trang đầu khi tìm
    }
}

AutoPagedSearchableCardList.template = "my_module.AutoPagedSearchableCardListTemplate";
