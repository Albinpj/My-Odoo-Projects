from odoo import api, fields, models


class ProductWishlist(models.Model):
    _name = "product.wishlist"
    _description = "Product Wishlist"

    product_id = fields.Many2one('product.product', string='Product')
    partner_id = fields.Many2one('res.partner', string='Customer')


