from .iv import candidates, observation_problem, pokemon_id


def result(valid, message):
    return {"valid": valid, "score": float(valid), "message": message, "details": {}}


def verify_input(value):
    problem = observation_problem(value)
    return result(problem is None, problem or "Observations are valid.")


def verify_output(input_value, output_value, workspace):
    if problem := observation_problem(input_value):
        return result(False, problem)
    if output_value.pokemon != pokemon_id(input_value.pokemon):
        return result(False, "The result must name the requested Pokémon.")
    if output_value.spreads != candidates(input_value):
        return result(False, "The result must contain every matching IV spread and level in order.")
    return result(True, "All matching IV spreads and levels verified.")
