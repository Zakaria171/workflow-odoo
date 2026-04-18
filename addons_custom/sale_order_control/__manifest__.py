{
    'name': 'Sale Order Control',
    'version': '1.0',
    'summary': 'Custom sale order control',
    'category': 'Sales',
    'author': 'workflow_odoo',
    'license': 'LGPL-3',
    'depends': ['sale'],
    'data': [
        "views/sale_order_view.xml",
        "security/security.xml",
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
