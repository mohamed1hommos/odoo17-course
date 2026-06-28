from odoo import models, api, fields

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'
    order_number = fields.Char(string='Order Number')
    free = fields.Boolean(string='Free Order')