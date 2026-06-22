# Carry-On Confidence — Phase 0 Project Log (Interim)
**Last updated:** 2026-06-21
**Status:** Phase 0 in progress — Tasks 0.1 and 0.2 complete, 0.3 next

---

## Completed

### Task 0.1 — Repo scaffold ✅
- Repo: `carry-on-confidence` (private, github.com/eth4nh4rdy)
- Entry point: `generate.py`
- Full directory structure created: `config/`, `fetchers/`, `exercises/`, `output/`
- `.gitignore` correctly configured: `.env` ignored, `output/*` ignored but `output/.gitkeep` tracked
- **Known platform note:** scaffold was first built on operator's CachyOS laptop, then rebuilt manually on operator's Windows PC due to a git auth/credential issue on CachyOS (git identity was never configured there). PC build verified identical via the same three-check verification process. PC version is committed and pushed to `main`. CachyOS local copy still exists uncommitted — not a current risk, but if the operator returns to the CachyOS machine, do NOT push from there without first pulling latest from `main` to avoid divergent history.
- Task 0.6 (final Phase 0 commit) is intentionally deferred until 0.3–0.5 are complete.

### Task 0.2 — Korean travel data source research ✅ (initial pass — see "Reopened" below)
Full findings doc: `task_0_2_findings.md` (delivered to operator, also belongs in repo as `/docs/task_0_2_findings.md` or similar — not yet copied into repo, follow up in Task 0.6 prep).

**Verified, confirmed usable sources:**
- **Naver Search API (official)** — covers blog + cafe search natively. Free, `openapi.naver.com`, requires `NAVER_CLIENT_ID`/`NAVER_CLIENT_SECRET`. No scraping needed.
- **YouTube Data API v3** — confirmed current (post Dec 2025) quota: 10,000 units/day, `search.list` = 100 units/call (100 searches/day max), `videos.list` = 1 unit/call. Must design fetcher to search sparingly and cache video IDs.
- **KOSIS OpenAPI** — free, auto-approved key, structured JSON, Python wrapper (`PublicDataReader`) already exists. Good for macro outbound-travel statistics only — not scenario/narrative content.
- **Hermes Agent + SearXNG** — confirmed real, actively maintained, OpenRouter-compatible, self-hosted SearXNG is free/unlimited. Logged as a Phase 1+ enhancement, not a Phase 0/1 dependency.

**Corrected/rejected:**
- **KNTO TourAPI 4.0** — confirmed this is *inbound/domestic* Korean tourism data (attractions, lodging, festivals within Korea), not outbound travel data. Does not fit Carry-On Confidence's use case. Removed from active source list. Replacement needed — see Task 1.0 below.

**Architectural takeaway:** `fetchers/travel_fetcher.py` must be a multi-source fetcher with pluggable sub-fetchers (Naver, YouTube, KOSIS), not a single monolithic client — each source has different auth, quota, and response shape. `config/sources.yaml` should reflect this when populated in Phase 1.

---

## Reopened — Task 0.2 is not fully closed

Operator feedback after initial research pass (2026-06-21):

1. **Fetch cadence — CONFIRMED DECISION:** Manual trigger only, no cron. YouTube and Naver are fetched **on every worksheet generation run** (i.e., every time `generate.py` is invoked), not on a separate scheduled refresh. This keeps material fresh per-worksheet without adding scheduling infrastructure. ⚠️ This corrects an earlier (incorrect) framing in conversation that suggested a weekly/bi-weekly cron-style refresh — that approach was rejected by the operator as unnecessary complexity. Phase 1 fetcher design should treat each fetch as happening synchronously as part of the `generate.py` run, with reasonable per-run quota usage (YouTube's 100 searches/day ceiling should be more than sufficient for a per-run fetch model, but worth confirming actual call volume per worksheet generation during Phase 1 implementation).
2. **KNTO TourAPI replacement** — still unresolved. Need an outbound-travel-specific alternative.
3. **New source candidates to research:** DC Inside (디시인사이드), Daum, and a broader sweep for additional Korean sources. Note: DC Inside has no official API and would require scraping a loosely-moderated forum structure — feasibility and risk need verification before any commitment, not assumed.

### New tracked task: Task 1.0 — Source Expansion Research
**Status:** Deferred — scheduled for after Phase 0 completes, before or alongside early Phase 1 work.
**Scope:**
- Find a viable outbound-travel-data replacement for KNTO TourAPI
- Verify feasibility (API availability, ToS risk, scraping complexity) of DC Inside as a source
- Verify feasibility of Daum (Cafe, Blog, or other surfaces) as a source
- Broader sweep for additional Korean-language travel data sources not yet considered
- Decision on whether Hermes Agent + SearXNG should be pulled forward into this research phase or remain a later enhancement

This task does not block Phase 0 completion. `topics.yaml` and `locations.yaml` (Tasks 0.3/0.4) do not depend on which additional sources get added later.

---

## Pending

- Task 0.3 — `topics.yaml` population (min 30 topics, 14 scenario categories) — next
- Task 0.4 — `locations.yaml` population (min 15 destinations)
- Task 0.5 — 6-month review protocol documentation
- Task 0.6 — Final Phase 0 commit + close-out log
- Task 1.0 — Source expansion research (see above)

## Operator action items (outside Claude Code's scope)
- Request free Naver Search API credentials (`NAVER_CLIENT_ID`/`NAVER_CLIENT_SECRET`) — manual approval, may take time
- Request free YouTube Data API v3 key via Google Cloud Console — instant
- Recommend doing both in parallel with Tasks 0.3/0.4
