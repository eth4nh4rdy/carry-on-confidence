"""
Carry-On Confidence — LLM worksheet generator.

Takes a live aggregator payload and returns a fully structured 8-page
worksheet content dict. Pure data transformation layer: builds the prompt,
calls OpenRouter, parses the response using section markers, and returns a
clean Python dict. Produces no files and has no knowledge of DOCX formatting.
"""

import logging
import os
from pathlib import Path

import requests
import yaml
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

_SEPARATOR = "______________________________________________________________________________________________"


def get_llm_client() -> dict:
    """
    Read config/llm.yaml and return a configured OpenRouter client dict.
    OpenRouter is the only supported provider — no branching logic for others.
    """
    llm_config_path = Path(__file__).parent / "config" / "llm.yaml"
    with open(llm_config_path, encoding="utf-8") as f:
        config = yaml.safe_load(f)

    provider = config["provider"]
    provider_config = config[provider]

    api_key_env = provider_config["api_key_env"]
    api_key = os.environ.get(api_key_env)
    if not api_key:
        raise RuntimeError(f"{api_key_env} not found in environment")

    generation = provider_config["generation"]

    return {
        "provider": provider,
        "base_url": provider_config["base_url"],
        "model": provider_config["model"],
        "api_key": api_key,
        "max_tokens": generation["max_tokens"],
        "temperature": generation["temperature"],
        "timeout": provider_config["timeout"],
    }


def load_exercise_bank(level: int) -> list:
    """
    Load exercises/carry_on_exercise_bank.yaml and return the list of
    exercise type dicts eligible for the requested level.
    """
    bank_path = Path(__file__).parent / "exercises" / "carry_on_exercise_bank.yaml"
    with open(bank_path, encoding="utf-8") as f:
        bank_config = yaml.safe_load(f)

    exercises = bank_config["exercises"]

    eligible = [
        e for e in exercises
        if e["difficulty_min"] <= level <= e["difficulty_max"]
    ]

    if len(eligible) < 4:
        eligible = [
            e for e in exercises
            if e["difficulty_min"] <= level + 1 and e["difficulty_max"] >= level - 1
        ]

    return eligible


def _build_system_prompt() -> str:
    """Build the system prompt. String concatenation only — no f-strings."""
    return (
        "You are an expert ESL worksheet creator for Primo English, a premium English coaching business in Seoul, South Korea. Your students are Korean university students and working professionals preparing for real-world travel situations overseas.\n\n" +
        "Your output must use the exact section markers provided. No text outside the markers. Every marker must appear exactly as written, on its own line. Never skip a marker.\n" +
        "Korean definitions are mandatory for every keyword — do not omit them under any circumstances."
    )


def _build_user_prompt(payload: dict, level: int, level_config: dict, exercise_bank: list) -> str:
    """
    Build the full user prompt from the aggregator payload, target level,
    level config, and filtered exercise bank. String concatenation only —
    no f-strings, since the prompt contains literal { and } characters in
    format examples.
    """
    location_display = payload["location"].replace("_", " ").title()
    topic_display = payload["topic"].replace("_", " ").title()

    # SECTION 1 — WORKSHEET CONTEXT
    section1 = (
        "WORKSHEET CONTEXT\n" +
        "Location: " + location_display + "\n" +
        "Topic: " + topic_display + "\n" +
        "Target level: " + str(level) + " — " + level_config["label"] + " (" + level_config["cefr"] + ")\n" +
        "Level description: " + level_config["description"] + "\n\n"
    )

    # SECTION 2 — KOREAN TRAVEL CONTENT (Naver)
    naver = payload.get("sources", {}).get("naver", {})
    naver_results = naver.get("results") or []
    if naver.get("error") is not None or len(naver_results) == 0:
        section2 = "KOREAN TRAVEL CONTENT\nNo Naver data available for this run.\n\n"
    else:
        section2 = "KOREAN TRAVEL CONTENT (what Korean travelers are saying about this destination and scenario)\n"
        for i, item in enumerate(naver_results[:8], start=1):
            section2 += str(i) + ". " + item.get("title", "") + " — " + item.get("description", "") + "\n"
        section2 += "\n"

    # SECTION 3 — INTERNATIONAL CONTENT (YouTube)
    youtube = payload.get("sources", {}).get("youtube", {})
    youtube_results = youtube.get("results") or []
    if youtube.get("error") is not None or len(youtube_results) == 0:
        section3 = "INTERNATIONAL CONTENT\nNo YouTube data available for this run.\n\n"
    else:
        section3 = "INTERNATIONAL CONTENT (what travelers internationally are saying)\n"
        for i, item in enumerate(youtube_results[:5], start=1):
            description = item.get("description", "")[:200]
            section3 += str(i) + ". " + item.get("title", "") + " — " + description + "\n"
        section3 += "\n"

    # SECTION 4 — EXERCISE TYPES
    section4 = (
        "EXERCISE TYPES AVAILABLE FOR LEVEL " + str(level) + "\n" +
        "Select exactly 8 exercises from the types below. Rules:\n" +
        "- Use at least 4 distinct exercise types\n" +
        "- No single type may appear more than 2 times\n" +
        "- All exercises must match the worksheet topic, destination, and level\n\n"
    )
    for exercise in exercise_bank:
        section4 += (
            exercise["id"] + ": " + exercise["display_name"] + "\n" +
            "Difficulty range: " + str(exercise["difficulty_min"]) + "-" + str(exercise["difficulty_max"]) + "\n" +
            "Instructions line: " + exercise["instructions"] + "\n" +
            "Keyword requirement: " + str(exercise["keyword_requirement"]) + "\n" +
            "Format:\n" +
            exercise["format"] +
            "\n---\n"
        )

    # SECTION 5 — PER-PAGE INSTRUCTIONS
    page1 = (
        "===PAGE1===\n" +
        "Generate exactly 3 small talk questions related to the scenario and destination. These are conversation starters — friendly, light, personally engaging. NOT comprehension questions. Level-appropriate.\n" +
        "A student dealing with " + topic_display + " in " + location_display + " might naturally say these to a stranger or a travel companion.\n" +
        "Count before submitting. Exactly 3. No more, no fewer.\n" +
        "Format: one question per line with a blank line between each.\n\n"
    )

    page2 = (
        "===PAGE2===\n" +
        "Select 3 vocabulary words essential for surviving the " + topic_display + " scenario in " + location_display + ". Selection criteria:\n" +
        "- Directly useful in this specific travel scenario\n" +
        "- Likely to be unfamiliar to Korean ESL learners at level " + str(level) + "\n" +
        "- Real-world functional vocabulary — not academic\n" +
        "- Level-appropriate\n\n" +
        "For each keyword, output this exact format:\n\n" +
        "**[word] ([part of speech])**\n" +
        "**English:** [one clear sentence definition]\n" +
        "**Korean:** [한국어로 한 문장 정의 — mandatory, never skip]\n" +
        "**Synonyms:** [synonym1] · [synonym2] · [synonym3]\n" +
        "**My sentence:** __________________________\n\n" +
        "______________________________________________________________________________________________\n\n" +
        "Three keywords. Three separator lines. No other text.\n" +
        "IMPORTANT: Every keyword block must end with the separator line above. " +
        "Three keywords = three separator lines. Count them before moving on.\n\n"
    )

    page3 = (
        "===PAGE3===\n" +
        "Three more vocabulary words for the " + topic_display + " scenario in " + location_display + ". Same format as PAGE2. Different words — do not repeat any word from PAGE2.\n" +
        "These 6 keywords together must give the student a complete survival vocabulary set for this scenario.\n" +
        "IMPORTANT: Every keyword block must end with the separator line. " +
        "Three keywords = three separator lines. Count them before moving on.\n\n"
    )

    page4 = (
        "===PAGE4===\n" +
        "Role Play situation card 1. Output this exact format:\n\n" +
        "🎭 SITUATION: [scenario title — short, punchy]\n\n" +
        "📍 Location: [specific place within " + location_display + "]\n" +
        "👤 You are: [Korean traveler — specific description]\n" +
        "👥 Your partner is: [who they are speaking to]\n\n" +
        "The situation:\n" +
        "[2-4 sentences — realistic chaos, things have gone slightly wrong, time is limited, language is a barrier]\n\n" +
        "Your goal:\n" +
        "[What the student must accomplish to succeed in this role play]\n\n" +
        "Try to use these words:\n" +
        "[3 keywords from PAGE2 and PAGE3 — choose the most useful for this card]\n\n" +
        "Card 1 places the student at the beginning of the scenario — arriving, first contact, initial problem.\n\n"
    )

    page5 = (
        "===PAGE5===\n" +
        "Role Play situation card 2. Same format as PAGE4.\n" +
        "Card 2 escalates or shifts — a different moment in the same scenario. Different specific location within " + location_display + ", different stakes, different partner role. The student is deeper into the situation.\n" +
        "Keywords should overlap partially but not identically with Card 1.\n" +
        "Do not make Card 2 a repeat of Card 1 with minor changes. It must feel like a different scene.\n\n"
    )

    page6 = (
        "===PAGE6===\n" +
        "Generate exactly 8 exercises for level " + str(level) + " using the EXERCISE TYPES AVAILABLE above.\n" +
        "Rules:\n" +
        "- Exactly 8 exercises — count before submitting\n" +
        "- At least 4 distinct exercise types\n" +
        "- No single type more than 2 times\n" +
        "- All exercises grounded in the " + topic_display + " scenario in " + location_display + "\n" +
        "- Tone: survival-focused, slightly chaotic, human — never dry or textbook\n\n" +
        "For each exercise output this exact format:\n\n" +
        "[exercise type id]: [Exercise Type Display Name]\n" +
        "Instructions: [instructions line from exercise bank — verbatim]\n" +
        "---\n" +
        "[Exercise content — generated from this worksheet's keywords, scenario, destination, and level]\n\n" +
        "After all 8 exercises output: ===EXERCISES_END===\n\n"
    )

    page8 = (
        "===PAGE8===\n" +
        "Homework task. Choose based on level " + str(level) + ":\n" +
        "- Levels 1-4: Writing task (3-5 sentences about the scenario)\n" +
        "- Levels 5-7: Writing or speaking task — student's choice\n" +
        "- Levels 8-10: Speaking task (2-minute monologue or recorded response)\n\n" +
        "Output 2-4 sentences describing the task. Level-appropriate. Tied directly to the " + topic_display + " scenario in " + location_display + " — not a generic prompt. End with a clear instruction to the student.\n\n" +
        "===END==="
    )

    return (
        section1 + section2 + section3 + section4 +
        page1 + page2 + page3 + page4 + page5 + page6 + page8
    )


def _parse_response(response_text: str) -> dict:
    """
    Split the raw LLM response on section markers into page1..page6, page8.
    There is no ===PAGE7=== — PAGE6 content spans two physical worksheet
    pages, handled by the formatter, not here. No answer_key key — this
    program does not produce answer keys.
    """
    markers = [
        "===PAGE1===", "===PAGE2===", "===PAGE3===",
        "===PAGE4===", "===PAGE5===", "===PAGE6===", "===PAGE8===",
    ]
    marker_keys = ["page1", "page2", "page3", "page4", "page5", "page6", "page8"]

    positions = {}
    for marker in markers:
        idx = response_text.find(marker)
        if idx == -1:
            raise RuntimeError("_parse_response: missing marker " + marker)
        positions[marker] = idx

    end_idx = response_text.find("===END===")
    has_end = end_idx != -1
    if not has_end:
        logger.warning("_parse_response: missing ===END=== marker; taking remainder after ===PAGE8=== as page8 content")

    content = {}
    for i, marker in enumerate(markers):
        start = positions[marker] + len(marker)
        if i + 1 < len(markers):
            end = positions[markers[i + 1]]
        else:
            end = end_idx if has_end else len(response_text)
        content[marker_keys[i]] = response_text[start:end].strip()

    return content


def _validate_output(content: dict) -> None:
    """Raise RuntimeError with a clear message on any validation failure."""
    required_keys = ["page1", "page2", "page3", "page4", "page5", "page6", "page8"]
    for key in required_keys:
        if not content.get(key):
            raise RuntimeError("_validate_output: " + key + " is missing or empty")

    page2_count = content["page2"].count(_SEPARATOR)
    if page2_count != 3:
        raise RuntimeError(
            "_validate_output: page2 separator count check failed (expected 3, got " +
            str(page2_count) + "): " + content["page2"][:200]
        )

    page3_count = content["page3"].count(_SEPARATOR)
    if page3_count != 3:
        raise RuntimeError(
            "_validate_output: page3 separator count check failed (expected 3, got " +
            str(page3_count) + "): " + content["page3"][:200]
        )

    if "🎭 SITUATION:" not in content["page4"]:
        raise RuntimeError(
            "_validate_output: page4 situation card check failed: " + content["page4"][:200]
        )

    if "🎭 SITUATION:" not in content["page5"]:
        raise RuntimeError(
            "_validate_output: page5 situation card check failed: " + content["page5"][:200]
        )

    if not content["page6"].strip():
        raise RuntimeError(
            "_validate_output: page6 non-empty check failed: " + content["page6"][:200]
        )

    logger.info("Validation passed")


def generate_worksheet(payload: dict, level: int, level_config: dict, exercise_bank: list) -> dict:
    """
    Orchestrate a single worksheet generation: build the prompt, call
    OpenRouter, parse the section-marked response, validate it, and return
    the content dict.
    """
    client_config = get_llm_client()
    system_prompt = _build_system_prompt()
    user_prompt = _build_user_prompt(payload, level, level_config, exercise_bank)

    url = client_config["base_url"] + "/chat/completions"
    headers = {
        "Authorization": "Bearer " + client_config["api_key"],
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/eth4nh4rdy/carry-on-confidence",
        "X-Title": "carry-on-confidence",
    }
    payload_body = {
        "model": client_config["model"],
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "max_tokens": client_config["max_tokens"],
        "temperature": client_config["temperature"],
    }

    logger.info("API call initiated to " + client_config["model"])

    try:
        response = requests.post(url, headers=headers, json=payload_body, timeout=client_config["timeout"])
    except requests.exceptions.RequestException as e:
        logger.error("API call failed: network error")
        raise RuntimeError("Network error: " + str(e))

    if response.status_code != 200:
        logger.error("API call failed: status " + str(response.status_code))
        raise RuntimeError("LLM API returned status " + str(response.status_code) + ": " + response.text)

    response_json = response.json()

    try:
        response_text = response_json["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as e:
        logger.error("API call failed: unexpected response shape")
        raise RuntimeError("Unexpected response shape: " + str(e))

    total_tokens = response_json.get("usage", {}).get("total_tokens")
    if total_tokens is not None:
        logger.info("Response received — total tokens: " + str(total_tokens))
    else:
        logger.info("Response received")

    content = _parse_response(response_text)

    try:
        _validate_output(content)
    except RuntimeError as e:
        logger.warning("Validation failed on first attempt — retrying: " + str(e))
        try:
            response = requests.post(url, headers=headers, json=payload_body, timeout=client_config["timeout"])
        except requests.exceptions.RequestException as e2:
            logger.error("API call failed on retry: network error")
            raise RuntimeError("Network error on retry: " + str(e2))
        if response.status_code != 200:
            logger.error("API call failed on retry: status " + str(response.status_code))
            raise RuntimeError("LLM API returned status " + str(response.status_code) + " on retry: " + response.text)
        try:
            response_text = response.json()["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as e2:
            raise RuntimeError("Unexpected response shape on retry: " + str(e2))
        content = _parse_response(response_text)
        try:
            _validate_output(content)
        except RuntimeError as e2:
            logger.error("Validation failed after retry: " + str(e2))
            raise

    return content
