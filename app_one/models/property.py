from urllib import error

import requests
from datetime import timedelta

from odoo import models, api, fields, exceptions
from odoo.exceptions import ValidationError
import re


class property(models.Model):
    _name = 'property'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Property '

    name = fields.Char(string="name", required=True, default="New", size=25)
    description = fields.Text()
    ref = fields.Char(default="New", readonly=True)
    postcode = fields.Char(required=True)
    internal_notes = fields.Char()
    date_of_birth = fields.Date(readonly=True)
    creator_id = fields.Many2one(
        'res.users',
        string='Creator'
    )
    date_availability = fields.Date(tracking=True)
    expected_selling_date = fields.Date()
    expected_price = fields.Float()
    selling_price = fields.Float()
    diff = fields.Float(compute='_compute_diff', readonly=False, store=True)
    bedrooms = fields.Integer()
    bathrooms = fields.Integer()
    living_rooms = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    free = fields.Char()
    garafe = fields.Boolean()
    is_late = fields.Boolean()
    garden_area = fields.Integer()
    active = fields.Boolean(default=True)
    gareden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West'),
    ])
    phone = fields.Char()
    Address = fields.Char()
    NickName = fields.Char()
    owner_id = fields.Many2one('owner')
    tag_ids = fields.Many2many('tag')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('cancel', 'Cancelled'),
        ('hold', 'Hold'),
    ], default='draft')
    company_id = fields.Many2one(
        'res.company',
        default=lambda self: self.env.company,
        string= 'Company',
        readonly=True,

    )
    owner_address = fields.Char(related='owner_id.address', readonly=False)
    owner_phone = fields.Char(related='owner_id.phone', store=True)

    line_ids = fields.One2many('property.line', 'property_id', string='Lines')

    def check_expected_selling_date(self):
        property_ids = self.search([])
        for rec in property_ids:
            if rec.expected_selling_date and rec.expected_selling_date < fields.date.today():
                rec.is_late = True

    def action_draft(self):
        for rec in self:
            rec.create_history_report(rec.state, 'draft')
            rec.state = 'draft'

    def action_open_related_owner(self):
        action = self.env['ir.actions.actions']._for_xml_id('app_one.owners_action')
        view_id = self.env.ref('app_one.owner_view_form').id
        action['res_id'] = self.owner_id.id
        action['views'] = [[view_id, 'form']]
        return action

    def action(self):
        print(self.env['property'].search([('name', '!=', 'proper')]))

    def action_pending(self):
        for rec in self:
            rec.create_history_report(rec.state, 'confirmed')
            rec.write({'state': 'confirmed'})

    def action_cancel(self):
        for rec in self:
            rec.create_history_report(rec.state, 'cancel')
            print("cancelled")
            rec.write({'state': 'cancel'})

    def action_hold(self):
        for rec in self:
            rec.create_history_report(rec.state, 'hold')
            rec.state = 'hold'

    def create_history_report(self, old_state, new_state):
        self.env["property.history"].create({
            'user_id': self.env.user.id,
            'property_id': self.id,
            'old_state': old_state,
            'new_state': new_state,
        })

    def action_open_change_state_wizard(self):
        action = self.env["ir.actions.act_window"]._for_xml_id('app_one.change_state_wizard_action')
        action['context'] = {'default_property_id': self.id}
        return action

    # @api.model_create_multi
    # def create(self, vals_list):
    #     res=super(property, self).create(vals_list)
    #     print("Done creating property")
    #     return res
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            # التحقق إذا كانت قيمة الـ ref فارغة أو تساوي "New"
            if vals.get('ref', 'New') == 'New':
                vals['ref'] = self.env["ir.sequence"].next_by_code("property_seq") or 'New'

        # تمرير القائمة كاملة للدالة الأم
        return super(property, self).create(vals_list)

    @api.model
    def _search(self, domain, offset=0, limit=None, order=None, access_rights_uid=None):
        res = super(property, self)._search(domain, offset=0, limit=None, order=None, access_rights_uid=None)
        print("Done searching property")
        return res
    @api.model_create_multi
    def create(self,vals_list):
        for vals in vals_list:
            if not vals.get("date_availability"):
                vals["date_availability"] = fields.Date.today()
        return super(property, self).create(vals_list)

    @api.model_create_multi
    def create(self,vals_list):
        for vals in vals_list:
            if not vals.get("expected_price"):
                vals["expected_price"] = 100
        return super(property, self).create(vals_list)

    @api.model_create_multi
    def create(self,vals_list):
        for vals in vals_list :
            if not vals.get("expected_selling_date"):
                vals["expected_selling_date"] = fields.Date.today()+timedelta(days=10)
        return super(property, self).create(vals_list)



    # def write(self, vals):
    #     res = super(property, self).write(vals)
    #     print("Done writing")
    # #     return res
    #
    # def unlink(self):
    #     res = super(property, self).unlink()
    #     print("Done unlinking")
    #     return res

    def get_properties_api(self):  # 3shan t call data from another app acting as 3rd part application
        payload = ()
        try:
            response = requests.get("http://localhost:8069/web/dataset/call_kw", data=payload)
            if response == 200:
                print("Successfully got response")
            else:
                print("Failed to get response")
        except  Exception as error:
            raise ValidationError(str(error))

    @api.depends('selling_price', 'expected_price', 'owner_id.phone')
    def _compute_diff(self):
        for rec in self:
            print("successfully compute diff")
            rec.diff = rec.selling_price - rec.expected_price

    @api.onchange('living_rooms')
    def _onchange_living_rooms(self):
        for rec in self:
            return {'warning': {
                'title': 'warning',
                'message': 'negative',
                'type': 'notification',
            }

            }

    @api.constrains("living_rooms")
    def _check_living_rooms(self):
        for rec in self:
            if rec.living_rooms == 0:
                raise ValidationError("not valid living_rooms")

    @api.constrains('name')
    def _check_name_letters_only(self):
        for record in self:
            if record.name and not re.match(r'^[a-zA-Z\u0600-\u06FF\s]+$', record.name):
                raise ValidationError("name shouuuuuuuuuuuuuuuuuuuuld nbe letter onnnnnly!")

    def property_xlsx_report(self):
        return {
            'type': 'ir.actions.act_url',
            'url': f'/property/excel/report/{self.env.context.get("active_ids")}',
            'target': 'new'
        }

    _sql_constraints = [
        ('unique_name', 'unique(name)', 'Name already exists!')]


class propertyLine(models.Model):
    _name = 'property.line'

    property_id = fields.Many2one('property')
    area = fields.Char()
    description = fields.Char()
    info = fields.Char()
    information = fields.Char()
    room = fields.Char()
    station = fields.Char()