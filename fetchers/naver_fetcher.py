"""
Naver Search API fetcher for Carry-On Confidence.

Queries both the blog and cafe endpoints using a Korean-language search query
built from the location and topic slugs. Results are merged into a single list
with a 'type' field ('blog' or 'cafe') distinguishing their origin.

Query construction is intentionally simple in Phase 1 — Phase 2 will refine
this once prompt development begins and real result quality can be evaluated.
"""

import os
import re

import requests

from fetchers.base_fetcher import BaseFetcher


def _strip_html(text: str) -> str:
    """Remove HTML tags (primarily Naver's <b>/<b> match highlighting)."""
    return re.sub(r"<[^>]+>", "", text)


class NaverFetcher(BaseFetcher):

    def __init__(self):
        super().__init__("naver")
        auth = self._get_config("auth")
        self.headers = {
            "X-Naver-Client-Id": os.environ[auth["client_id_env"]],
            "X-Naver-Client-Secret": os.environ[auth["client_secret_env"]],
        }

    def fetch(self, location: str, topic: str, level: int) -> dict:
        location_display = location.replace("_", " ")
        topic_display = topic.replace("_", " ")
        query = f"{location_display} 여행 {topic_display}"

        defaults = self._get_config("defaults")
        endpoints = self._get_config("endpoints")
        base_url = self._get_config("base_url")

        params = {
            "query": query,
            "display": defaults["display"],
            "sort": defaults["sort"],
        }

        results = []
        for endpoint_type, endpoint_path in endpoints.items():
            url = base_url + endpoint_path
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            for item in data.get("items", []):
                date = item.get("bloggingdate") or item.get("postdate") or ""
                results.append({
                    "type": endpoint_type,
                    "title": _strip_html(item.get("title", "")),
                    "link": item.get("link", ""),
                    "description": _strip_html(item.get("description", "")),
                    "date": date,
                })

        return {
            "source": self.source_name,
            "results": results,
        }
