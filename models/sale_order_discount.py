# -*- coding: utf-8 -*-
# Copyright 2017 Faros Inversiones Ltda.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _


class Sale_order_discount(models.Model):

    _description = 'Sale order global discount'
    _inherit = 'sale.order'

    discount_type = fields.Selection(
                                     [('percent','Percentage'),
                                      ('amount','Amount')],
                                      string = 'Discount Type',
                                      help = 'Select discount type',
                                      default = 'percent')
    discount_rate = fields.Float( string = 'Discount Rate', default = '0.0', store = True)

    amount_discount = fields.Float( string = 'Total Global Discount', compute='_compute_discount', store = True)


    @api.one
    @api.depends('discount_type','discount_rate','amount_total')
    def _compute_discount(self):

        mod_obj = self.env['ir.model.data']
        amount_discount = 0.0
        if self.discount_type == 'percent':
            amount_discount = self.amount_untaxed * self.discount_rate / 100
        else:
            amount_discount = self.discount_rate

        self.amount_discount = amount_discount



    @api.depends('order_line.price_total')
    @api.multi
    def _amount_all(self):
        """
        Compute the total amounts of the SO.
        """

        for order in self:
            amount_untaxed = amount_tax = amount_discount = 0.0
            for line in order.order_line:
                amount_untaxed += line.price_subtotal
                amount_tax += line.price_tax
            if self.discount_type == 'percent':
                amount_discount = amount_untaxed * self.discount_rate / 100
            else:
                amount_discount = self.discount_rate

            order.update({
                'amount_untaxed': order.pricelist_id.currency_id.round(amount_untaxed),
                'amount_tax': order.pricelist_id.currency_id.round(amount_tax),
                'amount_discount': order.pricelist_id.currency_id.round(amount_discount),
                'amount_total': amount_untaxed - amount_discount + amount_tax,
            })



    @api.model
    def _prepare_invoice(self):
        """
        This method send the discount_type, discount_rate and amount_discount to the
        account.invoice model
        """
        res = super(sale_order_discount, self)._prepare_invoice()
        res['discount_type'] = self.discount_type
        res['discount_rate'] = self.discount_rate

        return res

