# -*- coding: utf-8 -*-
{
    'name': "HR Planner and Manager",
    'summary': 'Module Odoo untuk menyimpan data kucing.',
    'description': 'Module Odoo untuk menyimpan dan menampilkan data kucing yang ada pada WillyWangky’s Pet Shop.',
    'sequence': -100,
    'author': "Thomas The Tank Engine",
    'category': 'Uncategorized',
    'version': '1.0',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/hrpm_menus.xml',
        'views/hrpm_trees.xml',
        'views/hrpm_forms.xml',
        'views/hrpm_calendar.xml',
    ],
    'demo': [
        'demo/demo.xml'
    ],
    'qweb': [

    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
