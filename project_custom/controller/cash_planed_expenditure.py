# -*- coding: utf-8 -*-
from datetime import date, timedelta, datetime

from dateutil.relativedelta import relativedelta

from odoo import http
from odoo.http import request


class CashPlannedExpenditureController(http.Controller):

    @http.route('/overview/get_planned_current_week', type='json', auth='user')
    def get_planned_current_week(self, **kw):
        company_ids = kw.get("active_company") or []
        if not isinstance(company_ids, (list, tuple)):
            company_ids = [company_ids]

        today = date.today()
        start_week = today - timedelta(days=today.isoweekday() - 1)
        end_week = start_week + timedelta(days=7)

        domain = [
            ('company_id', 'in', company_ids),
            ('date_entry', '>=', start_week),
            ('date_entry', '<', end_week),
        ]
        records = request.env['planned.expenditure'].search(domain)
        total_amount = sum(records.mapped('amount'))
        return {"amount": total_amount}

    @http.route('/overview/get_planned_next_week', type='json', auth='user')
    def get_planned_next_week(self, **kw):
        company_ids = kw.get("active_company") or []
        if not isinstance(company_ids, (list, tuple)):
            company_ids = [company_ids]

        today = date.today()
        start_current_week = today - timedelta(days=today.isoweekday() - 1)
        start_next_week = start_current_week + timedelta(days=7)
        end_next_week = start_next_week + timedelta(days=7)

        domain = [
            ('company_id', 'in', company_ids),
            ('date_entry', '>=', start_next_week),
            ('date_entry', '<', end_next_week),
        ]
        records = request.env['planned.expenditure'].search(domain)
        total_amount = sum(records.mapped('amount'))
        return {"amount": total_amount}

    @http.route('/overview/get_planned_table', type='json', auth='user')
    def get_planned_table(self, **kw):
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
        records = request.env['planned.expenditure'].search(domain, order="date_entry desc")
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

    @http.route('/overview/get_in_out_year_by_m_expense', type='json', auth='user')
    def get_in_out_year_by_m_expense(self, **kw):
        company_ids = kw.get("active_company") or []
        if not isinstance(company_ids, (list, tuple)):
            company_ids = [company_ids]
        filter_data = kw.get("filter") or {}
        date_from_filter = filter_data.get("date_from")  # dạng dd/mm/YYYY
        date_to_filter = filter_data.get("date_to")  # dạng dd/mm/YYYY
        if not date_from_filter or not date_to_filter:
            year = date.today().year
            date_from_obj = date(year, 1, 1)
            date_to_obj = date(year, 12, 31)
        else:
            date_from_obj = datetime.strptime(date_from_filter, "%Y-%m-%d").date()
            date_to_obj = datetime.strptime(date_to_filter, "%Y-%m-%d").date()
        date_from = date_from_obj.strftime("%Y-%m-%d")
        date_to = date_to_obj.strftime("%Y-%m-%d")
        planned_results = request.env['planned.expenditure'].read_group(
            domain=[('date_entry', '>=', date_from),
                    ('date_entry', '<=', date_to),
                    ('company_id', 'in', company_ids)],
            fields=['amount:sum'],
            groupby=['date_entry:month'],
            orderby='date_entry:month asc'
        )
        outflow_results = request.env['cash.outflows'].read_group(
            domain=[('date_entry', '>=', date_from),
                    ('date_entry', '<=', date_to),
                    ('company_id', 'in', company_ids)],
            fields=['amount:sum'],
            groupby=['date_entry:month'],
            orderby='date_entry:month asc'
        )
        planned_dict = {r['date_entry:month']: r['amount'] for r in planned_results}
        outflow_dict = {r['date_entry:month']: r['amount'] for r in outflow_results}
        planned_amounts, outflow_amounts, labels = [], [], []
        cur_date = date_from_obj.replace(day=1)
        while cur_date <= date_to_obj:
            month_num = cur_date.month
            year_num = cur_date.year
            labels.append(f"T{month_num}/{year_num}")
            context = f"tháng {month_num} {year_num}"
            planned_amounts.append(planned_dict.get(context, 0))
            outflow_amounts.append(outflow_dict.get(context, 0))
            cur_date += relativedelta(months=1)

        return {
            "labels": labels,
            "planned": planned_amounts,
            "outflow": outflow_amounts,
        }

    @http.route('/overview/get_dif_filter_expense', type='json', auth='user')
    def get_dif_filter_expense(self, **kw):
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
        inflow = request.env['planned.expenditure'].search(domain)
        inflow_amount = sum(inflow.mapped('amount'))
        outflow = request.env['cash.outflows'].search(domain)
        outflow_amount = sum(outflow.mapped('amount'))
        dif = inflow_amount - outflow_amount
        return {"amount": dif}
