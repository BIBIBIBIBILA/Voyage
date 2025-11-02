# === File Overview (auto-generated) ===
# Project: USYD Tower Adventure
# File: usyd_adventure_pygame_update2_run/game/ui.py
# Purpose: UI/HUD rendering and user prompts/icons.
#
# Key Notes:
# - UI/HUD rendering and user prompts/icons.
# - Uses pygame for rendering/input/audio.
# - Rendering routines.
# - Key/Inventory handling present.
# - HUD/stats (Knowledge/Energy/Social).
#
# Run instructions:
# - Recommended entry script: main.py (or any file with __main__ guard).
# - Example: `python main.py` from the project root.
#
# This header was auto-generated to help readers navigate the codebase.

import pygame
from .constants import TILE, COLORS, LEFT_UI_W, RIGHT_UI_W, BOTTOM_UI_H

class UI:
    def __init__(self, font):
        self.font = font
        # Dialogue state
        self.current_dialog = ""
        self.prev_dialog = ""
        # keep toast API for compatibility
        self.toast_text = None
        self.toast_t = 0

    # Backward-compatible: any code calling toast() now updates the persistent dialog areas
    def toast(self, text, sec=2.0):
        text = str(text) if text is not None else ""
        if text.strip():
            self.prev_dialog = self.current_dialog
            self.current_dialog = text
        # also keep legacy vars to avoid breaking old flows
        self.toast_text = self.current_dialog
        self.toast_t = 0  # we render persistently in the bottom bar now

    def _wrap_text(self, text, max_width):
        if not text:
            return []
        words = text.split()
        lines = []
        cur = ""
        for w in words:
            test = (cur + " " + w).strip()
            surf = self.font.render(test, True, COLORS["hud_fg"])
            if surf.get_width() <= max_width or not cur:
                cur = test
            else:
                lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
        return lines

    def draw_hud(self, screen, state, map_w, map_h, sprites, margins=(LEFT_UI_W, RIGHT_UI_W, BOTTOM_UI_H)):
        sw, sh = screen.get_size()
        left_w, right_w, bottom_h = margins
        map_px_w, map_px_h = map_w * TILE, map_h * TILE

        # --- LEFT BAR ---
        left_rect = pygame.Rect(0, 0, left_w, map_px_h)
        pygame.draw.rect(screen, COLORS["hud_bg"], left_rect)
        pygame.draw.rect(screen, (120,120,120), left_rect, width=2)

        # left-top: attributes
        pad = 10
        y = pad
        title = self.font.render("attribute", True, COLORS["hud_fg"])
        screen.blit(title, (left_rect.x + pad, y)); y += title.get_height() + 6

        # draw three stats
        stats = state.stats if hasattr(state, "stats") else {}
        for label_cn, key in [("knowledge", "knowledge"), ("social:", "social"), ("energy:", "energy")]:
            val = stats.get(key, 0)
            line = f"{label_cn}: {val}"
            surf = self.font.render(line, True, COLORS["hud_fg"])
            screen.blit(surf, (left_rect.x + pad, y))
            y += surf.get_height() + 4

        # left-bottom: previous dialog
        prev_title = self.font.render("Record", True, COLORS["hud_fg"])
        # reserve some space above bottom
        prev_area_top = y + 20
        prev_area = pygame.Rect(left_rect.x + pad, prev_area_top, left_rect.width - 2*pad, left_rect.bottom - prev_area_top - pad)
        pygame.draw.rect(screen, (235,235,235), prev_area)
        pygame.draw.rect(screen, (200,200,200), prev_area, width=1)
        screen.blit(prev_title, (prev_area.x, prev_area.y - prev_title.get_height() - 2))

        maxw = prev_area.width - 8
        yy = prev_area.y + 4
        for line in self._wrap_text(self.prev_dialog, maxw):
            surf = self.font.render(line, True, COLORS["hud_fg"])
            screen.blit(surf, (prev_area.x + 4, yy))
            yy += surf.get_height() + 2

        # --- RIGHT BAR ---
        right_rect = pygame.Rect(left_w + map_px_w, 0, right_w, map_px_h)
        pygame.draw.rect(screen, COLORS["hud_bg"], right_rect)
        pygame.draw.rect(screen, (120,120,120), right_rect, width=2)

        # right-top: current level
        y = pad
        title = self.font.render("Level", True, COLORS["hud_fg"])
        screen.blit(title, (right_rect.x + pad, y)); y += title.get_height() + 4
        lv_name = getattr(state, "level", "")
        lv_surf = self.font.render(str(lv_name), True, COLORS["hud_fg"])
        screen.blit(lv_surf, (right_rect.x + pad, y)); y += lv_surf.get_height() + 10

        # right-bottom: obtained items as 3-per-row icons
        inv = getattr(state, "inventory", {}) or {}
        items = [k for k, v in inv.items() if v and v > 0]
        # grid settings
        cols = 3
        cell = TILE  # icon base size
        spacing = 6
        grid_w = cols*cell + (cols-1)*spacing
        grid_left = right_rect.x + (right_rect.width - grid_w)//2
        grid_top = y + 8
        col = 0; row = 0
        for tok in items:
            x = grid_left + col*(cell+spacing)
            ycell = grid_top + row*(cell+spacing)
            dst = pygame.Rect(x, ycell, cell, cell)
            pygame.draw.rect(screen, (230,230,230), dst)
            pygame.draw.rect(screen, (200,200,200), dst, width=1)

            # icon: try sprite, else label
            spr = sprites.get(tok) if sprites is not None else None
            if spr is not None:
                # center inside dst with 2px padding
                pad_in = 2
                sr = spr.get_rect()
                target = pygame.Rect(dst.x+pad_in, dst.y+pad_in, dst.width-2*pad_in, dst.height-2*pad_in)
                # scale if necessary
                if sr.width != target.width or sr.height != target.height:
                    spr_scaled = pygame.transform.smoothscale(spr, (target.width, target.height))
                    screen.blit(spr_scaled, target)
                else:
                    sr.center = target.center
                    screen.blit(spr, sr)
            else:
                lbl = tok[:2].upper()
                ts = self.font.render(lbl, True, COLORS["hud_fg"])
                tr = ts.get_rect(center=dst.center)
                screen.blit(ts, tr)

            col += 1
            if col >= cols:
                col = 0; row += 1

        # --- BOTTOM BAR (for current dialog, persistent) ---
        bottom_rect = pygame.Rect(left_w, map_px_h, map_px_w, bottom_h)
        pygame.draw.rect(screen, COLORS["hud_bg"], bottom_rect)
        pygame.draw.rect(screen, (120,120,120), bottom_rect, width=2)

        # current dialog text
        padding = 10
        text_area = pygame.Rect(bottom_rect.x + padding, bottom_rect.y + padding,
                                bottom_rect.width - 2*padding, bottom_rect.height - 2*padding)
        lines = self._wrap_text(self.current_dialog, text_area.width)
        yy = text_area.y
        for line in lines:
            surf = self.font.render(line, True, COLORS["hud_fg"])
            screen.blit(surf, (text_area.x, yy))
            yy += surf.get_height() + 4

        # We intentionally do NOT draw the old toast bubble overlay anymore.