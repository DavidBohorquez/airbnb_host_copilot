"""Price analytics vs comps. Implement in M7 (docs/08_analytics_tools.md).

Returns a typed dict the LLM can cite (no prose here — that's the LLM's job).
"""

from __future__ import annotations


def price_position(listing_id: int) -> dict:
    """Price percentiles of the listing's peer group + where this listing sits.

    Return e.g. {'p25': ..., 'p50': ..., 'p75': ..., 'listing_price': ..., 'percentile': ...}. TODO M7.
    """
    raise NotImplementedError
