from odoo import models, fields

class ProjectStages(models.Model):
    _name = 'project.stages'
    _description = 'Project Stages'
    _order = 'sequence, id'          # ✅ order by sequence

    name = fields.Char(string='Name', required=True)
    state = fields.Selection([
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
    ], default='new', string='Status')
    description = fields.Text(string='Description')
    priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Urgent'),
    ], default='0')
    sequence = fields.Integer(
        string='Sequence',
        default=10
    )
    fold = fields.Boolean(
        string='Folded in Kanban',
        default=False
    )