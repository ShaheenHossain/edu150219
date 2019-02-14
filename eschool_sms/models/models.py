from odoo import api, fields, models


class inheritAttendanceLine(models.Model):
    _inherit = 'education.attendance.line'
    sms_sent=fields.Boolean('SMS Sent ?')
class defaultAbsentSms(models.Model):
    _name = 'default.absent.sms'
    name=fields.Char("Name")
    from_number=fields.Many2one('sms.number','From Number')
    template_id=fields.Many2one('sms.template',"SMS template")


class inheritAttendanceSheet(models.Model):
    _inherit='education.attendance'
    @api.multi
    def sms_action(self):
        self.ensure_one()
        for record in self:
            absentlist=[]
            guardian_list=[]
            defaults=self.env['default.absent.sms'].search([('name','=','Default Ful-day Absent SMS')],limit=1)
            template_id=defaults.template_id
            from_number=defaults.from_number.id
            mass_sms_heading= str(record.date)+" Full Day Absent "+ record.division_id.name


            absent = self.env['education.attendance.line'].search(
                [('full_day_absent', '=', True), ('attendance_id', '=', record.id), ('sms_sent', '!=', True)])
            if len(absent)>0 :
                for students in absent:
                    StId = students.student_id.partner_id.id
                    guardian=students.student_id.guardian_name.id
                    smsbody= template_id.template_body
                    absentlist.append(StId)
                    guardian_list.append(guardian)
                    students.sms_sent=True

                self.env['sms.mass'].create({'from_mobile':from_number,
                                             'mass_sms_state': 'draft',
                                             'stop_message': "send  STOP To Unsubscribe",
                                             'name': mass_sms_heading,
                                             'sms_template_id': template_id.id,
                                             'selected_records': [[6, 0, absentlist]],
                                             'sms_to': 'guardian',
                                             'message_text': smsbody})
                last_id = self.env['sms.mass'].search([])[-1]
                # send all mass SMS directly
                last_id.send_mass_sms()
            absentlist=[]
            guardian_list=[]
            defaults=self.env['default.absent.sms'].search([('name','=','Default half day Absent SMS')],limit=1)
            template_id=defaults.template_id
            from_number=defaults.from_number.id
            mass_sms_heading = str(record.date) + " Half Day Absent " + record.division_id.name


            absent = self.env['education.attendance.line'].search(
                [('half_day_absent', '=', True), ('attendance_id', '=', record.id), ('sms_sent', '!=', True)])
            if len(absent)>0 :
                for students in absent:
                    StId = students.student_id.partner_id.id
                    guardian=students.student_id.guardian_name.id
                    smsbody= template_id.template_body
                    absentlist.append(StId)
                    guardian_list.append(guardian)
                    students.sms_sent=True

                self.env['sms.mass'].create({'from_mobile':from_number,
                                             'mass_sms_state': 'draft',
                                             'stop_message': "send  STOP To Unsubscribe",
                                             'name': mass_sms_heading,
                                             'sms_template_id': template_id.id,
                                             'selected_records': [[6, 0, absentlist]],
                                             'sms_to': 'guardian',
                                             'message_text': smsbody})
                last_id = self.env['sms.mass'].search([])[-1]
                # send all mass SMS directly
                last_id.send_mass_sms()

class inheritStudent(models.Model):
    _inherit='education.student'

    @api.multi
    def sms_action(self):
        self.ensure_one()

        default_mobile = self.env['sms.number'].search([])[0]

        return {
            'name': 'SMS Compose',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'sms.compose',
            'target': 'new',
            'type': 'ir.actions.act_window',
            'context': {'default_from_mobile_id': default_mobile.id, 'default_to_number': self.mobile,
                        'default_record_id': self.id, 'default_model': 'education.student'}
        }

