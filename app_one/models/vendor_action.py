from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ResPart(models.Model):
    _inherit = 'res.partner'

    free=fields.Char(string='Free')
    x_priority= fields.Selection(
        selection=[('0','low'),('1','normal'),('2','high')],
        string='Priority',
        default='1',
        tracking=True,
    )

    wadge = fields.Float(string='Wage')
    Days = fields.Float(string='Days')
    Salary = fields.Float(string='Salary', compute='_compute_Salary', store=True)

    @api.depends('wadge', 'Days')
    def _compute_Salary(self):  # ← matches compute='' above
        for rec in self:
            if rec.Days > 0:
                rec.Salary = rec.wadge / rec.Days
            else:
                rec.Salary = 0




