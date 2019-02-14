# -*- coding: utf-8 -*-

from datetime import datetime
import time
from odoo import fields, models,api



class examStudent(models.Model):
    _name ="exam.student.details"

    exam_id=fields.Many2one('education.exam',"Exam")
    student_id=fields.Many2one('education.student',"GPA")
    total=fields.Float("Obtained")
    merit_class=fields.Integer("Position In Class")
    merit_section=fields.Integer("Position In section")
    attendance=fields.Float("Attendance")


class examsyllabus(models.Model):
    _name = "exam.syllabus.details"

    exam_id = fields.Many2one('education.exam', "Exam")
    syllabus_id = fields.Many2one('education.syllabus', "Subject")
    class_highest = fields.Float("Highest In Class")
    section_highest = fields.Float("Highest In Section")
