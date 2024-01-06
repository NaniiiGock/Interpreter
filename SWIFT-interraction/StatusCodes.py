from enum import Enum


class StatusCode(Enum):
    SAFE = 0  # No confirmation needed
    CONFIRM = 1
    ERROR = 7
    RAW_TEXT = 8
