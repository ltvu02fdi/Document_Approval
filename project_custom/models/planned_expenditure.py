from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class PlannedExpenditure(models.Model):
    _name = "planned.expenditure"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Planned Expenditure"

    def _default_company_id(self):
        return self.env.company.id if self.env.company.id else False

    date_entry = fields.Date(string="Entry Date", default=lambda self: fields.Date.today())
    category_id = fields.Many2one("expense.categories", string="Category")
    code_category = fields.Char(string="Code Category", related="category_id.code", store=True)
    plan_expenditure_date = fields.Date(string="Planned Expenditure Date", default=fields.Date.today())
    amount = fields.Float(string="Amount")
    description_receipt = fields.Char(string="Description Receipt")
    department_id = fields.Many2one("hr.department", string="Department")
    company_id = fields.Many2one("res.company", string="Company", default=lambda self: self._default_company_id())

    @api.constrains('amount')
    def _check_amount(self):
        for rec in self:
            if rec.amount <= 0:
                raise ValidationError("Số tiền phải lớn hơn 0.")