# -*- coding: utf-8 -*-
{
    'name': "Project Custom",
    "version": "0.1",
    "category": "Project",
    "summary": "",
    "description": "",
    'author': '',
    'depends': ['base', 'mail', 'hr', 'web', 'uom'],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/expense_categories_views.xml',
        'views/receipt_categories_views.xml',
        'views/document_date_views.xml',
        'views/planned_expenditure_views.xml',
        'views/cash_inflows_views.xml',
        'views/cash_outflows_views.xml',
        'views/menu_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'project_custom/static/src/**/*',
        ],
    },
}
