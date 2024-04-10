import pytest
import pytest_mock
from src.ayjay import AyJay

# Functionality tests
def test_ayjay_innit_no_error() -> None:
    aj = AyJay()

# Value erroer tests
def test_get_wrong_arg_type_value_error(api) -> None:
    with pytest.raises(ValueError):
        actual_response = api.list_breeds(
            query_dict="Invalid")

