
from odoo import models, fields, api


class EducationExamResults(models.Model):
    _name = 'education.exam.results'

    name = fields.Char(string='Name')
    exam_id = fields.Many2one('education.exam', string='Exam')
    class_id = fields.Many2one('education.class', string='Class')
    division_id = fields.Many2one('education.class.division', string='Division')
    student_id = fields.Many2one('education.student', string='Student')
    student_name = fields.Char(string='Student')
    subject_line = fields.One2many('results.subject.line', 'result_id', string='Subjects')
    academic_year = fields.Many2one('education.academic.year', string='Academic Year',
                                    related='division_id.academic_year_id', store=True)
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env['res.company']._company_default_get())
    total_pass_mark = fields.Integer(string='Total Pass Mark')
    total_max_mark = fields.Integer(string='Total Max Mark')
    general_obtained=fields.Integer("General_total")
    optional_obtained=fields.Integer("Optional total")
    extra_obtained=fields.Integer("extra total")
    all_obtained=fields.Integer("Total Obtained")
    general_count=fields.Integer("General Count")
    optional_count=fields.Integer("optional Count")
    extra_count=fields.Integer("extra Count")
    general_gp=fields.Char("general GP")
    optional_gp=fields.Char("Optional GP")
    extra_gp=fields.Char("Extra GP")
    general_gpa = fields.Char("general GPA")
    optional_gpa = fields.Char("Optional GPA")
    extra_gpa = fields.Char("Extra GPA")
    general_lg=fields.Float('general LG')
    optional_lg=fields.Float('Optional LG')
    extra_lg=fields.Float('Extra LG')
    working_days=fields.Integer('Working Days')
    attendance=fields.Integer('Attendance')
    percentage_of_attendance=fields.Float("Percentage of Attendance")
    behavior=fields.Char("Behavior")
    sports=fields.Char("Sports Program")
    uniform=fields.Char("Uniform")
    cultural=fields.Char("Caltural Activities")
    overall_pass = fields.Boolean(string='Overall Pass/Fail')
    no_of_general_subject=fields.Integer("No of General Subjects")
    state=fields.Selection([('draft',"Draft"),('done',"Done")],"State",default='draft')

    total_mark_scored = fields.Integer(string='Total Marks Scored')
    gpa=fields.Float("GPA")
    LG=fields.Char("Letter Grade")
    gpa_optional=fields.Float("GPA (Op)")
    gpa_net=fields.Float("GPA (Net)")
    lg_op=fields.Char("LG (Op)")
    lg_net=fields.Char("LG (Net)")
    @api.model
    def calculate_result(self,exam_id):
        results = self.env['education.exam.results'].search([('exam_id','=',exam_id.id)])
        for result in results:
            if result.state!='done':
                total_pass_mark = 0
                total_max_mark = 0
                total_mark_scored = 0
                overall_pass = True
                subject_list=[]
                general_total=0
                optional_total=0
                extra_total=0
                general_subject_count=0
                optional_subject_count=0
                extra_subject_count=0
                general_grade_point=0
                extra_grade_point=0
                optional_grade_point=0
                for subject in result.subject_line:
                    student_history = self.env['education.class.history'].search(
                        [('student_id', '=', result.student_id.id), ('academic_year_id', '=', exam_id.academic_year.id)])
                    if subject.subject_id in student_history.optional_subjects:
                        optional_total = optional_total + subject.mark_scored
                        optional_grade_point = optional_grade_point + subject.grade_point
                        if subject.subject_id.subject_id.id not in subject_list:
                            subject_list.append(subject.subject_id.subject_id.id)
                            optional_subject_count=optional_subject_count+1
                    elif subject.subject_id not in student_history.optional_subjects:
                        if subject.subject_id.evaluation_type == 'general':
                            general_total = general_total + subject.mark_scored
                            general_grade_point=general_grade_point+subject.grade_point
                            if subject.subject_id.subject_id.id not in subject_list:
                                subject_list.append(subject.subject_id.subject_id.id)
                                general_subject_count = general_subject_count + 1
                        elif subject.subject_id.evaluation_type == 'extra':
                            extra_total = extra_total + subject.mark_scored
                            extra_grade_point = extra_grade_point + subject.grade_point
                            if subject.subject_id.subject_id.id not in subject_list:
                                subject_list.append(subject.subject_id.subject_id.id)
                                extra_subject_count = extra_subject_count + 1
                result.state = 'done'
                result.general_obtained=general_total
                result.optional_obtained=optional_total
                result.extra_obtained=extra_total
                result.general_gp=general_grade_point
                result.optional_gp=optional_grade_point
                result.extra_gp=extra_grade_point
                result.no_of_general_subject = general_subject_count
                result.general_count=general_subject_count
                result.optional_count=optional_subject_count
                result.extra_count=extra_subject_count
                if general_subject_count !=0:
                    result.general_gpa = general_grade_point / general_subject_count
                if optional_subject_count !=0:
                    result.optional_gpa = optional_grade_point / optional_subject_count
                if extra_subject_count !=0:
                    result.extra_gpa = extra_grade_point / extra_subject_count




class ResultsSubjectLine(models.Model):
    _name = 'results.subject.line'

    tut_mark = fields.Integer(string='Tutorial')
    subj_mark = fields.Integer(string='Subjective')
    obj_mark = fields.Integer(string='Objective')
    prac_mark = fields.Integer(string='Practical')
    letter_grade=fields.Char('Grade')
    grade_point=fields.Float('GP')
    name = fields.Char(string='Name')
    subject_id = fields.Many2one('education.syllabus', string='Subject')
    max_mark = fields.Integer(string='Max Mark')
    pass_mark = fields.Integer(string='Pass Mark')
    mark_scored = fields.Integer(string='Mark Scored')
    pass_or_fail = fields.Boolean(string='Pass/Fail')
    result_id = fields.Many2one('education.exam.results', string='Result Id')
    exam_id = fields.Many2one('education.exam', string='Exam')
    class_id = fields.Many2one('education.class', string='Class')
    division_id = fields.Many2one('education.class.division', string='Division')
    student_id = fields.Many2one('education.student', string='Student')
    student_name = fields.Char(string='Student')
    academic_year = fields.Many2one('education.academic.year', string='Academic Year',
                                    related='division_id.academic_year_id', store=True)
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env['res.company']._company_default_get())

class exam_result_summery(models.Model):
    _name = 'education.exam.student.summary'
    exam_id =fields.Many2one('education.exam','Exam')
    student_id=fields.Many2one('education.student',string='Student')
    total_mark=fields.Integer('Total')
    total_gpa=fields.Many2one('education.result.grading', 'Total GPA')
    total_lg=fields.Integer( 'Total GPA')
    additional_mark=fields.Integer('additional')
    additional_gpa = fields.Many2one('education.result.grading', 'additional GPA')
    additional_lg = fields.Integer( 'additional Grade')
    extra_mark=fields.Integer('Extra')
    extra_gpa = fields.Many2one('education.result.grading', 'Extra GPA')
    extra_lg = fields.Integer('Extra Grade')
    net_mark=fields.Integer('net')
    net_gpa = fields.Many2one('education.result.grading', 'NET GPA')
    net_lg = fields.Integer('GPA')
    position_class=fields.Integer("Position in Class")
    position_section=fields.Integer("Position in Section")