from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class CashOutflow(models.Model):
    _name = "cash.outflows"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Cash Outflow"

    def _default_company_id(self):
        return self.env.company.id if self.env.company.id else False

    date_entry = fields.Date(string="Entry Date", default=lambda self: fields.Date.today())
    category_id = fields.Many2one("receipt.categories", string="Category")
    code_category = fields.Char(string="Code Category", related="category_id.code", store=True)
    amount = fields.Float(string="Amount")
    description_receipt = fields.Char(string="Description Receipt")
    document_date = fields.Date(string="Document Date", default=fields.Date.today())
    document_code = fields.Char(string="Document Code",)
    payer = fields.Char(string="Payer")
    department_id = fields.Many2one("hr.department", string="Department")
    company_id = fields.Many2one("res.company", string="Company", default=lambda self: self._default_company_id())

    @api.constrains('amount')
    def _check_amount(self):
        for rec in self:
            if rec.amount <= 0:
                raise ValidationError("Số tiền phải lớn hơn 0.")





