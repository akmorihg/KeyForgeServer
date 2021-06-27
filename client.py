class Client:
    def __init__(self, connection, address):
        self.id = 0
        self.connection = connection
        self.address = address
        self.account_id = 0
        self.player = None
