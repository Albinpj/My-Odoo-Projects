from odoo import api, models, fields


class ConfSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    parchase_order = fields.Boolean(string="Purchase Order")

    def set_values(self):
        super(ConfSettings, self).set_values()
        self.env['ir.config_parameter'].set_param(
            'purchase_order.parchase_order', self.parchase_order)

    @api.model
    def get_values(self):
        res = super(ConfSettings, self).get_values()
        params = self.env['ir.config_parameter'].sudo()
        res.update(
            parchase_order=params.get_param('purchase_order.parchase_order')
        )
        return res
