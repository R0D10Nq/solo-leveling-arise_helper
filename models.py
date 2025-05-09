from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class Profile:
    name: str = ''
    level: int = 0
    id: str = ''

@dataclass
class Character:
    name: str
    char_class: str
    rank: str
    hp: int = 0
    atk: int = 0
    defense: int = 0
    crit: int = 0

@dataclass
class Artifact:
    name: str
    type: str
    bonus: Dict[str, int] = field(default_factory=dict)
