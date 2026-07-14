"""
Carry-On Confidence — CLI entry point.
"""

import argparse
import sys
import yaml
from aggregator import aggregate
from generator import generate_worksheet, load_exercise_bank
from formatter import format_worksheet


def _load_valid_topics() -> set:
    with open("config/topics.yaml", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    slugs = set()
    for category in data["categories"].values():
        for topic in category["topics"]:
            slugs.add(topic["slug"])
    return slugs


def _load_valid_locations() -> set:
    with open("config/locations.yaml", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return {loc["slug"] for loc in data["locations"]}


def _validate_args(args, valid_topics, valid_locations) -> None:
    if args.level is None or not (1 <= args.level <= 10):
        print("Error: --level must be an integer between 1 and 10.")
        sys.exit(1)
    if args.topic not in valid_topics:
        print(f"Error: '{args.topic}' is not a valid topic. Run with --list-topics to see available options.")
        sys.exit(1)
    if args.location not in valid_locations:
        print(f"Error: '{args.location}' is not a valid location. Run with --list-locations to see available options.")
        sys.exit(1)


def main() -> None:
    parser = argparse.ArgumentParser(description="Carry-On Confidence worksheet generator")
    # Required for normal use but made optional here so --list-topics/--list-locations
    # can work without supplying all three args.
    parser.add_argument("--level", type=int, default=None)
    parser.add_argument("--topic", default=None)
    parser.add_argument("--location", default=None)
    parser.add_argument("--list-topics", action="store_true")
    parser.add_argument("--list-locations", action="store_true")
    args = parser.parse_args()

    valid_topics = _load_valid_topics()
    valid_locations = _load_valid_locations()

    if args.list_topics:
        for slug in sorted(valid_topics):
            print(slug)
        sys.exit(0)

    if args.list_locations:
        for slug in sorted(valid_locations):
            print(slug)
        sys.exit(0)

    _validate_args(args, valid_topics, valid_locations)

    with open("config/levels.yaml", "r", encoding="utf-8") as f:
        levels_data = yaml.safe_load(f)
    level_config = levels_data["levels"][args.level]

    exercise_bank = load_exercise_bank(args.level)

    payload = aggregate(args.location, args.topic, args.level)
    content = generate_worksheet(payload, args.level, level_config, exercise_bank)
    output_path = format_worksheet(content, args.level, level_config, args.topic, args.location)

    print(f"Worksheet saved: {output_path}")


if __name__ == "__main__":
    main()
