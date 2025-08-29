# -*- coding: utf-8 -*-
{
    'name': "Document Approval Custom",
    "version": "0.1",
    "category": "Documents Management",
    "summary": "Manager can approve or reject documents",
    "description": "User can create and upload various document for approvals."
                   "Manager can approve or reject documents.",
    'author': 'Cybrosys Techno Solutions',
    'depends': ['base', 'document_approval', 'hr', 'web', 'uom'],
    'data': [
        'security/ir.model.access.csv',
        'data/data.xml',
        'views/document_approval_views.xml',
        'report/report_cash_request.xml',
        'report/report_payment_request.xml',
        'report/report_purchase_request.xml',
    ],
}
