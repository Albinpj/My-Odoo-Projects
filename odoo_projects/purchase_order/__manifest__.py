{
    'name': 'Purchase Order',
    'version': '15.0.1.0',
    'category': 'automatic purchase order',
    'summary': 'automatic purchase order',
    'application': True,
    'depends': [
        'base',
        'purchase',
        'product',
    ],
    'data': [
        'security/ir.model.access.csv',
        'wizard/purchase_wizard.xml',
        'views/purchase_button.xml',
        'views/purchase_conf_settings.xml',

    ],
    'sequence': -300
}
