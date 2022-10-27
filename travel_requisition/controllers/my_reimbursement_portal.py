from odoo import http, _
from odoo.http import content_disposition, Controller, request, route
from odoo.addons.portal.controllers.portal import CustomerPortal


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

    @http.route('/my/MyReimbursement/<model("hr.expense"):expense>', auth='public', website=True)
    def display_my_expense_detail(self, expense):
        return http.request.render('travel_requisition.my_expense_detail', {
            'expense': expense,
            'page_name': 'pexpense',
        })


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
