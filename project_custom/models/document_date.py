from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class DocumentDate(models.Model):
    _name = "document.date"
    _description = "Document Date"
    _rec_name = "date"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    def _default_company_id(self):
        return self.env.company.id if self.env.company.id else False

    date = fields.Date(string="Date", default=fields.Date.today())
    day_number_of_week = fields.Integer(string="Days Number of Week")
    day_number_of_month = fields.Integer(string="Days Number of Month")
    day_number_of_year = fields.Integer(string="Days Number of Year")
    month = fields.Char(string="Month")
    calendar_month_number = fields.Integer(string="Calendar Month Number")
    calendar_month_label = fields.Char(string="Calendar Month Label")
    calendar_year_number = fields.Integer(string="Calendar Year Number")
    calendar_year_label = fields.Char(string="Calendar Year Label")
    iso_week_number_of_year = fields.Integer(string="ISO Week Number Of year")
    quarter = fields.Integer(string="Quarter")
    active = fields.Boolean(string="Active", default=True)
    company_id = fields.Many2one("res.company", string="Company", default=lambda self: self._default_company_id())


