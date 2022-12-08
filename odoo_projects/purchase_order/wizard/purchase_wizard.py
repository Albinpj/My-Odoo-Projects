from odoo import api, fields, models


class CreatePOWizard(models.TransientModel):
    _name = 'create.po.wizard'
    _description = 'CreatePOWizard '

    quantity = fields.Integer(string="Quantity")
    price = fields.Float(string="Price")
    product_id = fields.Many2one('product.template', string='Product')

    def action_confirm_po(self):
        sample = self.env['product.product'].search([('product_tmpl_id', '=', self.product_id.id)])
        for rec in self.product_id.seller_ids[0]:
            parchase_order = self.env['ir.config_parameter'].sudo().get_param('purchase_order.parchase_order')

            print(rec)
            # print(rec.name.id)
            # print(self.product_id.id)

            if parchase_order:
                purchase_id = self.env['purchase.order'].create([
                    {
                        'partner_id': rec.name.id,
                        'order_line': [(0, 0, {
                            'product_id': sample.id,
                            'product_qty': self.quantity,
                            'price_unit': self.price})],
                    }, ])
                purchase_id.button_confirm()
            else:
                sample = self.env['product.product'].search([('product_tmpl_id', '=', self.product_id.id)])
                purchase_ids = self.env['purchase.order'].search([('partner_id', '=', rec.name.id),
                                                                  ('state', '=', 'draft')])
                print(len(purchase_ids))
                if purchase_ids:
                    purchase_ids[0].write({
                        'order_line': [(0, 0, {
                            'product_id': sample.id,
                            'product_qty': self.quantity,
                            'price_unit': self.price})],
                    })
                else:
                    purchase_id = self.env['purchase.order'].create([
                        {
                            'partner_id': rec.name.id,
                            'order_line': [(0, 0, {
                                'product_id': sample.id,
                                'product_qty': self.quantity,
                                'price_unit': self.price})],
                        }, ])
                    print(purchase_id)
