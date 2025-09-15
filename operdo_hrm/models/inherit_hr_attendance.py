from odoo import models, api, exceptions, _

class InheritHrAttendance(models.Model):
    _inherit = 'hr.attendance'

    @api.constrains('check_in', 'check_out', 'employee_id')
    def _check_validity(self):
        """ Custom lại rule:
            - Không check lỗi khi có nhiều open attendance
            - Vẫn check overlap.
        """
        for attendance in self:
            last_attendance_before_check_in = self.env['hr.attendance'].search([
                ('employee_id', '=', attendance.employee_id.id),
                ('check_in', '<=', attendance.check_in),
                ('id', '!=', attendance.id),
            ], order='check_in desc', limit=1)

            if last_attendance_before_check_in and last_attendance_before_check_in.check_out \
                    and last_attendance_before_check_in.check_out > attendance.check_in:
                raise exceptions.ValidationError(
                    _("Cannot create new attendance record for %(empl_name)s, "
                      "the employee was already checked in on %(datetime)s",
                      empl_name=attendance.employee_id.name,
                      datetime=attendance.check_in)
                )
            #  Bỏ hẳn check open attendance (không raise lỗi nữa)
            if attendance.check_out:
                last_attendance_before_check_out = self.env['hr.attendance'].search([
                    ('employee_id', '=', attendance.employee_id.id),
                    ('check_in', '<', attendance.check_out),
                    ('id', '!=', attendance.id),
                ], order='check_in desc', limit=1)

                if last_attendance_before_check_out and last_attendance_before_check_in != last_attendance_before_check_out:
                    raise exceptions.ValidationError(
                        _("Cannot create new attendance record for %(empl_name)s, "
                          "the employee was already checked in on %(datetime)s",
                          empl_name=attendance.employee_id.name,
                          datetime=last_attendance_before_check_out.check_in)
                    )
