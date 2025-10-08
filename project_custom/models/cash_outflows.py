from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class CashOutflow(models.Model):
    _name = "cash.outflows"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Cash Outflow"

    def _default_company_id(self):
        return self.env.company.id if self.env.company.id else False

    date_entry = fields.Date(string="Entry Date", default=lambda self: fields.Date.today())
    category_id = fields.Many2one("expense.categories", string="Category",  domain=lambda self: [("company_id", "=", self.env.company.id)],)
    code_category = fields.Char(string="Code Category", related="category_id.code", store=True)
    amount = fields.Float(string="Amount")
    description_receipt = fields.Char(string="Description Receipt")
    document_date = fields.Date(string="Document Date", default=fields.Date.today())
    document_date_id = fields.Many2one("document.date", string="Document Date", ondelete='restrict')
    document_code = fields.Char(string="Document Code",)
    payer = fields.Char(string="Payer")
    department_id = fields.Many2one("hr.department", string="Department")
    company_id = fields.Many2one("res.company", string="Company", default=lambda self: self._default_company_id())
    partner_name = fields.Char(string="Partner Name",related="category_id.partner_id.name")

    @api.constrains('amount')
    def _check_amount(self):
        for rec in self:
            if rec.amount <= 0:
                raise ValidationError("Số tiền phải lớn hơn 0.")

    @api.constrains("category_id")
    def _check_partner_in_category(self):
        for rec in self:
            if rec.category_id and not rec.category_id.partner_id:
                raise ValidationError(
                    _("Không được phép chọn mã cha.")
                )

    @api.model
    def get_import_templates(self):
        return [{
            'label': 'Tải về mẫu tiền chi',
            'template': '/project_custom/static/template/tien_chi.xlsx',
        }]
