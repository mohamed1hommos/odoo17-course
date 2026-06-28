from odoo import  models, api, fields

class AccountMove(models.Model):
    _inherit = 'account.move'

    number = fields.Char( string='Number' )


    def action_do_something(self):
        print('action_do_something')

