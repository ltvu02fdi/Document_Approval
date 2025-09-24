from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class HrEmployeePrivateInherit(models.Model):
    _inherit = 'hr.employee'

    start_date = fields.Datetime(string='Start Date')
    start_date_company = fields.Datetime(string='Start Date Company')
    attendance_code = fields.Char(string='Attendance Code')
    contract_ids = fields.Many2one('hr.contract', string='Contracts', compute='_compute_contract')
    degree = fields.Char(string='Degree')
    date_of_ID_issuance = fields.Datetime(string='Date of ID issuance')
    place_of_ID_issuance = fields.Char(string='Place of ID card issuance')
    social_insurance = fields.Char(string='Social insurance book number')
    tax_code = fields.Char(string='Personal tax code')
    notes = fields.Char(string='Notes')

    def _compute_contract(self):
        for rec in self:
            contracts = self.env['hr.contract'].search([
                ('employee_id', '=', rec.id),
                ('state', '=', 'open')
            ], order='date_start desc', limit=1)
            rec.contract_ids = contracts
    @api.model
    def get_import_templates(self):
        return [{
            'label': _('Import Template for Employees'),
            'template': '/operdo_hrm/static/xls/hr_employee_sample.xls'
        }]

    @api.constrains('work_phone', 'work_email', 'identification_id', 'visa_no', 'mobile_phone')
    def check_unique_fields(self):
        for rec in self:
            if rec.work_phone:
                existing = self.search([
                    ('work_phone', '=', rec.work_phone),
                    ('id', '!=', rec.id)
                ], limit=1)
                if existing:
                    raise ValidationError(
                        _("The work phone number '%s' already exists in another employee record (ID: %s - %s).")
                        % (rec.work_phone, existing.id, existing.name)
                    )
            if rec.work_email:
                existing = self.search([
                    ('work_email', '=', rec.work_email),
                    ('id', '!=', rec.id)
                ], limit=1)
                if existing:
                    raise ValidationError(
                        _("The work email '%s' already exists in another employee record (ID: %s - %s).")
                        % (rec.work_email, existing.id, existing.name)
                    )
            if rec.identification_id:
                existing = self.search([
                    ('identification_id', '=', rec.identification_id),
                    ('id', '!=', rec.id)
                ], limit=1)
                if existing:
                    raise ValidationError(
                        _("The identification number '%s' already exists in another employee record (ID: %s - %s).")
                        % (rec.identification_id, existing.id, existing.name)
                    )
            if rec.visa_no:
                existing = self.search([
                    ('visa_no', '=', rec.visa_no),
                    ('id', '!=', rec.id)
                ], limit=1)
                if existing:
                    raise ValidationError(
                        _("The visa number '%s' already exists in another employee record (ID: %s - %s).")
                        % (rec.visa_no, existing.id, existing.name)
                    )
            if rec.mobile_phone:
                existing = self.search([
                    ('mobile_phone', '=', rec.mobile_phone),
                    ('id', '!=', rec.id)
                ], limit=1)
                if existing:
                    raise ValidationError(
                        _("The mobile phone number '%s' already exists in another employee record (ID: %s - %s).")
                        % (rec.mobile_phone, existing.id, existing.name)
                    )
