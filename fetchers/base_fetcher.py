"""
Abstract base class for all Carry-On Confidence data fetchers.

Subclasses implement fetch() for a specific source (Naver, YouTube, KOSIS, etc.).
The orchestrator always calls _safe_fetch() rather than fetch() directly —
_safe_fetch() wraps fetch() in a try/except and guarantees the standard return
shape even when the underlying API call fails.

Standard return shape:
    {
        "source":  str,   # source name, e.g. "naver"
        "results": list,  # source-specific result dicts; empty on error
        "error":   None | str  # None on success, exception message on failure
    }
"""

from abc import ABC, abstractmethod
from pathlib import Path

import yaml
from dotenv import load_dotenv


class BaseFetcher(ABC):

    def __init__(self, source_name: str):
        load_dotenv()
        self.source_name = source_name

        sources_path = Path(__file__).parent.parent / "config" / "sources.yaml"
        with open(sources_path, encoding="utf-8") as f:
            self.sources_config = yaml.safe_load(f)

    @abstractmethod
    def fetch(self, location: str, topic: str, level: int) -> dict:
        """
        Perform the actual API call and return the standard result shape.
        Must be implemented by every subclass.
        """

    def _safe_fetch(self, location: str, topic: str, level: int) -> dict:
        """Call fetch() and catch any exception, always returning the standard shape."""
        try:
            result = self.fetch(location, topic, level)
            result["error"] = None
            return result
        except Exception as exc:
            return {
                "source": self.source_name,
                "results": [],
                "error": str(exc),
            }

    def _get_config(self, key: str):
        """Return self.sources_config[source_name][key] with a clear error on miss."""
        source_block = self.sources_config.get(self.source_name)
        if source_block is None:
            raise KeyError(
                f"No config block found for source '{self.source_name}' in sources.yaml"
            )
        if key not in source_block:
            raise KeyError(
                f"Key '{key}' not found in sources.yaml under '{self.source_name}'"
            )
        return source_block[key]
