{
    'name': 'Travel Requisition Expense',
    'version': '1.1',
    'summary': 'Travel Requisition Expense',
    'sequence': 10,
    'description': """Travel Requisition Expense""",
    'depends': [
        'base', 'hr_expense', 'product', 'website', 'portal',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/travel_requisition_views.xml',
        'views/expenses_view.xml',
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
