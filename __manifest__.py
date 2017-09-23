# -*- coding: utf-8 -*-
# Copyright 2017 Faros Inversiones Ltda.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Sale Global Discount',
    'description': """
        Add global discount to sales flow""",
    'version': '10.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'Faros Inversiones Ltda.',
    'website': 'www.farosinv.cl',
    'depends': [
        'sale',
        'account',
    ],
    'data': [
        'views/invoice_global_discount.xml',
        'security/sale_order_discount.xml',
        'views/sale_order_discount.xml',
    ],
    'demo': [
    ],
}
