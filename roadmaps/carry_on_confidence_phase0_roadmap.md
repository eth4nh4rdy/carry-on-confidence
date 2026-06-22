carry_on_confidence_phase0_roadmap.md
Carry-On Confidence — Phase 0: Research & Scaffold
Primo English · Primo Curriculum Manager
Version: 0.1
Created: 2026-06-16 by MODE: MANAGER

Phase Goal
Set up the GitHub repository, identify and document live Korean travel data sources, populate the initial topics.yaml and locations.yaml config files, and establish the 6-month review protocol. No pipeline code is written in this phase.
Phase 0 is complete when:

GitHub repo exists and is cloned locally
Project scaffold is in place — directory structure, .gitignore, .env.example, requirements.txt stubs
Korean travel data sources are identified, evaluated, and documented
topics.yaml is populated with a minimum of 30 travel scenario topics across all confirmed categories
locations.yaml is populated with a minimum of 15 destinations with relevant metadata
levels.yaml is copied from an existing Primo program
6-month review protocol is documented in the Phase 0 project log
Clean initial commit on main with no untracked debris


Prerequisites

GitHub account eth4nh4rdy accessible
Git configured locally
Miniconda / Python 3.10+ available
carry_on_confidence_master_roadmap.md read and understood before starting


Steps

Task 0.1 — GitHub Repo Setup
Goal: Create the repo, clone it locally, and initialize the project scaffold.
Steps:

Operator creates new GitHub repo under eth4nh4rdy — name TBD by operator
Clone to local path:

bashgit clone https://github.com/eth4nh4rdy/[repo-name].git C:/users/smeefer/primo_english/[repo-name]
cd C:/users/smeefer/primo_english/[repo-name]

Create the following directory structure manually or via scaffold script:

[repo-name]/
    ├── [cli_entry_point].py               # Placeholder — name TBD by operator
    ├── generator.py                       # Placeholder
    ├── formatter.py                       # Placeholder
    ├── requirements.txt                   # Stub — populate in later phases
    ├── .env                               # Gitignored — do not commit
    ├── .env.example                       # Template — commit this
    ├── .gitignore
    ├── README.md                          # Basic project description
    ├── config/
    │     ├── topics.yaml                  # Populated in Task 0.3
    │     ├── locations.yaml               # Populated in Task 0.4
    │     ├── levels.yaml                  # Copied from existing Primo program
    │     ├── sources.yaml                 # Stub — populate in Phase 1
    │     └── llm.yaml                     # Stub — populate in Phase 1
    ├── fetchers/
    │     ├── __init__.py
    │     ├── base_fetcher.py              # Stub — populate in Phase 1
    │     └── travel_fetcher.py            # Stub — populate in Phase 1
    ├── exercises/
    │     └── carry_on_exercise_bank.yaml  # Stub — populate in Phase 3
    └── output/
            └── .gitkeep

Create .gitignore — minimum contents:

.env
__pycache__/
*.pyc
output/
*.docx

Create .env.example:

OPENROUTER_API_KEY=your_openrouter_key_here
TRAVEL_DATA_API_KEY=to_be_determined_in_phase_0

Copy levels.yaml from an existing Primo program repo (Autonewsheet or fluency-in-brainrot). No modifications needed — Primo Scale 1–10 is shared across all programs.
Write a basic README.md:

# Carry-On Confidence
## Travel English Worksheet Generator
### Primo English

Slogan: Fake It Till You Make the Flight

Scenario-driven, destination-aware ESL worksheet generator for Korean travelers at all levels.
Generates 8-page DOCX worksheets from live Korean travel data.

See carry_on_confidence_master_roadmap.md for full architecture and phase plan.
Verification:

Run git status — should show only untracked files, no errors
Run ls config/ — should show all 5 config file stubs
Confirm .env is gitignored: git check-ignore -v .env should return a match

No commit yet — commit happens in Task 0.6 after all Phase 0 tasks are complete.

Task 0.2 — Korean Travel Data Source Research
Goal: Identify, evaluate, and document live Korean travel data sources. Confirm what is fetchable, what is free, and what requires an API key. Recommend the fetcher architecture for Phase 1.
This is a research task. The sources listed below are starting points only. The developer must investigate beyond this list and document all findings. Additional sources will be needed before the fetcher architecture can be confirmed.

Starting Point Sources
Official Korean Tourism & Government Data

KNTO — Korea Tourism Organization (kto.visitkorea.or.kr) — Korean outbound tourism statistics, top destinations by year, traveler volume data. Check for open data portal or API access.
Korea Tourism Data Lab (datalab.visitkorea.or.kr) — detailed outbound travel statistics. May require registration.
Korean Statistical Information Service — KOSIS (kosis.kr) — Korean government statistics including overseas travel data. English interface available. Free.
Ministry of Culture, Sports and Tourism (mcst.go.kr) — annual tourism reports, outbound travel summaries.

Travel Booking & Trend Platforms

Naver Travel (travel.naver.com) — Korean traveler search trends, popular destinations. Check for public trend data or API.
Kakao Map / Kakao Travel — Korean traveler destination data. Check for developer API access.
Interpark Tours (tour.interpark.com) — major Korean travel booking platform. Check for public data or press releases on popular destinations.
Hana Tour (hanatour.com) — largest Korean travel agency. Publishes annual travel trend reports.
Mode Tour (modetour.com) — second largest Korean travel agency. Similar reports.

International Sources with Korean Traveler Data

UNWTO — UN World Tourism Organization (unwto.org) — international tourism statistics including Korean outbound data.
IATA Travel Centre — airline and airport data relevant to Korean departure volumes.
Skyscanner / Kayak trend APIs — if available, useful for real-time Korean destination popularity signals.

Travel Content & Community (for pain point research)

Naver Cafe — 여행 (cafe.naver.com) — Korean travel communities. Useful for understanding common traveler situations and difficulties.
TripAdvisor Korean reviews — Korean traveler reviews reveal common scenarios and language struggles.
Reddit r/koreatravel — English-language community with Korean traveler perspectives.


Research Deliverables
For each source investigated, document:
yamlsource_name: ""
url: ""
data_type: ""           # statistics / trends / live / reports / community
access_type: ""         # free / api_key_required / registration / paid
update_frequency: ""    # daily / monthly / annual / on-demand
fetchable: true/false
fetch_method: ""        # REST API / RSS / scrape / manual download
notes: ""
recommended: true/false
Final deliverable: Written summary covering:

Recommended primary data source for live fetch — confirmed fetchable, free or low cost
Recommended secondary sources for supplementary context
API keys required and how to obtain them
Recommended fetcher architecture for Phase 1
Any sources that require manual periodic download rather than live fetch — note these separately

This summary becomes part of the Phase 0 project log and is required reading before Phase 1 begins.

Task 0.3 — Initial topics.yaml Population
Goal: Populate topics.yaml with the full initial set of travel scenario topics. Minimum 30 topics at launch. The starting point list below must be expanded during this task based on research findings from Task 0.2 and common sense travel scenario coverage.
The list below is a starting point only. It must be reviewed, expanded, and refined before this task is marked complete.

Starting Point Topic Categories & Sub-Topics
yamltopics:

  airport:
    display_name: "Airport & Check-In"
    topics:
      - slug: check_in_counter
        display_name: "Check-In Counter"
        description: "Checking in for a flight, dropping bags, seat selection"
        difficulty_range: [1, 5]
      - slug: security_screening
        display_name: "Security Screening"
        description: "Going through airport security, liquids rules, removing items"
        difficulty_range: [1, 4]
      - slug: boarding_gate
        display_name: "Boarding Gate"
        description: "Finding the gate, boarding announcements, boarding process"
        difficulty_range: [1, 4]
      - slug: flight_delay
        display_name: "Flight Delay or Cancellation"
        description: "Handling delays, rebooking, communicating with airline staff"
        difficulty_range: [3, 7]

  immigration_customs:
    display_name: "Immigration & Customs"
    topics:
      - slug: immigration_desk
        display_name: "Immigration Desk"
        description: "Answering officer questions, purpose of visit, length of stay"
        difficulty_range: [2, 6]
      - slug: customs_declaration
        display_name: "Customs Declaration"
        description: "Declaring items, answering customs officer questions"
        difficulty_range: [2, 5]
      - slug: baggage_claim
        display_name: "Baggage Claim & Lost Luggage"
        description: "Finding baggage, reporting lost bags, filing a claim"
        difficulty_range: [2, 6]

  ground_transportation:
    display_name: "Ground Transportation"
    topics:
      - slug: taxi
        display_name: "Taking a Taxi"
        description: "Hailing a taxi, giving directions, paying"
        difficulty_range: [1, 4]
      - slug: rideshare
        display_name: "Rideshare (Uber / Grab / Lyft)"
        description: "Using a rideshare app, communicating with driver"
        difficulty_range: [1, 4]
      - slug: public_transport
        display_name: "Public Transport"
        description: "Buying tickets, asking for directions, navigating metro or bus"
        difficulty_range: [2, 6]
      - slug: car_rental
        display_name: "Car Rental"
        description: "Renting a car, insurance options, returning the vehicle"
        difficulty_range: [3, 7]

  hotel:
    display_name: "Hotel"
    topics:
      - slug: hotel_check_in
        display_name: "Hotel Check-In"
        description: "Checking in, room requests, key card, facilities questions"
        difficulty_range: [1, 5]
      - slug: hotel_check_out
        display_name: "Hotel Check-Out"
        description: "Checking out, reviewing the bill, late check-out requests"
        difficulty_range: [2, 5]
      - slug: room_issues
        display_name: "Room Issues & Complaints"
        description: "Reporting problems — noise, broken items, wrong room type"
        difficulty_range: [3, 7]
      - slug: concierge_requests
        display_name: "Concierge Requests"
        description: "Asking for recommendations, bookings, local information"
        difficulty_range: [3, 6]

  restaurants:
    display_name: "Restaurants & Ordering"
    topics:
      - slug: ordering_food
        display_name: "Ordering Food"
        description: "Reading a menu, ordering, asking about dishes, dietary needs"
        difficulty_range: [1, 5]
      - slug: paying_the_bill
        display_name: "Paying the Bill"
        description: "Asking for the check, splitting, tipping culture"
        difficulty_range: [2, 5]
      - slug: food_allergies
        display_name: "Food Allergies & Dietary Restrictions"
        description: "Communicating allergies and restrictions to staff"
        difficulty_range: [3, 7]
      - slug: making_a_reservation
        display_name: "Making a Restaurant Reservation"
        description: "Calling or requesting a table, special occasions"
        difficulty_range: [3, 6]

  getting_lost:
    display_name: "Getting Lost & Asking Directions"
    topics:
      - slug: asking_directions
        display_name: "Asking for Directions"
        description: "Asking strangers for help navigating on foot or by transit"
        difficulty_range: [1, 5]
      - slug: wrong_train
        display_name: "Wrong Train or Bus"
        description: "Realizing you are on the wrong route, asking for help"
        difficulty_range: [2, 6]
      - slug: map_navigation
        display_name: "Using Maps & Navigation Help"
        description: "Asking someone to help read a map or understand directions"
        difficulty_range: [1, 4]

  shopping:
    display_name: "Shopping"
    topics:
      - slug: finding_items
        display_name: "Finding Items in a Store"
        description: "Asking staff for help finding products"
        difficulty_range: [1, 4]
      - slug: returning_items
        display_name: "Returning or Exchanging Items"
        description: "Returning a purchase, exchange policy, receipts"
        difficulty_range: [3, 7]

  emergencies:
    display_name: "Emergency Situations"
    topics:
      - slug: medical_emergency
        display_name: "Medical Emergency"
        description: "Explaining symptoms, calling for help, visiting a clinic"
        difficulty_range: [4, 9]
      - slug: lost_documents
        display_name: "Lost Passport or Documents"
        description: "Reporting lost passport, contacting embassy, next steps"
        difficulty_range: [5, 9]
      - slug: theft_or_loss
        display_name: "Theft or Lost Belongings"
        description: "Reporting theft to police or hotel, filing a report"
        difficulty_range: [4, 8]

  medical_pharmacy:
    display_name: "Medical & Pharmacy"
    topics:
      - slug: pharmacy_visit
        display_name: "Visiting a Pharmacy"
        description: "Explaining symptoms, asking for over-the-counter medication"
        difficulty_range: [3, 7]
      - slug: doctors_visit
        display_name: "Visiting a Doctor or Clinic"
        description: "Describing symptoms, understanding instructions, insurance"
        difficulty_range: [5, 9]

  small_talk:
    display_name: "Small Talk with Strangers"
    topics:
      - slug: plane_conversation
        display_name: "Small Talk on the Plane"
        description: "Talking to a seatmate — introduction, travel plans, interests"
        difficulty_range: [3, 8]
      - slug: hotel_lobby_chat
        display_name: "Hotel Lobby Small Talk"
        description: "Casual conversation with other guests or staff"
        difficulty_range: [2, 7]
      - slug: tourist_attraction_chat
        display_name: "Chatting at a Tourist Attraction"
        description: "Meeting travelers, asking to take photos, sharing tips"
        difficulty_range: [2, 6]

  money_banking:
    display_name: "Money & Banking"
    topics:
      - slug: atm_use
        display_name: "Using an ATM Abroad"
        description: "Navigating foreign ATM interfaces, foreign transaction issues"
        difficulty_range: [1, 4]
      - slug: currency_exchange
        display_name: "Currency Exchange"
        description: "Exchanging money, asking about rates, understanding fees"
        difficulty_range: [2, 5]
After populating from the above starting point, the developer must:

Review the full list for gaps — what common travel situations are missing?
Add any scenarios identified during Task 0.2 research as high-frequency Korean traveler pain points
Ensure all 14 master roadmap scenario categories have at least 2 sub-topics each
Confirm difficulty ranges are appropriate per level
Target minimum: 30 topics total across all categories


Task 0.4 — Initial locations.yaml Population
Goal: Populate locations.yaml with the confirmed top travel destinations for Korean travelers. Minimum 15 locations at launch. The starting point list below must be validated and expanded during this task using research findings from Task 0.2.
The list below is a starting point only. Rankings and selections must be confirmed against actual Korean outbound travel data before this task is marked complete.

Starting Point Locations
yamllocations:

  - slug: japan
    display_name: "Japan"
    cities: ["Tokyo", "Osaka", "Kyoto", "Fukuoka", "Sapporo"]
    language_note: "English widely understood in tourist areas. Japanese staff often speak basic English."
    cultural_note: "Politeness and formality valued. Quiet in public transport. Tipping not practiced."
    priority: 1

  - slug: usa
    display_name: "United States"
    cities: ["New York", "Los Angeles", "Las Vegas", "Hawaii", "San Francisco"]
    language_note: "English only. Direct communication style."
    cultural_note: "Tipping expected (15–20%). Service is friendly and casual. Personal space valued."
    priority: 2

  - slug: thailand
    display_name: "Thailand"
    cities: ["Bangkok", "Chiang Mai", "Phuket", "Pattaya"]
    language_note: "English functional in tourist areas. Thai staff often speak basic English."
    cultural_note: "Buddhist culture — temples require modest dress. Bargaining expected in markets."
    priority: 3

  - slug: france
    display_name: "France"
    cities: ["Paris", "Nice", "Lyon", "Marseille"]
    language_note: "French preferred. English widely understood in Paris and tourist areas."
    cultural_note: "Formal greetings expected. Dining is leisurely. Tipping optional but appreciated."
    priority: 4

  - slug: vietnam
    display_name: "Vietnam"
    cities: ["Hanoi", "Ho Chi Minh City", "Da Nang", "Hoi An"]
    language_note: "English functional in tourist areas. Younger generation often speaks English."
    cultural_note: "Bargaining common in markets. Motorbike traffic intense — crossing streets is a skill."
    priority: 5

  - slug: spain
    display_name: "Spain"
    cities: ["Barcelona", "Madrid", "Seville", "Granada"]
    language_note: "Spanish preferred outside tourist areas. English understood in major cities."
    cultural_note: "Late dining culture. Lunch is the main meal. Siestas still observed in some areas."
    priority: 6

  - slug: uk
    display_name: "United Kingdom"
    cities: ["London", "Edinburgh", "Manchester", "Oxford"]
    language_note: "English only. British accent and vocabulary differ from American English."
    cultural_note: "Queuing strictly observed. Politeness expected. Tipping 10–15% in restaurants."
    priority: 7

  - slug: italy
    display_name: "Italy"
    cities: ["Rome", "Milan", "Florence", "Venice", "Naples"]
    language_note: "Italian preferred outside major cities. English understood in tourist areas."
    cultural_note: "Coffee culture — espresso standing at the bar. Fashion and appearance matter in Milan."
    priority: 8

  - slug: australia
    display_name: "Australia"
    cities: ["Sydney", "Melbourne", "Brisbane", "Gold Coast", "Perth"]
    language_note: "English only. Australian slang can be confusing for learners."
    cultural_note: "Casual and friendly culture. Tipping not mandatory but appreciated. Sun safety important."
    priority: 9

  - slug: singapore
    display_name: "Singapore"
    cities: ["Singapore City"]
    language_note: "English is an official language. Singlish accent present but widely understood."
    cultural_note: "Strict laws — no chewing gum, heavy fines for littering. Very safe and orderly."
    priority: 10

  - slug: germany
    display_name: "Germany"
    cities: ["Berlin", "Munich", "Frankfurt", "Hamburg", "Cologne"]
    language_note: "German preferred. English widely understood in cities and business contexts."
    cultural_note: "Punctuality is critical. Direct communication style. Formal in professional settings."
    priority: 11

  - slug: canada
    display_name: "Canada"
    cities: ["Toronto", "Vancouver", "Montreal", "Calgary"]
    language_note: "English (and French in Quebec). Very similar to American English."
    cultural_note: "Polite and multicultural. Tipping expected (15–20%). Cold winters in most cities."
    priority: 12

  - slug: philippines
    display_name: "Philippines"
    cities: ["Manila", "Cebu", "Boracay", "Palawan"]
    language_note: "English is an official language. Widely spoken across the country."
    cultural_note: "Warm and hospitable culture. Jeepney and tricycle transport unique to the country."
    priority: 13

  - slug: uae
    display_name: "United Arab Emirates"
    cities: ["Dubai", "Abu Dhabi"]
    language_note: "Arabic official but English widely used in business and tourism."
    cultural_note: "Dress modestly in public. Ramadan affects business hours. Alcohol only in licensed venues."
    priority: 14

  - slug: new_zealand
    display_name: "New Zealand"
    cities: ["Auckland", "Queenstown", "Wellington", "Christchurch"]
    language_note: "English only. New Zealand accent distinct but clear."
    cultural_note: "Maori culture prominent. Outdoor lifestyle. Very friendly and relaxed atmosphere."
    priority: 15
After populating from the above starting point, the developer must:

Validate rankings against actual Korean outbound travel data from Task 0.2
Add any destinations identified as high-volume Korean travel destinations not on this list
Adjust priority rankings based on data — the list above is based on general knowledge, not confirmed statistics
Add or refine cultural and language notes based on research findings
Target minimum: 15 locations confirmed and validated · expandable at any time


Task 0.5 — 6-Month Review Protocol
Goal: Document the review cadence so any operator or developer picking up the project in the future knows when and how to update the framework.
Write the following into the Phase 0 project log:
FRAMEWORK REVIEW PROTOCOL — Carry-On Confidence

Cadence: Every 6 months from the date of Phase 0 completion.
Next review due: [DATE — 6 months from Phase 0 completion date]

Review checklist:
□ Are these still the top destinations for Korean travelers? Check KNTO and travel agency annual reports.
□ Are there new scenario types to add? Check Korean travel communities (Naver Cafe, travel blogs) for emerging pain points.
□ Are any topics or locations obsolete or low-priority? Remove or deprioritize.
□ What travel trends have emerged since the last review? (New popular destinations, new traveler behaviors)
□ Update topics.yaml and locations.yaml accordingly.
□ Commit updated config files with message: "chore: 6-month framework review — [DATE]"
□ Note next review date in project log.

Task 0.6 — Initial Commit
Once Tasks 0.1 through 0.5 are complete and verified:
bashgit add .
git commit -m "chore: Phase 0 scaffold and research complete

Carry-On Confidence — Travel English Worksheet Generator
New standalone repo initialized.

Completed:
- Project scaffold: full directory structure, .gitignore, .env.example,
  requirements.txt stub, README.md
- Task 0.2: Korean travel data sources researched and documented
  Primary fetch source confirmed: [SOURCE NAME]
  API keys required: [LIST]
  Fetcher architecture recommendation: [SUMMARY]
- Task 0.3: config/topics.yaml populated
  [N] topics across [N] scenario categories
- Task 0.4: config/locations.yaml populated
  [N] destinations with language and cultural notes
  Rankings validated against [DATA SOURCE]
- Task 0.5: 6-month review protocol documented in project log
  Next review due: [DATE]
- config/levels.yaml: Primo Scale 1-10 copied from [SOURCE REPO]

Known issues: none
Next phase: Phase 1 — travel_fetcher.py"

Phase 0 Project Log
Write carry_on_confidence_phase0_project_log.json after the commit. Follow the same format as all existing Primo project logs. Required fields:

project
phase_completed: 0
phase_next: 1
log_date
log_author
purpose
context_files — required reading order for whoever picks up Phase 1
repo — name, remote URL, local path, branch, platform
phase_0_summary — what was done, what was found, what was decided
data_sources — confirmed primary and secondary sources with fetch method
topics_count — total topics in topics.yaml
locations_count — total locations in locations.yaml
review_protocol — next review date
known_issues — anything unresolved carried into Phase 1
next_phase_prerequisites — what must be true before Phase 1 can begin


Definition of Done

 GitHub repo exists and is cloned locally
 Directory structure matches the architecture in the master roadmap
 .gitignore excludes .env, output/, __pycache__/, *.docx
 .env.example contains correct key placeholders
 levels.yaml copied from existing Primo program and confirmed correct
 Task 0.2 research summary written and committed
 Primary Korean travel data source confirmed as fetchable
 topics.yaml has minimum 30 topics across all 14 scenario categories
 locations.yaml has minimum 15 destinations with metadata
 Rankings in locations.yaml validated against real data
 6-month review protocol documented
 Clean commit on main with detailed commit message
 carry_on_confidence_phase0_project_log.json written and saved


End of carry_on_confidence_phase0_roadmap.md
Version: 0.1 — 2026-06-16