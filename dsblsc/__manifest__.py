# -*- coding: utf-8 -*-
{
    'name': "dsblsc12",

    'summary': """
        This app is designed to import Dhaka Shikhsa Bord School's data """,

    'description': """
       This app is designed to import Dhaka Shikhsa Bord School's data 
    """,

    'author': "SM Ashraf",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','education_core','sms_frame','eschool_sms','eagle_mass_sms'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/all_student_2018/class_1/A/education.application.csv',
        'data/all_student_2018/class_1/B/education.application.csv',
        'data/all_student_2018/class_1/C/education.application.csv',
        'data/all_student_2018/class_2/A/education.application.csv',
        'data/all_student_2018/class_2/B/education.application.csv',
        'data/all_student_2018/class_2/C/education.application.csv',
        'data/all_student_2018/class_3/A/education.application.csv',
        'data/all_student_2018/class_3/B/education.application.csv',
        'data/all_student_2018/class_3/C/education.application.csv',
        'data/all_student_2018/class_4/A/education.application.csv',
        'data/all_student_2018/class_4/B/education.application.csv',
        'data/all_student_2018/class_5/A/education.application.csv',
        'data/all_student_2018/class_5/B/education.application.csv',
        'data/all_student_2018/class_6/A/education.application.csv',
        'data/all_student_2018/class_6/B/education.application.csv',
        'data/all_student_2018/class_7/A/education.application.csv',
        'data/all_student_2018/class_7/B/education.application.csv',
        'data/all_student_2018/class_8/A/education.application.csv',
        'data/all_student_2018/class_8/B/education.application.csv',
        'data/all_student_2018/class_9/A/education.application.csv',
        'data/all_student_2018/class_9/B/education.application.csv',
        'data/all_student_2018/class_9/C/education.application.csv',
        'data/all_student_2018/class_9/H/education.application.csv',
        'data/all_student_2018/class_10/A/education.application.csv',
        'data/all_student_2018/class_10/B/education.application.csv',
        'data/all_student_2018/class_10/C/education.application.csv',
        'data/all_student_2018/class_10/H/education.application.csv',
        'data/all_student_2018/class_11/A/education.application.csv',
        'data/all_student_2018/class_11/B/education.application.csv',
        'data/all_student_2018/class_11/C/education.application.csv',
        'data/all_student_2018/class_11/D/education.application.csv',
        'data/all_student_2018/class_11/H/education.application.csv',
        'data/all_student_2018/class_12/A/education.application.csv',
        'data/all_student_2018/class_12/B/education.application.csv',
        'data/all_student_2018/class_12/C/education.application.csv',

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