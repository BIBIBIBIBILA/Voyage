# === File Overview (auto-generated) ===
# Project: USYD Tower Adventure
# File: usyd_adventure_pygame_update2_run/game/level.py
# Purpose: Module for game logic
#
# Key Notes:
#
# Run instructions:
# - Recommended entry script: main.py (or any file with __main__ guard).
# - Example: `python main.py` from the project root.
#
# This header was auto-generated to help readers navigate the codebase.


from .constants import *
from . import maps
from collections import defaultdict

def tokenize_line(line: str):
    tokens = []
    i = 0
    n = len(line)
    while i < n:
        ch = line[i]
        if ch == '(':
            j = line.find(')', i+1)
            if j == -1:
                tokens.append(FLOOR); i += 1
            else:
                name = line[i+1:j].strip()
                tokens.append(name if name else FLOOR)
                i = j + 1
        else:
            tokens.append(ch)
            i += 1
    return tokens

class Level:
    def __init__(self, name: str):
        self.name = name
        raw_lines = maps.levels[name]
        self.raw = [tokenize_line(line) for line in raw_lines]
        self.h = len(self.raw)
        self.w = max((len(row) for row in self.raw), default=0)
        for r in range(self.h):
            if len(self.raw[r]) < self.w:
                self.raw[r] += [FLOOR] * (self.w - len(self.raw[r]))

        # build token index
        self.index = defaultdict(set)
        for r in range(self.h):
            for c in range(self.w):
                self.index[self.raw[r][c]].add((r, c))

    def in_bounds(self, rc):
        r, c = rc
        return 0 <= r < self.h and 0 <= c < self.w

    def get(self, rc):
        r, c = rc
        if not self.in_bounds(rc):
            return '#'
        return self.raw[r][c]

    def set(self, rc, value):
        r, c = rc
        if not self.in_bounds(rc):
            return
        old = self.raw[r][c]
        if old == value:
            return
        # update index
        try:
            self.index[old].discard((r, c))
        except Exception:
            pass
        self.raw[r][c] = value
        try:
            self.index[value].add((r, c))
        except Exception:
            pass

    def neighbors(self, rc):
        r, c = rc
        return [(r-1, c), (r+1, c), (r, c-1), (r, c+1)]

    def is_wall(self, token):
        return token in WALLS

    def is_door(self, token):
        return isinstance(token, str) and len(token) >= 2 and token[0] == 'd' and token[1:].isdigit()


    def find_one(self, token):
        s = self.index.get(token)
        if not s:
            return None
        # return an arbitrary element
        for rc in s:
            return rc
        return None

    def find_all(self, token):
        return set(self.index.get(token, set()))

    def adjacent_floor(self, rc):
        for nb in self.neighbors(rc):
            if self.get(nb) == FLOOR:
                return nb
        return None