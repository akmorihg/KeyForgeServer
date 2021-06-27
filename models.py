from random import sample
from peewee import *
from database import BaseModel


def generate_code():
    return ''.join([str(x) for x in sample(range(0, 9), 5)])


class AccountModel(BaseModel):
    id = PrimaryKeyField(column_name="id")
    username = TextField(column_name="username")
    password = TextField(column_name="password")

    class Meta:
        table_name = "accounts"


class HouseModel(BaseModel):
    id = PrimaryKeyField(column_name="id")
    name = TextField(column_name="name")

    class Meta:
        table_name = "houses"


class TypeModel(BaseModel):
    id = PrimaryKeyField(column_name="id")
    name = TextField(column_name="name")

    class Meta:
        table_name = "types"


class TraitModel(BaseModel):
    id = PrimaryKeyField(column_name="id")
    name = TextField(column_name="name")

    class Meta:
        table_name = "traits"


class CardModel(BaseModel):
    id = PrimaryKeyField(column_name="id")
    uuid = UUIDField(column_name="uuid")
    name = TextField(column_name="name")
    hp = IntegerField(column_name="hp")
    armor = IntegerField(column_name="armor")
    effect = TextField(column_name="effect", default="")
    amber = IntegerField(column_name="amber")
    steal = IntegerField(column_name="steal", default=0)
    damage = IntegerField(column_name="damage", default=0)
    add_card = IntegerField(column_name="add_card", default=0)
    image = TextField(column_name="image")
    house = ForeignKeyField(HouseModel)
    type = ForeignKeyField(TypeModel)

    class Meta:
        table_name = "cards"


class CardTraitModel(BaseModel):
    card = ForeignKeyField(CardModel)
    trait = ForeignKeyField(TraitModel)

    class Meta:
        table_name = "card_trait"


class DeckModel(BaseModel):
    id = PrimaryKeyField(column_name="id")
    name = TextField(column_name="name")

    class Meta:
        table_name = "decks"


class DeckCardModel(BaseModel):
    deck = ForeignKeyField(DeckModel)
    card = ForeignKeyField(CardModel)

    class Meta:
        table_name = "deck_card"


class DeckHouseModel(BaseModel):
    deck = ForeignKeyField(DeckModel)
    house = ForeignKeyField(HouseModel)

    class Meta:
        table_name = "deck_house"


class LobbyModel(BaseModel):
    id = PrimaryKeyField(column_name="id")
    code = TextField(column_name="code", default=generate_code())

    class Meta:
        table_name = "lobbies"


class PlayerModel(BaseModel):
    id = PrimaryKeyField(column_name="id")
    account = ForeignKeyField(AccountModel)
    deck = ForeignKeyField(DeckModel, null=True)

    class Meta:
        table_name = "players"


class LobbyPlayerModel(BaseModel):
    lobby = ForeignKeyField(LobbyModel)
    first_player = ForeignKeyField(PlayerModel, null=True)
    second_player = ForeignKeyField(PlayerModel, null=True)
    is_active = BooleanField(column_name="is_active", default=True)

    class Meta:
        table_name = "lobby_player"
