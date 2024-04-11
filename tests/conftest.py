import pytest
from ayjay import AyJay


@pytest.fixture(scope="session")
def ayjay_fixture():
    """Create the ayjay object."""
    ayjay_fixture = AyJay(cache_expiry=5)
    return ayjay_fixture


@pytest.fixture(scope="session")
def ayjay_fixture_no_cache():
    """Create the ayjay object."""
    ayjay_fixture = AyJay(disable_caching=True)
    return ayjay_fixture
