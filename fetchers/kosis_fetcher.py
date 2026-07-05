"""
KOSIS OpenAPI fetcher for Carry-On Confidence.

Retrieves Korean outbound departure statistics (내국인 출국자 수) as national
aggregate context — location and topic are accepted for interface parity with
other fetchers but are not used as filter parameters, since KOSIS does not
break this table down by destination.

NOTE: orgId and tblId below come from sources.yaml and are a starting
reference only (see config/sources.yaml target_stat.note). The KOSIS table
structure changes over time — these must be verified against the live KOSIS
OpenAPI (stat search) before relying on this fetcher's output. itmId "T10"
for 출국자수 is likewise unverified and should be confirmed the same way.
"""

import os
from datetime import datetime, timedelta

import requests

from fetchers.base_fetcher import BaseFetcher


class KosisFetcher(BaseFetcher):

    def __init__(self):
        super().__init__("kosis")
        auth = self._get_config("auth")
        self.api_key = os.environ[auth["api_key_env"]]
        self.base_url = self._get_config("base_url")
        target_stat = self._get_config("target_stat")
        self.org_id = target_stat["org_id"]
        self.table_id = target_stat["table_id"]

    def fetch(self, location: str, topic: str, level: int) -> dict:
        defaults = self._get_config("defaults")

        today = datetime.now()
        twelve_months_ago = today - timedelta(days=365)
        start_prd_de = twelve_months_ago.strftime("%Y%m")
        end_prd_de = today.strftime("%Y%m")

        params = {
            "method": "getList",
            "apiKey": self.api_key,
            "itmId": "T10",
            "objL1": "ALL",
            "objL2": "ALL",
            "format": defaults["format"],
            "jsonVD": "Y",
            "prdSe": "M",
            "startPrdDe": start_prd_de,
            "endPrdDe": end_prd_de,
            "orgId": self.org_id,
            "tblId": self.table_id,
        }

        response = requests.get(self.base_url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        results = []
        if isinstance(data, list):
            for item in data:
                raw_value = item.get("DT")
                try:
                    value = int(raw_value)
                except (TypeError, ValueError):
                    value = raw_value

                results.append({
                    "period": item.get("PRD_DE", ""),
                    "value": value,
                    "item_name": item.get("ITM_NM", ""),
                    "unit": item.get("UNIT_NM", ""),
                })

        return {
            "source": self.source_name,
            "results": results,
        }
