import pytest
import bear_test_data

@pytest.mark.parametrize('bears_to_add', [bear_test_data.stock_bears[0:1], bear_test_data.stock_bears[0:3]], ids = ['one bear', 'three bears'])
def test_delete_all_bears(api, bears_to_add):
    """Checks removal of all bears"""
    for bear in bears_to_add:
        api.create_bear(bear)
        
    existing_bears = api.get_all_bears()
    assert len(existing_bears) == len(bears_to_add), f'{len(existing_bears)} bears before removal, {len(bears_to_add)} expected.'
    
    status_code = api.delete_all_bears()
    
    bears_list = api.get_all_bears()
    assert len(bears_list) == 0, f'0 bears excected after removal, but {len(bears_list)} got'
