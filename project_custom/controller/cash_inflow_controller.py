# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http
from odoo.http import request

class CashInFlowController(http.Controller):
    @http.route('/overview/get_cash_inflow', type='json', auth='user')
    def get_cash_inflow(self, **kw):
        company_ids = kw.get("active_company") or []
        filter_data = kw.get("filter") or {}
        date_from = filter_data.get("date_from")
        date_to = filter_data.get("date_to")
        if not isinstance(company_ids, (list, tuple)):
            company_ids = [company_ids]
        domain = [('company_id', 'in', company_ids)]
        if date_from and date_to:
            domain += [
                ('date_entry', '>=', date_from),
                ('date_entry', '<=', date_to)
            ]
        records = request.env['cash.inflows'].search(domain)
        total_amount = sum(records.mapped('amount'))
        return {"amount": total_amount}

    # @http.route('/overview/get_top5_inflow', type='json', auth='user')
    # def get_top5_inflow(self, **kw):
    #     results = request.env['cash.inflows'].read_group(
    #         domain=[],
    #         fields=['amount:sum', 'partner_name'],
    #         groupby=['partner_name'],
    #         orderby='amount desc',
    #         limit=5
    #     )
    #     data = []
    #     for r in results:
    #         data.append({
    #             "partner_name": r['partner_name'],
    #             "amount": r['amount'],
    #             "formatted_amount": "{:,.2f}".format(r['amount'])
    #         })
    #     return data
