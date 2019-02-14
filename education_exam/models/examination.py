# -*- coding: utf-8 -*-


from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class EducationExam(models.Model):
    _name = 'education.exam'

    name = fields.Char(string='Name', default='New')
    generated_name=fields.Char(string='Gen Name',default='New')
    class_id = fields.Many2one('education.class', string='Class')
    division_id = fields.Many2one('education.class.division', string='Division')
    exam_type = fields.Many2one('education.exam.type', string='Type', required=True)
    school_class_division_wise = fields.Selection([('school', 'School'), ('class', 'Class'), ('division', 'Division')],
                                                  related='exam_type.school_class_division_wise',
                                                  string='School/Class/Division Wise')
    class_division_hider = fields.Char(string='Class Division Hider')
    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string='End Date', required=True)
    subject_line = fields.One2many('education.subject.line', 'exam_id', string='Subjects')
    state = fields.Selection([('draft', 'Draft'), ('ongoing', 'On Going'), ('close', 'Closed'), ('cancel', 'Canceled')],
                             default='draft')
    academic_year = fields.Many2one('education.academic.year', string='Academic Year',
                                    related='division_id.academic_year_id', store=True)
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env['res.company']._company_default_get())
    transcript_id=fields.Many2one('academic.transcript')
    result_sheet_created = fields.Boolean(string='result sheet Created')
    @api.multi
    @api.onchange('academic_year','exam_type')
    def get_class_domain(self):
        for rec in self:
            domain=[]
            existing_class=self.env['education.exam'].search([('exam_type.id','=',rec.exam_type.id),('academic_year.id','=',rec.academic_year.id)])
            for cls in existing_class:
                domain.append(cls.class_id.id)
        return {'domain': {'class_id': [('id', '!=', domain)]}}
    @api.model
    def create(self, vals):
        res = super(EducationExam, self).create(vals)
        if res.division_id:
            res.class_id = res.division_id.class_id.id
        return res

    @api.onchange('class_division_hider')
    def onchange_class_division_hider(self):
        self.school_class_division_wise = 'school'

    @api.constrains('start_date', 'end_date')
    def check_dates(self):
        for rec in self:
            if rec.start_date > rec.end_date:
                raise ValidationError(_("Start date must be Anterior to end date"))

    @api.multi
    def close_exam(self):
        all_completed=1
        valuation_status=self.env['education.exam.valuation'].search([('exam_id','=',self.id)])
        for line in valuation_status:
            if line.state != 'completed':
                all_completed=0
        if all_completed==1:
            self.state = 'close'
        else:
            raise ValidationError(_("Complete all valuation first!"))

    @api.multi
    def cancel_exam(self):
        self.state = 'cancel'

    @api.multi
    def confirm_exam(self):
        if len(self.subject_line) < 1:
            raise UserError(_('Please Add Subjects'))
        name = str(self.exam_type.name) + '-' + str(self.start_date)[0:10]
        if self.division_id:
            name = name + ' (' + str(self.division_id.name) + ')'
        elif self.class_id:
            name = name + ' (' + str(self.class_id.name) + ')'
        self.generated_name = name
        self.state = 'ongoing'
    @api.multi
    def check_student_section_subject(self,section_id,subject_id):
        sections=self.env['education.class.division'].search([('academic_year_id','=',self.academic_year.id),('class_id','=',self.class_id.id)])
        for section in sections:
            if section.id==section_id:
                section_in_history=self.env['education.class.history'].search([('class_id.id', '=', section.id)])
                record_count=len(section_in_history)
                if record_count>0:
                    for rec in section_in_history:
                        for sub in rec.compulsory_subjects:
                            if sub.id==subject_id:
                                return True
                    for rec in section_in_history:
                        for sub in rec.selective_subjects:
                            if sub.id==subject_id:
                                return True
                    for rec in section_in_history:
                            for sub in rec.optional_subjects:
                                if sub.id==subject_id:
                                    return True

        return False
    @api.multi
    def create_result_sheet(self):
        sections=self.env['education.class.division'].search([('academic_year_id','=',self.academic_year.id),('class_id','=',self.class_id.id)])
        subjects=self.subject_line
        for section in sections:
            for subject in subjects:
                # check student present for this subject in this section
                check_student = self.check_student_section_subject(section.id, subject.subject_id.id)
                if check_student==True:

                    self.env['education.exam.valuation'].create({
                        'exam_id':self.id,
                        'class_id':self.class_id.id,
                        'division_id':section.id,
                        # 'section_id':self.section,
                        'subject_id':subject.subject_id.id,
                        'academic_year':self.academic_year.id,
                    })

    @api.multi
    def get_subjects(self):
        for rec in self:
            subjline_obj=self.env['education.subject.line']

            subjects=self.env['education.syllabus'].search([('class_id','=',rec.class_id.id),('academic_year','=',rec.academic_year.id)])  #.search([('class_id', '=', self.id)])
            for subject in subjects :
                data={'subject_id': subject.id,
                      'exam_id': rec.id,
                      'time_from': '10.30',
                      'time_to': '12.30',
                      'date':rec.start_date
                      }
                subjline_obj.create(data)
class SubjectLine(models.Model):
    _name = 'education.subject.line'
    _rec_name = 'subject_id'
    subject_id = fields.Many2one('education.syllabus', string='Subject', required=True)
    display=fields.Char(related='subject_id.name')
    date = fields.Date(string='Date', required=True)
    time_from = fields.Float(string='Time From', required=True)
    time_to = fields.Float(string='Time To', required=True)
    mark = fields.Integer(string='Mark')
    exam_id = fields.Many2one('education.exam', string='Exam')
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env['res.company']._company_default_get())
    _sql_constraints = [('unque_subject_exam','unique(subject_id,exam_id)','Subject Already added!'),]

class EducationExamType(models.Model):
    _name = 'education.exam.type'

    name = fields.Char(string='Name', required=True)
    school_class_division_wise = fields.Selection([('school', 'School'), ('class', 'Class'), ('division', 'Division'), ('final', 'Final Exam (Exam that promotes students to the next class)')],
                                                  string='Exam Type', default='class')
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env['res.company']._company_default_get())
class examlist(models.AbstractModel):
    _name='exam.list'
    name=fields.Char("exam List")
    batch=fields.Many2one('education.academic.year',"batch")
    class_id= fields.Many2one('education.class',"Class")
    group= fields.Many2one('education.division',"Group")
    section= fields.Many2one('education.class.section',"Section")
    subject= fields.Many2one('education.syllabus',"Subject")
    exam_type= fields.Many2one('education.exam.type',"Exam")

    @api.onchange('batch')
    def change_batch(self):
        pass