# -*- coding: utf-8 -*-
from openerp import http

# class SaleGlobalDiscount(http.Controller):
#     @http.route('/sale_global_discount/sale_global_discount/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sale_global_discount/sale_global_discount/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('sale_global_discount.listing', {
#             'root': '/sale_global_discount/sale_global_discount',
#             'objects': http.request.env['sale_global_discount.sale_global_discount'].search([]),
#         })

#     @http.route('/sale_global_discount/sale_global_discount/objects/<model("sale_global_discount.sale_global_discount"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sale_global_discount.object', {
#             'object': obj
#         })