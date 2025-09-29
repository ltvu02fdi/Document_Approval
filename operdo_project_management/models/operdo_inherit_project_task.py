from odoo import models, fields


class OperdoInheritProjectTask(models.Model):
    _inherit = "project.task"

    department_id = fields.Many2one('hr.department',related='project_id.department_id',  string='Department')
