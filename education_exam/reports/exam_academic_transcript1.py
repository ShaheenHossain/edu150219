# -*- coding: utf-8 -*-

from datetime import datetime
import time
from odoo import fields, models,api


class acdemicTranscript1(models.AbstractModel):
    _name = 'report.education_exam.report_exam_academic_transcript1'

    def get_exams(self, objects):
        obj = []
        for object in objects.exams:
           obj.extend(object)

        return obj
    def get_students(self,objects):

        student=[]
        if objects.specific_student==True :
            student_list = self.env['education.class.history'].search([('student_id.id', '=', objects.student.id),('academic_year_id.id', '=', objects.academic_year.id)])
            for stu in student_list:
                student.extend(stu)
        elif objects.section:
            student_list=self.env['education.class.history'].search([('class_id.id', '=', objects.section.id)])
            for stu in student_list:
                student.extend(stu)
        elif objects.level:
            student_list = self.env['education.class.history'].search([('level.id', '=', objects.level.id),
                                                                       ('academic_year_id.id', '=', objects.academic_year.id)])
            for stu in student_list:
                student.extend(stu)

        return student

    def get_subjects(self,student,object):
        student_history=self.env['education.class.history'].search([('id', '=', student.id),('academic_year_id',"=",object.academic_year.id)])
        subjs = []
        for subj in student_history.compulsory_subjects:
            subjs.extend(subj)
        for subj in student_history.selective_subjects:
            subjs.extend(subj)
        for subj in student_history.optional_subjects:
            subjs.extend(subj)
        return subjs
    def get_gradings(self,obj):
        grading=self.env['education.result.grading'].search([('id','>','0')],order='min_per desc',)
        grades=[]
        for grade in grading:
            grades.extend(grade)
        return grades
    def get_marks(self,exam,subject,student_history):
        student=student_history.student_id
        marks=self.env['results.subject.line'].search([('exam_id','=',exam.id),('subject_id','=',subject.id),('student_id','=',student.id)])
        return marks
    def get_highest(self,exam,subject):
        highest = self.env['results.subject.line'].search(
            [('exam_id', '=', exam.id), ('subject_id', '=', subject.id)], limit=1, order='mark_scored DESC')
        return highest
    def get_gpa(self,student_history,exam):
        student = student_history.student_id
        gp=0
        count=0
        records = self.env['results.subject.line'].search(
            [('exam_id', '=',exam.id ),  ('student_id', '=', student.id)])
        for rec in records:
            gp=gp+ rec.grade_point
            count=count+1


        return float("{0:.2f}".format(gp/count))
    def get_row_count(self,student_history,exam):
        student = student_history.student_id
        count=0
        records = self.env['results.subject.line'].search(
            [('exam_id', '=',exam.id ),  ('student_id', '=', student.id)])
        for rec in records:
            count=count+1
        return count
    def get_date(self, date):
        date1 = datetime.strptime(date, "%Y-%m-%d")
        return str(date1.month) + ' / ' + str(date1.year)

    @api.model
    def get_report_values(self, docids, data=None):
        docs = self.env['academic.transcript'].browse(docids)
        return {
            'doc_model': 'education.exam.results',
            'docs': docs,
            'time': time,
            'get_students': self.get_students,
            'get_exams': self.get_exams,
            'get_subjects': self.get_subjects,
            'get_gradings':self.get_gradings,
            'get_marks':self.get_marks,
            'get_date': self.get_date,
            'get_highest': self.get_highest,
            'get_gpa': self.get_gpa,
            'get_row_count': self.get_row_count,
            # 'get_total': self.get_total,
        }
