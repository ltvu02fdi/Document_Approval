from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from datetime import date


class DocumentApproval(models.Model):
    _inherit = 'document.approval'
    _order = 'request_date desc'

    request_type = fields.Selection(selection=[('purchase_request', 'Purchase Request'),
                                               ('payment_request', 'Payment Request'),
                                               ('cash_request', 'Cast Advance Request'),
                                               ('advance_settlement', 'Advance Settlement'),
                                               ('client_request', 'Client Request'),
                                               ],
                                    default='purchase_request', string="Request Type", index=True,
                                    help='Request Type.')
    request_code = fields.Char(string="Request Code", tracking=True, default=_('Mới'), index=True)
    request_employee_id = fields.Many2one('hr.employee', string="Request Employee", index=True)
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
                                      string="Payment Method")
    recipient = fields.Char(string="Recipient")
    document_approval_ids = fields.One2many('document.approval.line', 'document_approval_id',
                                            string="Document Approvals Line", tracking=True)
    tax_code = fields.Char(string="Tax Code")
    account_number = fields.Char(string="STK")

    client_name = fields.Char(string="Client Name")
    client_lead = fields.Char(string="Client Lead")
    team_member = fields.Char(string="Team Member")
    date_hospitality = fields.Date(string="Date Hospitality", default=lambda self: fields.Date.today())
    venue = fields.Char(string="Venue")
    price_unit = fields.Float(string="Price Unit")

    @api.constrains('price_unit', 'request_type')
    def _check_price_unit(self):
        for rec in self:
            if rec.request_type == 'client_request':
                if rec.price_unit <= 0:
                    raise ValidationError("Chi phí dự kiến phải lớn hơn 0.")

    @api.onchange('request_type')
    def _onchange_payment_method(self):
        for rec in self:
            if rec.request_type == 'client_request':
                rec.payment_method = False
                rec.client_name = False
                rec.client_lead = False
                rec.team_member = False
                rec.date_hospitality = False
                rec.venue = False
                rec.price_unit = False

    @api.model
    def create(self, vals):
        if vals.get('request_code', _('New')) == _('New'):
            if vals.get('request_type') == 'purchase_request':
                seq_code = 'purchase.request.seq'
            elif vals.get('request_type') == 'payment_request':
                seq_code = 'payment.request.seq'
            elif vals.get('request_type') == 'cash_request':
                seq_code = 'cash.request.seq'
            elif vals.get('request_type') == 'advance_settlement':
                seq_code = 'advance.settlement.seq'
            elif vals.get('request_type') == 'client_request':
                seq_code = 'client.request.seq'
            else:
                seq_code = None

            if seq_code:
                vals['request_code'] = self.env['ir.sequence'].next_by_code(seq_code) or _('New')
        return super(DocumentApproval, self).create(vals)

    def action_print(self):
        if self.request_type == 'payment_request':
            url = 'report/pdf/document_apporval_custom.report_template_document_approval_view/%s' % (self.id)
        elif self.request_type == 'purchase_request':
            url = 'report/pdf/document_apporval_custom.report_template_document_approval_purchase_request_view/%s' % (self.id)
        elif self.request_type == 'cash_request':
            url = 'report/pdf/document_apporval_custom.report_template_document_approval_cash_request_view/%s' % (self.id)
        elif self.request_type == 'advance_settlement':
            url = 'report/pdf/document_apporval_custom.report_template_advance_settlement_view/%s' % (self.id)
        elif self.request_type == 'client_request':
            url = 'report/pdf/document_apporval_custom.report_template_document_approval_client_request_view/%s' % (self.id)
        return {
            'type': 'ir.actions.act_url',
            'url': url,
            'target': 'new',
            'res_id': self.id,
        }