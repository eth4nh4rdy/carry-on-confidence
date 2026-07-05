"""
Aggregator for Carry-On Confidence.

Runs every registered fetcher (Naver, YouTube, KOSIS) for a given
location/topic/level, collects their results via BaseFetcher._safe_fetch(),
and combines them into a single payload for the worksheet generator.
Fetcher-level failures are already isolated by _safe_fetch() — this module
only adds cross-source bookkeeping (totals, error flags, timestamp) and logs
what happened per source.
"""

import logging
from datetime import datetime, timezone

from fetchers.naver_fetcher import NaverFetcher
from fetchers.youtube_fetcher import YouTubeFetcher
from fetchers.kosis_fetcher import KosisFetcher

logger = logging.getLogger(__name__)


def aggregate(location: str, topic: str, level: int) -> dict:
    try:
        fetchers = {
            "naver": NaverFetcher(),
            "youtube": YouTubeFetcher(),
            "kosis": KosisFetcher(),
        }

        sources = {}
        has_errors = False
        total_results = 0

        for name, fetcher in fetchers.items():
            logger.info("Running fetcher: %s", name)
            result = fetcher._safe_fetch(location, topic, level)
            sources[name] = result

            result_count = len(result["results"])
            total_results += result_count
            logger.info("Fetcher %s returned %d results", name, result_count)

            if result["error"] is not None:
                has_errors = True
                logger.warning("Fetcher %s returned an error: %s", name, result["error"])

        return {
            "location": location,
            "topic": topic,
            "level": level,
            "sources": sources,
            "total_results": total_results,
            "has_errors": has_errors,
            "fetched_at": datetime.now(timezone.utc).isoformat(),
        }
    except Exception:
        logger.exception("Unexpected error during aggregate()")
        raise
