# -*- coding: utf-8 -*-

from odoo import models, fields, api

class examtabulationwizard(models.Model):
    _inherit = 'res.partner'
    name_b=fields.Char("নামের প্রথম অংশ")
    # middle_name=fields.Char('Middle Name')
    # last_name=fields.Char('Last Name')
    # middle_name_b=fields.Char("নামের মধ্যাংশ")
    # last_name_b=fields.Char("নামের শেষাংশ")
    nid_no=fields.Char('NID No')
    car_no=fields.Char('Car No')
    gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('other', 'Other')],
                              string='Gender', required=True, default='male', track_visibility='onchange')

    _sql_constraints = [
        ('nid_no', 'unique(nid_no)', "NID number must be unique!"),
    ]