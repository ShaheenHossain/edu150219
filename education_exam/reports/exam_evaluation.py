# -*- coding: utf-8 -*-

from datetime import datetime
import time
from odoo import fields, models,api


class examEvaluation(models.AbstractModel):
    _name = 'report.education_exam.report_exam_evaluation'
    def get_sections(self,object):
        sections=[]

        if object.section:
            return object.section
        elif object.level:
            section=self.env['education.class.division'].search([('class_id','=',object.level.id),('academic_year_id','=',object.academic_year.id)])
            return section
    def get_exams(self, objects):
        exams = []
        for exam in objects.exams:
           exams.extend(exam)

        return exams

    def get_students(self,objects):

        student=[]
        student_list=self.env['education.class.history'].search([('class_id.id', '=', objects.id)])
        for stu in student_list:
            student.extend(stu.student_id)
        return student
    def get_subjects(self, section,obj):
        subjs=self.env['education.syllabus'].search([('class_id','=',section.class_id.id),('academic_year','=',obj.academic_year.id)])
        subject_list=[]
        for subj in subjs:
            if len(subj.compulsory_for)>0:
                subject_list.append(subj)
            elif len(subj.optional_for)>0:
                subject_list.append(subj)
            elif len(subj.optional_for)>0:
                subject_list.append(subj)

        return subject_list
    def check_optional(self,subject,student,exam):
        is_optional=0
        student_history = self.env['education.class.history'].search(
            [('student_id', '=', student.id), ('academic_year_id', '=', exam.academic_year.id)])
        optional_subject=student_history.optional_subjects
        for sub in optional_subject:
            if sub.id==subject.id:
                is_optional=1


        return is_optional
    def get_marks(self,exam,subject,student):
        marks=self.env['results.subject.line'].search([('exam_id','=',exam.id),('subject_id','=',subject.id),('student_id','=',student.id)])
        return marks

    def get_exam_obtained_total(self, exam, student_history, optional, evaluation):
        grand_total = self.env['report.education_exam.report_exam_academic_transcript_s'].get_exam_obtained_total( exam,
                                                                                                                   student_history,
                                                                                                                   optional,
                                                                                                                    evaluation)
        return grand_total

    def get_exam_total(self,exam,student_history,optional,evaluation):
        grand_total=self.env['report.education_exam.report_exam_academic_transcript_s'].get_exam_total(exam,student_history,optional,evaluation)
        return grand_total

    def get_gpa(self, student_history, exam, optional, evaluation_type):
        gpa = self.env['report.education_exam.report_exam_academic_transcript_s'].get_gpa(student_history,exam,optional,evaluation_type)
        return gpa
    def get_lg(self, student_history, exam, optional, evaluation_type):
        gpa = self.env['report.education_exam.report_exam_academic_transcript_s'].get_gpa(student_history,exam,optional,evaluation_type)
        grades = self.env['education.result.grading'].search([('score', '<=', gpa)] ,limit=1, order='score DESC')

        gpa = grades.result
        return gpa


    def get_gradings(self,obj):
        grading=self.env['education.result.grading'].search([('id','>','0')],order='min_per desc',)
        grades=[]
        for grade in grading:
            grades.extend(grade)
        return grades


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
            'get_date': self.get_date,
            'get_sections': self.get_sections,
            'get_marks': self.get_marks,
            'get_gpa': self.get_gpa,
            'get_lg': self.get_lg,
            'get_exam_obtained_total': self.get_exam_obtained_total,
            'check_optional': self.check_optional,
        }
