import pytest

from tests.contract.validate_all import run

pytestmark = pytest.mark.contract


def test_all_event_contracts_valid():
    assert run() == 0
