# -*- coding: utf-8 -*-
# Copyright 2017 Faros Inversiones Ltda.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _


class GlobalDiscountConfig(models.TransientModel):
    _inherit = 'sale.config.settings'
    
    globaldiscount_account_id = fields.Many2one('account.account', company_dependent=True,
        string="Global Discount account",
        domain=[('deprecated', '=', False)],
        help="Account for discount moves expenses.")
 

    @api.multi
    def set_globaldiscount_account(self):
        return self.env['ir.values'].sudo().set_default(
            'sale.config.settings', 'globaldiscount_account_id', self.globaldiscount_account_id.id)