# -*- coding: utf-8 -*-

{
    'name': 'Estate',
    'depends': ['base_setup','web', 'base'],
    'data': [

        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_type.xml',
        'views/estate_property_tag.xml',
        'views/estate_property_offer.xml',
        'views/estate_property_inherit.xml'
    ],
    'application': True,
}