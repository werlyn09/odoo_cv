import jinja2

from odoo import http

loader = jinja2.PackageLoader('odoo.addons.theme_odoobim', 'views')
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
