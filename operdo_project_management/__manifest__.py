# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Operdo Project Management',
    'version': '18.0',
    'summary': 'Inherit PRM Base',
    'description': "",
    'category': '',
    'depends': ['project','hr'],
    'data': [
        'views/operdo_project_project.xml',
        'views/operdo_project_task.xml'
    ],
    'installable': True,
    'application': True,
    'assets': {
    },
    'license': 'LGPL-3',
}
