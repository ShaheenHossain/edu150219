# -*- coding: utf-8 -*-

from odoo import models, fields, api

class examtabulationwizard(models.Model):
    _name='education.tabulation.wizerd'
    academic_year=fields.Many2one('education.academic.year')
    # class_id=fields.Many2one('education.class')
    division_id=fields.Many2one('education.division')
    section_id=fields.Many2one('education.class.section')
    exam_id=fields.Many2one('education.exam.results')
    student_id=fields.Many2one('education.student')
    subject_id=fields.Many2one('education.subject')


# class eschool(models.Model):
#     _name = 'eschool.eschool'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100