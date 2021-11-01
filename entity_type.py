from enum import Enum

class EntityType(Enum):
    PERSON = 1
    ORG = 2
    LOCATION = 4
    WEB = 8
    EMAIL = 16
    AMOUNT = 32
