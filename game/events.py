# === File Overview (auto-generated) ===
# Project: USYD Tower Adventure
# File: usyd_adventure_pygame_update2_run/game/events.py
# Purpose: Portal mechanics present.
#
# Key Notes:
# - Portal mechanics present.
#
# Run instructions:
# - Recommended entry script: main.py (or any file with __main__ guard).
# - Example: `python main.py` from the project root.
#
# This header was auto-generated to help readers navigate the codebase.



PORTAL_GRAPH = {
    ("plane", "au"): ("customs", "ua"),
    ("customs", "ua"): ("plane", "au"),
    ("customs", "up"): ("airport", "pu"),
    ("airport", "pu"): ("customs", "up"),

    # Airport <-> Campus via street
    ("airport", "ac"): ("street_airport_to_campus", "at"),
    ("street_airport_to_campus", "at"): ("airport", "ac"),
    ("street_airport_to_campus", "tu"): ("campus", "ca"),
    ("campus", "ca"): ("street_airport_to_campus", "tu"),

    # Campus <-> Library
    ("campus", "cl"): ("library", "lc"),
    ("library", "lc"): ("campus", "cl"),

    # Campus <-> Quadrangle
    ("campus", "cq"): ("quadrangle", "qc"),
    ("quadrangle", "qc"): ("campus", "cq"),

    # Campus <-> Market via street
    ("campus", "cm"): ("street_campus_to_market", "tc"),
    ("street_campus_to_market", "tc"): ("campus", "cm"),
    ("street_campus_to_market", "tm"): ("market", "mc"),
    ("market", "mc"): ("street_campus_to_market", "tm"),

    # Campus <-> Dorm
    ("campus", "cd"): ("dorm", "dc"),
    ("dorm", "dc"): ("campus", "cd"),

    # Campus <-> Student Center
    ("campus", "cs"): ("student_center", "sc"),
    ("student_center", "sc"): ("campus", "cs"),

    # Engineering <-> Campus
    ("engineering", "ec"): ("campus", "ce"),
    ("campus", "ce"): ("engineering", "ec"),

    # Engineering <-> Lab
    ("engineering", "el"): ("lab", "le"),
    ("lab", "le"): ("engineering", "el"),

    # Market <-> Harbour
    ("market", "mh"): ("harbour", "hm"),
    ("harbour", "hm"): ("market", "mh"),

    # Dorm <-> Rooftop
    ("dorm", "dr"): ("rooftop", "rd"),
    ("rooftop", "rd"): ("dorm", "dr"),
}
PORTAL_REQUIREMENTS = {
    ("campus", "cm"): "bc",
}
