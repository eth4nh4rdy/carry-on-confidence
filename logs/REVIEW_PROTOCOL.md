# Carry-On Confidence — 6-Month Review Protocol

## Purpose
This document defines the standing review procedure for maintaining config accuracy over time.
Config files are static by design — live content is fetched at runtime by travel_fetcher.py.
This review ensures the static foundation stays accurate as travel trends and destinations evolve.

## Review Cadence
Every 6 months. Triggered manually by the operator — no automated scheduling.

## Files to Review

### config/topics.yaml
- Are all 14 scenario categories still relevant to Korean travelers?
- Are any topics obsolete or underrepresented given current travel trends?
- Should new topics be added based on traveler feedback or worksheet usage patterns?
- Minimum 30 topics must be maintained at all times.

### config/locations.yaml
- Are the most popular current Korean travel destinations represented?
- Should new cities or locations be added based on rising travel volume?
- Has English reliability changed for any existing entry (e.g. a destination's tourism economy has grown or contracted)?
- Are regional_notes and worksheet_notes still accurate?
- INCLUSION RULE CHECK: Confirm no entries exist where the local language (not English) is the realistic traveler fallback. Japan and China remain excluded.

### config/levels.yaml
- No scheduled changes — shared across all Primo English programs.
- Only modify after cross-program review with the Primo Manager.

### config/sources.yaml
- Are all listed data sources still active and accessible?
- Have any APIs changed their quota, terms, or authentication method?
- Are there new sources that should be added? (See Task 1.0 — Source Expansion Research)

### config/llm.yaml
- Is the configured model still the best available option on OpenRouter?
- Have any model costs, context windows, or capabilities changed significantly?

## Review Process

1. Pull the latest version of the repo
2. Review each config file against the checklist above
3. Cross-reference config/locations.yaml against current Korean outbound travel rankings (KOSIS, Agoda, or similar)
4. Make updates directly to the relevant config file
5. Commit with the message format: `config: 6-month review [YYYY-MM]`
6. Update PROJECT_LOG.md with a brief summary of what changed and why

## Data Sources for Location Review
- KOSIS OpenAPI (kosis.kr) — official Korean outbound departure statistics
- Agoda annual Korean traveler ranking — published each December
- Naver Blog/travel community trends — can be queried via Naver Search API

## First Review Due
December 2026 (6 months from Phase 0 completion, June 2026)
