from odoo import api, models,fields





class ResUsers(models.Model):
        _inherit = 'res.users'

        x_warehouse_id = fields.Many2one(
                'stock.warehouse',
                string='Warehouse mohamed'
            )
        warehouse_ids_custom = fields.Many2many(
            comodel_name='stock.warehouse',
            relation='res_users_warehouse_rel',  # must be UNIQUE across all Odoo
            column1='user_id',
            column2='warehouse_id',
            string='Allowed Warehouses',
        )

        @api.model_create_multi
        def create(self, vals_list):
            users = super(ResUsers, self).create(vals_list)
            self.clear_caches()
            return users

        def write(self, vals):
            res = super(ResUsers, self).write(vals)
            if 'warehouse_ids_custom' in vals:
                self.clear_caches()
            return res
        allow_partner_tag_ids = fields.Many2many(
            'res.partner.category',
            string='Allowed partner tags',
            # domain=[('customer_rank', '>', 0)]
        )