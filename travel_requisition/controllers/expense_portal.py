from odoo import http, _
from odoo.http import content_disposition, Controller, request, route
from odoo.addons.portal.controllers.portal import CustomerPortal


class AllExpense(http.Controller):
    @http.route('/my/MyReimbursement/', website=True, auth='public')
    def display_expenses(self, sortby=None, **kw):
        searchbar_sortings = {
            'date': {'label': _('Expense Date'), 'order': 'date desc'},
            'name': {'label': _('Name'), 'order': 'name'},
        }
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']

        all_expenses = http.request.env['hr.expense'].search(
            [('state', '=', ('draft', '', '', '', '')), ('payment_mode', '=', 'company_account')], order=order)
        return http.request.render('travel_requisition.portal_all_expenses_list', {
            'expenses': all_expenses,
            'page_name': 'expense',
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby
        })

    @http.route('/my/MyReimbursement/<model("hr.expense"):expense>', auth='public', website=True)
    def display_expense_detail(self, expense):
        return http.request.render('travel_requisition.expense_detail', {
            'expense': expense,
            'page_name': 'expense',
        })


class ExpenseCustomerPortal(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super(ExpenseCustomerPortal, self)._prepare_home_portal_values(counters)
        count_expenses = http.request.env['hr.expense'].search_count([])
        values.update({
            'count_expenses': count_expenses,
        })
        return values
