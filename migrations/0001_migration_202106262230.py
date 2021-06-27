# auto-generated snapshot
from peewee import *
import datetime
import peewee


snapshot = Snapshot()


@snapshot.append
class AccountModel(peewee.Model):
    id = PrimaryKeyField(primary_key=True)
    username = TextField()
    password = TextField()
    class Meta:
        table_name = "accounts"


@snapshot.append
class HouseModel(peewee.Model):
    id = PrimaryKeyField(primary_key=True)
    name = TextField()
    class Meta:
        table_name = "houses"


@snapshot.append
class TypeModel(peewee.Model):
    id = PrimaryKeyField(primary_key=True)
    name = TextField()
    class Meta:
        table_name = "types"


@snapshot.append
class CardModel(peewee.Model):
    id = PrimaryKeyField(primary_key=True)
    uuid = UUIDField()
    name = TextField()
    hp = IntegerField()
    armor = IntegerField()
    effect = TextField(default='')
    amber = IntegerField()
    steal = IntegerField(default=0)
    damage = IntegerField(default=0)
    add_card = IntegerField(default=0)
    image = TextField()
    house = snapshot.ForeignKeyField(index=True, model='housemodel')
    type = snapshot.ForeignKeyField(index=True, model='typemodel')
    class Meta:
        table_name = "cards"


@snapshot.append
class TraitModel(peewee.Model):
    id = PrimaryKeyField(primary_key=True)
    name = TextField()
    class Meta:
        table_name = "traits"


@snapshot.append
class CardTraitModel(peewee.Model):
    card = snapshot.ForeignKeyField(index=True, model='cardmodel')
    trait = snapshot.ForeignKeyField(index=True, model='traitmodel')
    class Meta:
        table_name = "card_trait"


@snapshot.append
class DeckModel(peewee.Model):
    id = PrimaryKeyField(primary_key=True)
    name = TextField()
    class Meta:
        table_name = "decks"


@snapshot.append
class DeckCardModel(peewee.Model):
    deck = snapshot.ForeignKeyField(index=True, model='deckmodel')
    card = snapshot.ForeignKeyField(index=True, model='cardmodel')
    class Meta:
        table_name = "deck_card"


@snapshot.append
class DeckHouseModel(peewee.Model):
    deck = snapshot.ForeignKeyField(index=True, model='deckmodel')
    house = snapshot.ForeignKeyField(index=True, model='housemodel')
    class Meta:
        table_name = "deck_house"


@snapshot.append
class LobbyModel(peewee.Model):
    id = PrimaryKeyField(primary_key=True)
    code = TextField(default='16732')
    class Meta:
        table_name = "lobbies"


@snapshot.append
class PlayerModel(peewee.Model):
    id = PrimaryKeyField(primary_key=True)
    account = snapshot.ForeignKeyField(index=True, model='accountmodel')
    deck = snapshot.ForeignKeyField(index=True, model='deckmodel', null=True)
    class Meta:
        table_name = "players"


@snapshot.append
class LobbyPlayerModel(peewee.Model):
    lobby = snapshot.ForeignKeyField(index=True, model='lobbymodel')
    first_player = snapshot.ForeignKeyField(index=True, model='playermodel', null=True)
    second_player = snapshot.ForeignKeyField(index=True, model='playermodel', null=True)
    is_active = BooleanField(default=True)
    class Meta:
        table_name = "lobby_player"


