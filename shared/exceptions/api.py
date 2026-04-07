class AppException(Exception):
    """Base application exception."""

    def __init__(self, message: str, error_code: str, status_code: int = 400, details: dict | None = None) -> None:
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.details = details or {}
        super().__init__(message)


class UnauthorizedException(AppException):
    def __init__(self, message: str = "Unauthorized", details: dict | None = None) -> None:
        super().__init__(message=message, error_code="AUTH_401", status_code=401, details=details)


class ForbiddenException(AppException):
    def __init__(self, message: str = "Forbidden", details: dict | None = None) -> None:
        super().__init__(message=message, error_code="AUTHZ_403", status_code=403, details=details)


class NotFoundException(AppException):
    def __init__(self, message: str = "Resource not found", details: dict | None = None) -> None:
        super().__init__(message=message, error_code="COMMON_404", status_code=404, details=details)


class ConflictException(AppException):
    def __init__(self, message: str = "Conflict", details: dict | None = None) -> None:
        super().__init__(message=message, error_code="COMMON_409", status_code=409, details=details)
