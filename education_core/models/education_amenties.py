# -*- coding: utf-8 -*-


from odoo import fields, models


class EducationAmenities(models.Model):
    _name = 'education.amenities'
    _description = 'Amenities in Institution'
    _order = 'name asc'
    _rec_name = 'name'

    name = fields.Char(string='Name', required=True, help='Name of amenity')
    code = fields.Char(string='Code', help='Code of amenity')

    _sql_constraints = [
        ('code', 'unique(code)', "Another Amenity already exists with this code!"),
    ]
