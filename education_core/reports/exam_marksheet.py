# -*- coding: utf-8 -*-

from datetime import datetime
import time
from odoo import fields, models,api


class EducationAmenities(models.AbstractModel):
    _name = 'report.education_core.report_exam_marksheet'

    def get_objects(self, objects):
        obj = []
        for object in objects:
           obj.extend(object)

        return obj

    def get_subjects(self, obj):
        subjs = []
        for subj in obj.subject_line:
            subjs.extend(subj)
        return subjs
    def get_gradings(self,obj):
        grading=self.env['education.result.grading'].search([('id','>','0')])
        grades=[]
        for grade in grading:
            grades.extend(grade)
        return grades


    def get_date(self, date):
        date1 = datetime.strptime(date, "%Y-%m-%d")
        return str(date1.month) + ' / ' + str(date1.year)

    @api.model
    def get_report_values(self, docids, data=None):
        docs = self.env['education.exam.results'].browse(docids)
        return {
            'doc_model': 'education.exam.results',
            'docs': docs,
            'time': time,
            'get_objects': self.get_objects,
            'get_subjects': self.get_subjects,
            'get_gradings':self.get_gradings,
            'get_date': self.get_date,
            # 'get_total': self.get_total,
        }
