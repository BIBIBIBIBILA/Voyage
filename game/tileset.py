# === File Overview (auto-generated) ===
# Project: USYD Tower Adventure
# File: usyd_adventure_pygame_update2_run/game/tileset.py
# Purpose: Map/tile handling: loading maps, collisions, coordinates, and rendering layers.
#
# Key Notes:
# - Map/tile handling: loading maps, collisions, coordinates, and rendering layers.
# - Uses pygame for rendering/input/audio.
# - Rendering routines.
#
# Run instructions:
# - Recommended entry script: main.py (or any file with __main__ guard).
# - Example: `python main.py` from the project root.
#
# This header was auto-generated to help readers navigate the codebase.


import os, json, pygame

def _default_tiles_dir():
    return os.path.join(os.path.dirname(__file__), "assets", "tiles")

class TileTextures:
    """
    Loads per-level wall/floor textures from assets/tiles/tiles_index.json
    and provides a simple blit interface.
    """
    def __init__(self, tiles_dir=None, tile_size=32):
        self.tiles_dir = tiles_dir or _default_tiles_dir()
        self.tile_size = tile_size
        self.index_path = os.path.join(self.tiles_dir, "tiles_index.json")
        self.index = self._load_index()
        self.cache = {}  # (level, kind) -> Surface

    def _load_index(self):
        try:
            with open(self.index_path, "r", encoding="utf-8") as f:
                idx = json.load(f)
                # ensure 'default' exists
                if "default" not in idx:
                    idx["default"] = {"wall":"default_wall.png", "floor":"default_floor.png"}
                return idx
        except Exception:
            return {"default":{"wall":"default_wall.png","floor":"default_floor.png"}}

    def _load_surface(self, filename):
        path = os.path.join(self.tiles_dir, filename)
        try:
            img = pygame.image.load(path).convert_alpha()
        except Exception:
            # Fallback: solid color surface
            img = pygame.Surface((self.tile_size, self.tile_size))
            img.fill((200,200,200))
        # Scale to tile size if needed
        if img.get_width() != self.tile_size or img.get_height() != self.tile_size:
            img = pygame.transform.smoothscale(img, (self.tile_size, self.tile_size))
        return img

    def get(self, level_name, kind):
        """
        kind in {"wall","floor"}
        """
        key = (level_name, kind)
        if key in self.cache:
            return self.cache[key]
        # pick filename
        mapping = self.index.get(level_name, self.index.get("default", {}))
        fname = mapping.get(kind)
        if not fname:
            # fallback to default kind
            fname = self.index.get("default", {}).get(kind, "")
        surf = self._load_surface(fname) if fname else pygame.Surface((self.tile_size, self.tile_size))
        self.cache[key] = surf
        return surf

    def blit(self, level_name, kind, screen, rect):
        tex = self.get(level_name, kind)
        # We align at tile topleft
        screen.blit(tex, rect.topleft)