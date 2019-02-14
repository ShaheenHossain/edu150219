# -*- coding: utf-8 -*-
from odoo import http

# class Eschool(http.Controller):
#     @http.route('/eschool/eschool/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/eschool/eschool/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('eschool.listing', {
#             'root': '/eschool/eschool',
#             'objects': http.request.env['eschool.eschool'].search([]),
#         })

#     @http.route('/eschool/eschool/objects/<model("eschool.eschool"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('eschool.object', {
#             'object': obj
#         })