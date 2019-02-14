{
    'name': 'Eagle Education Attendance Management',
    'version': '11.0.1.0.0',
    'summary': """Opener to Student Attendance Management System for Eagle ERP""",
    'description': 'An easy and efficient management tool to manage and track student'
                   ' attendance. Enables different types of filtration to generate '
                   'the adequate reports',
    'category': 'Industries',
    'author': 'Md. Shaheen Hossain',
    'company': 'Eagle ERP',
    'maintainer': 'Eagle ERP',
    'website': "http://www.eagle-it-services.com",
    'depends': ['education_core'],
    'data': [
        'views/students_attendance.xml',
        'views/student_view.xml',
        'security/ir.model.access.csv',
    ],
    'images': ['static/description/banner.jpg'],
    'license': 'AGPL-3',
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}
