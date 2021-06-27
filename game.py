import json
from models import *


def set_new_cards(path):
    houses = []
    with open(path, mode="r", encoding="utf-8") as f:
        json_text = f.read()
        cards = json.loads(json_text)
        for card in cards:
            if not houses.__contains__(card["house"]):
                houses.append(card["house"])

            house = HouseModel.select().where(HouseModel.name == card["house"]).exists()
            if not house:
                house = HouseModel(name=card["house"])
                house.save()
            type = TypeModel.select().where(TypeModel.name == card["cardType"]).exists()
            if not type:
                type = TypeModel(name=card["cardType"])
                type.save()

            card_exists = CardModel.select().where(CardModel.uuid == card["id"]).exists()
            if not card_exists:
                new_card = CardModel()

                new_card.uuid = card["id"]
                new_card.name = card["cardTitle"]

                new_card.house = HouseModel.get(name=card["house"])
                new_card.type = TypeModel.get(name=card["cardType"])

                new_card.image = card["frontImage"]

                new_card.amber = card["amber"]

                new_card.hp = card["power"]
                new_card.armor = card["armor"]

                new_card.save()
            else:
                _card = CardModel.get(CardModel.uuid == card["id"])

                _card.uuid = card["id"]
                _card.name = card["cardTitle"]

                _card.house = HouseModel.get(name=card["house"])
                _card.type = TypeModel.get(name=card["cardType"])

                _card.image = card["frontImage"]

                _card.amber = card["amber"]

                _card.hp = card["power"]
                _card.armor = card["armor"]

                _card.save()

    return houses


def set_new_deck(path):
    with open(path, mode="r", encoding="utf-8") as file:
        json_text = file.read()
        deck = json.loads(json_text)["deck"]

        exists = DeckModel.select().where(DeckModel.name == deck["name"]).exists()
        if not exists:
            new_deck = DeckModel()
            new_deck.name = deck["name"]
            new_deck.save()

            house_cards = deck["housesAndCards"]
            for house_card in house_cards:
                house_exists = HouseModel.select().where(HouseModel.name == house_card["house"]).exists()
                if not house_exists:
                    HouseModel(name=house_card["house"]).save()

                house = HouseModel.get(name=house_card["house"])
                DeckHouseModel(deck=new_deck, house=house).save()

                cards = house_card["cards"]
                for card in cards:
                    c = CardModel.get(name=card["cardTitle"])
                    DeckCardModel(deck=new_deck, card=c).save()


if __name__ == "__main__":
    path = "E:\\\\VisualStudio\\C#\\KeyForgeCardsAPI\\KeyForgeCardsAPI\\bin\\Debug\\my_deck.json"
    path2 = "E:\\\\VisualStudio\\C#\\KeyForgeCardsAPI\\KeyForgeCardsAPI\\bin\\Debug\\new_cardsss.json"
    set_new_deck(path)
