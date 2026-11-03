# Pokémon GO IV Calculator

A NanoAgent plugin that checks which Attack, Defense and HP individual values
(IVs) and Pokémon levels fit a catch. Try **“Calculate IVs for a 2,387 CP Mewtwo
from a regular raid.”** The one result is **15/15/15 at level 20**.

## Tools

| Tool | Does | Code |
|---|---|---|
| `acknowledge` | Returns a fixed acknowledgement with no catch data | `src/plugin/__main__.py` |

### Tasks

| Task | Does | Runner |
|---|---|---|
| `calculate-ivs` | Returns a verified set of IV spreads and Pokémon levels | `agent` |

Supply the species or form, caught CP, and encounter type. Max HP, trainer level
at acquisition, appraisal stars, and exact appraisal bars are optional. Use 4
stars for the pink perfect stamp. For eggs, use the trainer level when you
received the egg.

| Standard encounter | Pokémon level | Minimum per IV |
|---|---|---:|
| Wild | 1 through min(trainer level, 30) | 0 |
| Weather-boosted wild | 6 through min(trainer level, 30) + 5 | 4 |
| Egg | min(trainer level at acquisition, 20) | 10 |
| Research | 15 | 10 |
| Raid | 20 | 10 |
| Weather-boosted raid | 25 | 10 |

If trainer level is unknown, the calculation covers the full range for the
encounter. Zero results means the observations are inconsistent with those
rules. Supported encounters are fresh, unchanged catches or hatches. Power-ups,
evolution, trades, Shadow or purified Pokémon, Best Buddy boosts, and event
exceptions require separate rules.

## Layout

The agent solves the task from the observations and submits a typed answer.
The plugin spec requires a declared tool, so the agent can also call an
acknowledgement that always returns the same value. The IV enumerator runs
inside the verifier after submission. It checks the species and compares
the submitted spreads and levels with the complete expected set.

The enumerator adds the IVs to the base Attack, Defense and Stamina of the form.
It calculates CP as the floored product of Attack, the square roots of Defense
and Stamina, and the squared Pokémon level multiplier, divided by ten. It
calculates max HP as floored Stamina times the multiplier. Both have a minimum
of ten. Appraisal categories are based on the sum of the three IVs.

Form stats and whole-level multipliers come from the
[pinned PokeMiners Game Master](https://github.com/PokeMiners/game_masters/blob/8e227be44f288d34463e23bf04e9b564d3c16f79/latest/latest.json).
Use a specific form ID when relevant, such as `RAICHU_ALOLA`. The ambiguous
`NIDORAN_NORMAL` ID is excluded. Use `NIDORAN_FEMALE` or `NIDORAN_MALE`.
See also the [official appraisal guide](https://niantic.helpshift.com/hc/en/6-pokemon-go/faq/129-appraising-your-pokemon/).

## Develop and run

```bash
uv sync --frozen --extra dev
uv run --frozen pytest
uv run --frozen ruff check .
nanoagent plugin inspect .
```
