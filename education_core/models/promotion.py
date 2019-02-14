# -*- coding: utf-8 -*-


from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
from datetime import date, datetime

class EducationStudentClass(models.Model):
    _name = 'education.promotion'
    _description = 'Promote Student To Upper Class'
    _inherit = ['mail.thread']
    # _rec_name = 'class_assign_name'
    name = fields.Char('Promotion Register', compute='get_promotion_register_name')
    assign_date=fields.Date(default=fields.Date.today)
    previous_batch=fields.Many2one("education.academic.year",'Previous Batch')
    class_id = fields.Many2one('education.class', string='Previous Class')
    promote_to = fields.Many2one('education.class', string='Promote To' ,compute='get_promoted_class')
    sequence = fields.Integer(related='class_id.sequence')
    student_list = fields.One2many('education.promotion.list', 'connect_id', string="Students")
    admitted_class = fields.Many2one('education.class.division', string="From Section" )
    new_batch = fields.Many2one("education.academic.year", 'New Batch')
    promote_section = fields.Many2one('education.class.division', string="To Section" )
    assigned_by = fields.Many2one('res.users', string='Promoted By', default=lambda self: self.env.uid)
    state = fields.Selection([('draft', 'Draft'), ('done', 'Done')],
                             string='State', required=True, default='draft', track_visibility='onchange')
    @api.onchange('class_id')
    def get_promoted_class(self):
        promote_class=self.env['education.class'].search([('sequence','=',(self.sequence+1))])
        for rec in promote_class:
            self.promote_to=rec.id


    @api.multi
    def get_promotion_register_name(self):
        for rec in self:
            rec.name=rec.admitted_class.name + '(assigned on '+ rec.assign_date +')'
    @api.multi
    def promote_student(self):
        max_roll = self.env['education.class.history'].search([('class_id','=',self.promote_section.id)], order='roll_no desc', limit=1)
        if max_roll.roll_no:
            next_roll = max_roll.roll_no
        else:
            next_roll = 0

        for rec in self:

            if not self.student_list:
                raise ValidationError(_('No Student Lines'))
            com_sub = self.env['education.syllabus'].search(
                            [('class_id', '=', rec.promote_to.id),
                             ('academic_year', '=', rec.new_batch.id),
                             ('divisional','=',False),
                             ('selection_type', '=', 'compulsory')])
            elect_sub=self.env['education.syllabus'].search(
                            [('class_id', '=', rec.promote_to.id),
                             ('academic_year', '=', rec.new_batch.id),
                             ('divisional','=',True),
                             ('division_id','=',rec.promote_to.id),
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
                st.class_id = rec.promote_to.id
                line.roll_no=next_roll


                # create student history

                self.env['education.class.history'].create({'academic_year_id': rec.new_batch.id,
                                                            'class_id': rec.promote_section.id,
                                                            'student_id': line.student_id.id,
                                                            'roll_no': next_roll,
                                                            'from_date':rec.new_batch.ay_start_date,
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
            students = self.env['education.class.history'].search([
                ('class_id', '=', rec.admitted_class.id)])
            if not students:
                raise ValidationError(_('No Students Available.. !'))
            values = []
            for stud in students:
                stud_line = {
                    'class_id': rec.class_id.id,
                    'student_id': stud.student_id.id,
                    'connect_id': rec.id,
                    'section_id': rec.admitted_class.id,
                    'roll_no': stud.roll_no
                }
                stud.assigned=True
                values.append(stud_line)
            for line in values:
                rec.student_line = self.env['education.promotion.list'].create(line)


class EducationStudentList(models.Model):
    _name = 'education.promotion.list'
    _inherit = ['mail.thread']

    connect_id = fields.Many2one('education.student.class', string='Class')
    student_id = fields.Many2one('education.student', string='Student')
    stu_id=fields.Char(string="Id",related='student_id.student_id')
    class_id = fields.Many2one('education.class', string='Level')
    sequence=fields.Integer(related='class_id.sequence')
    section_id = fields.Many2one('education.class.division', string='Class')
    roll_no = fields.Integer( string='Roll No')
