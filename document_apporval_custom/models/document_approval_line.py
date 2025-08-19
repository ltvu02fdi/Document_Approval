from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from datetime import date


class DocumentApprovalLine(models.Model):
    _name = 'document.approval.line'
    _description = 'Document Approval Line'
    _order = 'sequence, id desc'

    sequence = fields.Integer(string='Sequence', default=0)
    voucher_code = fields.Char(string='Voucher Code')
    voucher_name = fields.Char(string='Voucher Name')
    expense_description = fields.Char(string='Expense Description')
    expense_date = fields.Date(string='Expense Date', default=lambda self: fields.Date.today())
    quantity = fields.Integer(string='Quantity', default=1)
    uom_id = fields.Many2one(
        'uom.uom',string="Uom")
    price_unit = fields.Float(string="Price Unit",)
    amount = fields.Monetary(
        string="Total Amount (VNĐ)",
        compute="_compute_amount",
        store=True,
        currency_field="currency_id",
    )

    currency_id = fields.Many2one(
        "res.currency",
        string="Currency",
        default=lambda self: self.env.company.currency_id.id,
    )
    attachment_ids = fields.Many2many(
        "ir.attachment",
        "document_approval_line_ir_attachment_rel",
        "line_id",
        "attachment_id",
        string="Attachment",
    )
    note = fields.Text(string="Note")
    document_approval_id = fields.Many2one('document.approval', string='Document Approval',
                                           ondelete='restrict')

    @api.depends("quantity", "price_unit")
    def _compute_amount(self):
        for rec in self:
            rec.amount = rec.quantity * rec.price_unit

    @api.constrains("expense_date")
    def _check_expense_date(self):
        for rec in self:
            if rec.expense_date and rec.expense_date > date.today():
                raise ValidationError("The transaction date cannot be later than the current date.")

    @api.constrains("quantity", "price_unit")
    def _check_positive_values(self):
        for rec in self:
            if rec.quantity <= 0:
                raise ValidationError("Quantity must be greater than 0.")
            if rec.price_unit < 0:
                raise ValidationError("Unit price must be greater than or equal to 0.")

    @api.onchange('document_approval_id')
    def _onchange_document_approval_id(self):
        if self.document_approval_id and not self.sequence:
            # lấy max sequence hiện có trong form cha
            existing_sequences = [line.sequence for line in self.document_approval_id.document_approval_ids]
            self.sequence = max(existing_sequences, default=0) + 1

    @api.model
    def create(self, vals):
        # nếu chưa có sequence thì tự tính
        if not vals.get('sequence'):
            parent_id = vals.get('document_approval_id')
            if parent_id:
                last_line = self.search(
                    [('document_approval_id', '=', parent_id)],
                    order="sequence desc",
                    limit=1
                )
                vals['sequence'] = last_line.sequence + 1 if last_line else 1
            else:
                vals['sequence'] = 1
        return super().create(vals)
