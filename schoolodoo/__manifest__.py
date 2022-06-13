# -*- coding: utf-8 -*-

{
    'name': 'OdooSchool',
    'depends': ['base_setup', 'base', 'web'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/student_details.xml',
        'views/subject_details.xml',
        'views/class_level.xml',
        'views/fees.xml',
        'views/exam.xml',
        'wizard/wizard.xml',
        'wizard/exam_question.xml',
        'report/report.xml',
        'report/record.xml',
        ],
    'application': True,

}
