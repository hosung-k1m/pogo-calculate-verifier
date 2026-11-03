from pathlib import Path

from contract import IVInput, IVOutput
from verifier.iv import candidates, observation_problem, pokemon_id


def calculate_ivs(value: IVInput, _workspace: Path) -> IVOutput:
    if problem := observation_problem(value):
        raise ValueError(problem)
    return IVOutput(pokemon_id(value.pokemon), candidates(value))
