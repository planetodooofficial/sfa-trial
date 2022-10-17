from num2words import num2words
from odoo import fields, api, models, _
import time
from odoo.exceptions import UserError, ValidationError

class InheritPaySlip(models.Model):
    _inherit = 'hr.payslip'

    amt = fields.Char(compute='amt_in_words', string='amt')

    def amt_in_words(self):
        self.amt = self.line_ids.filtered(lambda r: r.category_id.name=='Net').mapped('total')
        # return amount_to_text_fr(net_total, self.currency_id.symbol)
