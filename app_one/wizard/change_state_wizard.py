from email.policy import default

from docutils.parsers.rst import states

from odoo import api, fields, models, _

class ChangeStateWizard(models.TransientModel):
    _name = 'change_state'
    _description = 'Change State Wizard'

    property_id = fields.Many2one('property')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('cancel', 'Cancelled'),
    ],default='draft')
    reason = fields.Char()
    def action_confirm(self):
        old_state = self.property_id.state
        self.property_id.state = self.state
        self.property_id.create_history_report(old_state,self.state,)