class ClientError(Exception):
    def __init__(self, message):
        self.statusCode = 400
        self.message = message
        super().__init__(self.message)
