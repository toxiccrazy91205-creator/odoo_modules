# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class BoilerEstimation(models.Model):
    _name = 'boiler.estimation'
    _description = 'Boiler Estimation'
    _order = 'id desc'

    name = fields.Char(string='Name', required=True, copy=False, readonly=True, default=lambda self: _('New'))
    partner_id = fields.Many2one('res.partner', string='Customer', required=True)
    state = fields.Selection([
        ('draft', 'Sales Team Creates RFQ'),
        ('engineering', 'Engineering Validation'),
        ('bom', 'BOM Estimation'),
        ('costing', 'Costing & Margin'),
        ('done', 'Quotation Released')
    ], string='Status', default='draft', tracking=True)
    
    margin_percentage = fields.Float(string='Margin (%)')
    
    material_line_ids = fields.One2many('boiler.estimation.material', 'estimation_id', string='Raw Materials')
    fabrication_line_ids = fields.One2many('boiler.estimation.fabrication', 'estimation_id', string='Fabrication')
    testing_line_ids = fields.One2many('boiler.estimation.testing', 'estimation_id', string='Testing')
    logistics_line_ids = fields.One2many('boiler.estimation.logistics', 'estimation_id', string='Logistics')
    
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)
    
    total_material_cost = fields.Monetary(string='Total Material Cost', compute='_compute_totals', store=True)
    total_fabrication_cost = fields.Monetary(string='Total Fabrication Cost', compute='_compute_totals', store=True)
    total_testing_cost = fields.Monetary(string='Total Testing Cost', compute='_compute_totals', store=True)
    total_logistics_cost = fields.Monetary(string='Total Logistics Cost', compute='_compute_totals', store=True)
    total_base_cost = fields.Monetary(string='Total Base Cost', compute='_compute_totals', store=True)
    final_sales_price = fields.Monetary(string='Final Sales Price', compute='_compute_totals', store=True)
    
    sale_order_id = fields.Many2one('sale.order', string='Sale Order', readonly=True)

    @api.model_create_multi
    def create(self, vals_list):
        """ Override create to assign sequence number """
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('boiler.estimation') or _('New')
        return super().create(vals_list)

    @api.depends('material_line_ids.subtotal', 'fabrication_line_ids.subtotal', 
                 'testing_line_ids.subtotal', 'logistics_line_ids.subtotal', 'margin_percentage')
    def _compute_totals(self):
        """ Compute all totals and final sales price based on lines and margin """
        for rec in self:
            rec.total_material_cost = sum(rec.material_line_ids.mapped('subtotal'))
            rec.total_fabrication_cost = sum(rec.fabrication_line_ids.mapped('subtotal'))
            rec.total_testing_cost = sum(rec.testing_line_ids.mapped('subtotal'))
            rec.total_logistics_cost = sum(rec.logistics_line_ids.mapped('subtotal'))
            
            rec.total_base_cost = (rec.total_material_cost + rec.total_fabrication_cost + 
                                   rec.total_testing_cost + rec.total_logistics_cost)
            
            rec.final_sales_price = rec.total_base_cost + (rec.total_base_cost * (rec.margin_percentage / 100.0))

    def action_generate_quotation(self):
        """ Generate Quotation (sale.order) based on final sales price """
        self.ensure_one()
        # Find or create a generic 'Custom Boiler' product to use in the sale order line
        product = self.env['product.product'].search([('name', '=', 'Custom Boiler')], limit=1)
        if not product:
            product = self.env['product.product'].create({
                'name': 'Custom Boiler',
                'type': 'service',
                'list_price': 0.0,
            })
            
        sale_order = self.env['sale.order'].create({
            'partner_id': self.partner_id.id,
            'origin': self.name,
            'order_line': [(0, 0, {
                'product_id': product.id,
                'name': f'Custom Boiler - {self.name}',
                'product_uom_qty': 1,
                'price_unit': self.final_sales_price,
            })]
        })
        
        self.write({
            'sale_order_id': sale_order.id,
            'state': 'done'
        })
        
        return {
            'type': 'ir.actions.act_window',
            'name': 'Sale Order',
            'res_model': 'sale.order',
            'res_id': sale_order.id,
            'view_mode': 'form',
            'target': 'current',
        }

class BoilerEstimationLineMixin(models.AbstractModel):
    _name = 'boiler.estimation.line.mixin'
    _description = 'Estimation Line Mixin'

    estimation_id = fields.Many2one('boiler.estimation', string='Estimation', required=True, ondelete='cascade')
    product_id = fields.Many2one('product.product', string='Product', required=True)
    name = fields.Char(string='Description', required=True)
    quantity = fields.Float(string='Quantity', default=1.0, required=True)
    uom_id = fields.Many2one('uom.uom', string='Unit of Measure', related='product_id.uom_id', readonly=True)
    unit_cost = fields.Float(string='Unit Cost', required=True)
    subtotal = fields.Float(string='Subtotal', compute='_compute_subtotal', store=True)
    currency_id = fields.Many2one(related='estimation_id.currency_id')

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.name = self.product_id.display_name
            self.unit_cost = self.product_id.standard_price

    @api.depends('quantity', 'unit_cost')
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.quantity * line.unit_cost

class BoilerEstimationMaterial(models.Model):
    _name = 'boiler.estimation.material'
    _description = 'Raw Materials'
    _inherit = 'boiler.estimation.line.mixin'

class BoilerEstimationFabrication(models.Model):
    _name = 'boiler.estimation.fabrication'
    _description = 'Fabrication'
    _inherit = 'boiler.estimation.line.mixin'

class BoilerEstimationTesting(models.Model):
    _name = 'boiler.estimation.testing'
    _description = 'Testing'
    _inherit = 'boiler.estimation.line.mixin'

class BoilerEstimationLogistics(models.Model):
    _name = 'boiler.estimation.logistics'
    _description = 'Logistics'
    _inherit = 'boiler.estimation.line.mixin'
