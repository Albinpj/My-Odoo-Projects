from odoo import http
from odoo.http import request


class WebsiteForm(http.Controller):

    @http.route(['/help_desk'], type='http', auth="user", website=True)
    def rent_request(self):
        employees = request.env['hr.employee'].sudo().search([])
        help_desk_team = request.env['help.desk.team'].sudo().search([])
        print(employees)
        values = {'employees': employees, 'help_desk_team': help_desk_team}
        return request.render("help_desk.online_help_desk_form", values)

    @http.route(['/help_desk/submit'], type='http', auth="public", website=True)
    def help_desk_form_submit(self, **post):
        help_desk = request.env['help.desk.tickets'].sudo().create({
            'request': post.get('request'),
            'help_desk_team': post.get('help_desk_team'),
            'employee': post.get('employee'),
            'phone': post.get('phone'),
            'email':  post.get('email'),

        })
        vals = {
            'help_desk': help_desk,
        }
        print(vals)
        return request.render("help_desk.tmp_help_desk_form_success", vals)

