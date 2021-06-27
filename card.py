from enum import Enum


class House(Enum):
    NONE = 0,
    BROBNAR = 1,
    DIS = 2,
    LOGOS = 3,
    MARS = 4,
    SANCTUM = 5,
    SAURIAN = 6,
    SHADOWS = 7,
    STAR_ALLIANCE = 8,
    UNTAMED = 9


class CardType(Enum):
    NONE = 0,
    ACTION = 1,
    ARTIFACT = 2,
    CREATURE = 3,
    UPGRADE = 4


class Card:
    def __init__(self, id=0, uuid="", house=None, type=None, hp=0, armor=0, effect="", amber=0, steal=0, damage=0,
                 add_card=0, image="", traits=None):
        self.id = id
        self.uuid = uuid
        self.house = house if house else House.NONE
        self.type = type if type else CardType.NONE
        self.hp = hp
        self.armor = armor
        self.effect = effect
        self.amber = amber
        self.steal = steal
        self.damage = damage
        self.add_card = add_card
        self.image = image
        self.traits = traits if traits else []


class Deck:
    def __init__(self, id=0, name="", cards=None, houses=None):
        self.id = id
        self.name = name
        self.cards = cards if cards else []
        self.houses = houses if houses else []
