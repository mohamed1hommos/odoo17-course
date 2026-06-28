from odoo import  models, api, fields

class PropertyHistory(models.Model):
    _name = 'property.history'
    _description = 'property_history'

    user_id = fields.Many2one('res.users')
    property_id = fields.Many2one('property')
    old_state = fields.Char(groups="app_one.property_manager_group_one")
    new_state = fields.Char()
    reason = fields.Text()
    line_ids = fields.One2many('property.history.line', 'history_id')


class PropertyHistoryLine(models.Model):
    _name = 'property.history.line'
    _description = 'property_history'

    history_id = fields.Many2one('property.history')
    area = fields.Char()
    description = fields.Char()
