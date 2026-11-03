from dataclasses import replace
from pathlib import Path

from contract import Encounter, IVInput, IVOutput, IVSpread
from verifier import verify_task
from verifier.iv import candidates, observation_problem

WORKSPACE = Path(".")
RAID = IVInput("Mewtwo", Encounter.RAID, 2387, None, None, None, None, None, None)
WILD = IVInput("Magikarp", Encounter.WILD, 10, 1, 10, None, None, None, None)
TASK = "calculate-ivs"


def test_regular_and_weather_boosted_raid():
    assert candidates(RAID) == [IVSpread(15, 15, 15, [20])]
    boosted = replace(RAID, encounter=Encounter.WEATHER_RAID, cp=2984, hp=152, stars=4)
    assert candidates(boosted) == [IVSpread(15, 15, 15, [25])]
    assert candidates(replace(boosted, hp=151)) == []


def test_cp_floor_preserves_all_spreads_and_levels():
    spreads = candidates(replace(WILD, trainer_level=2, hp=None))
    assert len(spreads) == 4096
    assert spreads[0] == IVSpread(0, 0, 0, [1, 2])
    assert spreads[-1] == IVSpread(15, 15, 15, [1])
    assert candidates(replace(WILD, stars=4)) == [IVSpread(15, 15, 15, [1])]


def test_weather_floor_and_egg_acquisition_level():
    boosted = replace(WILD, encounter=Encounter.WEATHER_WILD, cp=30, hp=None)
    spreads = candidates(boosted)
    assert IVSpread(4, 4, 4, [6]) in spreads
    assert all(min(spread.attack, spread.defense, spread.hp) >= 4 and spread.levels == [6] for spread in spreads)
    assert candidates(replace(boosted, attack_iv=3)) == []
    egg = replace(RAID, encounter=Encounter.EGG, trainer_level=19)
    assert candidates(egg) == []
    assert candidates(replace(egg, trainer_level=80)) == [IVSpread(15, 15, 15, [20])]


def test_verifier_rejects_changed_output_and_invalid_input():
    correct = IVOutput("Mewtwo", [IVSpread(15, 15, 15, [20])])
    assert verify_task(TASK, RAID, correct, None, WORKSPACE)["valid"]
    for spreads in ([], [IVSpread(15, 15, 15, [21])], correct.spreads * 2):
        assert not verify_task(TASK, RAID, replace(correct, spreads=spreads), None, WORKSPACE)["valid"]
    assert observation_problem(replace(RAID, pokemon="Nidoran Normal"))
    assert observation_problem(replace(RAID, pokemon="Raichu Alola")) is None
    assert observation_problem(replace(RAID, trainer_level=81))


def test_verifier_scores_the_submission_against_the_reported_cp():
    impossible_raid = replace(RAID, cp=237)
    empty = IVOutput("Mewtwo", [])
    correct = IVOutput("Mewtwo", [IVSpread(15, 15, 15, [20])])
    wrong_iv = IVOutput("Mewtwo", [IVSpread(14, 15, 15, [20])])
    wrong_pokemon = replace(correct, pokemon="Pikachu")
    for observations, submission, expected in (
        (impossible_raid, empty, True),
        (impossible_raid, correct, False),
        (RAID, empty, False),
        (RAID, correct, True),
        (RAID, wrong_iv, False),
        (RAID, wrong_pokemon, False),
    ):
        verdict = verify_task(TASK, observations, submission, None, WORKSPACE)
        assert verdict["valid"] is expected
        assert verdict["score"] == float(expected)


def test_verifier_accepts_complete_submission_in_any_order():
    spreads = candidates(WILD)
    submission = IVOutput("MAGIKARP", list(reversed(spreads)))
    assert verify_task(TASK, WILD, submission, None, WORKSPACE)["valid"]
    assert not verify_task(TASK, WILD, replace(submission, spreads=spreads[:-1]), None, WORKSPACE)["valid"]
