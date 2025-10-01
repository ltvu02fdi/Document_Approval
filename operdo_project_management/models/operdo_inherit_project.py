from odoo import models, fields


class OperdoInheritProject(models.Model):
    _inherit = "project.project"

    department_id = fields.Many2one('hr.department', string='Department')
