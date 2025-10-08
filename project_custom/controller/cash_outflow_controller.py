# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from datetime import date, timedelta

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

    @http.route('/overview/get_cash_outflow_current_week', type='json', auth='user')
    def get_cash_outflow_current_week(self, **kw):
        company_ids = kw.get("active_company") or []
        if not isinstance(company_ids, (list, tuple)):
            company_ids = [company_ids]

        today = date.today()
        # ISO weekday: Monday=1, Sunday=7 → start of current week (Monday)
        start_week = today - timedelta(days=today.isoweekday() - 1)
        end_week = start_week + timedelta(days=7)

        domain = [
            ('company_id', 'in', company_ids),
            ('date_entry', '>=', start_week),
            ('date_entry', '<', end_week),
        ]
        records = request.env['cash.outflows'].search(domain)
        total_amount = sum(records.mapped('amount'))
        return {"amount": total_amount}

    @http.route('/overview/get_cash_outflow_last_week', type='json', auth='user')
    def get_cash_outflow_last_week(self, **kw):
        company_ids = kw.get("active_company") or []
        if not isinstance(company_ids, (list, tuple)):
            company_ids = [company_ids]

        today = date.today()
        # Lấy tuần trước
        start_current_week = today - timedelta(days=today.isoweekday() - 1)
        start_last_week = start_current_week - timedelta(days=7)
        end_last_week = start_current_week

        domain = [
            ('company_id', 'in', company_ids),
            ('date_entry', '>=', start_last_week),
            ('date_entry', '<', end_last_week),
        ]
        records = request.env['cash.outflows'].search(domain)
        total_amount = sum(records.mapped('amount'))
        return {"amount": total_amount}

    @http.route('/overview/get_top5_outflow', type='json', auth='user')
    def get_top5_outflow(self, **kw):
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
        results = request.env['cash.outflows'].read_group(
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

    @http.route('/overview/get_outflow_table', type='json', auth='user')
    def get_outflow_table(self, **kw):
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
        records = request.env['cash.outflows'].search(domain, order="date_entry desc")
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
