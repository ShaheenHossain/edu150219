# -*- coding: utf-8 -*-

from datetime import datetime
import time
from odoo import fields, models,api
import pandas as pd


class acdemicTranscript(models.AbstractModel):
    _name = 'report.education_exam.report_exam_academic_transcript'

    def get_exams(self, objects):
        obj = []
        for object in objects.exams:
           obj.extend(object)

        return obj
    def get_students(self,objects):
        student=[]
        if objects.specific_student==True :
            for stu in objects.student:
                student.extend(stu)

        return student

    def get_subjects(self, obj,result_type):
        object=self.env['education.exam.results'].browse(obj.id)
        subjs = []
        for subj in object.subject_line:
            if subj.subject_id.evaluation_type==result_type:
                subjs.extend(subj)
        return subjs
    def get_gradings(self,obj):
        grading=self.env['education.result.grading'].search([('id','>','0')],order='min_per desc',)
        grades=[]
        for grade in grading:
            grades.extend(grade)
        return grades
    def get_marks(self,exam,subject,student):
        marks=self.env['results.subject.line'].search([('exam_id','=',exam.id),('subject_id','=',subject.subject_id.id),('student_id','=',student.id)])
        return marks
    def get_highest(self,exam,subject):
        marks=self.env['results.subject.line'].search([('exam_id','=',exam.id),('subject_id','=',subject.subject_id.id)],order='mark_scored desc', limit=1)
        return marks.mark_scored

    def get_gpa(self,student,exam,evaluation_type):
        gp=0
        count=0
        records = self.env['results.subject.line'].search(
            [('exam_id', '=',exam.id ),  ('student_id', '=', student.id)])

        for rec in records:
                if rec.subject_id.evaluation_type==evaluation_type :
                    gp=gp+ rec.grade_point
                    count=count+1

        if count==0:
            return 0
        else :
            return round(gp/count,2)


    def get_merit_list(self,object,stud):
        list=[]
        stu=[]
        total_scor=[]
        exa=[]
        section=[]
        merit_class=[]
        merit_section=[]
        index=1
        student_list=[]
        for exam in object.exams:
            exa=[]
            scor=[]
            merit_class=[]
            merit_section=[]
            if index==1:
                student_list = self.env['education.class.history'].search([('level.id', '=', object.level.id)])
            for student in student_list:
                total=0
                mark_line = self.env['results.subject.line'].search(
                    [('student_id', '=', student.student_id.id), ('exam_id', '=', exam.id)])
                for line in mark_line:
                    if line.mark_scored:
                        total=total+line.mark_scored
                section.append(student.section)
                stu.append(student)
                exa.append(exam)
                scor.append(total)
                merit_class.append(0)
                merit_section.append(0)
            if index==1:
                data={'student':stu,'section':section,"exam"+ str(index) :exa,
                      'Score'+ str(index) :scor,'merit_class'+ str(index) :merit_class,'merit_section'+ str(index) :merit_section,
                      'Score': scor, 'merit_class': merit_class,
                      'merit_section' : merit_section}
                df= pd.DataFrame(data)
            else:
                df.insert(3, 'exam'+str(index), exa, allow_duplicates=False)
                df.insert(4, 'Score'+str(index), scor, allow_duplicates=False)
                df.insert(4, 'merit_class'+str(index), merit_class, allow_duplicates=False)
                df.insert(4, 'merit_section'+str(index), merit_section, allow_duplicates=False)

            result = df.sort_values(by=['Score'+str( index) ], ascending=False)
            result=result.reset_index(drop=True)
            for i in range(0,len(result)):
                df.loc[df[ 'student' ] == result.at[i,'student'], 'merit_class'+ str(index) ] = i+1
                if index>1:
                    df.loc[df[ 'student' ] == result.at[i,'student'], 'Score' ] = result.at[i,'Score']+result.at[i,'Score'+str(index)]
                # result.at[i,'merit_class']=i+1
                i=i+1
            section_list=df.section.unique()
            for rec in section_list:
                df1 = df[(df['section'] ==rec )]
                result = df1.sort_values(by=['Score'+str (index) ], ascending=False)
                result = result.reset_index(drop=True)
                for i in range(0, len(result)):
                    df.loc[df['student'] == result.at[i, 'student'], 'merit_section'+str (index) ] = i + 1
                    # result.at[i, 'merit_section'] = i + 1
                    i = i + 1
            index = index + 1
        result = df.sort_values(by=['Score'], ascending=False)
        result = result.reset_index(drop=True)
        for i in range(0, len(result)):
            df.loc[df['student'] == result.at[i, 'student'], 'merit_class'] = i + 1

            # result.at[i,'merit_class']=i+1
            i = i + 1
        section_list = df.section.unique()
        for rec in section_list:
            df1 = df[(df['section'] == rec)]
            result = df1.sort_values(by=['Score'], ascending=False)
            result = result.reset_index(drop=True)
            for i in range(0, len(result)):
                df.loc[df['student'] == result.at[i, 'student'], 'merit_section'] = i + 1
                # result.at[i, 'merit_section'] = i + 1
                i = i + 1

        k=df.loc[df['student'] == stud.id, 'merit_section'].values[0]
        return df.loc[df['student'] == stud.id, 'merit_section'].values[0]

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
            'get_marks': self.get_marks,
            'get_highest': self.get_highest,
            'get_gpa': self.get_gpa,
            'get_merit_list': self.get_merit_list,
            # 'get_total': self.get_total,
        }
