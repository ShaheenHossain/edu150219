# -*- coding: utf-8 -*-


from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
from datetime import date, datetime

class EducationStudentClass(models.Model):
    _name = 'education.student.class'
    _description = 'Assign the Students to Class'
    _inherit = ['mail.thread']
    # _rec_name = 'class_assign_name'
    name = fields.Char('Class Assign Register', compute='get_class_assign_name')
    assign_date=fields.Date(default=fields.Date.today)

    class_id = fields.Many2one('education.class', string='Class')
    student_list = fields.One2many('education.student.list', 'connect_id', string="Students")
    admitted_class = fields.Many2one('education.class.division', string="Admitted Class" )
    assigned_by = fields.Many2one('res.users', string='Assigned By', default=lambda self: self.env.uid)
    state = fields.Selection([('draft', 'Draft'), ('done', 'Done')],
                             string='State', required=True, default='draft', track_visibility='onchange')

    @api.multi
    def get_class_assign_name(self):
        for rec in self:
            rec.name=rec.admitted_class.name + '(assigned on '+ rec.assign_date +')'
    @api.multi
    def assign_class(self):
        max_roll = self.env['education.class.history'].search([('class_id','=',self.admitted_class.id)], order='roll_no desc', limit=1)
        if max_roll.roll_no:
            next_roll = max_roll.roll_no
        else:
            next_roll = 0

        for rec in self:

            if not self.student_list:
                raise ValidationError(_('No Student Lines'))
            com_sub = self.env['education.syllabus'].search(
                            [('class_id', '=', rec.class_id.id),
                             ('academic_year', '=', rec.admitted_class.academic_year_id.id),
                             ('divisional','=',False),
                             ('selection_type', '=', 'compulsory')])
            elect_sub=self.env['education.syllabus'].search(
                            [('class_id', '=', rec.class_id.id),
                             ('academic_year', '=', rec.admitted_class.academic_year_id.id),
                             ('divisional','=',True),
                             ('division_id','=',rec.admitted_class.id),
                             ('selection_type', '=', 'compulsory')])
            com_subjects = [] # compulsory Subject List
            el_subjects = [] # Elective Subject List
            for sub in com_sub:
                com_subjects.append(sub.id)
            for sub in elect_sub:
                el_subjects.append(sub.id)
            for line in self.student_list:
                next_roll = next_roll + 1
                st=self.env['education.student'].search([('id','=',line.student_id.id)])
                st.roll_no = next_roll
                st.class_id = rec.admitted_class.id
                line.roll_no=next_roll


                # create student history

                self.env['education.class.history'].create({'academic_year_id': rec.admitted_class.academic_year_id.id,
                                                            'class_id': rec.admitted_class.id,
                                                            'student_id': line.student_id.id,
                                                            'roll_no': next_roll,
                                                            'compulsory_subjects': [(6, 0,com_subjects)],
                                                            'selective_subjects': [(6, 0, el_subjects)]
                                                            })


            self.write({
                'state': 'done'
                })


    @api.multi
    def unlink(self):
        """Return warning if the Record is in done state"""
        for rec in self:
            if rec.state == 'done':
                raise ValidationError(_("Cannot delete Record in Done state"))

    @api.multi
    def get_student_list(self):
        """returns the list of students applied to join the selected class"""
        for rec in self:
            for line in rec.student_list:
                line.unlink()
            # TODO apply filter not to get student assigned previously
            students = self.env['education.student'].search([
                ('class_id', '=', rec.admitted_class.id),('assigned', '=', False)])
            if not students:
                raise ValidationError(_('No Students Available.. !'))
            values = []
            for stud in students:
                stud_line = {
                    'class_id': rec.class_id.id,
                    'student_id': stud.id,
                    'connect_id': rec.id,
                    'roll_no': stud.application_id.roll_no
                }
                stud.assigned=True
                values.append(stud_line)
            for line in values:
                rec.student_line = self.env['education.student.list'].create(line)


class EducationStudentList(models.Model):
    _name = 'education.student.list'
    _inherit = ['mail.thread']

    connect_id = fields.Many2one('education.student.class', string='Class')
    student_id = fields.Many2one('education.student', string='Student')
    stu_id=fields.Char(string="Id",related='student_id.student_id')
    class_id = fields.Many2one('education.class', string='Level')
    section_id = fields.Many2one('education.class.division', string='Class')
    roll_no = fields.Integer( string='Roll No')
