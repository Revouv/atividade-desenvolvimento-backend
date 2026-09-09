class DomainError(Exception):

    status_code: int = 400

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


class NotFoundError(DomainError):

    status_code = 404


class ConflictError(DomainError):

    status_code = 409


class BadRequestError(DomainError):

    status_code = 400
