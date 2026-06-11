{
    'name': 'CRM Inquiry & Sales Flow',
    'version': '1.0',
    'category': 'Sales/CRM',
    'summary': 'Customizes Odoo CRM and Sales apps to fit a specific Inquiry and Sales flow.',
    'depends': ['crm', 'sale_management', 'utm', 'contacts'],
    'data': [
        'data/crm_stage_data.xml',
        'data/utm_source_data.xml',
        'data/crm_tag_data.xml',
        'data/crm_lost_reason_data.xml',
        'views/crm_lead_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
