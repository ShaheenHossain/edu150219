# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError

class AcademyRoomNo(models.Model):
    _name='education.rooms'
    name=fields.Char('Room Name')
    code=fields.Integer('Room No')
    capacity=fields.Integer('Capacity')
    amenities_ids = fields.One2many('education.class.amenities', 'room_id', string='Amenities')
class EducationAcademic(models.Model):
    _name = 'education.academic.year'
    _description = 'Academic Year'
    _order = 'sequence asc'
    _rec_name = 'name'

    @api.model
    def create(self, vals):
        """Over riding the create method and assigning the 
        sequence for the newly creating record"""
        vals['sequence'] = self.env['ir.sequence'].next_by_code('education.academic.year')
        res = super(EducationAcademic, self).create(vals)
        return res

    @api.multi
    def unlink(self):
        """return validation error on deleting the academic year"""
        for rec in self:
            raise ValidationError(_("Academic Year can not be deleted, You only can Archive it."))

    name = fields.Char(string='Name', required=True, help='Name of academic year')
    ay_code = fields.Char(string='Code', required=True, help='Code of academic year')
    sequence = fields.Integer(string='Sequence', required=True)
    ay_start_date = fields.Date(string='Start date', required=True, help='Starting date of academic year')
    ay_end_date = fields.Date(string='End date', required=True, help='Ending of academic year')
    ay_description = fields.Text(string='Description', help="Description about the academic year")
    active = fields.Boolean('Active', default=True,
                            help="If unchecked, it will allow you to hide the Academic Year without removing it.")

    _sql_constraints = [
        ('ay_code', 'unique(ay_code)', "Code already exists for another academic year!"),
    ]

    @api.constrains('ay_start_date', 'ay_end_date')
    def validate_date(self):
        """Checking the start and end dates of the syllabus,
        raise warning if start date is not anterior"""
        for rec in self:
            if rec.ay_start_date >= rec.ay_end_date:
                raise ValidationError(_('Start date must be Anterior to End date'))
