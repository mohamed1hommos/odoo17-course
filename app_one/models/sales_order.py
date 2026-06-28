from odoo import  models, api, fields
from odoo.exceptions import ValidationError, UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    property_id = fields.Many2one('property')
    owner_id = fields.Many2one('owner')
    margin_amount = fields.Monetary(
        string="Margin",
        compute="_compute_margin",
        currency_field='currency_id',
        store=True,
    )
    #
    # def write(self, vals):
    #     for order in self:
    #         # التحقق مما إذا كانت الحالة الحالية confirmed (sale) أو done
    #         # واستثنينا حالة لو السيستم بيحاول يغير الحالة نفسها أو يلغيها
    #         if order.state in ['sale', 'done'] and not 'state' in vals:
    #             raise UserError(" Can't Edit!")
    #
    #     return super(SaleOrder, self).write(vals)

    @api.depends('order_line.product_id',
    'order_line.price_subtotal',
    'order_line.purchase_price',
    'order_line.product_uom_qty')
    def _compute_margin(self):
        for order in self:
            margin = 0
            for line in order.order_line:
                cost = line.cost_price * line.product_uom_qty
                margin += line.price_subtotal - cost
            order.margin_amount = margin



    def action_confirm(self):
        for order in self:
            for line in order.order_line:
                if not line.product_id:
                    continue

                cost = line.product_id.standard_price
                sale_price = line.price_unit

                if sale_price < cost:
                    raise ValidationError(
                        (
                            "You cannot confirm this Sales Order.\n\n"
                            "Product: %s\n"
                            "Cost Price: %s\n"
                            "Sale Price: %s"
                        )
                        % (
                            line.product_id.display_name,
                            cost,
                            sale_price,
                        )
                    )
        return super().action_confirm()


