from enum import IntEnum, Enum


class Keys(Enum):
    occurrence = 'occurrence'
    tags = 'tags'
    base = 'base'


class Columns(IntEnum):
    word = 0
    occurrence = 1
    tags = 2
    base = 3
