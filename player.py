from models import DeckModel, DeckCardModel, CardModel, PlayerModel
from factories import RepositoryFactory

player_rep = RepositoryFactory(PlayerModel).create()
card_rep = RepositoryFactory(CardModel).create()
deck_card_rep = RepositoryFactory(DeckCardModel).create()
deck_rep = RepositoryFactory(DeckModel).create()


class Player:
    def __int__(self, client):
        self.client = client
        self.deck = []
        self.table = []

        player = player_rep.get(PlayerModel.account == client.account_id)
        deck = deck_rep.get(DeckModel.id == player.deck)
        deck_cards = deck_card_rep.get_all(DeckCardModel.deck == deck)
        for deck_card in deck_cards:
            card = card_rep.get(CardModel.id == deck_card.card)
            self.deck.append(card)
