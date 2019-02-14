# -*- coding: utf-8 -*-
{
    'name': "dsblsc",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
# 'data/Class1-A/education.application.csv',
#         'data/Class1-B/education.application.csv',
#         'data/Class1-C/education.application.csv',
#         'data/Class2-A/education.application.csv',
#         'data/Class2-B/education.application.csv',
#         'data/Class2-C/education.application.csv',
#         'data/Class3-A/education.application.csv',
#         'data/Class3-B/education.application.csv',
#         'data/Class3-C/education.application.csv',
#         'data/Class4-A/education.application.csv',
#         'data/Class4-B/education.application.csv',
#         'data/Class5-A/education.application.csv',
#         'data/Class5-B/education.application.csv',
        'data/sms.number.csv',
        'data/sms.template.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}