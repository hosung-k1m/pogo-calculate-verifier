from dataclasses import dataclass
from enum import Enum
from typing import Annotated

from slimconfig import Output


class Tool(Enum):
    CALCULATE_IVS = "calculate_ivs"


class Task(Enum):
    CALCULATE_IVS = "calculate-ivs"


class Encounter(Enum):
    WILD = "wild"
    WEATHER_WILD = "weather-wild"
    EGG = "egg"
    RESEARCH = "research"
    RAID = "raid"
    WEATHER_RAID = "weather-raid"


@dataclass
class IVInput(Output):
    pokemon: Annotated[str, "Species or Game Master form ID, for example Pikachu or RAICHU_ALOLA"]
    encounter: Annotated[Encounter, "Standard encounter for an unchanged Pokémon"]
    cp: Annotated[int, "Caught Pokémon CP"]
    trainer_level: Annotated[int | None, "Trainer level at capture or egg acquisition, or null"]
    hp: Annotated[int | None, "Maximum HP, or null"]
    stars: Annotated[int | None, "Appraisal stars, with 4 for the pink perfect stamp, or null"]
    attack_iv: Annotated[int | None, "Exact Attack IV from 0 to 15, or null"]
    defense_iv: Annotated[int | None, "Exact Defense IV from 0 to 15, or null"]
    hp_iv: Annotated[int | None, "Exact HP IV from 0 to 15, or null"]


@dataclass
class IVSpread(Output):
    attack: int
    defense: int
    hp: int
    levels: list[int]


@dataclass
class IVOutput(Output):
    pokemon: str
    spreads: Annotated[list[IVSpread], "Every compatible IV spread and all its possible Pokémon levels"]


TOOLS = {Tool.CALCULATE_IVS: (IVInput, IVOutput)}
TASKS = {Task.CALCULATE_IVS: TOOLS[Tool.CALCULATE_IVS]}
