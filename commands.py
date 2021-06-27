import bcrypt
from builder import *
from models import *
from abc import ABC, abstractmethod
from factories import RepositoryFactory

account_rep = RepositoryFactory(AccountModel).create()
player_rep = RepositoryFactory(PlayerModel).create()
deck_rep = RepositoryFactory(DeckModel).create()
lobby_rep = RepositoryFactory(LobbyModel).create()
lobby_player_rep = RepositoryFactory(LobbyPlayerModel).create()


class Command(ABC):
    def __init__(self, command):
        self.command = command

    def check_command(self, command):
        if self.command == command:
            return True
        return False

    @abstractmethod
    def execute(self, **kwargs):
        pass


class LoginCommand(Command):
    def __init__(self):
        super(LoginCommand, self).__init__("login")

    def check_password(self, password, hash):
        return bcrypt.checkpw(bytes(password, "utf-8"), bytes(hash, "utf-8"))

    def execute(self, **kwargs):
        username = kwargs.get("username")
        password = kwargs.get("password")
        is_exists = account_rep.exists(account_rep.model.username == username)

        if is_exists and username and password:
            account = account_rep.get(account_rep.model.username == username)
            hash = account.password
            if self.check_password(password, hash):
                return ResponseBuilder().add_attribute_status(self.command, StatusCode.OK).\
                    add_attribute("account_id", account.id).build()

            return ResponseBuilder(StatusCode.FAIL).add_attribute_status(self.command, StatusCode.FAIL).\
                add_attribute("cause", "wrong password").build()

        return ResponseBuilder(StatusCode.FAIL).add_attribute_status(self.command, StatusCode.FAIL).\
            add_attribute("cause", "no such user").build()
    
    
class RegisterCommand(Command):
    def __init__(self):
        super(RegisterCommand, self).__init__("register")

    def get_hash_password(self, password):
        return bcrypt.hashpw(bytes(password, "utf-8"), bcrypt.gensalt())

    def execute(self, **kwargs):
        username = kwargs.get("username")
        password = kwargs.get("password")
        is_exists = account_rep.exists(account_rep.model.username == username)

        if not is_exists and username and password:
            hash_password = self.get_hash_password(password)
            new_account = AccountModel(username=username, password=hash_password)
            account_rep.add(new_account)
            new_player = PlayerModel(account=new_account)
            player_rep.add(new_player)

            account = account_rep.get(account_rep.model.username == username)
            return ResponseBuilder().add_attribute_status(self.command, StatusCode.OK).\
                add_attribute("account_id", account.id).build()

        return ResponseBuilder(StatusCode.FAIL).add_attribute_status(self.command, StatusCode.FAIL).\
            add_attribute("cause", "username have already exists").build()


class DeckChooseCommand(Command):
    def __init__(self):
        super(DeckChooseCommand, self).__init__("deck_choose")

    def execute(self, **kwargs):
        account_id = kwargs.get("account_id")
        deck_id = kwargs.get("deck_id")
        is_exists = player_rep.exists(player_rep.model.account == account_id)

        if is_exists and deck_id:
            deck = deck_rep.get(DeckModel.id == deck_id)
            if deck:
                player = player_rep.get(player_rep.model.account == account_id)
                player.deck = deck
                player_rep.update(player)

                return ResponseBuilder().add_attribute_status(self.command, StatusCode.OK).build()

            return ResponseBuilder(StatusCode.FAIL).add_attribute_status(self.command, StatusCode.FAIL).\
                add_attribute("cause", "doesn't such deck").build()

        return ResponseBuilder(StatusCode.FAIL).add_attribute_status(self.command, StatusCode.FAIL).\
            add_attribute("cause", "account doesn't exists")
    

class LobbyJoinCommand(Command):
    def __init__(self):
        super(LobbyJoinCommand, self).__init__("lobby_join")

    def execute(self, **kwargs):
        account_id = kwargs.get("account_id")
        lobby_code = kwargs.get("lobby_code")
        account = account_rep.get(account_rep.model.id == account_id)
        lobby = lobby_rep.get(lobby_rep.model.code == lobby_code)

        if account and lobby:
            player = player_rep.get(player_rep.model.account == account)
            active_lobby = None
            lobbies = lobby_player_rep.get_all(LobbyPlayerModel.lobby == lobby)

            for l in lobbies:
                if l.is_active:
                    active_lobby = l
                    break

            if active_lobby.second_player:
                active_lobby.first_player = player
            elif active_lobby.first_player:
                active_lobby.second_player = player
            else:
                active_lobby.first_player = player

            lobby_player_rep.update(active_lobby)

            return ResponseBuilder().add_attribute_status(self.command, StatusCode.OK).build()

        return ResponseBuilder(StatusCode.FAIL).add_attribute_status(self.command, StatusCode.FAIL).\
            add_attribute("cause", "no such player or lobby").build()


class LobbyCreateCommand(Command):
    def __init__(self):
        super(LobbyCreateCommand, self).__init__("lobby_create")

    def execute(self, **kwargs):
        account_id = kwargs.get("account_id")
        player = player_rep.get(player_rep.model.account == account_id)

        if player:
            lobby_player = lobby_player_rep.get(LobbyPlayerModel.first_player == player or LobbyPlayerModel.second_player == player)
            has_active_lobby = False
            for l in lobby_player:
                if l.is_active:
                    has_active_lobby = True

            if not has_active_lobby:
                new_lobby = LobbyModel()
                lobby_rep.add(new_lobby)
                new_lobby_player = LobbyPlayerModel()
                new_lobby_player.lobby = new_lobby
                new_lobby_player.first_player = player
                lobby_player_rep.add(new_lobby_player)
                return ResponseBuilder().add_attribute_status(self.command, StatusCode.OK).build()
            else:
                return ResponseBuilder(StatusCode.FAIL).add_attribute_status(self.command, StatusCode.FAIL).\
                    add_attribute("cause", "player has active lobbies").build()

        return ResponseBuilder(StatusCode.FAIL).add_attribute_status(self.command, StatusCode.FAIL).\
            add_attribute("cause", "no such player").build()


class LobbyExitCommand(Command):
    def __init__(self):
        super(LobbyExitCommand, self).__init__("lobby_exit")

    def execute(self, **kwargs):
        account_id = kwargs.get("account_id")
        lobby_id = kwargs.get("lobby_id")
        account = account_rep.get(account_rep.model.id == account_id)
        lobby = lobby_rep.get(lobby_rep.model.id == lobby_id)

        if account and lobby:
            player = player_rep.get(player_rep.model.account == account)
            active_lobby = None
            lobbies = lobby_player_rep.get_all(LobbyPlayerModel.lobby == lobby)

            for l in lobbies:
                if l.is_active:
                    active_lobby = l
                    break

            if active_lobby.first_player == player:
                active_lobby.first_player = None
            elif active_lobby.second_player == player:
                active_lobby.second_player = None

            lobby_player_rep.update(active_lobby)

            return ResponseBuilder().add_attribute_status(self.command, StatusCode.OK).build()

        return ResponseBuilder(StatusCode.FAIL).add_attribute_status(self.command, StatusCode.FAIL). \
            add_attribute("cause", "no such player or lobby").build()


if __name__ == "__main__":
    c = DeckChooseCommand()
    data = {"deck_id": "1", "account_id": "1"}
    print(c.execute(**data))
