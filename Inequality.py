import ResourceQuality
import math


def mean_log_dev(state):
    """
    The mean_log_dev function analyzes the inequality of a given world state's distribution
    of resources among countries.
    state: the world state to analyze.
    Return: the mean-log deviation (MLD) of the world state.
    """

    total_state_qual = 0
    n_countries = 0
    constant_offset = 0

    for country_name in state.countries:
        country = state.countries[country_name]

        # Call the State Quality Function that we already defined. This calculates state quality
        # according to the Resource weights and thresholds that are pre-defined.
        quality = ResourceQuality.getStateQuality(country.resources)

        # Determine xbar, N, and normalizing constant (to ensure all scores are >= 1 for ln() analysis later.
        total_state_qual += quality
        n_countries += 1

        # Adjust constant offset, if applicable
        if quality < 1:
            if (1 - quality) > constant_offset:
                constant_offset = 1 - quality

    # Now determine the x-bar and N
    xbar = (total_state_qual / n_countries) + constant_offset

    # Now iterate through countries again for final calculation steps
    MLD = 0

    for c_name in state.countries:
        country = state.countries[c_name]

        xi = ResourceQuality.getStateQuality(country.resources) + constant_offset

        MLD += (1 / n_countries) * math.log(xbar / xi, math.e)

    # MLD is now calculated
    return MLD
