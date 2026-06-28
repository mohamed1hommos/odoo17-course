from odoo import  models, api, fields

class Owner(models.Model):
    _name = 'owner'

    name = fields.Char(  string="name" )
    phone = fields.Char()
    address = fields.Char()
    property_ids = fields.One2many(""'property','owner_id')

    _sql_constraints = [
        ('unique_name', 'unique(name)', 'This name i')]
    _sql_constraints = [
        ('unique_phone', 'unique(phone)', 'This phone i')]