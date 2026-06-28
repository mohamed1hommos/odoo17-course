from odoo import  models, api, fields

class Owner(models.Model):
    _name = 'tag'

    name = fields.Char(  string="name" )
