from src.errors.ClientError import ClientError

class AuthenticationError(ClientError):
    def __init__(self, message):
        super().__init__(message, 401)
        self.name = 'AuthenticationError'