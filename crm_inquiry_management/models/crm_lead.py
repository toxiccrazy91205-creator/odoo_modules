from odoo import fields, models

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    competitor_name = fields.Char(
        string='Competitor Name',
        help='Name of the competitor tracking this inquiry.'
    )
