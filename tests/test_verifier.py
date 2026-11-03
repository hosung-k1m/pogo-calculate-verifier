from dataclasses import replace
from pathlib import Path

from contract import Encounter, IVInput, IVOutput, IVSpread
from plugin import calculate_ivs
from verifier import verify_input, verify_output, verify_task

WORKSPACE = Path(".")
RAID = IVInput("Mewtwo", Encounter.RAID, 2387, None, None, None, None, None, None)
WILD = IVInput("Magikarp", Encounter.WILD, 10, 1, 10, None, None, None, None)
TOOL = "calculate_ivs"


def test_regular_and_weather_boosted_raid():
    assert calculate_ivs(RAID, WORKSPACE) == IVOutput("MEWTWO", [IVSpread(15, 15, 15, [20])])
    boosted = replace(RAID, encounter=Encounter.WEATHER_RAID, cp=2984, hp=152, stars=4)
    assert calculate_ivs(boosted, WORKSPACE).spreads == [IVSpread(15, 15, 15, [25])]
    assert calculate_ivs(replace(boosted, hp=151), WORKSPACE).spreads == []


def test_cp_floor_preserves_all_spreads_and_levels():
    output = calculate_ivs(replace(WILD, trainer_level=2, hp=None), WORKSPACE)
    assert len(output.spreads) == 4096
    assert output.spreads[0] == IVSpread(0, 0, 0, [1, 2])
    assert output.spreads[-1] == IVSpread(15, 15, 15, [1])
    assert calculate_ivs(replace(WILD, stars=4), WORKSPACE).spreads == [IVSpread(15, 15, 15, [1])]


def test_weather_floor_and_egg_acquisition_level():
    boosted = replace(WILD, encounter=Encounter.WEATHER_WILD, cp=30, hp=None)
    spreads = calculate_ivs(boosted, WORKSPACE).spreads
    assert IVSpread(4, 4, 4, [6]) in spreads
    assert all(min(spread.attack, spread.defense, spread.hp) >= 4 and spread.levels == [6] for spread in spreads)
    assert calculate_ivs(replace(boosted, attack_iv=3), WORKSPACE).spreads == []
    egg = replace(RAID, encounter=Encounter.EGG, trainer_level=19)
    assert calculate_ivs(egg, WORKSPACE).spreads == []
    assert calculate_ivs(replace(egg, trainer_level=80), WORKSPACE).spreads == [IVSpread(15, 15, 15, [20])]


def test_verifier_rejects_changed_output_and_invalid_input():
    output = calculate_ivs(RAID, WORKSPACE)
    assert verify_task("calculate-ivs", RAID, output, None, WORKSPACE)["valid"]
    assert not verify_output(TOOL, RAID, replace(output, spreads=[]), WORKSPACE)["valid"]
    assert not verify_output(TOOL, RAID, replace(output, spreads=[IVSpread(15, 15, 15, [21])]), WORKSPACE)["valid"]
    assert not verify_input(TOOL, replace(RAID, pokemon="Nidoran Normal"))["valid"]
    assert verify_input(TOOL, replace(RAID, pokemon="Raichu Alola"))["valid"]
    assert not verify_input(TOOL, replace(RAID, trainer_level=81))["valid"]
