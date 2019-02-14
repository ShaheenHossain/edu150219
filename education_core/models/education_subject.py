# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class EducationSubject(models.Model):
    _name = 'education.subject'

    name = fields.Char(string='Name', required=True, help="Name of the Subject")
    # is_language = fields.Boolean(string="Language", help="Tick if this subject is a language")
    # is_lab = fields.Boolean(string="Lab", help="Tick if this subject is a Lab")
    code = fields.Char(string="Code", help="Enter the Subject Code")
    # type = fields.Selection([('compulsory', 'Compulsory'), ('elective', 'Elective')],
    #                         string='Type', default="compulsory",
    #                         help="Choose the type of the subject")
    # weightage = fields.Float(string='Weightage', default=1.0,
    #                          help="Enter the weightage for this subject")
    description = fields.Text(string='Description')

    _sql_constraints = [
        ('code', 'unique(code)', "Another Subject already exists with this code!"),
    ]

    # @api.constrains('weightage')
    # def check_weightage(self):
    #     """return warning if the weightage given is not a possitive value"""
    #     for rec in self:
    #         if rec.weightage <= 0:
    #             raise ValidationError(_('Weightage must be Possitive'))


class StandardMedium(models.Model):
    _name = "education.medium"
    _description = "Standard Medium"

    name = fields.Char(string='Name', required=True,
                       help="Enter the Name of the Medium")
    code = fields.Char(string='Code', help="Enter the Medium Code")
    description = fields.Text(string='Description')


class EducationMotherTongue(models.Model):
    _name = "education.mother.tongue"
    _description = "Mother Tongue Language"

    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code')


class EducationSyllabus(models.Model):
    _name = 'education.syllabus'
    _rec_name = 'display'
    name = fields.Char('Name')
    display=fields.Char('Subject')
    code = fields.Char('Code', compute="_get_code")
    class_id = fields.Many2one('education.class', string='Class')
    has_group=fields.Integer(related='class_id.division_count')
    divisional=fields.Boolean("Grouping ?")
    division_id = fields.Many2one('education.division', string='Group')
    academic_year = fields.Many2one('education.academic.year', string='Batch')
    subject_id = fields.Many2one('education.subject', string='Subject')
    paper = fields.Char( string='Paper')
    active=fields.Boolean('Active?',related='academic_year.active')
    compulsory_for=fields.Many2many('education.class.history','education_syllabus_class_history_rel',
                                    'compulsory_for','compulsory_subjects','compulsory for')
    selective_for=fields.Many2many('education.class.history','education_syllabus_class_history_1_rel',
                                    'selective_for','selective_subjects','selective for')
    optional_for=fields.Many2many('education.class.history','education_syllabus_class_history_optional_rel',
                                    'optional_for','optional_subjects','Optional for')

    subject_type = fields.Selection(
        [('theory', 'Theory'), ('practical', 'Practical'),
         ('both', 'Both'), ('other', 'Other')],
        'Subject Type', default="theory", required=True)
    selection_type = fields.Selection(
        [('compulsory', 'Compulsory'), ('elective', 'Elective')],
        'Selection Type', default="compulsory", required=True)
    evaluation_type = fields.Selection(
        [('general', 'General'),('extra','Extra')],
        'Evaluation Type', default="general", required=True)

    # total_hours = fields.Float(string='Total Hours')
    total_mark=fields.Integer('Total')
    pass_mark=fields.Integer('Pass')
    tut_mark=fields.Integer('Tutorial')
    tut_pass=fields.Integer('pass')
    subj_mark = fields.Integer('Subjective')
    subj_pass = fields.Integer('pass')
    obj_mark = fields.Integer('Objective')
    obj_pass = fields.Integer('pass')
    prac_mark = fields.Integer('Practical')
    prac_pass = fields.Integer('pass')
    description = fields.Text(string='Syllabus Modules')

    @api.onchange('academic_year','class_id','division_id','subject_id','paper')
    def _get_code(self):
        for rec in self:
            recname=''
            reccode=''
            if rec.paper and rec.subject_id:
                recname=rec.subject_id.name +'-'+ rec.paper
                reccode=rec.subject_id.code +'-'+ rec.paper
            elif rec.subject_id:
                recname=rec.subject_id.name
                reccode=rec.subject_id.code
            rec.display = recname
            if recname != '':

                if rec.divisional == True:
                    recname=recname + rec.class_id.name +'-' + rec.academic_year.name # +' ('+rec.division_id.name +')'
                    reccode=reccode + rec.class_id.code +'-' + rec.academic_year.ay_code # +' ('+rec.division_id.code +')'
                else:
                    recname = recname + rec.class_id.name + '-' + rec.academic_year.name
                    reccode = reccode + rec.class_id.code + '-' + rec.academic_year.ay_code
                    rec.division_id=False
            rec.name=recname
            rec.code=reccode
    @api.model
    @api.onchange('tut_mark','subj_mark','obj_mark','prac_mark','tut_pass','subj_pass','obj_pass','prac_pass')
    def calculate_total_mark(self):
        for rec in self:
            rec.total_mark=rec.tut_mark+rec.subj_mark+rec.obj_mark+rec.prac_mark
            rec.pass_mark=rec.tut_pass+rec.subj_pass+rec.obj_pass+rec.prac_pass
    _sql_constraints = [('unque_syllabus_batch_level','unique(subject_id,academic_year,division_id,class_id,paper)','Subject Already added!'),]