# === File Overview (auto-generated) ===
# Project: USYD Tower Adventure
# File: usyd_adventure_pygame_update2_run/game/player.py
# Purpose: Player entity: movement, collision, animation and inventory handling.
#
# Key Notes:
# - Player entity: movement, collision, animation and inventory handling.
# - Uses pygame for rendering/input/audio.
# - Defines Player class.
# - Rendering routines.
# - Door mechanics present.
#
# Run instructions:
# - Recommended entry script: main.py (or any file with __main__ guard).
# - Example: `python main.py` from the project root.
#
# This header was auto-generated to help readers navigate the codebase.


import pygame
from .constants import TILE, COLORS

class Player:
    # Non-passable bump-only interact nodes
    BUMP_ONLY = {"b1","b2","b3","b4","al"}

    def __init__(self, rc=(1,1)):
        self.rc = rc
        self.color = COLORS.get("player", (50, 150, 255))

    def try_move(self, dr, dc, level, state, ui):
        nr, nc = self.rc[0] + dr, self.rc[1] + dc
        to = (nr, nc)
        if not level.in_bounds(to):
            return None
        tok = level.get(to)
        # Doors: require key and consume it
        if level.is_door(tok):
            need = f"k{tok[1:]}"
            if state.has_item(need):
                state.consume_item(need, 1)
                level.set(to, '.')
                ui.toast(f"Unlocked with {need} (consumed).")
                self.rc = to
                return ('move', to)
            else:
                ui.toast(f"Door locked. Need {need}.")
                return None
        # NPC
        if isinstance(tok, str) and tok.startswith('p') and tok[1:].isdigit():
            return ('npc', to)
        # Bump-only
        if isinstance(tok, str) and tok in self.BUMP_ONLY:
            return ('item_bump', to)
        # Passable
        if not level.is_wall(tok):
            self.rc = to
            return ('move', to)
        return None

    def draw(self, screen, origin=(0,0)):
        r, c = self.rc
        ox, oy = origin
        rect = pygame.Rect(ox + c*TILE, oy + r*TILE, TILE, TILE)
        pygame.draw.rect(screen, self.color, rect)