import pytest
import bear_test_data

@pytest.mark.parametrize('bear_position_to_receive', [0, 2, -1], ids = ['first', 'third', 'last'])
def test_get_bear(api, bear_position_to_receive):
    """Checks getting one bear by id"""
    bears_to_add = [ dict(bear) for bear in bear_test_data.stock_bears ]
    for bear_to_add in bears_to_add:
        bear_to_add['bear_id'] = api.create_bear(bear_to_add)
    
    bear = api.get_bear(bears_to_add[bear_position_to_receive]['bear_id'])
    assert type(bear) is dict, f'dict bear structure expected, {bear} recieved'
    assert bear['bear_id'] == bears_to_add[bear_position_to_receive]['bear_id'], f'bear #{bear_id_to_recieve} requested, bear #{bear["bear_id"]} received'
    
    bear_to_compare = bears_to_add[bear_position_to_receive]

    for k in bear_to_compare.keys():
        assert bear_to_compare[k] == bear[k], f'requested and received bears are not matching (added: {bear}, exists: {bear_to_compare})'
