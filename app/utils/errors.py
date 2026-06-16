class TMDBError(Exception):
    def __init__(self, message: str, status_code: int = 502):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class NotFoundError(Exception):
    def __init__(self, message: str = "Not found"):
        self.message = message
        super().__init__(message)


class ValidationError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)
