# === File Overview (auto-generated) ===
# Project: USYD Tower Adventure
# File: usyd_adventure_pygame_update2_run/game/state.py
# Purpose: Key/Inventory handling present.
#
# Key Notes:
# - Key/Inventory handling present.
# - HUD/stats (Knowledge/Energy/Social).
#
# Run instructions:
# - Recommended entry script: main.py (or any file with __main__ guard).
# - Example: `python main.py` from the project root.
#
# This header was auto-generated to help readers navigate the codebase.


class State:
    def __init__(self):
        self.level = None
        self.stats = {"knowledge": 0, "social": 0, "energy": 0}
        self.inventory = {}
        self.flags = set()

    def add_item(self, name, amt=1):
        self.inventory[name] = self.inventory.get(name, 0) + amt

    def has_item(self, name):
        return self.inventory.get(name, 0) > 0

    def has_key(self, n):
        return self.inventory.get(f"k{n}", 0) > 0

    def consume_item(self, name, amt=1):
        if self.inventory.get(name, 0) >= amt:
            self.inventory[name] -= amt
            if self.inventory[name] <= 0:
                self.inventory.pop(name, None)
            return True
        return False