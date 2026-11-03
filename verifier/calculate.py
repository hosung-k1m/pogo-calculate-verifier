from .iv import candidates, observation_problem, pokemon_id


def result(valid, message):
    return {"valid": valid, "score": float(valid), "message": message, "details": {}}


def spread_keys(spreads):
    return sorted((spread.attack, spread.defense, spread.hp, sorted(spread.levels)) for spread in spreads)


def verify_submission(input_value, output_value):
    if problem := observation_problem(input_value):
        return result(False, problem)
    if pokemon_id(output_value.pokemon) != pokemon_id(input_value.pokemon):
        return result(False, "The result must name the requested Pokémon.")
    if spread_keys(output_value.spreads) != spread_keys(candidates(input_value)):
        return result(False, "The submission must contain every matching IV spread and level exactly once.")
    return result(True, "All submitted IV spreads and levels verified.")
