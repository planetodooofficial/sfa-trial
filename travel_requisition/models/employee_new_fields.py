from odoo import models, fields, api, _
from datetime import datetime
from dateutil.relativedelta import relativedelta


class HrEmployeeInherit(models.Model):
    _inherit = 'hr.employee'

    # overried field for adding options
    marital = fields.Selection([
        ('single', 'Single'),
        ('married', 'Married'),
        ('cohabitant', 'Legal Cohabitant'),
        ('widower', 'Widower'),
        ('divorced', 'Divorced'),
        ('na', 'NA')
    ], string='Marital Status', groups="hr.group_hr_user", default='single', tracking=True)

    emp_code = fields.Char(string='Employee Code', required=True, copy=False, readonly=True, index=True,
                           default=lambda self: _('New'))
    name_on_passport = fields.Char(string='Name on Passport')
    dl_no = fields.Char(string="Driving License Number")
    title = fields.Selection([('mr', 'Mr.'), ('ms', 'Ms.'), ('mrs', 'Mrs.')], string='Title')
    age = fields.Char(string="Age", readonly=False)
    qualification = fields.Char(string="Qualification")

    emp_category = fields.Char(string="Category")
    confirm_date = fields.Date(string="Confirmation Date")

    personal_email = fields.Char(string="Personal Email ID")

    new_aadhar_no = fields.Char(string="Aadhar Card No.")
    new_pf_account_no = fields.Char(string="PF Account No.")

    pre_exp = fields.Char(string="Previous Experience")
    emp_vis = fields.Char(string="Employee Visibility")
    emp_status = fields.Selection([('active', 'Active'), ('inactive', 'Inactive')], string="Status")

    # address fields
    cur_add = fields.Text(string="Current Address", store=True)
    per_add = fields.Text(string="Permanent Address", store=True)
    cur_same_per = fields.Boolean(string="Permanent Address is same as Current Address")
    emp_city = fields.Char(string="City")
    emp_state_id = fields.Char(string="State")

    # bank fields
    bank_name = fields.Char(string="Bank Name")
    bank_accountno = fields.Integer(string="Bank Account Number")
    bank_ifsc = fields.Char(string="Bank IFSC Code")

    # master data fields
    designation = fields.Many2one('designation.master', 'Designation')
    grade = fields.Many2one('grade.master', 'Grade')
    cadre = fields.Many2one('cadre.master', 'Cadre')
    grade_title = fields.Many2one('grade.title.master', 'Grade Title')

    sub_designation = fields.Char(string="Sub Designation")

    emp_join_source = fields.Char(string='Employee Joining Source')
    sub_source = fields.Char(string='Sub Source')

    date_of_resignation = fields.Date(string="Date of Resignation")
    dol = fields.Date(string="Date of leaving (DOL)")
    va_iv = fields.Selection([('va', 'VA'), ('iv', 'IV')], string="VA/IV")
    reason_for_leave = fields.Char(string='Reason For Leaving')

    # salary related fields
    tenure = fields.Float(string="Tenure in SFA")
    tenure_detail = fields.Char(string="Tenure Detail")
    basic_sal = fields.Float(string="Basic Salary")
    hra = fields.Float(string="HRA")
    convy = fields.Float(string="Convy")
    lta = fields.Float(string="LTA")
    choice_pay = fields.Float(string="Choice Pay")
    special_allow = fields.Float(string="Special Allowance")
    gross_per_month = fields.Float(string="Gross per Month")
    gross_per_annum = fields.Float(string="Gross per Annum")
    pf_fund_no = fields.Integer(string="Provident Fund No. (PF)")
    gratuity = fields.Float(string="Gratuity")
    total_retiral = fields.Float(string="Total Retiral")
    annual_retiral = fields.Float(string="Annual Retiral")
    fixed_total_ctc = fields.Float(string="Fixed Total Retiral")
    pb = fields.Float(string="PB")
    total_ctc = fields.Float(string="Total CTC")

    # Overriding the create method and assigning the sequence for the record
    @api.model
    def create(self, vals):
        if vals.get('emp_code', _('New')) == _('New'):
            vals['emp_code'] = self.env['ir.sequence'].next_by_code(
                'hr.employee') or _('New')
        res = super(HrEmployeeInherit, self).create(vals)
        return res

    # function for calculate age based on birthdate
    # @api.depends('birthday')
    # def _compute_age(self):
    #     for emp in self:
    #         age = relativedelta(datetime.now().date(), fields.Datetime.from_string(emp.birthday)).years
    #         emp.age = str(age) + " Years"

    @api.onchange('cur_same_per')
    def _compute_address(self):
        if self.cur_same_per == True:
            self.per_add = self.cur_add


class HrContractInherit(models.Model):
    _inherit = 'hr.contract'

    total_cost_to_comp = fields.Float(string="Total cost to Company")
    lta = fields.Float(string="LTA %")
    basic = fields.Float(string="Basic %")
    conveyance = fields.Float(string="Conveyance %")
    choice_pay = fields.Float(string="Choice Pay %")
    date_of_leaving = fields.Date(string="Date of Leaving (DOL)")
    bank_name = fields.Char(string="Bank Name")
    bank_account_no = fields.Integer(string="Bank Account Number")
    bank_ifsc = fields.Char(string="Bank IFSC")

    @api.model
    def create(self, vals):
        res = super(HrContractInherit, self).create(vals)
        if res:
            res.state = 'open'
        return res
