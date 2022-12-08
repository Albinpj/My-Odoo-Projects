from odoo import api, fields, models


class HelpDeskTickets(models.Model):
    _name = "help.desk.tickets"
    _description = "Help Desk Tickets"
    _rec_name = "sequence"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    request = fields.Text(string='Request', required=True)
    help_desk_team = fields.Many2one('help.desk.team', string='Helpdesk Team', required=True)
    sequence = fields.Char(string="Sequence Number", readonly=True, required=True, copy=False, default='New')
    employee = fields.Many2one('hr.employee', string='Employee', required=True)
    email = fields.Char(string="Email")
    phone = fields.Char(string="Phone")
    state = fields.Selection(
        [('in_progress', 'In Progress'), ('approved', 'Approved'), ('cancelled', 'Cancelled')],
        default="in_progress",
        string="State")
    user_id = fields.Many2one('res.users', string="User", default=lambda self: self.env.user,
                              readonly=True)
    company_id = fields.Many2one('res.company', string="Company", default=lambda self: self.env.company,
                                 readonly=True)

    @api.model
    def create(self, vals):
        if vals.get('sequence', 'New') == 'New':
            vals['sequence'] = self.env['ir.sequence'].next_by_code('help.desk.tickets') or 'New'
        result = super(HelpDeskTickets, self).create(vals)
        return result

    def button_to_approve(self):
        self.state = 'approved'

    def button_in_cancel(self):
        self.state = 'cancelled'
