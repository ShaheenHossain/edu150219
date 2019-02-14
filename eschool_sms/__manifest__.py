# -*- coding: utf-8 -*-
{
    'name': "eschool_sms",

    'summary': """
        Intigrate EagleSMS to escool""",

    'description': """
        Long description of module's purpose
    """,

    'author': "SM Ashraf",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'SMS',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sms_frame','education_core','education_attendances','eschool','eagle_mass_sms'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/attendance.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}