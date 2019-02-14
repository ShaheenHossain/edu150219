# -*- coding: utf-8 -*-

from odoo.exceptions import ValidationError
from odoo import fields, models, api, _

class educationClassSection(models.Model):
    _name='education.class.section'
    _description='Sections'
    name=fields.Char('Section')
    level_ids=fields.Many2many('education.class',column1='level_ids',column2='section_ids')
    classes_ids=fields.Many2many('education.class','section_ids',string='Classes')
class EducationClass(models.Model):
    _name = 'education.class'
    _description = "Standard"
    sequence=fields.Integer("Sequence")
    section_ids=fields.Many2many('education.class.section',column2='level_ids',column1='section_ids',string='Sections')
    name = fields.Char(string='Name', required=True, help="Enter the Name of the Class")
    code = fields.Char(string='Code', required=True, help="Enter the Code of the Class")
    syllabus_ids = fields.One2many('education.syllabus', 'class_id')
    # division_ids = fields.Many2many('education.division''class_id', 'class_id')
    division_ids=fields.Many2many('education.division','class_dev_rel','division_ids','classes_ids')
    division_count=fields.Integer('Total Group',compute='_division_count')
    section_count=fields.Integer('Total Sections',compute='_division_count')
    @api.multi
    def _division_count(self):
        """Return the count of the division in the level"""
        for rec in self:
            rec.division_count = len(self.division_ids)
            rec.section_count = len(self.section_ids)

    def view_division(self):
        """Return the list of current students in this class"""
        self.ensure_one()
        divisions = self.env['education.division'].search([('classes_ids', '=', self.id)])
        divisions_list = divisions.mapped('id')
        return {
            'domain': [('id', 'in', divisions_list)],
            'name': _('Divisions'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'education.division',
            'view_id': False,
            # 'context': {'default_classes_ids': self.id},
            'type': 'ir.actions.act_window'
        }
class EducationDivision(models.Model):
    _name = 'education.division'
    _description = "Standard Division"

    name = fields.Char(string='Name', required=True, help="Enter the Name of the Division")
    code = fields.Char(string='Code', required=True, help="Enter the Code of the Division")
    strength = fields.Integer(string='Max Student No',default='100', help="Total strength of the class")
    faculty_id = fields.Many2one('education.faculty', string='Class Faculty', help="Class teacher/Faculty")
    classes_ids = fields.Many2many('education.class','class_dev_rel','classes_ids','division_ids', string='Class')



class EducationClassDivision(models.Model):
    _name = 'education.class.division'
    _description = "Class room"

    name = fields.Char(string='Name', readonly=True)
    display=fields.Char('Class Name')
    actual_strength = fields.Integer(string='Max student No', help="Total strength of the class")
    faculty_id = fields.Many2one('education.faculty', string='Class Teacher', help="Class teacher/Faculty")
    academic_year_id = fields.Many2one('education.academic.year', string='Academic Year',
                                       help="Select the Academic Year", required=True)
    class_id = fields.Many2one('education.class', string='Class', required=True,
                               help="Select the Class")
    division_id = fields.Many2one('education.division', string='Division',help="Select the Division")
    section_id = fields.Many2one('education.class.section', string='Section', help="Select the Section")
    student_ids = fields.One2many('education.student', 'class_id', string='Students')
    amenities_ids = fields.Char( string='Amenities')
    student_count = fields.Integer(string='Students Count', compute='_get_student_count')
    class_room=fields.Many2one('education.rooms','Room No')
    @api.model
    def create(self, vals):
        """Return the name as a str of class + division"""
        # res = super(EducationClassDivision, self).create(vals)
        class_id = self.env['education.class'].browse(vals['class_id'])
        division_id = self.env['education.division'].browse(vals['division_id'])
        section_id = self.env['education.class.section'].browse(vals['section_id'])
        batch = self.env['education.academic.year'].browse(vals['academic_year_id'])
        className=''
        divisionName=''
        sectionName=''
        batchName=batch.ay_code
        if class_id.id>0:
            className=class_id.name
        if division_id.id>0:
            divisionName=division_id.name
        if section_id.id>0:
            sectionName=section_id.name
        name = str(className + '-' + divisionName+ '-' + sectionName+ '-' + batchName)
        vals['name'] = name
        return super(EducationClassDivision, self).create(vals)

    @api.multi
    def view_students(self):
        """Return the list of current students in this class"""
        self.ensure_one()
        students = self.env['education.student'].search([('class_id', '=', self.id)])
        students_list = students.mapped('id')
        return {
            'domain': [('id', 'in', students_list)],
            'name': _('Students'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'education.student',
            'view_id': False,
            'context': {'default_class_id': self.id},
            'type': 'ir.actions.act_window'
        }

    def _get_student_count(self):
        """Return the number of students in the class"""
        for rec in self:
            students = self.env['education.student'].search([('class_id', '=', rec.id)])
            student_count = len(students) if students else 0
            rec.update({
                'student_count': student_count
            })

    @api.constrains('actual_strength')
    def validate_strength(self):
        """Return Validation error if the students strength is not a non-zero number"""
        for rec in self:
            if rec.actual_strength <= 0:
                raise ValidationError(_('Max Student No must be greater than Zero'))

    _sql_constraints=[
        ('ad_no', 'unique(name)', "class should be unique!"),
    ]

class EducationClassDivisionHistory(models.Model):
    _name = 'education.class.history'
    _description = "Student Class history"
    _rec_name = 'class_id'

    academic_year_id = fields.Many2one('education.academic.year', string='Academic Year',
                                       help="Select the Academic Year")
    class_id = fields.Many2one('education.class.division', string='Class',
                               help="Select the class")
    level=fields.Many2one('education.class',string='level',related='class_id.class_id',store=True) #related='class_id.class_id'
    section=fields.Many2one('education.class.section',string='section',related='class_id.section_id') #
    from_date=fields.Date('From')
    till_date=fields.Date('Till')
    student_id = fields.Many2one('education.student', string='Students')
    roll_no=fields.Integer('Roll No',required=True)
    compulsory_subjects=fields.Many2many('education.syllabus','education_syllabus_class_history_rel',
                                         'compulsory_subjects','compulsory_for',string='Compulsory')
    selective_subjects=fields.Many2many('education.syllabus','education_syllabus_class_history_1_rel',
                                        'selective_subjects','selective_for',string='Selective')
    optional_subjects=fields.Many2many('education.syllabus','education_syllabus_class_history_optional_rel',
                                        'optional_subjects','optional_for',string='Optional')
    # selective_subjects=fields.Many2many('education.syllabus','selective_for',string='Selective')
    # optional_subjects=fields.Many2many('education.syllabus','optional_for',string='Optional')
    _sql_constraints = [
        ('student_class_history', 'unique(academic_year_id,student_id)', "Student mustbe Unique for a year"),
        ('student_class_history', 'unique(academic_year_id,class_id,roll_no)', "Roll no must be qnique for Class"),
    ]


class EducationClassAmenities(models.Model):
    _name = 'education.class.amenities'
    _description = "Amenities in Class"

    name = fields.Many2one('education.amenities', string="Amenities",
                           help="Select the amenities in class room")
    qty = fields.Float(string='Quantity', help="The quantity of the amenities", default=1.0)
    room_id = fields.Many2one('education.rooms', string="Class Room")

    @api.constrains('qty')
    def check_qty(self):
        """returns validation error if the qty is 0 or negative"""
        for rec in self:
            if rec.qty <= 0:
                raise ValidationError(_('Quantity must be Positive'))
