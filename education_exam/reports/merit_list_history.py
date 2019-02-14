# -*- coding: utf-8 -*-

from datetime import datetime
import time
from odoo import fields, models,api


class ExamMeritListHistory(models.AbstractModel):
    _name = 'exam.merit_list.history'
    student_history=fields.Many2one('education.class.history')
    level=fields.Many2one('education.class','Level')
    section=fields.Many2one('education.class.division','Section')
    exam=fields.Many2one('education.exam','Level')
    score=fields.Float('Score')
    addl_score=fields.Float('Additional Score')
    net_score=fields.Float('Net Score')
    lg=fields.Many2one('education.result.grading')
    gp=fields.Float('Grade Point')
    gpa=fields.Float('GPA')
