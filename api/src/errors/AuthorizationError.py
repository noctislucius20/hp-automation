from src.errors.ClientError import ClientError

class AuthorizationError(ClientError):
    def __init__(self, message):
        super().__init__(message, 403)
        self.name = 'AuthorizationError'