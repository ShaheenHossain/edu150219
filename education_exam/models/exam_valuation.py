# -*- coding: utf-8 -*-


from odoo import models, fields, api, _
from odoo.exceptions import UserError



class EducationExamValuation(models.Model):
    _name = 'education.exam.valuation'

    name = fields.Char(string='Name', default='New')
    exam_id = fields.Many2one('education.exam', string='Exam', required=True, domain=[('state', '=', 'ongoing')])
    class_id = fields.Many2one('education.class', string='Class', required=True)
    division_id = fields.Many2one('education.class.division', string='Division', required=True)
    subject_id = fields.Many2one('education.syllabus', string='Subject', required=True)
    teachers_id = fields.Many2one('education.faculty', string='Evaluator')
    mark = fields.Integer(string='Max Mark', related='subject_id.total_mark')
    pass_mark = fields.Integer(string='Pass Mark', related='subject_id.pass_mark')
    tut_mark = fields.Integer('Tutorial Mark',related='subject_id.tut_mark')
    tut_pass_mark = fields.Integer('Tutorial Pass Mark',related='subject_id.tut_pass')
    subj_mark = fields.Integer('Subjective Mark',related='subject_id.subj_mark')
    subj_pass_mark = fields.Integer('Subjective Pass Mark',related='subject_id.subj_pass')

    obj_mark = fields.Integer('Objective Mark',related='subject_id.obj_mark')
    obj_pass_mark = fields.Integer('Objective Pass Mark',related='subject_id.obj_pass')

    prac_mark = fields.Integer('Practical Mark',related='subject_id.prac_mark')
    prac_pass_mark = fields.Integer('Practical Pass Mark',related='subject_id.prac_pass')

    state = fields.Selection([('draft', 'Draft'), ('completed', 'Completed'), ('cancel', 'Canceled')], default='draft')
    valuation_line = fields.One2many('exam.valuation.line', 'valuation_id', string='Students')
    mark_sheet_created = fields.Boolean(string='Mark sheet Created')
    date = fields.Date(string='Date', default=fields.Date.today)
    academic_year = fields.Many2one('education.academic.year', string='Academic Year',
                                    related='division_id.academic_year_id', store=True)
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env['res.company']._company_default_get())
    highest=fields.Integer('Highest mark Obtained')
    # @api.multi
    # def get_highest(self):
    #     for rec in self:
    #         evlauation_line=self.env['exam.valuation.line'].search([('valuation_id','=',rec.id)],order='mark_scored asc',limit=1)
    #
    #         rec.highest=evlauation_line.mark_scored
    @api.onchange('exam_id','division_id')
    def domain4subject(self):
        domain = []
        for rec in self:
            if rec.division_id.id:
                result_created=self.env['education.exam.valuation'].search([('exam_id.id','=',rec.exam_id.id),('division_id.id','=',rec.division_id.id)])
                for res in result_created:
                    domain.append(res.subject_id.id)
        return {'domain': {'subject_id': [('id', '!=', domain)]}}
    @api.onchange('tut_mark','tut_pass_mark','subj_mark','subj_pass_mark','obj_mark','obj_pass_mark','prac_mark','prac_pass_mark')
    def calculate_marks(self):
        for rec in self:
            rec.mark=rec.tut_mark+rec.subj_mark+rec.obj_mark+rec.prac_mark
            rec.pass_mark=rec.tut_pass_mark+rec.subj_pass_mark+rec.obj_pass_mark+rec.prac_pass_mark





    @api.onchange('class_id')
    def onchange_class_id(self):
        domain = []
        if self.division_id.class_id != self.class_id:
            self.division_id = ''
        if self.class_id:
            domain = [('class_id', '=', self.class_id.id)]
        return {'domain': {'division_id': domain}}

    # @api.onchange('pass_mark')
    # def onchange_pass_mark(self):
    #     if self.pass_mark > self.mark:
    #         raise UserError(_('Pass mark must be less than Max Mark'))
    #     for records in self.valuation_line:
    #         if records.mark_scored >= self.pass_mark:
    #             records.pass_or_fail = True
    #         else:
    #             records.pass_or_fail = False

    @api.onchange('exam_id', 'subject_id')
    def onchange_exam_id(self):
        if self.exam_id:
            if self.exam_id.division_id:
                self.class_id = self.exam_id.class_id
                self.division_id = self.exam_id.division_id
            elif self.exam_id.class_id:
                self.class_id = self.exam_id.class_id
            else:
                self.class_id = ''
                self.division_id = ''
            self.mark = ''
            if self.subject_id:
                for sub in self.exam_id.subject_line:
                    if sub.subject_id.id == self.subject_id.id:
                        if sub.mark:
                            self.mark = sub.mark
        domain = []
        subjects = self.exam_id.subject_line
        for items in subjects:
            domain.append(items.subject_id.id)
        return {'domain': {'subject_id': [('id', 'in', domain)]}}

    @api.multi
    def create_mark_sheet(self):


        valuation_line_obj = self.env['exam.valuation.line']
        history = self.env['education.class.history'].search([('class_id','=',self.division_id.id),
                                                              '|',('compulsory_subjects','=',self.subject_id.id),'|',('selective_subjects','=',self.subject_id.id),
                                                              ('optional_subjects','=',self.subject_id.id)])     #division_id.student_ids
        if len(history) < 1:
            raise UserError(_('There are no students in this Division'))
        for student in history:
            data = {
                'student_id': student.student_id.id,
                'student_name': student.student_id.name,
                'valuation_id': self.id,
                'tut_mark': 0,
                'subj_mark': 0,
                'obj_mark': 0,
                'letter_grade': 'F',
                'prac_mark': 0,
                'grade_point': 0,
            }
            valuation_line_obj.create(data)
        self.mark_sheet_created = True
    @api.model
    def create(self, vals):
        res = super(EducationExamValuation, self).create(vals)
        valuation_obj = self.env['education.exam.valuation']
        search_valuation = valuation_obj.search(
            [('exam_id', '=', res.exam_id.id), ('division_id', '=', res.division_id.id),
             ('subject_id', '=', res.subject_id.id), ('state', '!=', 'cancel')])
        if len(search_valuation) > 1:
            raise UserError(
                _('Valuation Sheet for \n Subject --> %s \nDivision --> %s \nExam --> %s \n is already created') % (
                    res.subject_id.name, res.division_id.name, res.exam_id.name))
        return res

    @api.multi
    def valuation_completed(self):
        self.name = str(self.exam_id.exam_type.name) + '-' + str(self.exam_id.start_date)[0:10] + ' (' + str(
            self.division_id.name) + ')'
        result_obj = self.env['education.exam.results']
        result_line_obj = self.env['results.subject.line']
        for students in self.valuation_line:
            search_result = result_obj.search(
                [('exam_id', '=', self.exam_id.id), ('division_id', '=', self.division_id.id),
                 ('student_id', '=', students.student_id.id)])
            if len(search_result) < 1:
                result_data = {
                    'name': self.name,
                    'exam_id': self.exam_id.id,
                    'class_id': self.class_id.id,
                    'division_id': self.division_id.id,
                    'student_id': students.student_id.id,
                    'student_name': students.student_name,
                }
                result = result_obj.create(result_data)
                result_line_data = {
                    'name': self.name,
                    'tut_mark': students.tut_mark,
                    'obj_mark': students.obj_mark,
                    'subj_mark': students.subj_mark,
                    'prac_mark': students.prac_mark,
                    'subject_id': self.subject_id.id,
                    'max_mark': self.mark,
                    'pass_mark': self.pass_mark,
                    'mark_scored': students.mark_scored,
                    'pass_or_fail': students.pass_or_fail,
                    'result_id': result.id,
                    'exam_id': self.exam_id.id,
                    'class_id': self.class_id.id,
                    'division_id': self.division_id.id,
                    'student_id': students.student_id.id,
                    'student_name': students.student_name,
                    'letter_grade': students.letter_grade,
                    'grade_point': students.grade_point,
                }
                result_line_obj.create(result_line_data)
            else:
                result_line_data = {
                    'subject_id': self.subject_id.id,
                    'max_mark': self.mark,
                    'pass_mark': self.pass_mark,
                    'tut_mark': students.tut_mark,
                    'obj_mark': students.obj_mark,
                    'subj_mark': students.subj_mark,
                    'prac_mark': students.prac_mark,
                    'mark_scored': students.mark_scored,
                    'pass_or_fail': students.pass_or_fail,
                    'result_id': search_result.id,
                    'exam_id': self.exam_id.id,
                    'class_id': self.class_id.id,
                    'division_id': self.division_id.id,
                    'student_id': students.student_id.id,
                    'student_name': students.student_name,
                    'letter_grade': students.letter_grade,
                    'grade_point': students.grade_point,
                }
                result_line_obj.create(result_line_data)
        self.state = 'completed'

    @api.multi
    def set_to_draft(self):
        result_line_obj = self.env['results.subject.line']
        result_obj = self.env['education.exam.results']
        for students in self.valuation_line:
            search_result = result_obj.search(
                [('exam_id', '=', self.exam_id.id), ('division_id', '=', self.division_id.id),
                 ('student_id', '=', students.student_id.id)])
            for rec in search_result:
                rec.state='draft'
            search_result_line = result_line_obj.search(
                [('result_id', '=', search_result.id), ('subject_id', '=', self.subject_id.id)])
            search_result_line.unlink()
        self.state = 'draft'

    @api.multi
    def valuation_canceled(self):
        self.state = 'cancel'


class StudentsExamValuationLine(models.Model):
    _name = 'exam.valuation.line'

    student_id = fields.Many2one('education.student', string='Students')
    roll_no=fields.Integer('roll no',related='student_id.roll_no')
    student_name = fields.Char(string='Students')
    mark_scored = fields.Integer(string='Mark',compute='calculate_marks')
    tut_mark=fields.Integer(string='Tutorial',default=0)
    subj_mark=fields.Integer(string='Subjective' ,default=0)
    obj_mark=fields.Integer(string='Objective',default=0)
    prac_mark=fields.Integer(string='Practical',default=0)
    pass_or_fail = fields.Boolean(string='Pass/Fail')
    valuation_id = fields.Many2one('education.exam.valuation', string='Valuation Id')
    letter_grade=fields.Char('Letter Grade')
    grade_point=fields.Float('Grade Point')
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env['res.company']._company_default_get())

    @api.onchange('mark_scored', 'pass_or_fail')
    def onchange_mark_scored(self):

        per_obtained = (self.mark_scored * 100) / self.valuation_id.mark
        grades = self.env['education.result.grading'].search([['id', '>', '0']])
        for gr in grades:
            if gr.min_per <= per_obtained and gr.max_per >= per_obtained:
                self.letter_grade = gr.result
                self.grade_point = gr.score

        if self.mark_scored > self.valuation_id.mark:
            raise UserError(_('Mark Scored must be less than Max Mark'))
        # if self.mark_scored >= self.valuation_id.pass_mark:
        #     self.pass_or_fail = True
        # else:
        #     self.pass_or_fail = False
        if self.tut_mark >= self.valuation_id.tut_pass_mark and \
                self.prac_mark >= self.valuation_id.prac_pass_mark and \
                self.subj_mark >= self.valuation_id.subj_pass_mark and \
                self.obj_mark >= self.valuation_id.obj_pass_mark :
           self.pass_or_fail=True
        else :
            self.pass_or_fail=False



    @api.multi
    @api.onchange('tut_mark','subj_mark','obj_mark','prac_mark')
    def calculate_marks(self):
        for rec in self:

            if rec.tut_mark<0:
                raise UserError(_('Mark Scored must be greater than Zero'))
            elif rec.tut_mark>rec.valuation_id.tut_mark:
                raise UserError(_('Mark Scored must be less than Max Tutorial Mark'))
            if rec.obj_mark<0:
                raise UserError(_('Mark Scored must be greater than Zero'))
            elif rec.obj_mark>rec.valuation_id.obj_mark:
                raise UserError(_('Mark Scored must be less than Max Objective Mark'))
            if rec.subj_mark<0:
                raise UserError(_('Mark Scored must be greater than Zero'))
            elif rec.subj_mark>rec.valuation_id.subj_mark:
                raise UserError(_('Mark Scored must be less than Max Subjective Mark'))
            if rec.prac_mark<0:
                raise UserError(_('Mark Scored must be greater than Zero'))
            elif rec.prac_mark>rec.valuation_id.prac_mark:
                raise UserError(_('Mark Scored must be less than Max Practical Mark'))
            rec.mark_scored = rec.tut_mark + rec.obj_mark + rec.subj_mark + rec.prac_mark
            if rec.mark_scored > rec.valuation_id.highest:
                rec.valuation_id.highest = rec.mark_scored