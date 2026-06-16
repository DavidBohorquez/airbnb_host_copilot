"""Occupancy / demand from the 4.5M-row calendar. Implement in M7 (docs/08_analytics_tools.md).

Use DuckDB to query calendar.csv directly — never load it fully into pandas.
"""

from __future__ import annotations


def occupancy_stats(listing_id: int) -> dict:
    """Booked-night ratio for the listing vs its peer group, from calendar availability.

    Return e.g. {'listing_occupancy': ..., 'peer_median_occupancy': ...}. TODO M7.
    """
    raise NotImplementedError
