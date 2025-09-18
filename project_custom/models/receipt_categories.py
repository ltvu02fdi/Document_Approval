from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class ReceiptCategory(models.Model):
    _name = "receipt.categories"
    _description = "Receipt Category"
    _order = "create_date desc"
    _rec_name = "name"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    def _default_company_id(self):
        return self.env.company.id if self.env.company.id else False

    code = fields.Char(string="Code", help="Code cannot be empty", index=True)
    name = fields.Char(string="Name", help="Name cannot be empty", copy=False)
    active = fields.Boolean(string="Active", default=True)
    company_id = fields.Many2one("res.company", string="Company", default=lambda self: self._default_company_id())

    @api.onchange("code")
    def _onchange_code(self):
        if self.code:
            self.code = self.code.upper().replace(" ", "")

    @api.model
    def create(self, vals):
        if 'code' in vals:
            vals['code'] = vals['code'].upper().replace(" ", "")
        return super(ReceiptCategory, self).create(vals)

    def write(self, vals):
        if 'code' in vals:
            vals['code'] = vals['code'].upper().replace(" ", "")
        res = super(ReceiptCategory, self).write(vals)
        return res

