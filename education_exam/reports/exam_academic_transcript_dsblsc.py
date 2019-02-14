# -*- coding: utf-8 -*-

from datetime import datetime
import time
from odoo import fields, models,api
import pandas as pd
import numpy


class acdemicTranscripts(models.AbstractModel):
    _name = 'report.education_exam.report_exam_academic_transcript_dsblsc'
    def get_student_marks(self,student):
        student_or_history = getattr(student_history.student_id, 'id', 'history')
        if student_or_history == 'history':
            student = student_history
            student_history = self.env['education.class.history'].search(
                [('student_id', '=', student.id), ('academic_year_id', '=', exam.academic_year.id)])
        else:
            student = student_history.student_id
        results=self.env['education.exam.results'].search([()])



    def get_results(self,student,exam):
        results=self.env['education.exam.results'].search([('exam_id','=',exam.id),('student_id','=',student.id)])
        for result in results:
            return result

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

    def get_subjects(self,student,object,selection_type,evaluation_type):
        student_history=self.env['education.class.history'].search([('id', '=', student.id),('academic_year_id',"=",object.academic_year.id)])
        subjs = []
        if selection_type=='non_optional':
            for subj in student_history.compulsory_subjects:
                if subj.evaluation_type==evaluation_type :
                    subjs.extend(subj)
            for subj in student_history.selective_subjects:
                if subj.evaluation_type==evaluation_type:
                    subjs.extend(subj)
        else:
            for subj in student_history.optional_subjects:
                subjs.extend(subj)

        return subjs

    def get_subject_group(self,syllabuses):
        groups={}
        for sub in syllabuses:
            subj_id=sub.subject_id
            if groups.get(subj_id)==None:
                groups[subj_id]=[1,sub]
            else:
                groups[subj_id][0]=groups[subj_id][0]+1
                groups[subj_id].append(sub)
        return groups

    def get_paper_total(self,subject,exam,student_history,subjects):
        papers=[]
        total=0
        for subj in subjects:
            if subj.subject_id==subject.subject_id:
                papers.append(subj)
        for paper in papers:
            mark=self.get_marks( exam, paper, student_history)
            total=total+mark.mark_scored
        return total

    def paper_highest(self,subject,exam,subjects):
        papers = []
        total = 0
        for subj in subjects:
            if subj.subject_id == subject.subject_id:
                papers.append(subj)
        for paper in papers:
            mark=self.get_highest(exam, subject)
            total=total+ mark.mark_scored
        return total

    def paper_grade_point(self,subject,exam,student_history,subjects):
        papers = {}
        grade_point=0
        count=0
        gp = 0
        obtained=0
        fulmark=0
        for subj in subjects:
            if subj.subject_id == subject.subject_id:
                if subj.subject_id not in papers:
                    papers[subj.subject_id]=[]
                papers[subj.subject_id].append(subj)
                count=count+1

        for main_subject, syllabus in papers.items():
            total = 0
            pass_mark = 0
            if main_subject.id==2 : # main subject.id 2 is used for english
                for rec in papers[main_subject]:
                    mark = self.get_marks(exam, rec, student_history)
                    total = total + mark.mark_scored
                    pass_mark=pass_mark+mark.pass_mark
                    obtained=obtained+mark.mark_scored
                    fulmark = fulmark + mark.max_mark
                if pass_mark > total:
                    return 0
            elif main_subject.id==6: #main_subject.id 6 is for ICT
                for rec in papers[main_subject]:
                    mark = self.get_marks(exam, rec, student_history)
                    total = total + mark.mark_scored
                    pass_mark = pass_mark + mark.pass_mark
                    obtained = obtained + mark.mark_scored
                    fulmark = fulmark + mark.max_mark
                    if rec.tut_pass > mark.tut_mark:
                        return 0
                    if rec.subj_pass > mark.subj_mark:
                        return 0
                    if rec.obj_pass > mark.obj_mark:
                        return 0
                    if rec.prac_pass > mark.prac_mark:
                        return 0
                    if mark.prac_mark+mark.obj_mark<17:
                        return 0
            else:
                for rec in papers[main_subject]:
                    mark = self.get_marks(exam, rec, student_history)
                    total = total + mark.mark_scored
                    pass_mark = pass_mark + mark.pass_mark
                    fulmark = fulmark + mark.max_mark
                    obtained = obtained + mark.mark_scored
                    if rec.tut_pass> mark.tut_mark:
                        return 0
                    if rec.subj_pass> mark.subj_mark:
                        return 0
                    if rec.obj_pass> mark.obj_mark:
                        return 0
                    if rec.prac_pass> mark.prac_mark:
                        return 0
            if fulmark!=0:
                per_obtained = ((obtained * 100) / fulmark)
                grades = self.env['education.result.grading'].search([['id', '>', '0']])
                for gr in grades:
                    if gr.min_per <= per_obtained and gr.max_per >= per_obtained:
                        grade_point = gr.score
        return grade_point

    def get_optional_subjects(self,student_history,object):
        # student_history = self.env['education.class.history'].search(
        #     [('id', '=', student.id), ('academic_year_id', "=", object.academic_year.id)])
        subjs = []
        for subj in student_history.optional_subjects:
            subjs.extend(subj)
        return subjs

    def count_subjects(self,student_history,object,optional):
        count = 0
        if optional=='optional':
            for subj in student_history.optional_subjects:
                count=count+0
        else:
            for subj in student_history.compulsory_subjects:
                count = count + 0
            for subj in student_history.selective_subjects:
                count = count + 0
        return count

    def get_leter_grade(self,grade_point):
        grades = self.env['education.result.grading'].search([('score', '<=', grade_point)], limit=1, order='score DESC')
        return grades.result

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

    def get_exam_obtained_total(self,exam,student_history,optional,evaluation):
        student_or_history=getattr(student_history.student_id,'id','history')
        if student_or_history=='history':
            student = student_history
            student_history=self.env['education.class.history'].search([('student_id','=',student.id),('academic_year_id','=',exam.academic_year.id)])
        else: student = student_history.student_id
        marks = self.env['results.subject.line'].search(
            [('exam_id', '=', exam.id),('student_id', '=', student.id)])
        total=0
        general_total=0
        extra_total=0
        optional_total=0
        for subject in marks:
            if subject.subject_id in student_history.optional_subjects:
                optional_total=optional_total+ subject.mark_scored
            elif subject.subject_id.evaluation_type == 'general':
                    general_total=general_total+ subject.mark_scored
            elif subject.subject_id.evaluation_type=='extra':
                        extra_total=extra_total+subject.mark_scored
        if optional=='all':
            additional=self.get_exam_total(exam,student_history,'optional','general')
            if additional>0:
                sur_plus=optional_total-(additional*40/100)
                if sur_plus>0:
                    return int(sur_plus+general_total)
                else: return general_total
            else:
                return general_total

        if optional == 'optional':
            return optional_total
        elif evaluation == 'general':
            return general_total
        elif evaluation == 'extra':
            return extra_total
    def check_pass_fail(self,exam,subject,student):
        fail=0
        if isinstance(subject, list):
            x=1
        else:
            #do for single subject

            mark=self.get_marks( exam, subject, student)
            if mark.tut_mark <mark.subject_id.tut_pass:
                fail=fail+1
            if mark.prac_mark <mark.subject_id.prac_pass:
                fail = fail + 1
            if mark.subj_mark <mark.subject_id.subj_pass:
                fail = fail + 1
            if mark.obj_mark <mark.subject_id.obj_pass:
                fail = fail + 1
        if fail>0:
            return "fail"
        else:
            return"pass"



    def get_exam_total(self,exam,student_history,optional,evaluation):
        student = student_history.student_id
        marks = self.env['results.subject.line'].search(
            [('exam_id', '=', exam.id), ('student_id', '=', student.id)])
        total = 0
        optional_total=0
        extra_total=0
        general_total=0

        for subject in marks:
            if subject.subject_id in student_history.optional_subjects:
                optional_total = optional_total + subject.subject_id.total_mark

            elif subject.subject_id not in student_history.optional_subjects:
                if subject.subject_id.evaluation_type == 'general':
                    general_total = general_total + subject.subject_id.total_mark
                elif subject.subject_id.evaluation_type == 'extra':
                    extra_total = extra_total + subject.subject_id.total_mark
        if optional=='optional':
            return optional_total
        elif evaluation=='general':
            return general_total
        elif evaluation=='extra':
            return extra_total
        elif optional=='all':
            return total

    def get_highest(self,exam,subject):
        highest = self.env['results.subject.line'].search(
            [('exam_id', '=', exam.id), ('subject_id', '=', subject.id)], limit=1, order='mark_scored DESC')
        return highest

    def get_gpa(self,student_history,exam,optional,evaluation_type,subjects):
        student_or_history = getattr(student_history.student_id, 'id', 'history')
        if student_or_history == 'history':
            student = student_history
            student_history = self.env['education.class.history'].search(
                [('student_id', '=', student.id), ('academic_year_id', '=', exam.academic_year.id)])
        else:
            student = student_history.student_id
        gp=0
        s_count=0
        optional_gp=0
        o_count=0
        extra_gp=0
        extra_count=0
        general_gp=0
        paper_group=[]
        general_count=0
        records = self.env['results.subject.line'].search(
            [('exam_id', '=',exam.id ),  ('student_id', '=', student.id)])

        for rec in records:
            if rec.subject_id in student_history.optional_subjects:
                optional_gp = optional_gp + rec.grade_point
                o_count = o_count + 1
            elif rec.subject_id.evaluation_type == 'general':
                if rec.subject_id.subject_id not in paper_group:
                    paper_group.append(rec.subject_id.subject_id)
                    general_gp=general_gp+self.paper_grade_point(rec.subject_id, exam, student_history, subjects)

                    general_count = general_count + 1
            else:
                extra_gp = extra_gp + rec.grade_point
                extra_count = extra_count + 1
        if optional=='all':
            if o_count!=0:
                # since optional  gpa over 2 is added
                additional_gp=(optional_gp/o_count)-2
                if additional_gp<0:
                    additional_gp=0
                gp=(general_gp+additional_gp)/general_count
                if gp>5:
                    return 5
                else:
                    return round(gp,2)
            else:
                gp=general_gp
                gpa= round(gp/general_count,2)
                if gpa>4.99:
                    gpa=5
                return gpa

        elif optional =="optional":
            if o_count!=0:
                return round(optional_gp/o_count,2)
            else: return 0
        elif evaluation_type =="extra":
            if extra_count!=0:
                return round(extra_gp/extra_count,2)
            else: return 0
        elif evaluation_type =="general":
            if general_count!=0:
                return round(general_gp/general_count,2)
            else: return 0

    def get_merit_list(self,object):
        list=[]
        stu=[]
        total_scor=[]
        exa=[]
        section=[]
        merit_class=[]
        merit_section=[]
        exam_list=[]
        exam_sl=1
        student_list = self.env['education.class.history'].search([('level.id', '=', object.level.id)])
        for exam in object.exams:
            exam_list.append(exam.id)
            exa=[]
            scor=[]
            merit_class=[]
            merit_section=[]
            fail_in_extra=[]

            for student in student_list:
                obtained_total=0
                optional_obtained=0
                extra_obtained=0
                optional_count=0
                optional_total=0
                fail_extra=0
                mark_line = self.env['results.subject.line'].search(
                    [('student_id', '=', student.student_id.id), ('exam_id', '=', exam.id)])
                for line in mark_line:
                    # filter the subject is not optional for the student
                    if line.subject_id  not in student.optional_subjects:
                        if line.subject_id.evaluation_type != 'extra':
                            if line.mark_scored:
                                obtained_total=obtained_total+line.mark_scored
                        elif line.mark_scored:
                            extra_obtained=extra_obtained+line.mark_scored
                            if line.letter_grade=='F':
                                fail_extra=1

                    elif line.mark_scored:  #calculate optiional Marks
                        optional_count=optional_count+1
                        optional_total=optional_total+line.subject_id.total_mark
                        optional_obtained=optional_obtained+line.mark_scored
                additional_mark=optional_obtained-(optional_total*0.4)  # calculate optional mark over 40%
                if additional_mark>0:
                    obtained_total=obtained_total+additional_mark
                section.append(student.section.id)
                stu.append(student.student_id.id)
                exa.append(exam.id)
                scor.append(obtained_total)
                merit_class.append(0)
                merit_section.append(0)
                fail_in_extra.append(fail_extra)
            if exam_sl==1:
                data={'student':stu,
                      'section':section,"exam"+ str(exam.id) :exa,
                      'score'+ str(exam.id) :scor,
                      'merit_class'+ str(exam.id) :merit_class,
                      'merit_section'+ str(exam.id) :merit_section,
                      'score': 0,
                      'merit_class': merit_class,
                      'merit_section' : merit_section,
                      'fail_in_extra'+ str(exam.id) :merit_class,
                      'fail_in_extra':merit_class}
                df= pd.DataFrame(data)
            else:
                df.insert(3, 'exam'+str(exam.id), exa, allow_duplicates=False)
                df.insert(4, 'score'+str(exam.id), scor, allow_duplicates=False)
                df.insert(4, 'merit_class'+str(exam.id), merit_class, allow_duplicates=False)
                df.insert(4, 'merit_section'+str(exam.id), merit_section, allow_duplicates=False)
                df.insert(4, 'fail_in_extra'+str(exam.id), fail_in_extra, allow_duplicates=False)
            exam_sl+=1
        if len(exam_list)>0: #if more than one exam 0 will represent the combined result
            exam_list.append(0)
        section_list = df.section.unique()
        sections=[]
        for section in section_list:
            sections.append(section)
        sections.append(0)


        # calculate merit list
        exam_name=''
        for  exam in exam_list:
            if exam!=0:
                exam_name=str(exam)
                for index, row in df.iterrows():
                    df.loc[df['student'] == row['student'], 'score'] = row['score'] + row['score' + exam_name]
                    if row['fail_in_extra' + exam_name] != 0:
                        df.loc[df['student'] == row['student'], 'fail_in_extra'] = 1
            else:exam_name=''


            for section in sections:
                if section ==0:
                    df1=df
                    merit='merit_class'
                else:
                    merit = 'merit_section'
                    df1 = df[(df['section'] == section)]
                result = df1.sort_values(by=['score' + exam_name], ascending=False)
                in_place = 0
                out_place = 10
                for index,row in result.iterrows():
                    if in_place < 10:
                        if row['fail_in_extra'+exam_name] == 0:  # check if the student not failed in extra subject
                            in_place = in_place + 1
                            place=in_place
                        else:  # as failed in extra should be placed after 10
                            out_place = out_place + 1
                            place=out_place
                    else:  # after place 10 extra fail check not necesary
                        out_place = out_place + 1
                        place = out_place
                    df.loc[df['student'] == row[ 'student'], merit + exam_name] = place

        return df

    def num2serial(self,numb):
        if numb < 20:  # determining suffix for < 20
            if numb == 1:
                suffix = 'st'
            elif numb == 2:
                suffix = 'nd'
            elif numb == 3:
                suffix = 'rd'
            else:
                suffix = 'th'
        else:  # determining suffix for > 20
            tens = str(numb)
            tens = tens[-2]
            unit = str(numb)
            unit = unit[-1]
            if tens == "1":
                suffix = "th"
            else:
                if unit == "1":
                    suffix = 'st'
                elif unit == "2":
                    suffix = 'nd'
                elif unit == "3":
                    suffix = 'rd'
                else:
                    suffix = 'th'
        return str(numb) + suffix

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
            'get_merit_list':self.get_merit_list,
            'get_date': self.get_date,
            'get_highest': self.get_highest,
            'get_gpa': self.get_gpa,
            'get_row_count': self.get_row_count,
            'get_optional_subjects': self.get_optional_subjects,
            'get_exam_total': self.get_exam_total,
            'get_exam_obtained_total': self.get_exam_obtained_total,
            'count_subjects': self.count_subjects,
            'num2serial': self.num2serial,
            'get_paper_total': self.get_paper_total,
            'get_subject_group': self.get_subject_group,
            'paper_highest': self.paper_highest,
            'get_results': self.get_results,
            'get_leter_grade': self.get_leter_grade,
            'paper_grade_point': self.paper_grade_point,
            'check_pass_fail': self.check_pass_fail,
        }
