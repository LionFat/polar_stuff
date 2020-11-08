import pytest
import bear_test_data

@pytest.mark.parametrize('bear_position_to_update', [0, 2, -1], ids = ['first', 'third', 'last'])
@pytest.mark.parametrize('bear_property', bear_test_data.valid_bear_props, ids = lambda p: f'{p["property_name"]}:{p["property_value"]}')
def test_update_bear(api, bear_property, bear_position_to_update):
    """Checks the specified position bear in has updated its property right"""
    bear_ids = [ api.create_bear(bear) for bear in bear_test_data.stock_bears ]
    bear_id_to_update = bear_ids[bear_position_to_update]
    
    bear = api.get_bear(bear_id_to_update)
    
    assert type(bear) is dict, f'dict bear structure expected, {bear} recieved'
    assert bear['bear_id'] == bear_id_to_update, f'bear #{bear_id_to_update} requested, bear #{bear["bear_id"]} received'
    
    bear[bear_property['property_name']] = bear_property['property_value']
    api.update_bear(bear_id_to_update, data=bear)
    
    updated_bear = api.get_bear(bear_id_to_update)
    assert type(updated_bear) is dict, f'dict bear structure expected, {updated_bear} recieved'
    assert bear['bear_id'] == bear_id_to_update, f'bear #{bear_id_to_update} requested, bear #{bear["bear_id"]} received'
    
    for k in updated_bear.keys():
        assert bear[k] == updated_bear[k], f'expected bear and received updated bear are not matching (updated: {bear}, received: {updated_bear}'