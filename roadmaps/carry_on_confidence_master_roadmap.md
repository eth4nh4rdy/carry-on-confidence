carry_on_confidence_master_roadmap.md
Carry-On Confidence — Travel English Worksheet Generator
Primo English · Primo Curriculum Manager
Slogan: Fake It Till You Make the Flight
Version: 0.1 — Approved foundation. Modify only when build direction changes.
Created: 2026-06-16 by MODE: MANAGER

What This Is
Carry-On Confidence is a scenario-driven, destination-aware ESL worksheet generator for Korean travelers at all levels. It fetches live Korean travel data on each run, constructs a realistic travel scenario based on the selected topic and destination, and generates an 8-page classroom worksheet in DOCX format. Each worksheet is fresh. The scenario framework — topics and locations — is reviewed and updated every 6 months to stay aligned with current Korean travel trends.
This is the first program in the Primo English travel English product ladder. It targets nervous beginners through advanced learners preparing for real-world travel situations overseas — tourists, first-time business travelers, spouses of executives, and anyone who needs enough English to keep moving.
The ladder:

✈️ Carry-On Confidence — "Fake It Till You Make the Flight"
↓ Level Up ↓
🕹️ Corporate Survival Simulator — "The Airport Was Just the Tutorial"


Tone & Identity

Friendly, funny, encouraging, slightly chaotic
"We're all winging it."
Duolingo meets travel disaster stories
Exercises and scenarios lean into the chaos — things go wrong, people panic, students laugh and learn
Never dry. Never textbook. Always human.


Repository

Repo name: TBD — operator to name and initialize
Local path: C:/users/smeefer/primo_english/[repo-name]/
Platform: Windows 11, Python 3.10+, Miniconda
Git initialized before any code is written — no exceptions
Branch strategy: main (stable) + feature branches per phase
This is a standalone repo — not a fork of any existing Primo program


Page Structure
PageContent1Program header · Name/Date · 3 small talk questions related to the scenario and destination23 keywords — word, POS, EN def, KO def, 3 synonyms, My sentence blank33 keywords — same format43 keywords — same format5Role Play situation card 1 — open scenario using keywords, performed with partner or teacher6Role Play situation card 2 — second open scenario, different situation, same keyword set7Exercises — 3–4 tone-matched exercises from the Carry-On Confidence exercise bank8Homework — writing or speaking production task
Answer key generated as a separate DOCX file. Never included on the student worksheet.

Keyword Block Format (Pages 2–4)
One block per keyword, 3 blocks per page, 9 keywords total per worksheet:
**[word] ([part of speech])**
**English:** [one clear sentence definition]
**Korean:** [한국어로 한 문장]
**Synonyms:** [synonym1] · [synonym2] · [synonym3]
**My sentence:** __________________________

______________________________________________________________________________________________
Keywords are selected to be practically useful in the scenario context. Selection criteria:

Directly useful in the travel scenario being practiced
Likely to be unfamiliar to Korean ESL students at the target level
Real-world travel vocabulary — functional, not academic
Level-appropriate — grounded by the Primo Scale 1–10


Role Play Pages (Pages 5–6)
Each Role Play page contains one open situation card. The student performs the scenario with a partner or the teacher. Both cards draw on the 9 keywords introduced in pages 2–4.
Card format:
🎭 SITUATION: [scenario title]

📍 Location: [e.g. Immigration desk at JFK Airport]
👤 You are: [e.g. a Korean traveler arriving for the first time]
👥 Your partner is: [e.g. an immigration officer]

The situation:
[2–4 sentence description of the scenario — what has happened, what needs to happen]

Your goal:
[What the student needs to accomplish in this role play]

Try to use these words:
[keyword1] · [keyword2] · [keyword3]
Card 1 and Card 2 share the same destination and topic but place the student in a different moment — different location, different stakes, different partner role.

Exercise Bank — Carry-On Confidence Types
A dedicated carry_on_exercise_bank.yaml is built in Phase 3. All exercise types are tone-matched to the program — immersive, survival-focused, slightly chaotic. Standard ESL exercise formats are not used.
Exercise type examples (to be fully defined in Phase 3):

What Do You Say When...? — survival response prompts
Panic or Polish — two responses to a situation; identify which is appropriate and why
Lost in Translation — a culturally awkward or incorrect phrase; fix it
Fill the Silence — a conversation stalls; what do you say next?
Survival Dialogue Completion — partial travel dialogue; complete the missing lines
Cultural Misunderstanding Fix-It — identify what went wrong and rewrite

The LLM generates actual exercise content per run based on the scenario, destination, and keywords. The YAML bank defines type, instructions, difficulty range, and format spec only — no static content.

Config Files
FilePurposeReview Cadencetopics.yamlFixed travel scenario categories — expandableEvery 6 monthslocations.yamlPre-defined destination list — top Korean traveler destinationsEvery 6 monthslevels.yamlPrimo Scale 1–10 — reused from existing programsAs neededsources.yamlLLM provider config + travel data API configAs neededllm.yamlLLM provider, model, timeout, fallbackAs needed
Initial Topic Categories (to be expanded in Phase 0)
These are the confirmed scenario categories. Each maps to multiple specific worksheet topics.

Airport & Check-In
Immigration & Customs
Ground Transportation
Hotel Check-In & Issues
Restaurants & Ordering
Getting Lost & Asking Directions
Shopping & Bargaining
Emergency Situations
Medical & Pharmacy
Sightseeing & Tourist Situations
Phone Calls & Communication
Small Talk with Strangers
Public Transport
Money & Banking

Marketing module names (not used in config — for branding only):
Airport Panic · Restaurant Roulette · Taxi Talks · Please Speak Slowly · I Think I'm Lost · Small Talk with Strangers (Final Boss)
Initial Locations (to be populated in Phase 0 research)
Built from research into the top travel destinations for Korean travelers. Initial list to be defined in Phase 0. Locations are destination-aware — the scenario, cultural notes, and relevant vocabulary adjust per location.
Examples of likely inclusions: Japan, USA, France, Thailand, Australia, Vietnam, Spain, UK, Italy, Canada, UAE, Singapore, Philippines, Germany, New Zealand.

Data Source & Refresh Strategy
Live fetch on every worksheet generation. Korean travel data is fetched each time a worksheet is generated to ensure content stays fresh and relevant.
Data targets (to be confirmed in Phase 0 research):

Top Korean travel destinations — current rankings
Common traveler scenarios and pain points — what Korean tourists actually struggle with
Destination-specific cultural and practical context
Travel trend signals — what is growing, what is new

6-month framework review. Separately from the live fetch, topics.yaml and locations.yaml are manually reviewed and updated every 6 months. This is not automated — it is an operator research task. The review ensures the scenario pool and destination list reflect current Korean travel trends. A review reminder should be noted in the project log at each update.

Architecture
carry-on-confidence/
    ├── [cli_entry_point].py               # CLI entry point — operator to name
    ├── generator.py                       # LLM prompt — 8-page worksheet generation
    ├── formatter.py                       # DOCX renderer — 8-page structure
    ├── requirements.txt
    ├── .env                               # API keys — gitignored
    ├── .env.example                       # Key template — committed
    ├── .gitignore
    ├── README.md
    ├── config/
    │     ├── topics.yaml                  # Travel scenario categories
    │     ├── locations.yaml               # Destination list
    │     ├── levels.yaml                  # Primo Scale 1–10
    │     ├── sources.yaml                 # LLM + travel data API config
    │     └── llm.yaml                     # LLM provider config
    ├── fetchers/
    │     ├── __init__.py
    │     ├── base_fetcher.py              # Abstract base
    │     └── travel_fetcher.py           # Korean travel data fetch
    ├── exercises/
    │     └── carry_on_exercise_bank.yaml  # Carry-On Confidence exercise types
    └── output/
            └── .gitkeep

LLM Provider
OpenRouter only. No Anthropic API key. No other providers at launch. llm.yaml controls active provider — no code changes needed to rotate. Default model: configurable in llm.yaml.

CLI
bashpython [entry_point].py --level 6 --topic airport --location tokyo
python [entry_point].py --level 3 --topic restaurant --location paris
python [entry_point].py --level 8 --topic emergency --location new_york
--level accepts Primo Scale 1–10. --topic accepts slugs from topics.yaml. --location accepts slugs from locations.yaml. All three arguments required. Defaults TBD during Phase 5.

Syllabus Generator (Phase 6)
Following the Bleep Tests model. Takes a student profile and trip context, generates a class-by-class syllabus in DOCX, CSV, and JSON.
CLI:
bashpython syllabus_generator.py --student "Park Jisoo" --level 4 --destination tokyo --trip_type tourism --classes 8
Inputs:

Student name and level
Number of classes
Destination
Trip type (tourism, first business trip, accompanying family, etc.)
Weak areas (optional)
Trip date (optional — enables urgency sequencing)

Outputs: DOCX syllabus · CSV syllabus · JSON syllabus (input to worksheet generator)

Phase Overview
PhaseNameGoalStatus0Research & ScaffoldGitHub repo setup · identify live Korean travel data sources · populate initial topics.yaml and locations.yaml · establish 6-month review cadenceNot started1FetcherBuild travel_fetcher.py — live fetch of Korean travel data per worksheet generationNot started2GeneratorBuild generator.py — 8-page LLM prompt from topic + location + level + fetched dataNot started3Exercise BankBuild carry_on_exercise_bank.yaml — tone-matched survival exercise typesNot started4FormatterBuild formatter.py — 8-page python-docx renderer + separate answer keyNot started5CLI IntegrationWire all components into CLI entry point — end-to-end pipeline runNot started6Syllabus GeneratorBuild syllabus_generator.py — student profile + trip context → DOCX, CSV, JSON syllabusNot started7Testing & CommitFull self-test across multiple levels, topics, and locations · fix failures · git commit · project logNot started8Delivery (deferred)Telegram delivery via worksheet_willie.py — same pattern as AutonewsheetDeferred

Phase 0 — Research & Scaffold (detailed)
No pipeline code is written in this phase. Output is repo scaffold + research findings + populated config files.
Task 0.1 — GitHub Repo Setup

Operator creates new GitHub repo — name TBD
Clone to C:/users/smeefer/primo_english/[repo-name]/
Initialize project scaffold — directory structure, .gitignore, .env.example, requirements.txt stubs
Confirm clean initial commit on main

Task 0.2 — Korean Travel Data Source Research
Identify what Korean travel data is available and fetchable. Research targets:

Korean tourism statistics APIs or datasets — KNTO (Korea Tourism Organization), Visit Korea, Korean Air, travel booking platforms
Top Korean overseas travel destinations — current rankings with volume data
Common Korean traveler pain points and scenarios — what situations cause the most difficulty
English-language travel content relevant to Korean travelers — blogs, forums, travel advisories
Any freely available APIs or RSS feeds relevant to Korean travel trends

Deliverable: written summary of available sources, recommended fetcher architecture, and API keys required. Confirmed before any fetcher code is written.
Task 0.3 — Initial topics.yaml Population
Based on research findings and the confirmed scenario category list, populate topics.yaml with:

All confirmed scenario categories as top-level keys
Sub-topics under each category as individual worksheet topic slugs
Metadata per topic: difficulty range, category, short description
Minimum 30 topics at launch — expandable

Task 0.4 — Initial locations.yaml Population
Based on research into top Korean travel destinations:

Populate with confirmed top destinations
Each location entry includes: slug, display name, country, language notes, cultural context flag
Minimum 15 locations at launch — expandable

Task 0.5 — 6-Month Review Protocol
Document the review cadence in the project log. Next review date noted. Review checklist:

Are these still the top destinations for Korean travelers?
Are there new scenario types to add?
Are any topics or locations obsolete or low-priority?
What travel trends have emerged since the last review?

Task 0.6 — Initial Commit
git add .
git commit -m "chore: Phase 0 scaffold and research complete

Carry-On Confidence — Travel English Worksheet Generator
New standalone repo. No fork.

Completed:
- Project scaffold: directory structure, .gitignore, .env.example, requirements.txt stubs
- Phase 0 research: Korean travel data sources identified and documented
- config/topics.yaml: [N] topics across [N] scenario categories
- config/locations.yaml: [N] destinations populated
- config/levels.yaml: Primo Scale 1-10 (copied from existing programs)
- 6-month review protocol documented in project log

Next: Phase 1 — travel_fetcher.py"

Key Decisions
DecisionRationaleStandalone repo — not a forkDifferent content source and architecture from all existing programsLive fetch every generationContent stays fresh and destination-relevant; same model as Autonewsheet and 뇌썩유창반6-month framework reviewTravel trends shift but not daily; framework stays current without over-engineering2 Role Play pages instead of summaryFunctional fluency program — production and practice take priority over passive readingExercises reduced to 3–4Role play pages expand the worksheet; exercise count adjusted to maintain 8 pagesSmall talk questions on Page 1Matches the program identity — travel conversation starts with small talk, not warm-up drillsDestination-aware generationKorean travelers go to specific places; generic travel English is less useful than Paris-specific or Tokyo-specific Englishtopics.yaml + locations.yaml as configKeeps content framework maintainable, expandable, and separated from codeExercise bank separate phaseExercise design requires its own research and design pass — not an afterthoughtOpenRouter onlyOperational constraint — never use Anthropic API key in this pipelinePrimo Scale 1–10, all levelsAll Primo programs cover the full level rangeSyllabus generator in Phase 6Core worksheet pipeline must be stable before adding the syllabus layerTelegram delivery deferred to Phase 8Stability first — worksheet must be classroom-tested before delivery automation

Environment
OPENROUTER_API_KEY=your_openrouter_key_here
[TRAVEL_DATA_API_KEY]=to_be_determined_in_phase_0
Required keys to be confirmed after Phase 0 research identifies the data source.

Development Workflow (per phase)

Read this roadmap + most recent project log
Confirm phase steps — raise any blockers before starting
Generate implementation prompt for Claude Code or OpenClaw
Manual testing and verification
Git commit with detailed message
Update project log
Move to next phase


End of carry_on_confidence_master_roadmap.md
Version: 0.1 — 2026-06-16