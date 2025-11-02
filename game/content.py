# === File Overview (auto-generated) ===
# Project: USYD Tower Adventure
# File: usyd_adventure_pygame_update2_run/game/content.py
# Purpose: Key/Inventory handling present.
#
# Key Notes:
# - Key/Inventory handling present.
# - Door mechanics present.
# - Portal mechanics present.
#
# Run instructions:
# - Recommended entry script: main.py (or any file with __main__ guard).
# - Example: `python main.py` from the project root.
#
# This header was auto-generated to help readers navigate the codebase.

# Clean content definitions

KEY_LABELS = {}
DOOR_LABELS = {}
ITEM_LABELS = {}
NPC_DIALOGS = {}
PORTAL_LABELS = {}

# Token -> icon filename in game/assets/
SPRITES = {
    'grass3':'grass3.png',
    'grass2':'grass2.png',
    'grass1':'grass1.png',
    'p1':       'service.png',
    'p0':       'service.png',
    'k9':       'idcard.png',
    'p2':       'student.png',
    'p3':       'student.png',
    'p4':       'student.png',
    'p5':       'student.png',
    'p6':       'student.png',
    'p7':       'student.png',
    'p8':       'student.png',
    'p9':       'student.png',
    'p12':      'server.png',
    'p13':      'server.png',
    'p10':      'teacher.png',
    'p11':      'teacher.png',
    'ps':       'ps.png',
    'clo':      'clo.png',
    'sky':      'sky.png',
    'wings':    'wings.png',
    'wingLB':   'wingLB.png',
    'wingR' :   'wingR.png',
    'wingsE':   'wingsE.png',
    'wingsL':   'wingsL.png',
    'wingsRE':  'wingsRE.png',
    'k14':      'ticket.png.',
    'tk':       'ticket.png.',
    'bc':       'opal.png',
    'k2':       'k2.png',
    'k3':       'k1.png',
    'k4':       'k1.png',
    'k5':       'k1.png',
    'k6':       'k1.png',
    'k7':       'k1.png',
    'k8':       'k1.png',
    'k10':       'k1.png',
    'k13':      'k1.png',
    'k1':       'k_flower.png',
    'k12':      'canvas.png',
    're1':      'rest1.png',
    're2':      'rest.png',
    'b1':       'book1.png',
    'b2':       'book1.png',
    'b3':       'book1.png',
    'b4':       'book2.png',
    'sea':      'sea.png',
    'sea1':     'sea1.png',
    'hp':       'harbour_photo.png',
    'cp':       'coffee_photo.png',
    'se':       'sheet.png',
    'al':       'magic.png',
    'mw':       'wand.png',
    'cf':       'coffee.png',
    'k11':      'python.png',
    'ne':       'note.png'

}


# --- Door sprite configuration ---
DOOR_SPRITES = {
    'd14':      'd14.png',
    'd0':       'door1.png',
    'd1':       'doorq.png',
    'd2':       'door1.png',
    'd3':       'door1.png',
    'd4':       'door1.png',
    'd5':       'door1.png',
    'd6':       'door1.png',
    'd7':       'door_dorm.png',
    'd8':       'door_dorm.png',
    'd9':       'door_dorm_own.png',
    'd10':      'door1.png',
    'd11':      'doorq.png',
    'd12':      'door1.png',
    'd13':      'door1.png'
}

# Per-door padding (pixels). Size = TILE - 2*padding.
DOOR_PADDING = {
    'default': 0,
    'd14': 0,
}

# Background color for doors when drawing: 'wall' or 'floor'
DOOR_BG = {
    'default': 'floor',
    'd14': 'floor',
}


# --- Item sprite configuration (non-door tokens) ---
# e.g., ITEM_SPRITES = {'ps': 'passport.png', 'tk': 'ticket.png'}
ITEM_SPRITES = {
    # 'ps': 'ps.png',  # example
    # 'tk': 'tk.png',
}

# Per-item padding (pixels). Size = TILE - 2*padding for non-door sprites.
ITEM_PADDING = {
    'default': 2,  # default keep 2px inset (same as TILE-4)
    # 'ps': 1,
    # 'tk': 0,
}