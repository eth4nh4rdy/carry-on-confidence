# Task 0.2 — Korean Travel Data Source Research
## Carry-On Confidence — Findings (Verified via live web search, June 2026)

Researched and verified by MODE: DEV before handoff to implementation. All sources below were confirmed live — none are assumed from training data.

---

## SOURCE CATEGORY 1 — Government / Statistical (structured, low-risk)

### ✅ KOSIS (국가통계포털) — Outbound travel statistics
- **What it is:** Korea's national statistics portal aggregating data from all government stat-producing agencies, including outbound departure counts by destination.
- **Access:** Free OpenAPI via the KOSIS 공유서비스 portal (kosis.kr/openapi). Registration + API key request is typically auto-approved.
- **Format:** JSON or XML, structured.
- **Tooling:** A working Python wrapper already exists — PublicDataReader (pip-installable) — plus an independent R package (kosis). Both are actively maintained open-source.
- **Verdict:** Strong, low-risk source for macro trend data (e.g. "departures to Japan up X% this quarter"). Not useful for scenario/situational content — this is aggregate statistics, not narrative or experiential data.
- **Phase 1 fit:** Good as a periodic (not per-run) trend-confirmation source.

### ⚠️ KNTO TourAPI 4.0 — Correction to roadmap assumption
- **What it is:** Korea Tourism Organization's official OpenAPI, free via data.go.kr.
- **Important correction:** This is inbound/domestic Korean tourism data — attractions, lodging, restaurants, festivals within Korea. It is NOT an outbound travel data source.
- **Verdict:** Not usable for Carry-On Confidence's core purpose. Removed from active source list.

---

## SOURCE CATEGORY 2 — Social / UGC (Naver Blog, Naver Cafe)

### ✅ Naver Search API (official) — covers blog + cafe
- **What it is:** Naver's own developer API (openapi.naver.com), not a scraper. Officially supports search across blog, cafe, news, and more.
- **Access:** Free, requires NAVER_CLIENT_ID + NAVER_CLIENT_SECRET from the Naver Developers portal.
- **Quota:** ~25,000 calls/day per category (confirm current figure on the developer console at setup time).
- **Verdict:** Correct tool for Naver Blog + Naver Cafe sourcing. No scraping needed, no ToS risk, real structured JSON responses.
- **Phase 1 fit:** High priority.

---

## SOURCE CATEGORY 3 — YouTube

### ✅ YouTube Data API v3 — confirmed current quota math (post Dec 2025 update)
- **Default quota:** 10,000 units/day.
- **search.list cost:** 100 units/call = 100 searches/day max on free tier.
- **videos.list cost:** 1 unit/call — use this for follow-up detail pulls.
- **Fetch cadence — CONFIRMED DECISION:** Fetched on every worksheet generation run (synchronously as part of generate.py). No cron, no scheduled refresh. Manual trigger only.
- **Phase 1 design note:** Each generate.py run should use a small, targeted search query set. 100 searches/day ceiling is more than sufficient for per-run fetch model.

---

## SOURCE CATEGORY 4 — Future Research Agent

### ✅ Hermes Agent + SearXNG — confirmed compatible with OpenRouter-only constraint
- Hermes Agent (Nous Research): open-source, actively developed, native SearXNG integration.
- SearXNG: free, self-hosted, no API key, no rate limits, aggregates 70+ search engines.
- OpenRouter support: confirmed, switchable with no code changes.
- One-click Railway deploy template available bundling both services.
- **Verdict:** Legitimate future enhancement. Treat as Phase 1+ upgrade, not a Phase 0/1 dependency.

---

## SUMMARY — Recommended Phase 1 Source Stack

| Source | Use Case | Access Cost | Priority |
|---|---|---|---|
| Naver Search API (official) | Blog + Cafe trend/experience content | Free, ~25k calls/day | High |
| YouTube Data API v3 | International traveler video trends | Free, 10k units/day | High |
| KOSIS OpenAPI | Macro outbound travel statistics | Free, auto-approved | Medium (periodic only) |
| Hermes Agent + SearXNG | Deep/autonomous trend research | Free (self-hosted) | Future enhancement |
| ~~KNTO TourAPI~~ | ~~N/A~~ | ~~N/A~~ | **Remove — wrong data domain** |

**Architectural takeaway for Phase 1:** fetchers/travel_fetcher.py must be a multi-source fetcher with pluggable sub-fetchers (Naver, YouTube, KOSIS). config/sources.yaml should reflect this multi-source structure when populated in Phase 1.

**Open items logged as Task 1.0 (Source Expansion Research):**
- Find outbound-travel replacement for KNTO TourAPI
- Verify DC Inside (디시인사이드) feasibility as a source
- Verify Daum feasibility as a source
- Broader sweep for additional Korean-language travel sources

**Operator action items before Phase 1:**
- Request Naver Search API credentials (NAVER_CLIENT_ID / NAVER_CLIENT_SECRET) — manual approval, may take time
- Request YouTube Data API v3 key via Google Cloud Console — instant
---

STEP 2 — Create docs/PHASE0_PROJECT_LOG.md with the following content:

---
# Carry-On Confidence — Phase 0 Project Log
**Completed:** June 2026
**Status:** Phase 0 complete — all tasks 0.1 through 0.6 done

---

## Completed Tasks

### Task 0.1 — Repo scaffold ✅
- Repo: carry-on-confidence (private, github.com/eth4nh4rdy)
- Entry point: generate.py
- Full directory structure created: config/, fetchers/, exercises/, output/
- .gitignore correctly configured: .env ignored, output/* ignored, output/.gitkeep tracked
- Platform note: scaffold was first built on operator's CachyOS laptop, then rebuilt on Windows PC due to git auth issue on CachyOS. PC version is the canonical version committed to main.
- Task 0.6 final commit closes Phase 0.

### Task 0.2 — Korean travel data source research ✅ (initial pass)
- Full findings: docs/task_0_2_findings.md
- Confirmed sources: Naver Search API, YouTube Data API v3, KOSIS OpenAPI, Hermes Agent + SearXNG (future)
- Corrected: KNTO TourAPI is inbound/domestic data — removed from active source list
- Fetch cadence decision: manual trigger per generate.py run, no cron
- Task 1.0 (Source Expansion Research) logged for after Phase 0 — see below

### Task 0.3 — topics.yaml population ✅
- 42 topics across 14 fixed scenario categories (minimum was 30)
- All slugs unique, all categories populated
- Tone reviewed and approved: scenario-specific, survival-focused, matches brand voice

### Task 0.4 — locations.yaml population ✅
- 25 location entries: cities, country-level, and city-state entries
- Flat registry — all entries are independently valid --location argument values
- Inclusion rule enforced and written into file header: English must be realistic tourist fallback
- Japan and China explicitly excluded
- Fields on every entry: slug, display_name, scope, parent, english_reliability, local_languages, regional_notes, worksheet_note
- One fix applied post-generation: barcelona english_reliability corrected from medium-high to high

### Task 0.5 — 6-month review protocol ✅
- Written to docs/REVIEW_PROTOCOL.md
- First review due: December 2026
- Covers: topics.yaml, locations.yaml, levels.yaml, sources.yaml, llm.yaml

### Task 0.6 — Final Phase 0 commit ✅
- See git log for commit hash and message

---

## Pending / Carry-Forward

### Task 1.0 — Source Expansion Research (Phase 1 pre-task)
**Status:** Not started — scheduled before or alongside early Phase 1 work
**Scope:**
- Find viable outbound-travel replacement for KNTO TourAPI
- Verify DC Inside (디시인사이드) feasibility as a source (no official API — scraping risk assessment needed)
- Verify Daum feasibility as a source
- Broader sweep for additional Korean-language travel sources
- Decide whether Hermes Agent + SearXNG should be pulled forward into Phase 1

### Operator Action Items Before Phase 1
- Request Naver Search API credentials (NAVER_CLIENT_ID / NAVER_CLIENT_SECRET) — manual approval
- Request YouTube Data API v3 key via Google Cloud Console — instant

---

## Key Decisions Made in Phase 0

| Decision | Outcome |
|---|---|
| Repo name | carry-on-confidence |
| CLI entry point | generate.py |
| Fetch cadence | Per generate.py run — no cron, manual trigger only |
| Location registry structure | Flat list — all scopes (city/country/city_state) coexist as peers |
| Japan/China inclusion | Excluded — Korean travelers use local language, not English |
| English-viability test | "Will the traveler realistically use English?" not "Is this an English-speaking country?" |
| KNTO TourAPI | Removed — inbound/domestic data, wrong domain for this product |
| locations.yaml english_reliability scale | high / medium / low (three values only — medium-high is invalid) |
| Phase 0 minimum locations | 25 entries (original spec said "minimum 15" at country level — superseded by city-level flat registry design) |
| topics.yaml minimum | 42 topics across 14 categories (minimum was 30) |