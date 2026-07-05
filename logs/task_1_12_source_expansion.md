---

# Task 1.12 — Source Expansion Research
## Carry-On Confidence — Phase 1 Findings

*Completed: 2026-07-06 by MODE: DEV (Claude)*
*Required reading before Phase 2 source decisions are made.*

---

## Summary

Three sources were assessed: DC Inside (디시인사이드), Daum/Kakao Search API, and a broader sweep for outbound travel data. One source is a strong Phase 2 addition (Kakao Search API). One is a no-go (DC Inside). KOSIS status confirmed from Phase 1.

---

## Source 1 — DC Inside (디시인사이드)

**Verdict: NO-GO**

```yaml
source_name: "dcinside"
url: "https://gall.dcinside.com"
data_type: "community / UGC"
access_type: "scraping only — no official API"
update_frequency: "real-time"
fetchable: false
fetch_method: "scraping — high complexity, high risk"
notes: >
  No official API exists. DC Inside has a mobile API endpoint (api.dcinside.com)
  used by their own app, but it is undocumented, unofficial, and subject to
  IP blocks and anti-bot enforcement. Third-party scraping tools exist
  (e.g. HashScraper, various GitHub scripts) but all require IP rotation,
  browser emulation, or paid services to avoid blocks. Content quality is
  also a concern — DC Inside is a loosely moderated anonymous forum; travel
  content is mixed with off-topic, low-quality, and potentially inappropriate
  posts. Filtering signal from noise would require significant post-processing.
  ToS prohibits unauthorized scraping.
recommended: false
priority: "not recommended — do not integrate"
```

**Reason to pass:** No official API, active anti-scraping enforcement, low content signal-to-noise ratio for worksheet use. Naver Blog and Cafe already cover the Korean UGC travel content use case through a clean, official API.

---

## Source 2 — Daum / Kakao Search API

**Verdict: STRONG YES — Phase 2 priority addition**

```yaml
source_name: "kakao_search"
url: "https://dapi.kakao.com/v2/search/"
data_type: "blog + cafe search / UGC"
access_type: "api_key_required — free, instant approval via Kakao Developers"
update_frequency: "real-time (searches are live)"
fetchable: true
fetch_method: "REST API — simple GET requests with Authorization header"
notes: >
  Daum was acquired by Kakao in 2014 and is now fully under the Kakao
  Developers platform (developers.kakao.com). The Kakao Search API provides
  official search access to Daum Blog, Daum Cafe, web documents, news, books,
  and images. Authentication is via a REST API key (KakaoAK header) — no OAuth
  required for search. Registration is instant via Kakao Developers.

  Endpoints relevant to Carry-On Confidence:
  - GET https://dapi.kakao.com/v2/search/blog — Daum Blog search
  - GET https://dapi.kakao.com/v2/search/cafe — Daum Cafe search
  - GET https://dapi.kakao.com/v2/search/web — general web search

  Response fields include: title, contents (snippet), url, datetime, cafename
  (for cafe results). Clean JSON, no HTML tags in content fields (unlike Naver).
  Quota: monthly and daily limits apply — exact figures require checking the
  Kakao Developers console at registration time.

  This is a direct complement to the Naver Search API: same content types
  (blog + cafe), different platform, different user base. Daum Cafe has
  significant travel communities (여행 카테고리) that do not overlap with
  Naver Cafe. Adding Kakao Search meaningfully expands source diversity
  without adding architectural complexity — it fits the existing
  BaseFetcher pattern cleanly.
recommended: true
priority: "Phase 2 — first priority addition after KOSIS resolution"
env_var_needed: "KAKAO_REST_API_KEY"
registration_url: "https://developers.kakao.com"
```

**Integration estimate:** Low effort. Follows the same pattern as NaverFetcher. New class KakaoFetcher(BaseFetcher), two endpoint calls (blog + cafe), same return shape. Credential acquisition is instant.

---

## Source 3 — KOSIS Status Confirmation

**Verdict: DEFERRED — table codes still needed**

Status unchanged from Phase 1. Correct table confirmed as:
- `orgId: 314` (한국관광통계 — Korea Tourism Statistics)
- `tblId: DT_SEX_DEP_DSTN_AGG_MONTH` (내국인출국 성별/행선지별, monthly)

Valid `itmId` and `objL1` codes must be obtained manually via the kosis.kr browser UI — the stat table pages are JS-rendered and codes are not accessible via HTTP requests. Once codes are confirmed, `kosis_fetcher.py` is already implemented and requires only config updates to `sources.yaml`.

**Action for Phase 2:** Before Phase 2 begins, manually browse `kosis.kr`, find the table `DT_SEX_DEP_DSTN_AGG_MONTH` under 한국관광통계 (orgId 314), and note the valid item codes and classification codes from the dropdown/table UI. Update `sources.yaml` accordingly and re-run the KOSIS fetcher live test.

---

## Source 4 — Broader Sweep Findings

No additional sources identified as Phase 2 priorities beyond Kakao Search. Sources assessed and ruled out:

- **Hana Tour / Mode Tour annual reports** — PDF format only, no API, manual download. Useful for 6-month review context but not live-fetchable. Not integrated.
- **TripAdvisor Korean reviews** — no official API for review data. Web scraping is ToS-prohibited. Pass.
- **Reddit r/koreatravel** — English-language only, small community, low Korean traveler voice. Not useful for the target use case.
- **UNWTO / IATA data** — aggregate global statistics, annual cadence, PDF or manual download. Not live-fetchable. Note for 6-month review use only.

---

## Recommendations for Phase 2

| Priority | Action | Effort |
|---|---|---|
| 1 | Add Kakao Search API (blog + cafe) as 4th fetcher | Low — 1-2 hours |
| 2 | Resolve KOSIS table codes via manual browser lookup | Low — 30 min manual task |
| 3 | Improve Naver/Kakao query construction for non-Korean location slugs | Medium — Phase 2 prompt tuning |

---

*End of task_1_12_source_expansion.md*
