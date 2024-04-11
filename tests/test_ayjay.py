import pytest


# Functionality tests
def test_ayjay_innit_no_error(ayjay_fixture) -> None:
    _ = ayjay_fixture


def test_ayjay_cached_disabled_innit_no_error(ayjay_fixture_no_cache) -> None:
    _ = ayjay_fixture_no_cache


def test_get_wrong_arg_type_value_error(ayjay_fixture) -> None:
    with pytest.raises(ValueError):
        _ = ayjay_fixture.get("http://test.com/", params="Invalid")


def test_get_wrong_arg_name_value_error(ayjay_fixture) -> None:
    with pytest.raises(TypeError):
        _ = ayjay_fixture.get("http://test.com/", query="Invalid")


# Mocked test
def test_get_correct_response_no_cache(mocker, ayjay_fixture_no_cache) -> None:
    mocked_endpoint = "http://fakeapi.test.com/"
    mocked_call_api_value = [
        {
            "player_name": "Jordan Mabey",
            "position": "goalkeeper",
            "team_name": "Barcelona",
            "goals_scored": 32,
            "matches_played": 39,
        }
    ]

    mocker.patch("ayjay.AyJay.get", return_value=mocked_call_api_value)
    actual_mock_response = ayjay_fixture_no_cache.get(
        mocked_endpoint, params={"fakeParamA": 1, "fakeParamB": 2, "fakeParamC": 1}
    )
    assert mocked_call_api_value == actual_mock_response


def test_get_correct_response(mocker, ayjay_fixture) -> None:
    mocked_endpoint = "http://fakeapi.test.com/"

    # call 1
    mocked_call_api_value_1 = [
        {
            "player_name": "Dennie Mulberry",
            "position": "defender",
            "team_name": "Manchester United",
            "goals_scored": 21,
            "matches_played": 7,
        }
    ]

    mocker.patch("ayjay.AyJay.get", return_value=mocked_call_api_value_1)
    actual_mock_response_1 = ayjay_fixture.get(
        mocked_endpoint, params={"fakeParamD": 1}
    )
    # call 2
    mocked_call_api_value_2 = [
        {
            "player_name": "Hale Jagiela",
            "position": "defender",
            "team_name": "Real Madrid",
            "goals_scored": 11,
            "matches_played": 10,
        },
        {
            "player_name": "Barby Malham",
            "position": "goalkeeper",
            "team_name": "Barcelona",
            "goals_scored": 33,
            "matches_played": 14,
        },
    ]

    mocker.patch("ayjay.AyJay.get", return_value=mocked_call_api_value_2)
    actual_mock_response_2 = ayjay_fixture.get(
        mocked_endpoint, params={"fakeParamD": 2}
    )
    assert (
        mocked_call_api_value_1 == actual_mock_response_1
        and mocked_call_api_value_2 == actual_mock_response_2
        and actual_mock_response_1 != actual_mock_response_2
    )
