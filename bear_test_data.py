# -*- coding: utf-8 -*-

stock_bears = [
    {'bear_type':'POLAR', 'bear_name':'MIKHAIL', 'bear_age':1.0},
    {'bear_type':'BLACK', 'bear_name':'Михаил', 'bear_age':0.0},
    {'bear_type':'BROWN', 'bear_name':'Grylls', 'bear_age':17.5},
    {'bear_type':'GUMMY', 'bear_name':'Gruffi', 'bear_age':33.5}
]

valid_bear_names = ['MICHAEL', 'mikhail', 'Михаил', 'バラライククマ', 'Bear Grylls', 'Mikhail Палыч Jr.']
valid_bear_types = ['POLAR', 'BROWN', 'BLACK', 'GUMMY']
valid_bear_ages = [0, 0.0, 1, 1.0, 3.14]

valid_bear_props = [ {'property_name': 'bear_name', 'property_value': value} for value in valid_bear_names ] \
                + [ {'property_name': 'bear_type', 'property_value': value} for value in valid_bear_types ] \
                + [ {'property_name': 'bear_age', 'property_value': value} for value in valid_bear_ages ]
