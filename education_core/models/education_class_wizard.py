# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class ApplicationClassDetails(models.Model):
    _name = 'class.details'
    _description = "Student Allocation"

    student_class = fields.Many2one('education.class', string="Admission For", readonly=True,
                                    help="Select the Class to which the students applied")
    assigned_by = fields.Many2one('res.users', string='Assigned By', default=lambda self: self.env.uid,
                                  help="Student Assigning is done by")
    class_id = fields.Many2one('education.class.division', string="Class", required=True,
                               help="Students are alloted to this Class")
    @api.multi
    def action_assign_class(self):
        """Assign the class for the selected students after admission by the faculties"""
        # search max roll no of the class
        max_roll=self.env['education.class.history'].search([],order='roll_no asc', limit=1)
        if max_roll.roll_no:
            next_roll=max_roll.roll_no
        else:
            next_roll=0

        for rec in self:
            assign_request = self.env['education.student.class'].browse(self.env.context.get('active_ids'))
            assign_request.get_student_list()
            if not assign_request.student_list:
                raise ValidationError(_('No Student Lines'))
            for line in assign_request.student_list:
                # TODO filter previously assigned student not to assign again
                line.student_id.class_id = rec.class_id.id
                #create student history
                next_roll=next_roll+1
                self.env['education.class.history'].create({'academic_year_id': rec.class_id.academic_year_id.id,
                                                            'class_id': rec.class_id.id,
                                                            'student_id':line.student_id.id,
                                                            'roll_no': next_roll
                                                            })


            assign_request.write({
                'state': 'done',
                'admitted_class': rec.class_id.id,
                'assigned_by': rec.assigned_by.id
            })



