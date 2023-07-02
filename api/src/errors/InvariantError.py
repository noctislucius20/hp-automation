from src.errors.ClientError import ClientError

class InvariantError(ClientError):
    def __init__(self, message):
        self.name = 'InvariantError'
        super().__init__(message)

