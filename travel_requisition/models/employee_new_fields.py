from odoo import models, fields, api, _
from datetime import datetime
from dateutil.relativedelta import relativedelta


class HrEmployeeInherit(models.Model):
    _inherit = 'hr.employee'

    emp_code = fields.Char(string='Employee Code', required=True, copy=False, readonly=True, index=True,
                           default=lambda self: _('New'))
    name_on_passport = fields.Char(string='Name on Passport')
    dl_no = fields.Char(string="Driving License Number")
    pan_no = fields.Char(string='Pan Card Number')
    title = fields.Selection([('mr', 'Mr.'), ('ms', 'Ms.')], string='Title')
    age = fields.Char(string="Age", compute="_compute_age")

    # Overriding the create method and assigning the sequence for the record
    @api.model
    def create(self, vals):
        if vals.get('emp_code', _('New')) == _('New'):
            vals['emp_code'] = self.env['ir.sequence'].next_by_code(
                'hr.employee') or _('New')
        res = super(HrEmployeeInherit, self).create(vals)
        return res

    # function for calculate age based on birthdate
    @api.depends('birthday')
    def _compute_age(self):
        for emp in self:
            age = relativedelta(datetime.now().date(), fields.Datetime.from_string(emp.birthday)).years
            emp.age = str(age) + " Years"
