from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from datetime import date


class DocumentApproval(models.Model):
    _inherit = 'document.approval'

    request_type = fields.Selection(selection=[('purchase_request', 'Purchase Request'),
                                               ('payment_request', 'Payment Request'),
                                               ('cash_request', 'Cast Advance Request'),
                                               ],
                                    default='purchase_request', string="Request Type",
                                    help='Request Type.')
    name = fields.Char(string='Request Name', required=True,
                       help='Name of the record.')
    request_code = fields.Char(string="Request Code", tracking=True)
    request_name = fields.Char(string="Request Name", tracking=True)
    request_employee_id = fields.Many2one('hr.employee', string="Request Employee")
    job_id = fields.Many2one('hr.job',
                             string="Job Title",
                             related='request_employee_id.job_id', store=True)
    department_id = fields.Many2one(
        'hr.department',
        string="Department",
        related='request_employee_id.department_id',
        store=True,
    )
    request_date = fields.Date(string="Request Date", default=lambda self: fields.Date.today())
    due_date = fields.Date(string="Due Date", default=lambda self: fields.Date.today())
    description = fields.Text(string="Description")
    company_id = fields.Many2one('res.company', string="Company", default=lambda self: self.env.company)
    payment_method = fields.Selection(selection=[('cash', 'Cash'), ('bank_transfer', 'Bank Transfer')],
                                      default='cash', string="Payment Method")
    recipient = fields.Char(string="Recipient")
    document_approval_ids = fields.One2many('document.approval.line', 'document_approval_id',
                                            string="Document Approvals Line", tracking=True)
    tax_code = fields.Char(string="Tax Code")

    @api.constrains('request_code')
    def _check_validate_code(self):
        for rec in self:
            if rec.request_code:
                exists = self.search([
                    ('request_code', '=', rec.request_code),
                    ('id', '!=', rec.id)
                ], limit=1)
                if exists:
                    raise ValidationError("Request code already exists, please enter another one!")

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('document.approval') or 'New'
        return super(DocumentApproval, self).create(vals)
