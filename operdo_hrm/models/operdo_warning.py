from datetime import datetime, date

from odoo import models, fields, api


class OperdoWarningContract(models.Model):
    _name = 'operdo.warning.contract'

    employee_id = fields.Many2one('hr.employee', string='Employee')
    contract_id = fields.Many2one('hr.contract', string='Contract',store=True)
    department_id = fields.Many2one('hr.department', related='employee_id.department_id', string='Department')
    job_title = fields.Char(related='employee_id.job_title')
    contract_type_id = fields.Many2one('hr.contract.type', related='employee_id.contract_id.contract_type_id', string='Contract Type')
    date_expires = fields.Char(string='Expiration Contract Date')
    date_start = fields.Date(string='Start Date', related='contract_id.date_start')
    date_end = fields.Date(string='End Date', related='contract_id.date_end')
    id_employee = fields.Integer(related='employee_id.id', string='ID Employee')
    start_date_company = fields.Datetime(string='Start Date', related='employee_id.start_date_company')

    @api.model
    def _cron_about_expire_contract(self):
        today = date.today()
        notice_period = self.env.company.contract_expiration_notice_period
        Warning = self.env['operdo.warning.contract']
        contracts = self.env['hr.contract'].search([("date_end", "!=", False)])
        for rec in contracts:
            date_end = fields.Date.from_string(rec.date_end)
            diff = (date_end - today).days
            if 0 <= diff <= notice_period or diff < 0:
                existing = Warning.search([
                    ("contract_id", "=", rec.id),
                ], limit=1)
                if not existing:
                    Warning.create({
                        "employee_id": rec.employee_id.id,
                        "contract_id": rec.id,
                    })
