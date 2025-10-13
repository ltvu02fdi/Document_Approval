from odoo import models, fields, api
from odoo.exceptions import ValidationError


class EmployeeBirthdayWizard(models.TransientModel):
    _name = 'employee.birthday.wizard'
    _description = 'Search Employee by Birthday Range'

    date_start = fields.Date(string="From Date", required=True)
    date_end = fields.Date(string="To Date", required=True)

    @api.constrains('date_start', 'date_end')
    def _check_date_range(self):
        for rec in self:
            if rec.date_end and rec.date_start and rec.date_end < rec.date_start:
                raise ValidationError("Ngày kết thúc không được nhỏ hơn ngày bắt đầu.")

    def action_search(self):
        employees = self.env['hr.employee'].search([('birthday', '!=', False)])
        employees = employees.filtered(
            lambda e: e.birthday.month >= self.date_start.month
                      and e.birthday.month <= self.date_end.month
        )
        return {
            'type': 'ir.actions.act_window',
            'name': 'Employee Birthday List',
            'res_model': 'hr.employee',
            'view_mode': 'list',
            'domain': [('id', 'in', employees.ids)],
            'views': [
                (self.env.ref('operdo_hrm.view_operdo_employee_list').id, 'list'),
            ],
            'context': {
                'create': False,
                'edit': False,
                'delete': False,
                "no_breadcrumbs" : True,
            },
            'target': 'current',
        }

