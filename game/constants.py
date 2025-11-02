# === File Overview (auto-generated) ===
# Project: USYD Tower Adventure
# File: usyd_adventure_pygame_update2_run/game/constants.py
# Purpose: Global constants, paths, tuning parameters, key bindings.
#
# Key Notes:
# - Global constants, paths, tuning parameters, key bindings.
# - Portal mechanics present.
# - HUD/stats (Knowledge/Energy/Social).
#
# Run instructions:
# - Recommended entry script: main.py (or any file with __main__ guard).
# - Example: `python main.py` from the project root.
#
# This header was auto-generated to help readers navigate the codebase.


TILE = 32
FPS = 60
FONT_NAME = "Arial"
SCREEN_MARGIN = 240

# New UI layout sizes (px)
LEFT_UI_W = 160
RIGHT_UI_W = 160
BOTTOM_UI_H = 96

COLORS = {
    "bg": (245, 246, 248),
    "wall": (0, 0, 0),         # pure black
    "floor": (255, 255, 255),  # pure white
    "portal": (180, 220, 255),
    "npc": (255, 210, 80),
    "pickup": (120, 230, 120),
    "locked": (230, 80, 80),
    "hud_bg": (245, 245, 245),
    "hud_fg": (30, 30, 30),
    "toast_bg": (0, 0, 0),
    "toast_fg": (255, 255, 255),
    "player": (50, 150, 255),
}

FLOOR = "."
WALLS = set("#X")