# -*- coding: utf-8 -*-


from odoo import models, fields, api


class resultGradingSystem(models.Model):
    _name = 'education.result.grading'
    _rec_name = 'result'

    min_per = fields.Integer('Minimum Percentage', required=True)
    max_per = fields.Integer('Maximum Percentage', required=True)
    result = fields.Char('Result to Display', required=True)
    score = fields.Float('Score')