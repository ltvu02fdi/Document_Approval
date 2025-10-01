# -*- coding: utf-8 -*-
from dateutil.relativedelta import relativedelta

from odoo import http
from odoo.http import request
from datetime import date, datetime


class CashOverviewFlowController(http.Controller):

    @http.route('/overview/get_in_out_year', type='json', auth='user')
    def get_in_out_year(self, **kw):
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
        inflow_results = request.env['cash.inflows'].read_group(
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
        inflow_dict = {
            r['date_entry:month']: r['amount']
            for r in inflow_results if r.get('date_entry:month')
        }
        outflow_dict = {
            r['date_entry:month']: r['amount']
            for r in outflow_results if r.get('date_entry:month')
        }
        inflow_cum, outflow_cum, labels = [], [], []
        cum_in, cum_out = 0, 0
        cur_date = date_from_obj.replace(day=1)
        while cur_date <= date_to_obj:
            month_num = cur_date.month
            year_num = cur_date.year
            labels.append(f"Tháng {month_num}")
            context = f"tháng {month_num} {year_num}"
            cum_in += inflow_dict.get(context, 0)
            cum_out += outflow_dict.get(context, 0)

            inflow_cum.append(cum_in)
            outflow_cum.append(cum_out)
            cur_date += relativedelta(months=1)
        return {
            "labels": labels,
            "inflow": inflow_cum,
            "outflow": outflow_cum,
        }

    @http.route('/overview/get_in_out_year_by_m', type='json', auth='user')
    def get_in_out_year_by_m(self, **kw):
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
        inflow_results = request.env['cash.inflows'].read_group(
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
        inflow_dict = {r['date_entry:month']: r['amount'] for r in inflow_results}
        outflow_dict = {r['date_entry:month']: r['amount'] for r in outflow_results}
        inflow_amounts, outflow_amounts, labels = [], [], []
        cur_date = date_from_obj.replace(day=1)
        while cur_date <= date_to_obj:
            month_num = cur_date.month
            year_num = cur_date.year
            labels.append(f"T{month_num}/{year_num}")
            context = f"tháng {month_num} {year_num}"
            inflow_amounts.append(inflow_dict.get(context, 0))
            outflow_amounts.append(outflow_dict.get(context, 0))
            cur_date += relativedelta(months=1)

        return {
            "labels": labels,
            "inflow": inflow_amounts,
            "outflow": outflow_amounts,
        }
