from odoo import models, fields

class SaleOrder(models.Model):
    _inherit = "sale.order"

    promo_active = fields.Boolean(string="Promo Active", default=False)