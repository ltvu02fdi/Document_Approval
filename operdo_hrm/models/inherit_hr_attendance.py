from datetime import timedelta

from odoo import models, api, exceptions, fields, _
from odoo.http import request
from odoo.tools import convert, format_duration, format_time, format_datetime, float_round


class InheritHrAttendance(models.Model):
    _inherit = 'hr.attendance'
    work_day = fields.Float(string='Work day', default=0.0, compute='_compute_work_day', store=True)

    @api.depends('employee_id', 'check_in', 'check_out')
    def _compute_display_name(self):
        tz = request.httprequest.cookies.get('tz') if request else None
        for attendance in self:
            if not attendance.check_out:
                attendance.display_name = _(
                    "From %s",
                    format_time(self.env, attendance.check_in, time_format=None, tz=tz, lang_code=self.env.lang),
                )
            else:
                attendance.display_name = _(
                    "%(check_in)s - %(check_out)s",
                    check_in=(attendance.check_in + timedelta(hours=7)).strftime(
                        "%H:%M") if attendance.check_in else "",
                    check_out=(attendance.check_out + timedelta(hours=7)).strftime(
                        "%H:%M") if attendance.check_out else "",
                )

    @api.depends('check_in', 'check_out', 'employee_id')
    def _compute_work_day(self):
        for rec in self:
            if rec.check_in and rec.check_out:
                work_day = rec.worked_hours/ 8
                work_day_exact = float_round(work_day, precision_digits=2)
                rec.work_day = min(work_day_exact, 1.0)
            else:
                rec.work_day = 0.0
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
                      datetime=(attendance.check_in + timedelta(hours=7)).strftime("%Y-%m-%d %H:%M:%S"))
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
                            datetime = (last_attendance_before_check_out.check_in + timedelta(hours=7)).strftime("%Y-%m-%d %H:%M:%S"))
                    )
