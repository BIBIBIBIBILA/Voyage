# === File Overview (auto-generated) ===
# Project: USYD Tower Adventure
# File: usyd_adventure_pygame_update2_run/game/engine.py
# Purpose: Core game engine: main loop, state management, drawing and update orchestration.
#
# Key Notes:
# - Core game engine: main loop, state management, drawing and update orchestration.
# - Uses pygame for rendering/input/audio.
# - Defines Game class (game states, loop, event handling).
# - Rendering routines.
# - Update loop / timing.
# - Key/Inventory handling present.
#
# Run instructions:
# - Recommended entry script: main.py (or any file with __main__ guard).
# - Example: `python main.py` from the project root.
#
# This header was auto-generated to help readers navigate the codebase.


import pygame, re, os
from .constants import *
from . import maps
from .level import Level, tokenize_line
from .player import Player
from .state import State
from .ui import UI
from .tileset import TileTextures
from .events import PORTAL_GRAPH, PORTAL_REQUIREMENTS
from .content import SPRITES as SPRITE_CONFIG
from .content import DOOR_SPRITES, DOOR_PADDING, DOOR_BG
from .content import ITEM_SPRITES, ITEM_PADDING
from .content import SPRITES as SPRITE_CONFIG

# ==== Portal Sprite Mapping (auto-loaded from content/portal_sprites.json) ====
try:
    import json as _json, os as _os
    PORTAL_SPRITES  # check if already defined
except NameError:
    PORTAL_SPRITES = {}
try:
    _here = _os.path.dirname(__file__)
    _root = _os.path.dirname(_here)
    _candidates = [
        _os.path.join(_root, "content", "portal_sprites.json"),
        _os.path.join(_here, "content", "portal_sprites.json"),
        _os.path.join(_os.getcwd(), "content", "portal_sprites.json"),
    ]
    for _cfg in _candidates:
        if _os.path.exists(_cfg):
            with open(_cfg, "r", encoding="utf-8") as _f:
                _d = _json.load(_f)
                if isinstance(_d, dict):
                    PORTAL_SPRITES.update(_d)
            break
except Exception as _e:
    print(f"[PORTAL] Failed to load portal_sprites.json: {_e}")
# ============================================================================

SPRITES = dict(SPRITE_CONFIG)
SPRITES.setdefault('d14', 'd14.png')
# --- merge portal sprite mapping into master SPRITES dict ---
for _ptok, _pfname in PORTAL_SPRITES.items():
    SPRITES.setdefault(_ptok, _pfname)
# ----------------------------------------------------------------

class Game:
    def __init__(self):
        pygame.init()
        # robust font pick to avoid missing glyphs
        for fname in ["Microsoft YaHei", "SimHei", "Arial Unicode MS", "Noto Sans CJK SC", "Arial", None]:
            try:
                self.font = pygame.font.SysFont(fname, 20)
                break
            except Exception:
                continue

        self.state = State()
        self.levels = {name: Level(name) for name in maps.levels.keys()}
        # Tile textures per level
        self.tiletex = TileTextures(tile_size=TILE)

        # viewport + sidebar
        self.map_w = max(level.w for level in self.levels.values())
        self.map_h = max(level.h for level in self.levels.values())
        left = LEFT_UI_W
        right = RIGHT_UI_W
        bottom = BOTTOM_UI_H
        self.ui_margins = (left, right, bottom)
        self.screen = pygame.display.set_mode((self.map_w*TILE + left + right, self.map_h*TILE + bottom))
        self.clock = pygame.time.Clock()
        self.ui = UI(self.font)

        
        self.sprites = {}
        self.door_bg = {}
        try:
            assets_dir = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "assets"))

            # 1) start with non-door sprites
            SPRITES = dict(SPRITE_CONFIG)
            # merge portal-sprite mapping
            for _ptok, _pfname in PORTAL_SPRITES.items():
                SPRITES.setdefault(_ptok, _pfname)

            # 2) auto-detect door files like d14.png -> token 'd14'
            try:
                for fname in os.listdir(assets_dir):
                    if not fname.lower().endswith(".png"):
                        continue
                    m = re.match(r"^d(\d+)\.png$", fname, re.I)
                    if m:
                        token = f"d{m.group(1)}"
                        SPRITES[token] = fname
            except Exception as _e:
                print(f"[SPRITE] auto-detect error: {_e}")

            # 3) apply explicit overrides from content.DOOR_SPRITES
            for t, f in DOOR_SPRITES.items():
                SPRITES[t] = f

            # 4) load & scale
            for token, fname in SPRITES.items():
                try:
                    # resolve path (allow absolute/relative)
                    path = fname if ("/" in fname or "\\" in fname or os.path.isabs(fname)) else os.path.join(assets_dir, fname)
                    img = pygame.image.load(path).convert_alpha()

                    # size rule: doors use padding table; others use 2px inset
                    if isinstance(token, str) and len(token) >= 2 and token[0] == 'd' and token[1:].isdigit():
                        pad = DOOR_PADDING.get(token, DOOR_PADDING.get('default', 0))
                        w, h = max(1, TILE - 2*pad), max(1, TILE - 2*pad)
                        img = pygame.transform.scale(img, (w, h))
                        # store bg pref
                        self.door_bg[token] = DOOR_BG.get(token, DOOR_BG.get('default', 'floor'))
                    else:
                        img = pygame.transform.scale(img, (TILE-4, TILE-4))

                    self.sprites[token] = img
                except Exception as _e:
                    print(f"[SPRITE] Loader failed for {token} ({fname}): {_e}")

        except Exception as _e:
            print(f"[SPRITE] assets dir error: {_e}")
        # --- generic sprite loader (robust) ---
        self.sprites = {}
        try:
            assets_dir = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "assets"))
            for token, fname in SPRITES.items():
                try:
                    path = fname if ("/" in fname or "\\" in fname or os.path.isabs(fname)) else os.path.join(assets_dir, fname)
                    img = pygame.image.load(path).convert_alpha()
                    # Scaling rules
                    if token == 'd14':
                        img = pygame.transform.scale(img, (TILE, TILE))
                    elif isinstance(token, str) and len(token) >= 2 and token[0] == 'd' and token[1:].isdigit():
                        img = pygame.transform.scale(img, (TILE, TILE))
                    else:
                        img = pygame.transform.scale(img, (TILE, TILE))
                    self.sprites[token] = img
                except Exception as _e:
                    print(f"[SPRITE] Loader failed for {token} ({fname}): {_e}")
        except Exception as _e:
            print(f"[SPRITE] assets dir error: {_e}")
        # --- generic sprite loader from content.SPRITES ---
        self.sprites = {}
        try:
            assets_dir = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "assets"))
            for token, fname in SPRITES.items():
                try:
                    path = os.path.join(assets_dir, fname)
                    img = pygame.image.load(path).convert_alpha()
                    img = pygame.transform.smoothscale(img, (TILE, TILE))
                    self.sprites[token] = img
                except Exception:
                    pass
        except Exception:
            self.sprites = {}



        # start level
        self.state.level = "plane" if "plane" in self.levels else list(self.levels.keys())[0]
        start = self._find_token(self.state.level, "os") or self._first_floor(self.state.level) or (1, 1)
        self.player = Player(rc=start)
        if self.level.get(start) == "os":
            self.level.set(start, '.')

        self.prev_rc = self.player.rc
        self.once = set()

        # regex for keys on ground
        self._re_key = re.compile(r'^k(\d+)$')

    # ---------- helpers ----------
    def _first_floor(self, level_name):
        lvl = self.levels[level_name]
        for r in range(lvl.h):
            for c in range(lvl.w):
                if lvl.get((r, c)) == '.':
                    return (r, c)
        return None

    def _find_token(self, level_name, token):
        lvl = self.levels[level_name]
        for r in range(lvl.h):
            for c in range(lvl.w):
                if lvl.get((r, c)) == token:
                    return (r, c)
        return None

    @property
    def level(self):
        return self.levels[self.state.level]

    def _reset_customs_d14(self):
        """Reset all d14 doors in customs back to closed state when leaving customs."""
        if "customs" not in maps.levels:
            return
        # parse original blueprint
        blueprint = [tokenize_line(line) for line in maps.levels["customs"]]
        lvl = self.levels.get("customs")
        if not lvl:
            return
        for r in range(min(lvl.h, len(blueprint))):
            row_bp = blueprint[r]
            for c in range(min(lvl.w, len(row_bp))):
                if row_bp[c] == "d14":
                    lvl.raw[r][c] = "d14"

    def _synthesize_at_altar(self):
        """Synthesis at altar (materials NOT consumed; altar persists).
        k6: mw + python + ne(smart_note)
        k0: se + mw
        Prefer k6; then k0; otherwise show missing materials.
        """
        have_wand = self.state.has_item("mw")
        have_py   = self.state.has_item("python")
        have_ne   = self.state.has_item("smart_note") or self.state.has_item("ne")
        have_se   = self.state.has_item("se")

        if have_wand and have_py and have_ne and not self.state.has_item("k6"):
            self.state.add_item("k6")
            self.ui.toast("Synthesis success: k6 created at altar.")
            return True

        if have_wand and have_se and not self.state.has_item("k0"):
            self.state.add_item("k0")
            self.ui.toast("Synthesis success: k0 created at altar.")
            return True

        missing_k6 = []
        if not have_wand: missing_k6.append("mw")
        if not have_py:   missing_k6.append("python")
        if not have_ne:   missing_k6.append("ne")
        if missing_k6:
            self.ui.toast("Altar k6 needs: " + ", ".join(missing_k6))
        else:
            missing_k0 = []
            if not have_wand: missing_k0.append("mw")
            if not have_se:   missing_k0.append("se")
            if missing_k0:
                self.ui.toast("Altar k0 needs: " + ", ".join(missing_k0))
            else:
                self.ui.toast("Altar: nothing to synthesize.")
        return False

    # ---------- main loop ----------
    def run(self):
        running = True
        while running:
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    running = False
                elif ev.type == pygame.KEYDOWN:
                    if ev.key == pygame.K_ESCAPE:
                        running = False
                    elif ev.key in (pygame.K_UP, pygame.K_w):
                        self.prev_rc = self.player.rc
                        res = self.player.try_move(-1, 0, self.level, self.state, self.ui); self._post_move(res)
                    elif ev.key in (pygame.K_DOWN, pygame.K_s):
                        self.prev_rc = self.player.rc
                        res = self.player.try_move(1, 0, self.level, self.state, self.ui); self._post_move(res)
                    elif ev.key in (pygame.K_LEFT, pygame.K_a):
                        self.prev_rc = self.player.rc
                        res = self.player.try_move(0, -1, self.level, self.state, self.ui); self._post_move(res)
                    elif ev.key in (pygame.K_RIGHT, pygame.K_d):
                        self.prev_rc = self.player.rc
                        res = self.player.try_move(0, 1, self.level, self.state, self.ui); self._post_move(res)

            self.draw()
            self.clock.tick(FPS)
        pygame.quit()

    # ---------- movement aftermath ----------
    def _post_move(self, res):
        if not res:
            return
        kind, rc = res
        if kind == 'npc':
            self.handle_npc(rc)
            return
        if kind == 'item_bump':
            tok = self.level.get(rc)
            # Books: one-time knowledge +1; tiles stay
            if tok in ("b1", "b2", "b3", "b4"):
                once = f"book:{self.state.level}:{rc}"
                if once not in self.once:
                    self.once.add(once)
                    self.state.stats["knowledge"] += 1
                    self.ui.toast("Read a book. Get knowledge.(knowledge + 1)")
                else:
                    self.ui.toast("You can't learn more from this book")
                return
            if tok == "al":
                self._synthesize_at_altar()
                return

        if kind == 'move':
            tok = self.level.get(rc)
            # Portals
            if (self.state.level, tok) in PORTAL_GRAPH:
                self._use_portal(tok)
                return
            # Keys on the ground (pickup)
            m = self._re_key.match(tok if isinstance(tok, str) else "")
            if m:
                n = m.group(1)
                if n == "14" and "customs_cleared" not in self.state.flags:
                    # cannot pick k14 before customs cleared
                    self.player.rc = self.prev_rc
                    self.ui.toast("You should finish the customer check first.")
                    return
                self.state.add_item(f"k{n}")
                self.ui.toast(f"Picked key k{n}.")
                self.level.set(rc, '.')
                return
            # Items
            self._handle_item(rc, tok)

    # ---------- items ----------
    def _handle_item(self, rc, tok):
        lvl = self.state.level
        # Passport: +1 to all base stats
        if tok == "ps":
            self.state.add_item("ps")
            self.state.stats["knowledge"] += 1
            self.state.stats["social"] += 1
            self.state.stats["energy"] += 1
            self.ui.toast("Got passport.You are about to start your learning journey. (All stats +1.)")
            self.level.set(rc, '.')
            return

        # Ticket: allowed only after customs cleared (+k0)
        if tok == "tk":
            if "customs_cleared" in self.state.flags:
                self.state.add_item("tk")
                self.state.add_item("k0")
                self.ui.toast("Got ticket (+k0).")
                self.level.set(rc, '.')
            else:
                self.player.rc = self.prev_rc
                self.ui.toast("Finish customer check first.")
            return

        # Bus card
        if tok == "bc":
            self.state.add_item("bc")
            self.ui.toast("Got bus card.")
            self.level.set(rc, '.')
            return

        # Books (fallback safety if map made them passable)
        if tok in ("b1", "b2", "b3", "b4"):
            once = f"book:{lvl}:{rc}"
            if once not in self.once:
                self.once.add(once)
                self.state.stats["knowledge"] += 1
                self.ui.toast("Read a book. Get knowledge.(knowledge + 1)")
            else:
                self.ui.toast("You can't learn more from this book")
            return

        # Smart note: +2 knowledge
        if tok == "ne":
            self.state.stats["knowledge"] += 2
            self.state.add_item("ne")
            self.ui.toast("You get the smart note getting smarter now. (knowledge + 2)")
            self.level.set(rc, '.')
            return

        # Sheet (se)
        if tok == "se":
            self.state.add_item("se")
            self.ui.toast("Picked S1 sheet, you did great at S1..")
            self.level.set(rc, '.')
            return

        # Campus knowledge spot
        if tok == "kn1":
            self.state.stats["knowledge"] += 1
            self.ui.toast("Knowledge +1")
            self.level.set(rc, '.')
            return

        # Lecture tile in engineering
        if tok == "le" and lvl == "engineering":
            self.state.stats["knowledge"] += 1
            self.ui.toast("Attended a lecture. (Knowledge + 1)")
            self.level.set(rc, '.')
            return

        # Rest
        if tok in ("re1", "re2"):
            self.state.stats["energy"] += 1
            self.ui.toast("You rest for a moment. (energy + 1)")
            self.level.set(rc, '.')
            return

        # Coffee
        if tok in ("cf", "cd"):
            self.state.stats["energy"] += 1
            self.ui.toast("Drink a cup of white. (Energy +1)")
            self.level.set(rc, '.')
            return

        # Photos (persist after exchanges)
        if tok == "cp":
            self.state.add_item("cp")
            self.state.stats["energy"] += 1
            self.ui.toast("Got coffee bar photo, feeling the coze atmosphere. (Energy + 1)")
            self.level.set(rc, '.')
            return
        if tok == "hp":
            self.state.add_item("hp")
            self.state.stats["energy"] += 1
            self.ui.toast("Got harbour photo, feeling the breath of art. (Energy + 1)")
            self.level.set(rc, '.')
            return

        # Magic wand
        if tok == "mw":
            if self.state.stats["knowledge"] >= 10 and not self.state.has_item("mw"):
                self.state.add_item("mw")
                self.ui.toast("Got magic wand.")
                self.level.set(rc, '.')
            else:
                self.player.rc = self.prev_rc
                need = "Knowledge≥10" if self.state.stats["knowledge"] < 10 else "already have one"
                self.ui.toast(f"Cannot take magic wand ({need}).")
            return

        # Altar (in case stepped on)
        if tok == "al":
            self._synthesize_at_altar()
            return

    # ---------- portals ----------
    def _use_portal(self, tok):
        # Static requirement gate (e.g., campus->cm needs bc)
        req = PORTAL_REQUIREMENTS.get((self.state.level, tok))
        if req and not self.state.has_item(req):
            self.ui.toast(f"Entry requires {req}.")
            return

        # Dynamic gate: after first disembark from plane, returning to plane from customs via 'ua' requires 'tk'
        if self.state.level == "customs" and tok == "ua":
            if "disembarked" in self.state.flags and not self.state.has_item("tk"):
                self.ui.toast("Need ticket (tk) to board the plane.")
                return

        # Compute destination
        to_level, to_code = PORTAL_GRAPH[(self.state.level, tok)]

        # Mark first disembark (plane -> customs)
        if self.state.level == "plane" and to_level == "customs":
            self.state.flags.add("disembarked")

        # Reset customs doors when leaving customs
        if self.state.level == "customs" and to_level != "customs":
            if hasattr(self, "_reset_customs_d14"):
                self._reset_customs_d14()

                # Locate destination portal tile (optimized via index)
        target = self.levels[to_level]
        dest = None
        if hasattr(target, 'find_one'):
            dest = target.find_one(to_code)
        if not dest:
            # fallback scan
            for r in range(target.h):
                for c in range(target.w):
                    if target.get((r, c)) == to_code:
                        dest = (r, c)
                        break
                if dest:
                    break
        if not dest:
            return

                # Choose spawn adjacent to portal (or portal tile if no floor)
        spawn = None
        if hasattr(target, 'adjacent_floor'):
            spawn = target.adjacent_floor(dest)
        if not spawn:
            for nb in target.neighbors(dest):
                if target.get(nb) == '.':
                    spawn = nb
                    break
        if not spawn:
            spawn = dest

        self.state.level = to_level
        self.player.rc = spawn
        self.ui.toast(f"Entered {to_level}")
    def handle_npc(self, rc):
        lvl = self.state.level
        tok = self.level.get(rc)

        # Customs officer p0
        if lvl == "customs" and tok == "p0":
            if self.state.has_item("ps"):
                if "customs_cleared" not in self.state.flags:
                    self.state.flags.add("customs_cleared")
                    self.ui.toast("Customs checked.")
                else:
                    self.ui.toast("Officer: You're all set.")
            else:
                self.ui.toast("Officer: Need passport (ps).")
            return

        # Airport staff p1: grant se (Energy>=5 & Social>=10), then k14 if se owned
        if lvl == "airport" and tok == "p1":
            if self.state.stats["energy"] >= 5 and self.state.stats["social"] >= 10:
                if not self.state.has_item("se"):
                    self.state.add_item("se")
                    self.ui.toast("Staff: Here is the sheet (se).")
                if self.state.has_item("se") and not self.state.has_item("k14"):
                    self.state.add_item("k14")
                    self.ui.toast("Staff: You can take key k14.")
            else:
                self.ui.toast("Staff: You need Energy ≥ 5 and Social ≥ 10.")
            return

        # Library p9
        if lvl == "library" and tok == "p9":
            if not self.state.has_item("k12"):
                self.state.add_item("k12")
                self.ui.toast("Librarian: This is the Canvas app, it may help you to know which lecture should join..")
            else:
                self.ui.toast("Librarian: Keep studying!")
            return

        # Engineering lecturer p10: +1 knowledge (once)
        if lvl == "engineering" and tok == "p10":
            key = f"lecture_once:{lvl}:{rc}"
            if key not in self.once:
                self.once.add(key)
                self.state.stats["knowledge"] += 1
                self.ui.toast("Lecture: Knowledge +1")
            else:
                self.ui.toast("Lecture: The lecture was done, see you next time.")
            return

        # Lab tutor p11: first talk +1 knowledge (once). Later talks may grant Python.
        if lvl == "lab" and tok == "p11":
            key = f"tutor_once:{lvl}:{rc}"
            if key not in self.once:
                self.once.add(key)
                self.state.stats["knowledge"] += 1
                self.ui.toast("Tutor: You reviewed fundamentals. (Knowledge + 1)")
                return
            if self.state.stats["knowledge"] >= 8 and not self.state.has_item("k11"):
                self.state.add_item("python")
                self.state.add_item("k11")
                self.ui.toast("Tutor: You are smart enough, I'll teach you how to use Python. (Got Python skill).")
            elif self.state.stats["knowledge"] < 8:
                self.ui.toast("Tutor: You need more knowledge before I can teach you Python.")
            else:
                self.ui.toast("Tutor: Keep practicing.")
            return

        # Market staff p12
        if lvl == "market" and tok == "p12":
            key = f"npc_once:{lvl}:{rc}"
            if key not in self.once:
                self.once.add(key)
                self.state.stats["social"] += 1
            if self.state.has_item("hp") and not self.state.has_item("k8"):
                self.state.add_item("k8")
                self.ui.toast("Trader: Thanks for the photo, you are friend now, I'm also a student of sydney university. Here is my address.")
            elif not self.state.has_item("hp"):
                self.ui.toast("Trader: I want to see the beautiful scenery of sydney harbour, but I'm too busy.")
            else:
                self.ui.toast("Trader: Happy to see you again.")
            return

        # Barista p13
        if lvl == "market" and tok == "p13":
            key = f"npc_once:{lvl}:{rc}"
            if key not in self.once:
                self.once.add(key)
                self.state.stats["social"] += 1
            if self.state.has_item("cp") and not self.state.has_item("k13"):
                self.state.add_item("k13")
                self.ui.toast("Barista: Thanks! Here is the ticket for sydney harbour you can have a look now.")
            elif not self.state.has_item("cp"):
                self.ui.toast("Barista: What a nice coffee bar right, could you take a photo of this?")
            else:
                self.ui.toast("Barista: Enjoy!")
            return

        # Generic students: +1 social once
        if isinstance(tok, str) and tok.startswith('p'):
            key = f"npc_once:{lvl}:{rc}"
            if key not in self.once:
                self.once.add(key)
                self.state.stats["social"] += 1
                self.ui.toast("Chatted with student. Social +1")
            else:
                self.ui.toast("Nice to see you again.")
            return

    # ---------- draw ----------
    def draw(self):
        self.screen.fill(COLORS["bg"])
        for r in range(self.level.h):
            for c in range(self.level.w):
                tok = self.level.get((r, c))
                ox, oy = getattr(self, 'ui_margins', (0,0,0))[0], 0
                rect = pygame.Rect(ox + c*TILE, oy + r*TILE, TILE, TILE)
                if tok in WALLS:
                    self.tiletex.blit(self.state.level, "wall", self.screen, rect)
                    continue
                if isinstance(tok, str) and len(tok) >= 2 and tok[0] == 'd' and tok[1:].isdigit():

                    spr = self.sprites.get(tok)

                    if spr is not None:

                        _bg_kind = 'floor'

                        self.tiletex.blit(self.state.level, _bg_kind, self.screen, rect)

                        sr = spr.get_rect()

                        sr.topleft = rect.topleft

                        self.screen.blit(spr, sr)

                        continue

                    pygame.draw.rect(self.screen, COLORS["locked"], rect)

                    lbl = tok[1:]

                    txt = self.font.render(lbl, True, (255, 255, 255))

                    self.screen.blit(txt, (rect.x+6, rect.y+6))

                    continue
                # Portals
                from .events import PORTAL_GRAPH as _PG
                if (self.state.level, tok) in _PG:
                    spr = self.sprites.get(tok)
                    if spr is not None:
                        self.tiletex.blit(self.state.level, "floor", self.screen, rect)
                        sr = spr.get_rect(); sr.center = rect.center
                        self.screen.blit(spr, sr)
                    else:
                        self.tiletex.blit(self.state.level, "floor", self.screen, rect)
                        txt = self.font.render(tok, True, (20, 20, 20))
                        self.screen.blit(txt, (rect.x+4, rect.y+6))
                    continue
                # NPC
                if isinstance(tok, str) and tok.startswith('p') and tok[1:].isdigit():
                    spr = self.sprites.get(tok)
                    if spr is not None:
                        self.tiletex.blit(self.state.level, "floor", self.screen, rect)
                        sr = spr.get_rect(); sr.topleft = rect.topleft
                        self.screen.blit(spr, sr)
                    else:
                        pygame.draw.rect(self.screen, COLORS["npc"], rect)
                        txt = self.font.render("!", True, (20, 20, 20))
                        self.screen.blit(txt, (rect.x + TILE//3, rect.y + TILE//4))
                    continue
                # Keys / items (visible)
                is_key = isinstance(tok, str) and tok.startswith('k') and tok[1:].isdigit()
                visible = is_key or tok in {"ps","tk","bc","ne","se","le","re1","re2","kn1","cf","cd","cp","hp","mw","al"} or tok in self.sprites
                if visible:

                    spr = self.sprites.get(tok)
                    if spr is not None:
                        self.tiletex.blit(self.state.level, "floor", self.screen, rect)
                        sr = spr.get_rect(); sr.center = rect.center
                        self.screen.blit(spr, sr)
                        continue
                    self.tiletex.blit(self.state.level, "floor", self.screen, rect)
                    lbl = "K" if is_key else tok[:2].upper()
                    txt = self.font.render(lbl, True, (20, 20, 20))
                    self.screen.blit(txt, (rect.x+6, rect.y+6))
                    continue
                self.tiletex.blit(self.state.level, "floor", self.screen, rect)
        self.player.draw(self.screen, origin=(getattr(self, 'ui_margins', (0,0,0))[0], 0))
        self.ui.draw_hud(self.screen, self.state, self.level.w, self.level.h, self.sprites, margins=getattr(self, 'ui_margins', (0,0,0)))
        pygame.display.flip()