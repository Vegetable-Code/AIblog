# Tile encoding
# w1-w9: 一万 to 九万  (characters suit)
# t1-t9: 一筒 to 九筒  (dots/bamboo suit)
# s1-s9: 一条 to 九条  (bamboo suit)
# dong, nan, xi, bei: winds
# zhong, fa, bai: dragons

SUITS = ["w", "t", "s"]
HONORS = ["dong", "nan", "xi", "bei", "zhong", "fa", "bai"]

ALL_TILES = [f"{s}{n}" for s in SUITS for n in range(1, 10)] + HONORS

TILE_DISPLAY = {
    "dong": "东", "nan": "南", "xi": "西", "bei": "北",
    "zhong": "中", "fa": "发", "bai": "白",
}
SUIT_NAMES = {"w": "万", "t": "筒", "s": "条"}
NUM_CN = ["一","二","三","四","五","六","七","八","九"]

TILE_ORDER = {}
for s_i, s in enumerate(SUITS):
    for n in range(1, 10):
        TILE_ORDER[f"{s}{n}"] = (s_i, n)
for h_i, h in enumerate(HONORS):
    TILE_ORDER[h] = (3 + h_i // 4, 10 + h_i % 4)

import random
from collections import Counter

def sort_tiles(tiles):
    return sorted(tiles, key=lambda t: TILE_ORDER.get(t, (9, 99)))

def tile_label(tile):
    if tile[0] in SUITS:
        s = tile[0]
        n = int(tile[1])
        return f"{NUM_CN[n-1]}{SUIT_NAMES[s]}"
    return TILE_DISPLAY.get(tile, tile)

def tile_suit(tile):
    if tile in HONORS:
        return "honor"
    return {"w":"wan","t":"tong","s":"tiao"}.get(tile[0], "honor")

def tile_value(tile):
    if tile in HONORS:
        return 0
    return int(tile[1])

def create_deck():
    deck = []
    for tile in ALL_TILES:
        deck.extend([tile] * 4)
    random.shuffle(deck)
    return deck

def check_pung(hand, tile):
    return hand.count(tile) >= 2

def check_kong(hand, tile):
    return hand.count(tile) >= 3

def check_hu(tiles_14):
    """Check if a 14-tile hand is a winning hand."""
    if len(tiles_14) != 14:
        return False

    c = Counter(tiles_14)

    # 7 pairs
    if len(c) == 7 and all(v == 2 for v in c.values()):
        return True
    # 5 pairs + 1 quad = 7 pairs variant
    if all(v in (2, 4) for v in c.values()) and sum(1 for v in c.values() if v == 2) == 5:
        return True

    sorted_hand = sort_tiles(tiles_14)
    for i in range(len(sorted_hand)):
        if i + 1 < len(sorted_hand) and sorted_hand[i] == sorted_hand[i + 1]:
            remaining = sorted_hand[:i] + sorted_hand[i+2:]
            if _can_form_all_sets(remaining):
                return True
    return False

def _can_form_all_sets(tiles):
    if not tiles:
        return True
    if len(tiles) < 3:
        return False

    first = tiles[0]
    # Try pung
    if tiles.count(first) >= 3:
        r = tiles[:]
        for _ in range(3):
            r.remove(first)
        if _can_form_all_sets(r):
            return True

    # Try chow (only for suited tiles)
    if first[0] in SUITS:
        s = first[0]
        v = int(first[1])
        needed = [f"{s}{v}", f"{s}{v+1}", f"{s}{v+2}"]
        if v <= 7 and all(t in tiles for t in needed):
            r = tiles[:]
            for t in needed:
                r.remove(t)
            if _can_form_all_sets(r):
                return True

    return False
