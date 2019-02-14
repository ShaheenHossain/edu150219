# -*- coding: utf-8 -*-


from odoo import models, fields, api, _
from odoo.exceptions import UserError

class academicTranscript(models.Model):
    _name ='academic.transcript'
    _description='print academic transcript for selected exams'
    academic_year=fields.Many2one('education.academic.year',"Academic Year")
    level=fields.Many2one('education.class',"Level")
    exams=fields.Many2many('education.exam','transcript_id')
    specific_section = fields.Boolean('For a specific section')
    section=fields.Many2one('education.class.division')
    specific_student=fields.Boolean('For a specific Student')
    student=fields.Many2one('education.student','Student')
    state=fields.Selection([('draft','Draft'),('done','Done')],compute='calculate_state')
    @api.multi
    def calculate_state(self):
        results=self.env[('education.exam.results')].search([('academic_year','=',self.academic_year.id),('class_id','=','level')])
        for exam in self.exams:
            rec=results.search([('exam_id','=',exam.id)])
            for line in rec:
                if line.state!='done':
                    self.state='draft'
                    return True
        self.state='done'


    @api.multi
    @api.onchange('level', 'section')
    def get_student_domain(self):
        for rec in self:
            domain = []
            if rec.section:
                domain.append(('class_id','=',rec.section.id))
            else:
                domain.append(('class_id.class_id.id', '=', rec.level.id))

        return {'domain': {'student':domain}}
    @api.multi
    @api.onchange('specific_section')
    def onchange_specific_section(self):
        for rec in self:
            if rec.specific_section==False:
                rec.specific_student=False
                rec.section=False
    @api.multi
    def generate_results(self):
        for rec in self:
            for exam in self.exams:
                results=self.env['education.exam.results'].search([('exam_id','=',exam.id)])
                for result in results:
                    self.env['education.exam.results'].calculate_result(exam)

