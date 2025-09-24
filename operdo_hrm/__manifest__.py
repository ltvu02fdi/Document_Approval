# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Operdo HRM',
    'version': '18.0',
    'summary': 'Inherit HRM Base',
    'description': "",
    'category': '',
    'depends': ['hr', 'hr_contract','hr_attendance'],
    'data': [
        'views/operdo_hr_department_views.xml',
        'views/operdo_hr_employee_views.xml',
        'views/operdo_hr_contract_views.xml',
        # security
        'security/ir.model.access.csv',
        # data
        'data/ir_cron_data.xml',
    ],
    'installable': True,
    'application': True,
    'assets': {
        'web.assets_backend': [
            'operdo_hrm/static/src/webclient/**/*',
        ],
    },
    'license': 'LGPL-3',
}
