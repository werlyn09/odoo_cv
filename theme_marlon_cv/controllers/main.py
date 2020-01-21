import jinja2

from odoo import http

loader = jinja2.PackageLoader('odoo.addons.theme_marlon_cv', 'views')
env = jinja2.Environment(loader=loader, autoescape=True)


class MainController(http.Controller):

    @http.route('/', methods=['GET'], auth='none')
    def cv_endpoint(self, **kwargs):
        company = http.request.env['res.company'].sudo().search([], limit=1)
        return env.get_template('index.html').render({
            'company': company,
            'company_fhone': company.phone,
            'company_email': company.email,
            'logo': company.logo and 'data:image/png;base64,%s' % company.logo.decode()
        })

    @http.route('/modal', methods=['GET'], auth='public')
    def modal(self, **kwargs):
        return env.get_template('modal.html').render({
            'csrf_token': http.request.csrf_token(),
        })

    @http.route('/modal', type='json', auth='public')
    def modal_response(self, name, phone, email, message, city, **kwargs):
        partner = http.request.env['res.partner'].sudo().search([('email', 'ilike', email.strip())], limit=1)
        if not partner:
            partner = partner.sudo().create({
                'name': name.strip(),
                'phone': phone.strip(),
                'email': email.strip(),
            })
        http.request.env['crm.lead'].sudo().create({
            'name': '%s  <%s>' % (name.strip(), email.strip()),
            'partner_id': partner.id,
            'email_from': email.strip(),
            'user_id':2,
            'description': '%s' % (message.strip()),
        })
        return {
            'name': name,
        }