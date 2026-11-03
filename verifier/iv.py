import re
from itertools import product
from math import sqrt

from contract import Encounter, IVInput, IVSpread

from .game_master import MULTIPLIERS, STATS


def pokemon_id(name: str) -> str:
    return re.sub(r"[\s-]+", "_", name.strip().upper())


def observation_problem(value: IVInput) -> str | None:
    if pokemon_id(value.pokemon) not in STATS:
        return "Unknown Pokémon or form. Use its Game Master ID, such as RAICHU_ALOLA."
    if value.cp < 10:
        return "Caught CP must be at least 10."
    if value.hp is not None and value.hp < 10:
        return "Maximum HP must be at least 10."
    if value.trainer_level is not None and not 1 <= value.trainer_level <= 80:
        return "Trainer level must be from 1 to 80."
    if value.stars is not None and not 0 <= value.stars <= 4:
        return "Appraisal must be 0–4, with 4 for the perfect stamp."
    if any(iv is not None and not 0 <= iv <= 15 for iv in (value.attack_iv, value.defense_iv, value.hp_iv)):
        return "Each IV must be from 0 to 15."
    return None


def encounter_bounds(value: IVInput) -> tuple[range, int]:
    trainer = value.trainer_level
    match value.encounter:
        case Encounter.WILD:
            return range(1, min(trainer or 30, 30) + 1), 0
        case Encounter.WEATHER_WILD:
            return range(6, min(trainer or 30, 30) + 6), 4
        case Encounter.EGG:
            if trainer is None:
                return range(1, 21), 10
            level = min(trainer, 20)
            return range(level, level + 1), 10
        case Encounter.RESEARCH:
            return range(15, 16), 10
        case Encounter.RAID:
            return range(20, 21), 10
        case Encounter.WEATHER_RAID:
            return range(25, 26), 10
    raise ValueError(f"Unsupported encounter: {value.encounter}")


def candidates(value: IVInput) -> list[IVSpread]:
    base_attack, base_defense, base_stamina = STATS[pokemon_id(value.pokemon)]
    levels, minimum_iv = encounter_bounds(value)
    ivs = [
        [iv for iv in range(minimum_iv, 16) if observed is None or observed == iv]
        for observed in (value.attack_iv, value.defense_iv, value.hp_iv)
    ]
    spreads = []
    for attack, defense, hp in product(*ivs):
        stars = sum(attack + defense + hp >= threshold for threshold in (23, 30, 37, 45))
        if value.stars is not None and stars != value.stars:
            continue
        stamina = base_stamina + hp
        stat_product = (base_attack + attack) * sqrt(base_defense + defense) * sqrt(stamina)
        matches = []
        for level in levels:
            multiplier = MULTIPLIERS[level - 1]
            cp = max(10, int(stat_product * multiplier**2 / 10))
            max_hp = max(10, int(stamina * multiplier))
            if cp == value.cp and (value.hp is None or value.hp == max_hp):
                matches.append(level)
        if matches:
            spreads.append(IVSpread(attack, defense, hp, matches))
    return spreads
