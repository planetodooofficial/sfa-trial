from odoo import http, _
from odoo.http import content_disposition, Controller, request, route
from odoo.addons.portal.controllers.portal import CustomerPortal
from datetime import date


class AllExpense(http.Controller):
    @http.route('/my/TravelRequisition/', website=True, auth='public')
    def display_expenses(self, sortby=None, **kw):
        searchbar_sortings = {
            'date': {'label': _('Expense Date'), 'order': 'date desc'},
            'name': {'label': _('Name'), 'order': 'name'},
        }
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']

        all_expenses = http.request.env['hr.expense'].search(
            [('state', '=', ('draft', 'reported', 'approved', 'done', 'refused')),
             ('payment_mode', '=', 'company_account')], order=order)
        return http.request.render('travel_requisition.portal_all_expenses_list', {
            'expenses': all_expenses,
            'page_name': 'expense',
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby
        })

    @http.route('/my/TravelRequisition/<model("hr.expense"):expense>', auth='public', website=True)
    def display_expense_detail(self, expense):
        return http.request.render('travel_requisition.expense_detail', {
            'expense': expense,
            'page_name': 'expense',
        })

    @http.route('/create/TravelRequisition', website=True, auth='public')
    def travelrequisition_form(self, **kw):
        # get current login user
        userid = request.env.user.employee_id

        # get products based on search filter from many 2 one
        t_product = request.env['product.product'].sudo().search(
            [('travel_requisition', '=', True), ('can_be_expensed', '=', True)])

        # get current date
        cdate = date.today()

        # get default selected account based on search filter from many 2 one
        t_account_id_def = request.env['account.account'].sudo().search(
            [('internal_type', '=', 'other'), ('code', '=', '210700')])
        # get all account list based on search filter from many 2 one
        t_account_id = request.env['account.account'].sudo().search([('internal_type', '=', 'other')])

        # get currency from many 2 one
        t_currency_name = request.env['res.currency'].sudo().search([])

        # get all account list based on search filter from many 2 many
        t_tax_name = request.env['account.tax'].sudo().search(
            [('type_tax_use', '=', 'purchase'), ('price_include', '=', True)])

        # get all analytic account list based on search filter from many 2 one
        t_analytic_account = request.env['account.analytic.account'].sudo().search([])

        # get all account list based on search filter from many 2 many
        t_analytic_account_tag = request.env['account.analytic.tag'].sudo().search([])

        # get field for getting paid by value
        # t_paid_id = request.env['hr.expense'].sudo().search([('travel_requisition_opt', '=', True)], limit=1)

        tautofill_data = {
            # 'module_fields_name' : defined_fields_name
            'user': userid,
            't_product': t_product,
            'cdate': cdate,
            't_currency_name': t_currency_name,
            't_tax_name': t_tax_name,
            't_analytic_account': t_analytic_account,
            't_analytic_account_tag': t_analytic_account_tag,
            't_account_id': t_account_id,
            't_account_id_def': t_account_id_def,
            # 't_paid_id': t_paid_id,
        }
        if kw:

            # writing if condition to get value from many 2 one if value not present then pass false to the field
            if kw.get('t_tax_name'):
                # here tax_name many 2 many getting id in string is convert into integer and store in field
                t_tax_ids = int(kw.get('t_tax_name'))
            else:
                # if tax_name not select then pass false
                t_tax_ids = False

            if kw.get('t_product'):
                # here r_product many 2 one getting id in string is convert into integer and store in field
                t_product_name = int(kw.get('t_product'))
            else:
                # if product not select then pass false
                t_product_name = False

            if kw.get('t_account_id'):
                t_accountid = int(kw.get('t_account_id'))
            else:
                t_accountid = False

            if kw.get('t_analytic_account'):
                t_analytic_acc = int(kw.get('t_analytic_account'))
            else:
                t_analytic_acc = False

            if kw.get('t_analytic_account_tag'):
                # here analytic_account_tag many 2 many getting id in string is convert into integer and store in field
                t_analytic_tagid = int(kw.get('t_analytic_account_tag'))
            else:
                # if analytic_account_tag not select then pass false
                t_analytic_tagid = False

            tvals = {
                'name': kw.get('t_expname'),
                'product_id': t_product_name,

                # this if condition and security condition is for many 2 many field
                'tax_ids': False if t_tax_ids is False else [(4, t_tax_ids)],

                'reference': kw.get('ref'),
                'account_id': t_accountid,
                'analytic_account_id': t_analytic_acc,

                # this if condition and security condition is for many 2 many field
                'analytic_tag_ids': False if t_analytic_tagid is False else [(4, t_analytic_tagid)],

                # don't know about this field, this field shows mandatory therefore i pass 1
                'unit_amount': 1,
                'payment_mode': 'company_account'
                # 'payment_mode': 'company_account' if kw.get('payment_mode') == 'company_account' else 'company_account'
            }

            # create method override to create record from form
            create_record = request.env['hr.expense'].sudo().create(tvals)

        return http.request.render('travel_requisition.create_travel_requisition', tautofill_data)


class ExpenseCustomerPortal(CustomerPortal):
    def _prepare_home_portal_values(self, counters):
        values = super(ExpenseCustomerPortal, self)._prepare_home_portal_values(counters)
        count_expenses = http.request.env['hr.expense'].search_count(
            [('state', '=', ('draft', 'reported', 'approved', 'done', 'refused')),
             ('payment_mode', '=', 'company_account')])
        values.update({
            'count_expenses': count_expenses,
        })
        return values
