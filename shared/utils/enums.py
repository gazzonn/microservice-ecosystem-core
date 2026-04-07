from enum import Enum


class UserStatus(str, Enum):
    ACTIVE = "ACTIVE"
    BLOCKED = "BLOCKED"
    DISABLED = "DISABLED"


class TokenType(str, Enum):
    ACCESS = "ACCESS"
    REFRESH = "REFRESH"


class ServiceStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    UNAVAILABLE = "UNAVAILABLE"


class RoleName(str, Enum):
    ADMIN = "ADMIN"
    USER = "USER"
    SERVICE = "SERVICE"
