from odoo import  models, api, fields

class Owner(models.Model):
    _name = 'building'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'building Record'
    _rec_name = 'code'

    number = fields.Char(  string="name" )
    code = fields.Char()
    description = fields.Text()
    active = fields.Boolean(default=True)


    _sql_constraints = [
        ('unique_name', 'unique(number)', 'This name i')]

