from odoo import http
from odoo.addons.portal.controllers.portal import CustomerPortal


class ExpensePortal(http.Controller):

    @http.route('/my/expenses/', auth='public', website=True)
    def display_expense(self, **kw):
        show_expenses = http.request.env['hr.expense'].search(
            [('state', 'in', ('draft', 'reported', 'approved', 'done', 'refused'))])
        return http.request.render('hr.expense', {
            'expenses': show_expenses,
        })


class ExpenseCustomerPortal(CustomerPortal):

    def _prepare_home_portal_values(self):
        values = super(ExpenseCustomerPortal, self)._prepare_home_portal_values()
        count_expense = http.request.env['hr.expense'].search_count(
            [('state', 'in', ('draft', 'reported', 'approved', 'done', 'refused'))])
        values.update({
            'count_expense': count_expense,
        })
        return values
