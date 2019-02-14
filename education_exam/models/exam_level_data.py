# -*- coding: utf-8 -*-


from odoo import models, fields, api


class EducationExamClass(models.Model):
    _name='exam.level.sumary'
    _description='Sumary data of a level per exam'

    exam_id=fields.Many2one('education.exam',string='Exam')
    level_id=fields.Many2one('education.class','Level')


