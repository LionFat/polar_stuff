# -*- coding: utf-8 -*-

import pytest
import requests, json

stock_bears = [
    {'bear_type':'POLAR', 'bear_name':'MIKHAIL', 'bear_age':1.0},
    {'bear_type':'BLACK', 'bear_name':'Михаил', 'bear_age':0.0},
    {'bear_type':'BROWN', 'bear_name':'Grylls', 'bear_age':17.5},
    {'bear_type':'GUMMY', 'bear_name':'Gruffi', 'bear_age':33.5}
]

bear_names = ['MICHAEL', 'mikhail', 'Михаил', 'バラライククマ', 'Bear Grylls', 'Mikhail Палыч Jr.']
bear_types = ['POLAR', 'BROWN', 'BLACK', 'GUMMY']
bear_ages = [0, 0.0, 1, 1.0, 3.14]
bears_key_value = [ ('bear_name', value) for value in bear_names ] \
                + [ ('bear_type', value) for value in bear_types ] \
                + [ ('bear_age', value) for value in bear_ages ]

@pytest.mark.parametrize('key_value', bears_key_value,  ids = lambda v: f'{v[0]}={v[1]}')
def test_bear_adding(api, delete_all_bears, key_value):
    
    global stock_bears
    
    field_name = key_value[0]
    field_value = key_value[1]
    
    bear_to_add = dict(stock_bears[0])
    bear_to_add[field_name] = field_value
    
    added_bear_id = api.post('/bear', data=json.dumps(bear_to_add)).text
    
    existing_bears = api.get('/bear').json()
    existing_bear_ids = [ str(bear['bear_id']) for bear in existing_bears ]
    
    assert len(existing_bears) == 1, f'only one bear adding expected, {len(existing_bear_ids)} existing'
    assert added_bear_id == existing_bear_ids[0], f'bear #{existing_bear_ids[0]} exists, bear #{added_bear_id} expected'
    for k in bear_to_add.keys():
        assert bear_to_add[k] == existing_bears[0][k], f'added and existing bears don\'t match (added: {bear_to_add}, exists: {existing_bears[0]})'
        
@pytest.mark.parametrize('bears_to_add', [[], stock_bears[0:1], stock_bears[0:3]], ids = ['no bears', 'one bear', 'three bears'])
def test_bear_list_receiving(api, delete_all_bears, bears_to_add):
    
    for i in range(0, len(bears_to_add)):
        bears_to_add[i]['bear_id'] = int(api.post('/bear', data=json.dumps(bears_to_add[i])).text)
    
    res = api.get('/bear')
    existing_bears = res.json()
    assert res.status_code == 200, f'bears receiving 200 status code expected, got {res.status_code}'
    assert len(bears_to_add) == len(existing_bears), f'{len(bears_to_add)} bears expected, got {len(existing_bears)}'
    
    for bear in bears_to_add:
        bears_to_compare = [ b for b in existing_bears if b['bear_id'] == bear['bear_id'] ]
        assert len(bears_to_compare) > 0, f'no existing bears with specific id {bear["bear_id"]}'
        bear_to_compare = bears_to_compare[0]
        
        for k in bear.keys():
            assert bear[k] == bear_to_compare[k], f'added and existing bears are not matching (added: {bear}, exists: {bear_to_compare})'

@pytest.mark.parametrize('bear_position_to_receive', [0, 2, -1], ids = ['first', 'third', 'last'])
def test_one_bear_receiving(api, delete_all_bears, bear_position_to_receive):
    
    global stock_bears
    
    bear_ids = [ api.post('/bear', data=json.dumps(bear)).text for bear in stock_bears ]
    bear_id_to_recieve = bear_ids[bear_position_to_receive]
    
    res = api.get('/bear/' + bear_id_to_recieve)
    bear = res.json()
    assert res.status_code == 200, f'bears receiving 200 status code expected, got {res.status_code}'
    assert type(bear) is dict, f'dict bear structure expected, {bear} recieved'
    assert str(bear['bear_id']) == bear_id_to_recieve, f'bear #{bear_id_to_recieve} requested, bear #{bear["bear_id"]} received'
    
    bear_to_compare = stock_bears[bear_position_to_receive]
    
    for k in bear_to_compare.keys():
        assert bear[k] == bear_to_compare[k], f'requested and received bears are not matching (added: {bear}, exists: {bear_to_compare})'
    
@pytest.mark.parametrize('bear_position_to_update', [0, 2, -1], ids = ['first', 'third', 'last'])
@pytest.mark.parametrize('key_value', bears_key_value,  ids = lambda v: f'{v[0]}={v[1]}')
def test_bear_updating(api, delete_all_bears, key_value, bear_position_to_update):
    
    global stock_bears
    
    bear_ids = [ api.post('/bear', data=json.dumps(bear)).text for bear in stock_bears ]
    bear_id_to_update = bear_ids[bear_position_to_update]
    
    res = api.get('/bear/' + bear_id_to_update)
    bear = res.json()
    assert res.status_code == 200, f'bears receiving status 200 code expected, got {res.status_code}'
    assert type(bear) is dict, f'dict bear structure expected, {bear} recieved'
    assert str(bear['bear_id']) == bear_id_to_update, f'bear #{bear_id_to_update} requested, bear #{bear["bear_id"]} received'
    
    bear[key_value[0]] = key_value[1]
    res = api.put('/bear/' + bear_id_to_update, data=json.dumps(bear))
    assert res.status_code == 200, f'bear updating status code 200 expected, got {res.status_code}'
    
    res = api.get('/bear/' + bear_id_to_update)
    updated_bear = res.json()
    assert res.status_code == 200, f'bears receiving status 200 code expected, got {res.status_code}'
    assert type(updated_bear) is dict, f'dict bear structure expected, {updated_bear} recieved'
    assert str(bear['bear_id']) == bear_id_to_update, f'bear #{bear_id_to_update} requested, bear #{bear["bear_id"]} received'
    
    for k in updated_bear.keys():
        assert bear[k] == updated_bear[k], f'expected bear and received updated bear are not matching (updated: {bear}, received: {updated_bear}'
    

@pytest.mark.parametrize('bears_to_add', [stock_bears[0:1], stock_bears[0:3]], ids = ['one bear', 'three bears'])
def test_all_bears_removal(api, delete_all_bears, bears_to_add):
    
    for bear in bears_to_add:
        api.post('/bear', data=json.dumps(bear))
        
    existing_bears = api.get('/bear').json()
    assert len(existing_bears) == len(bears_to_add), f'{len(existing_bears)} bears before removal, {len(bears_to_add)} expected.'
    
    status_code = api.delete('/bear').status_code
    assert status_code == 200, f'/delete 200 status code expected, got {status_code}'
    
    bears_list = api.get('/bear').json()
    assert len(bears_list) == 0, f'0 bears excected after removal, {len(bears_list)} got'
    
@pytest.mark.parametrize('bear_position_to_delete', [0, 2, -1], ids = ['first', 'third', 'last'])
def test_specified_bear_removal(api, delete_all_bears, bear_position_to_delete):
    
    global stock_bears
    
    bear_ids = [ api.post('/bear', data=json.dumps(bear)).text for bear in stock_bears ]
    bear_id_to_delete = bear_ids[bear_position_to_delete]
    
    existing_bears = api.get('/bear').json()
    assert len(existing_bears) == len(stock_bears), f'{len(existing_bears)} bears before removal, {len(stock_bears)} expected.'

    status_code = api.delete('/bear/' + bear_ids[bear_position_to_delete]).status_code
    assert status_code == 200, f'/delete 200 status code expected, got {status_code}'
    
    existing_bear_ids = [ str(bear['bear_id']) for bear in api.get('/bear').json() ]
    removed_bear_ids = [ id for id in bear_ids if id not in existing_bear_ids ]
    removed_bear_id = removed_bear_ids[0]
    
    assert len(removed_bear_ids) == 1, f'one bear removal expected, but {len(removed_bear_ids)} removed'
    assert bear_id_to_delete == removed_bear_id, f'bear #{bear_id_to_delete} removal expected, bear #{removed_bear_id} removed (before removal: {bear_ids}, after: {existing_bear_ids})'
    
