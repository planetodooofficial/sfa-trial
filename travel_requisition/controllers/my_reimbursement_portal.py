from odoo import http, _
from odoo.http import content_disposition, Controller, request, route
from odoo.addons.portal.controllers.portal import CustomerPortal
from datetime import date


class AllMyExpense(http.Controller):
    @http.route('/my/MyReimbursement/', website=True, auth='public')
    def display_my_expenses(self, sortby=None, **kw):
        searchbar_sortings = {
            'date': {'label': _('Expense Date'), 'order': 'date desc'},
            'name': {'label': _('Name'), 'order': 'name'},
        }
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']

        all_my_expenses = http.request.env['hr.expense'].search(
            [('state', '=', ('draft', 'reported', 'approved', 'done', 'refused')),
             ('payment_mode', '=', 'own_account')], order=order)
        return http.request.render('travel_requisition.portal_all_my_expenses_list', {
            'my_expenses': all_my_expenses,
            'page_name': 'pexpense',
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby
        })

    @http.route('/my/MyReimbursement/<model("hr.expense"):rexpense>', auth='public', website=True)
    def display_my_expense_detail(self, rexpense):
        return http.request.render('travel_requisition.my_expense_detail', {
            'rexpense': rexpense,
            'page_name': 'pexpense',
        })

    @http.route('/create/MyReimbursement', website=True, auth='public')
    def myreimbursement_form(self, **kw):
        userid = request.env.user.employee_id

        r_product = request.env['product.product'].sudo().search(
            [('travel_requisition', '=', False), ('can_be_expensed', '=', True)])
        cdate = date.today()

        account_id_def = request.env['account.account'].sudo().search(
            [('internal_type', '=', 'other'), ('code', '=', '210700')])
        account_id = request.env['account.account'].sudo().search([('internal_type', '=', 'other')])

        currency_name = request.env['res.currency'].sudo().search([])
        tax_name = request.env['account.tax'].sudo().search(
            [('type_tax_use', '=', 'purchase'), ('price_include', '=', True)])
        analytic_account = request.env['account.analytic.account'].sudo().search([])
        analytic_account_tag = request.env['account.analytic.tag'].sudo().search([])
        paid_id = request.env['hr.expense']

        autofill_data = {
            'user': userid,
            'r_product': r_product,
            'cdate': cdate,
            'currency_name': currency_name,
            'tax_name': tax_name,
            'analytic_account': analytic_account,
            'analytic_account_tag': analytic_account_tag,
            'account_id': account_id,
            'account_id_def': account_id_def,
            'paid_id': paid_id,
        }
        if kw:

            tax_ids = int(kw.get('tax_name'))
            product_name = int(kw.get('r_product'))
            accountid = int(kw.get('account_id'))
            analytic_acc = int(kw.get('analytic_account'))
            analytic_tagid = int(kw.get('analytic_account_tag'))
            vals = {
                'name': kw.get('expname'),
                'product_id': product_name,
                'tax_ids': [(4, tax_ids)],
                'reference': kw.get('ref'),
                'account_id': accountid,
                'analytic_account_id': analytic_acc,
                'analytic_tag_ids': [(4, analytic_tagid)],
                'unit_amount': 1,
            }
            create_record = request.env['hr.expense'].sudo().create(vals)

        return http.request.render('travel_requisition.create_my_reimbursement', autofill_data)


class MyExpenseCustomerPortal(CustomerPortal):
    def _prepare_home_portal_values(self, counters):
        values = super(MyExpenseCustomerPortal, self)._prepare_home_portal_values(counters)
        count_my_expenses = request.env['hr.expense'].sudo().search_count(
            [('state', '=', ('draft', 'reported', 'approved', 'done', 'refused')),
             ('payment_mode', '=', 'own_account')])
        values.update({
            'count_my_expenses': count_my_expenses,
        })
        return values
