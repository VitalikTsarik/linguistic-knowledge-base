from enum import IntEnum, Enum


class Keys(Enum):
    occurrence = 'occurrence'
    tag = 'tag'


class Columns(IntEnum):
    word = 0
    occurrence = 1
    tag = 2
