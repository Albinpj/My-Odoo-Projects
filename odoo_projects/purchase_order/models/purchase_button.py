from odoo import api, fields, models


class ServerAction(models.Model):
    _inherit = "product.template"

    def wizard_fun(self):
        return {
            'name': 'Create Purchase Order',
            'res_model': 'create.po.wizard',
            'view_mode': 'form',
            'view_type': 'form',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': {
                'default_product_id': self.id,

            }
        }
