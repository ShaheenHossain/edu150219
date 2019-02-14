# -*- coding: utf-8 -*-
from odoo import http

# class EschoolSms(http.Controller):
#     @http.route('/eschool_sms/eschool_sms/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/eschool_sms/eschool_sms/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('eschool_sms.listing', {
#             'root': '/eschool_sms/eschool_sms',
#             'objects': http.request.env['eschool_sms.eschool_sms'].search([]),
#         })

#     @http.route('/eschool_sms/eschool_sms/objects/<model("eschool_sms.eschool_sms"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('eschool_sms.object', {
#             'object': obj
#         })