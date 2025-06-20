from enum import Enum, auto
from typing import List
import textwrap

"""
mechanics to consider...
anger - add a copy of this card
armaments - upgrade a card in your hand
body slam - deal damage equal to your block
clash - can only be played if every card in your hand is an attack
sword boomerang - deal 3 damage to a random enemy 3 times
wild strike - deal 12 damage, shuffle a wound into your draw pile
blood for blood - costs 1 less for each time you lose hp
searing blow - can be upgraded any number of times
sever soul - exhaust all non-attack cards in your hand
feed - if fatal, raise your max hp by 3
forethought - put a card from your hand to the bottom of your draw pile, costs 0 until player

NOTES:
* AOE damage is stil considered sequential in the action queue, i.e. if there are 3 enemies, 3 Damage actions will be enqueued. Important if each enemy has thorns, so each tick of damage must be separate.
* 
"""


class CardType(Enum):
    ATTACK = auto()
    SKILL = auto()
    POWER = auto()
    STATUS = auto()
    CURSE = auto()


class CardRarity(Enum):
    BASIC = auto()
    COMMON = auto()
    UNCOMMON = auto()
    RARE = auto()
    SPECIAL = auto()


class CardCategory(Enum):
    IRONCLAD = auto()
    SILENT = auto()
    DEFECT = auto()
    WATCHER = auto()
    COLORLESS = auto()


class Card:
    def __init__(
        self,
        name,
        description,
        cost,  # -1 if cost is X cost
        type: CardType,
        rarity: CardRarity,
        category: CardCategory,
        targeted: bool,  # used to prompt the user to select target
    ):
        self.name = name
        self.description = description
        self.cost = cost
        self.type = type
        self.rarity = rarity
        self.category = category
        self.targeted = targeted

        self.upgraded = False
        self.exhaust = False
        self.retain = False
        self.ethereal = False

    def get_card_info_string(self):
        return "{} ({}) | Cost: {} | Type: {}".format(
            self.name,
            self.description,
            self.cost,
            self.type.name,
        )

    def play_card(self, target, battle):
        raise NotImplementedError("Each card must define its play behavior.")

    def upgrade(self):
        """Upgrade the card's effects or stats."""
        self.upgraded = True
        # Implement upgrade logic in subclass or override this

    def make_copy(self):
        """Return a new instance of the same card (e.g., for cloning)."""
        return (
            self.__class__()
        )  # Assuming each card can be initialized without args or has its own override

    def is_playable(self, battle):
        """Check if the card can be played (enough energy, etc)."""
        return battle.player.energy >= self.cost

    def __str__(self):
        return f"{self.name} ({self.type.name}) - Cost: {self.cost}"


def build_card_table(title, cards: List[Card], col_widths=(22, 6, 9, 45)):
    name_w, cost_w, type_w, desc_w = col_widths

    def pad(s, width):
        return s.ljust(width)

    def draw_line(char="-"):
        return "+" + "+".join([char * w for w in col_widths]) + "+"

    def format_row(name, cost, typ, desc):
        wrapped_desc = textwrap.wrap(desc, desc_w)
        lines = max(1, len(wrapped_desc))
        rows = []
        for i in range(lines):
            row = "|"
            row += pad(f" {name}" if i == 0 else "", name_w) + "|"
            row += pad(f" {str(cost)}" if i == 0 else "", cost_w) + "|"
            row += pad(f" {typ}" if i == 0 else "", type_w) + "|"
            row += pad(f" {wrapped_desc[i]}", desc_w) + "|"
            rows.append(row)
        return rows

    output = []
    output.append("+" + "-" * (sum(col_widths) + 3) + "+")
    output.append("|" + title.center(sum(col_widths) + 3) + "|")
    output.append(draw_line("="))
    output.append(
        "|"
        + pad(" NAME", name_w)
        + "|"
        + pad(" COST", cost_w)
        + "|"
        + pad(" TYPE", type_w)
        + "|"
        + pad(" DESCRIPTION", desc_w)
        + "|"
    )
    output.append(draw_line("="))

    for card in cards:
        output.extend(
            format_row(card.name, card.cost, card.type.name, card.description)
        )

    output.append(draw_line("-"))
    return output
