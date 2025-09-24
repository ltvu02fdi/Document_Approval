from odoo import models, fields, api, _
from odoo.exceptions import UserError
from itertools import groupby
from zk import ZK
from datetime import datetime, timedelta


class ZKDevice(models.Model):
    _name = "zk.device"
    _description = "ZKTeco Attendance Device"

    def sync_attendance(self, ip="192.168.1.201", port=4370, timeout=5):
        zk = ZK(ip, port=port, timeout=timeout)
        conn = False
        try:
            conn = zk.connect()
            attendances = conn.get_attendance()
            users = conn.get_users()
            user_dict = {str(u.user_id): u for u in users}

            # Build attendance logs
            attendance_logs = []
            for log in attendances:
                user_id = str(log.user_id)
                user = user_dict.get(user_id)
                attendance_logs.append({
                    "user_id": user_id,
                    "name": user.name if user else "UNKNOWN",
                    "timestamp": log.timestamp - timedelta(hours=7),
                })

            if attendance_logs:
                self.process_logs(attendance_logs)

        except Exception as e:
            raise UserError(_("Không thể đồng bộ từ %s:%s - %s") % (ip, port, e))
        finally:
            if conn:
                conn.disconnect()

    def process_logs(self, logs):
        Attendance = self.env['hr.attendance']
        Employee = self.env["hr.employee"]

        sorted_logs = sorted(logs, key=lambda l: (l["user_id"], l["timestamp"]))

        for (user_id, day), day_logs in groupby(
                sorted_logs, key=lambda l: (l["user_id"], l["timestamp"].date())
        ):
            day_logs = list(day_logs)
            employee = Employee.search([("attendance_code", "=", user_id)], limit=1)
            if not employee:
                continue
            check_in = day_logs[0]["timestamp"] if day_logs else False
            check_out = day_logs[-1]["timestamp"] if len(day_logs) > 1 else False
            if check_out and check_out.date() != day:
                check_out = False
            start_of_day = datetime.combine(day, datetime.min.time())
            end_of_day = datetime.combine(day, datetime.max.time())
            att = Attendance.search([
                ("employee_id", "=", employee.id),
                ("check_in", ">=", start_of_day),
                ("check_in", "<=", end_of_day),
            ], limit=1)
            if att:
                # cập nhật check_out thành log muộn nhất nếu có
                if check_out and (not att.check_out or check_out > att.check_out):
                    att.write({"check_out": check_out})
            else:
                Attendance.create({
                    "employee_id": employee.id,
                    "check_in": check_in,
                    "check_out": check_out or False,
                })
