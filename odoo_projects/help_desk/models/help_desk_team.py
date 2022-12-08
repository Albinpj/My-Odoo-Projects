from odoo import api, fields, models


class HelpDeskTickets(models.Model):
    _name = "help.desk.team"
    _description = "Help Desk Team"
    _rec_name = "help_desk_team"

    help_desk_team = fields.Char(string='Helpdesk Team', required=True)
    responsible_person = fields.Many2one('res.users', string="Responsible Person", default=lambda self: self.env.user)
