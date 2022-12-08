{
    'name': 'Stock Move Report',
    'version': '16.0.1.0',
    'sequence': -102,
    'category': 'Stock Move Report',
    'summary': 'Stock Move Report',
    'application': True,
    'depends': [
        'base',
        'product',
        'stock'
    ],
    'data': [
        'security/ir.model.access.csv',
        'wizard/stock_move_wizard.xml',
        'views/stock_move_button.xml',
        'report/stock_move_report.xml',
        'report/stock_move_report_template.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'stock_move_report/static/src/js/stock_move_report.js']
    }
}
