import pytest
import bear_test_data

@pytest.mark.parametrize('bear_property', bear_test_data.valid_bear_props, ids = lambda p: f'{p["property_name"]}:{p["property_value"]}')
def test_create_bear(api, bear_property):
    """ Checks all bears with specified property created correctly. """
    bear_to_add = dict(bear_test_data.stock_bears[0])
    bear_to_add[bear_property['property_name']] = bear_property['property_value']
    
    added_bear_id = api.create_bear(bear_to_add)
    
    existing_bears = api.get_all_bears()
    existing_bear_ids = [ bear['bear_id'] for bear in existing_bears ]
    
    assert len(existing_bears) == 1, f'only one bear adding expected, {len(existing_bear_ids)} existing'
    assert added_bear_id == existing_bear_ids[0], f'bear #{existing_bear_ids[0]} exists, bear #{added_bear_id} expected'
    for k in bear_to_add.keys():
        assert bear_to_add[k] == existing_bears[0][k], f'added and existing bears don\'t match (added: {bear_to_add}, exists: {existing_bears[0]})'
        
