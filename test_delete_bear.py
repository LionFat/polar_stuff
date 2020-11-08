import pytest
import bear_test_data

@pytest.mark.parametrize('bear_position_to_delete', [0, 2, -1], ids = ['first', 'third', 'last'])
def test_delete_bear(api, bear_position_to_delete):
    """Checks bear removal"""
    bear_ids = [ api.create_bear(bear) for bear in bear_test_data.stock_bears ]
    bear_id_to_delete = bear_ids[bear_position_to_delete]
    
    existing_bears = api.get_all_bears()
    assert len(existing_bears) == len(bear_test_data.stock_bears), f'{len(existing_bears)} bears before removal, {len(bear_test_data.stock_bears)} expected.'

    api.delete_bear(bear_ids[bear_position_to_delete])
    
    existing_bear_ids = [ bear['bear_id'] for bear in api.get_all_bears() ]
    removed_bear_ids = [ id for id in bear_ids if id not in existing_bear_ids ]
    
    assert len(removed_bear_ids) == 1, f'one bear removal expected, but {len(removed_bear_ids)} removed'
    
    removed_bear_id = removed_bear_ids[0]
    assert bear_id_to_delete == removed_bear_id, f'bear #{bear_id_to_delete} removal expected, bear #{removed_bear_id} removed (before removal: {bear_ids}, after: {existing_bear_ids})'
    
