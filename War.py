# Determine the Outcome of a war

import ResourceQuality
from numpy.random import default_rng


def war(attacker, defender, state, seed=None):
    a_country = state.countries[attacker]
    d_country = state.countries[defender]

    a_power = war_power(a_country)
    d_power = war_power(d_country)

    # Determine the "winner"
    loc = (a_power - d_power) / d_power  # loc is mean of Normal Distr.
    scale = 1  # scale = std. dev of Normal Distr.

    rng = default_rng(seed)
    val = rng.normal(loc, scale, 1)

    a_winner = val >= 0

    # Handle redistribution of resources
    if a_winner:
        state = distribute_spoils(attacker, defender, state, 0.1)
    else:
        state = distribute_spoils(defender, attacker, state, 0.1)

    return state


def war_power(country):
    c_resources = country.resources
    power = 0

    # Iterate across resources
    for res in c_resources:
        quantity = c_resources[res]
        quality = ResourceQuality.resourceDict[res][0]  # TODO: Point to new column for 'war weight'

        power += quality * quantity

    return power


def distribute_spoils(victor, loser, state, proportion):
    v_country = state.countries[victor]
    l_country = state.countries[loser]

    for res in v_country.resources:
        taking = l_country[res] * proportion

        v_country.resources[res] += taking
        l_country.resources[res] -= taking

    state.countries[victor] = v_country
    state.countries[loser] = l_country

    return state
