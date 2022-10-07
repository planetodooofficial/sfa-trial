from lxml import etree

from odoo import models, fields, api, _


class TravelRequisitionExpense(models.Model):
    _inherit = 'hr.expense'

    name_new = fields.Many2one('hr.employee', string='Name')
    emp_code = fields.Char(string='Employee Code', related='name_new.emp_code', store=True)
    band = fields.Char(string='Band')
    mobile = fields.Char(string='Mobile No.', related='name_new.mobile_phone', store=True)
    designation = fields.Char(string='Designation', related='name_new.job_title', store=True)
    department = fields.Char(string='Department', related='name_new.department_id.name', store=True)
    company = fields.Char(string='Company', related='name_new.company_id.name', store=True)
    purpose_of_visit = fields.Char(string='Purpose of Visit')
    approved_by = fields.Char(string='Approved By', related='name_new.parent_id.name', store=True)
    pan_dl_no = fields.Char(string='Pan Card Number', related='name_new.pan_no', store=True)
    dl_number = fields.Char(string='Driving License Number', related='name_new.dl_no', store=True)
    age = fields.Integer(string='Age')
    pass_name = fields.Char(string='Name on Passport', related='name_new.name_on_passport', store=True)
    pass_no = fields.Char(string='Passport No.', related='name_new.passport_id', store=True)
    date_place = fields.Char(string='Date & Place of Issue')
    visa_required = fields.Boolean(string='Visa Required')
    travel_detail_line_ids = fields.One2many('travel.details.line', 'hr_exp_id', 'Travel Detail Line')
    stay_detail_line_ids = fields.One2many('stay.details.line', 'hr_exp_id', 'Stay Detail Line')
    travel_requisition_opt = fields.Boolean(string='Travel Requisition')

    # @api.model
    # def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
    #     res = super(TravelRequisitionExpense, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar,
    #                                                           submenu=submenu)
    #     if view_type == 'form':
    #         expense = [("travel_requisition", "=", True)] if self._context.get('travel_requisition_opt') is True else [
    #             ("travel_requisition", "=", False)]
    #         doc = etree.XML(res['arch'])
    #         for node in doc.xpath(f"//field[@name='product_id']"):
    #             node.set('domain', f"{expense}")
    #             res['arch'] = etree.tostring(doc)
    #     return res

    # product id field for travel requisition to filter product list based on menu selected
    # travel_product_id = fields.Many2one('product.product', string='Product', readonly=False, tracking=True,
    #                                     states={'draft': [('readonly', False)], 'reported': [('readonly', False)],
    #                                             'approved': [('readonly', False)], 'refused': [('readonly', False)]},
    #                                     domain="[('can_be_expensed', '=', True), '|', ('company_id', '=', False), ('company_id', '=', company_id), ('travel_requisition','=',True)]",
    #                                     ondelete='restrict')

    # product_id actual field override and pass the context for the field
    product_id = fields.Many2one('product.product', string='Product', readonly=False, tracking=True,
                                 states={'draft': [('readonly', False)], 'reported': [('readonly', False)],
                                         'approved': [('readonly', False)], 'refused': [('readonly', False)]},
                                 domain="[('can_be_expensed', '=', True), '|', ('company_id', '=', False), ('company_id', '=', company_id), ('travel_requisition', '=', context.get('travel_prd', False))]",
                                 ondelete='restrict')

    # function for product fields = when travel requisition product is selected then function set paid by field on Company
    # @api.onchange('product_id')
    # def _onchange_product_expense(self):
    #     if self.product_id:
    #         if self.product_id.travel_requisition == True:
    #             self.payment_mode = 'company_account'

    # CREATING DOMAIN ON PRODUCT_ID FIELD TO DIFFERENTIATE DATA BASED ON FIELD TRUE AND FALSE
    # @api.depends('travel_requisition_opt')
    # def _ondepends_product_id_view(self):
    #     domain = {}
    #     if self.travel_requisition_opt:
    #         if self.travel_requisition_opt == True & self.payment_mode == 'company_account':
    #             domain = {'product_id': [('product_id.travel_requisition', '=', True)]}
    #         if self.travel_requisition_opt == False & self.payment_mode == 'own_account':
    #             domain = {'product_id': [('product_id.travel_requisition', '=', False)]}
    #         return {'domain': domain}

    class TravelDetailsLine(models.Model):
        _name = 'travel.details.line'

        hr_exp_id = fields.Many2one('hr.expense', string='Hr Expense Id')
        date = fields.Date(string='Date')
        from_dates = fields.Date(string='From')
        to_dates = fields.Date(string='To')
        departs_time = fields.Float(string='Departs Time')
        arrives_time = fields.Float(string='Arrives Time')
        mode_and_class = fields.Char(string='Mode & Class')

    class StayDetailsLine(models.Model):
        _name = 'stay.details.line'

        hr_exp_id = fields.Many2one('hr.expense', string='Hr Expense Id')
        name_line = fields.Many2one('hr.employee', string='Name')
        band_line = fields.Char(string='Band')
        hotel_guest_line = fields.Char(string='Hotel / Guest House')
        location_line = fields.Char(string='Location')
        check_in_date = fields.Date(string='Check in Date')
        check_out_date = fields.Date(string='Check Out Date')

    class ExpenseProductInherit(models.Model):
        _inherit = 'product.product'

        travel_requisition = fields.Boolean('Travel Requisitions')

    class HrEmployeeInherit(models.Model):
        _inherit = 'hr.employee'

        emp_code = fields.Char(string='Employee Code')
        name_on_passport = fields.Char(string='Name on Passport')
        dl_no = fields.Char(string="Driving License Number")
        pan_no = fields.Char(string='Pan Card Number')
