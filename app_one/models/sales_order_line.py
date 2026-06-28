from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    cost_price = fields.Float(
        string="Cost Price",
        related="product_id.standard_price",
        readonly=True,
    )
    barcode = fields.Char(
        string="Barcode",
        related="product_id.barcode",
        readonly=True,
    )
    purchase_price = fields.Float(
        compute='_compute_purchase_price',
        string="Purchase_Price",
        readonly=True,
    )

    @api.depends('product_id', 'product_id.purchase_ok')
    def _compute_purchase_price(self):
        for line in self:
            po_line = self.env['purchase.order.line'].search([
                ('product_id', '=', line.product_id.id),
                ('order_id.state', 'in', ['purchase', 'done'])
            ], limit=1)
            line.purchase_price = po_line.price_unit if po_line else 0.0