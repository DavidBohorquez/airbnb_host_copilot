"""M1 checkpoint. Unskip each test as you implement the matching function in data/loaders.py."""

import pytest

from host_copilot.data import loaders


@pytest.mark.skip(reason="implement parse_price in M1")
def test_parse_price():
    assert loaders.parse_price("$1,234.00") == 1234.0
    assert loaders.parse_price("") is None


@pytest.mark.skip(reason="implement accommodates_band in M1")
def test_accommodates_band():
    assert loaders.accommodates_band(1) == "1-2"
    assert loaders.accommodates_band(4) == "3-4"


@pytest.mark.skip(reason="implement peer_key in M1")
def test_peer_key():
    assert loaders.peer_key("Chartrons", "Entire home/apt", 4) == "Chartrons|Entire home/apt|3-4"
