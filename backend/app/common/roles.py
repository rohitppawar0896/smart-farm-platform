from enum import Enum


class TenantRole(str, Enum):
    OWNER = "OWNER"
    ADMIN = "ADMIN"
    VIEWER = "VIEWER"
