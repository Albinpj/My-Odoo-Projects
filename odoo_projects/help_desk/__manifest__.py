{
    'name': 'Help Desk',
    'version': '15.0.5.0',
    'category': 'Help Desk',
    'sequence': -1502,
    'summary': 'Help Desk For Employee',
    'application': True,
    'depends': [
        'base',
        'hr',
        'mail',
        'website',

    ],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/help_desk_menus.xml',
        'views/help_desk_tickets.xml',
        'views/help_desk_team.xml',
        'data/sequence.xml',
        'views/help_desk_website.xml',
        'views/help_desk_website_template.xml',

    ],


}
