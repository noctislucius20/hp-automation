from src.exceptions.ClientError import ClientError

class InvariantError(ClientError):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

