import pytest
import bear_test_data

@pytest.mark.parametrize('bears_to_add', [[], bear_test_data.stock_bears[0:1], bear_test_data.stock_bears[0:3]], ids = ['no bears', 'one bear', 'three bears'])
def test_get_all_bears(api, bears_to_add):
    """Checks getting all bears"""
    for bear_to_add in bears_to_add:
        bear_to_add['bear_id'] = api.create_bear(bear_to_add)
    
    existing_bears = api.get_all_bears()
    assert len(bears_to_add) == len(existing_bears), f'{len(bears_to_add)} bears expected, got {len(existing_bears)}'
    
    for bear in bears_to_add:
        bears_to_compare = [ b for b in existing_bears if b['bear_id'] == bear['bear_id'] ]
        assert len(bears_to_compare) > 0, f'no existing bears with specific id {bear["bear_id"]}'
        assert len(bears_to_compare) == 1, f'multiple bears with specific id {bear["bear_id"]}'
        bear_to_compare = bears_to_compare[0]
        
        for k in bear.keys():
            assert bear[k] == bear_to_compare[k], f'added and existing bears are not matching (added: {bear}, exists: {bear_to_compare})'
