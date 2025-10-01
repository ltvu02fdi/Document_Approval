# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http
from odoo.http import request

class CashOutFlowController(http.Controller):
    @http.route('/overview/get_cash_outflow', type='json', auth='user')
    def get_cash_outflow(self, **kw):
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
        records = request.env['cash.outflows'].search(domain)
        total_amount = sum(records.mapped('amount'))
        return {"amount": total_amount}