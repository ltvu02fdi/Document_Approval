# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from datetime import date

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

    @http.route('/overview/get_cash_inflow_current_m', type='json', auth='user')
    def get_cash_inflow_current_m(self, **kw):
        company_ids = kw.get("active_company") or []
        if not isinstance(company_ids, (list, tuple)):
            company_ids = [company_ids]
        today = date.today()
        start_month = today.replace(day=1)
        if today.month == 12:
            next_month = today.replace(year=today.year + 1, month=1, day=1)
        else:
            next_month = today.replace(month=today.month + 1, day=1)
        end_month = next_month
        domain = [
            ('company_id', 'in', company_ids),
            ('date_entry', '>=', start_month),
            ('date_entry', '<', end_month),
        ]
        records = request.env['cash.inflows'].search(domain)
        total_amount = sum(records.mapped('amount'))
        return {"amount": total_amount}

    @http.route('/overview/get_cash_inflow_from_first_m', type='json', auth='user')
    def get_cash_inflow_from_first_m(self, **kw):
        company_ids = kw.get("active_company") or []
        if not isinstance(company_ids, (list, tuple)):
            company_ids = [company_ids]
        today = date.today()
        start_year = today.replace(month=1, day=1)
        domain = [
            ('company_id', 'in', company_ids),
            ('date_entry', '>=', start_year),
            ('date_entry', '<=', today),
        ]
        records = request.env['cash.inflows'].search(domain)
        total_amount = sum(records.mapped('amount'))
        return {"amount": total_amount}

    @http.route('/overview/get_top5_inflow', type='json', auth='user')
    def get_top5_inflow(self, **kw):
        company_ids = kw.get("active_company") or []
        if not isinstance(company_ids, (list, tuple)):
            company_ids = [company_ids]
        filter_data = kw.get("filter") or {}
        date_from_filter = filter_data.get("date_from")
        date_to_filter = filter_data.get("date_to")
        domain = [('company_id', 'in', company_ids)]
        if date_from_filter and date_to_filter:
            domain += [
                ('date_entry', '>=', date_from_filter),
                ('date_entry', '<=', date_to_filter)
            ]
        else:
            year = date.today().year
            date_from_obj = date(year, 1, 1)
            date_to_obj = date(year, 12, 31)
            domain += [
                ('date_entry', '>=', date_from_obj),
                ('date_entry', '<=', date_to_obj)
            ]
        results = request.env['cash.inflows'].read_group(
            domain=domain,
            fields=['amount:sum', 'partner_name'],
            groupby=['partner_name'],
            orderby='amount desc',
            limit=5
        )
        data = []
        for r in results:
            data.append({
                "partner_name": r['partner_name'],
                "amount": r['amount'],
            })
        return data

    @http.route('/overview/get_inflow_table', type='json', auth='user')
    def get_inflow_table(self, **kw):
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
        else:
            year = date.today().year
            date_from_obj = date(year, 1, 1)
            date_to_obj = date(year, 12, 31)
            domain += [
                ('date_entry', '>=', date_from_obj),
                ('date_entry', '<=', date_to_obj)
            ]
        records = request.env['cash.inflows'].search(domain, order="date_entry desc")
        data = []
        for rec in records:
            data.append({
                "id": rec.id,
                "date_entry": rec.date_entry,
                "partner_name": rec.partner_name,
                "company_name": rec.company_id.name,
                "amount": rec.amount,
                "category_name": rec.category_id.name,
            })

        return data

