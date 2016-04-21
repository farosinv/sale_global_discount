# -*- coding: utf-8 -*-

from openerp import models, fields, api, _
from samba.dcerpc.dns import res_rec
from openerp.tools import float_is_zero, float_compare


class sale_order_discount(models.Model):
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
    
            
class invoice_global_discount(models.Model):
    _description = 'Invoice global discount'
    _inherit = 'account.invoice'
     
    discount_type = fields.Selection(
                                     [('percent','Percentage'),
                                      ('amount','Amount')],
                                      string = 'Discount Type',
                                      help = 'Select discount type',
                                      default = 'percent')
    discount_rate = fields.Float( string = 'Discount Rate', default = '0.0', store = True)
    
    amount_discount = fields.Monetary( string = 'Total Global Discount', compute='_compute_discount', store = True) 
    
    
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
    

    @api.one
    @api.depends('invoice_line_ids.price_subtotal', 'tax_line_ids.amount', 'currency_id', 'company_id')
    def _compute_amount(self):

        self.amount_untaxed = sum(line.price_subtotal for line in self.invoice_line_ids)
        self.amount_tax = sum(line.amount for line in self.tax_line_ids)
        amount_discount = amount_total = 0.0
        if self.discount_type == 'percent':
            amount_discount = self.amount_untaxed * self.discount_rate / 100
        else:
            amount_discount = self.discount_rate
                
        amount_total = self.amount_untaxed - amount_discount + self.amount_tax
        self.amount_total = amount_total
        
        amount_total_company_signed = amount_total
        amount_untaxed_signed = self.amount_untaxed
        if self.currency_id and self.currency_id != self.company_id.currency_id:
            amount_total_company_signed = self.currency_id.compute(self.amount_total, self.company_id.currency_id)
            amount_untaxed_signed = self.currency_id.compute(self.amount_untaxed, self.company_id.currency_id)
        sign = self.type in ['in_refund', 'out_refund'] and -1 or 1
        self.amount_total_company_signed = amount_total_company_signed * sign
        self.amount_total_signed = self.amount_total * sign
        self.amount_untaxed_signed = amount_untaxed_signed * sign

    @api.one
    @api.depends(
        'state', 'currency_id', 'invoice_line_ids.price_subtotal',
        'move_id.line_ids.amount_residual',
        'move_id.line_ids.currency_id')
    def _compute_residual(self):
        residual = 0.0
        residual_company_signed = 0.0
        sign = self.type in ['in_refund', 'out_refund'] and -1 or 1
        for line in self.sudo().move_id.line_ids:
            if line.account_id.internal_type in ('receivable', 'payable'):
                residual_company_signed += line.amount_residual
                if line.currency_id == self.currency_id:
                    residual += line.amount_residual_currency if line.currency_id else line.amount_residual
                else:
                    from_currency = (line.currency_id and line.currency_id.with_context(date=line.date)) or line.company_id.currency_id.with_context(date=line.date)
                    residual += from_currency.compute(line.amount_residual, self.currency_id)
        self.residual_company_signed = abs(residual_company_signed) * sign - self.amount_discount
        self.residual_signed = abs(residual) * sign - self.amount_discount
        self.residual = abs(residual) - self.amount_discount
        digits_rounding_precision = self.currency_id.rounding
        if float_is_zero(self.residual, precision_rounding=digits_rounding_precision):
            self.reconciled = True
        else:
            self.reconciled = False