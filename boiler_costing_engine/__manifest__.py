# -*- coding: utf-8 -*-
{
    'name': 'Boiler Costing & Estimation Engine',
    'version': '1.0',
    'category': 'Sales',
    'summary': 'Custom Estimation & Costing flow for Boilers',
    'description': """
        Custom Estimation & Costing flow for Boilers.
        Provides a comprehensive workflow from RFQ to Quotation Release with detailed breakdown of:
        - Raw Materials
        - Fabrication & Labour
        - Testing
        - Logistics
    """,
    'author': 'Antigravity',
    'depends': ['sale_management', 'product', 'mrp'],
    'data': [
        'security/ir.model.access.csv',
        'data/product_data.xml',
        'views/boiler_estimation_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
