"""
YouTube Data API v3 fetcher for Carry-On Confidence.

Runs a single search.list call per fetch() to stay within quota (100 units/call,
10,000 units/day). Query is built in English with relevanceLanguage: "ko" to bias
results toward Korean-language content, since a Korean-language query would need
translation we can't reliably produce here.
"""

import os

from googleapiclient.discovery import build

from fetchers.base_fetcher import BaseFetcher


class YouTubeFetcher(BaseFetcher):

    def __init__(self):
        super().__init__("youtube")
        auth = self._get_config("auth")
        self.api_key = os.environ[auth["api_key_env"]]

    def fetch(self, location: str, topic: str, level: int) -> dict:
        location_display = location.replace("_", " ")
        topic_display = topic.replace("_", " ")
        query = f"{location_display} travel {topic_display}"

        defaults = self._get_config("defaults")

        youtube = build("youtube", "v3", developerKey=self.api_key)
        search_response = youtube.search().list(
            part="snippet",
            type=defaults["type"],
            maxResults=defaults["max_results"],
            relevanceLanguage=defaults["relevance_language"],
            q=query,
        ).execute()

        results = []
        for item in search_response.get("items", []):
            video_id = item.get("id", {}).get("videoId")
            if not video_id:
                continue
            snippet = item.get("snippet", {})
            results.append({
                "video_id": video_id,
                "title": snippet.get("title", ""),
                "description": snippet.get("description", "")[:300],
                "channel": snippet.get("channelTitle", ""),
                "published_at": snippet.get("publishedAt", ""),
                "url": f"https://www.youtube.com/watch?v={video_id}",
            })

        return {
            "source": self.source_name,
            "results": results,
        }
