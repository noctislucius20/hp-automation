class ClientError(Exception):
    def __init__(self, message, status_code = 400):
        self.status_code = status_code
        self.name = 'ClientError'
        super().__init__(message)
