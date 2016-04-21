# -*- coding: utf-8 -*-
{
    'name': "Sale Global Discount",

    'summary': """
        Sale Global Discount for Sale Orders and Invoices by amount or percentage""",

    'description': """
        Add fields to Sale order and Invoice to set Global discount on total untaxed amount
    """,

    'author': "Faros Inversiones Ltda.",
    'website': "http://github.com/farosinv",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'sales',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/invoice_form_view.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}