# Determine whether an event should happen to a country for a given turn.
# If the event does transpire, modify the state appropriately.

from ast import literal_eval
import random
import ReadInterventions


def intervention_manager(state, key, interventions_list=ReadInterventions.getInterventions()):
    """
    Manage the interventions that may/may not occur to a country during a given turn.
    NOTE: This function relies on a file being read in to populate interventions_list.
    :param state: The current world state
    :param key: The country that is to be given (or spared) interventions.
    :param interventions_list: A dictionary of possible interventions.
    TODO: Format details
    :return: The country state after any possible interventions are applied.
    """
    country = state.countries[key]
    c_resources = country.resources

    for i_name in interventions_list:
        # name, type, base probability, min probability, max probability, scaling formula, impacts
        intervention = interventions_list.get(i_name)

        i_type = intervention[0]
        i_base_prob = intervention[1]
        i_min_prob = intervention[2]
        i_max_prob = intervention[3]
        i_scaling_list = intervention[4]
        i_impacts_list = intervention[5]

        # Now determine if this is a natural or deterministic event
        probability = i_base_prob

        if i_type == "deterministic":
            # [] syntax to {} in case user forgot to use {} in place of [] in excel file.
            i_scaling_list = str.replace(i_scaling_list, "[", "'{")
            i_scaling_list = str.replace(i_scaling_list, "]", "}'")

            # Convert String in the input file into a Python Dictionary
            scale_dict = literal_eval(i_scaling_list)

            # Now apply the scaling
            for res in scale_dict:
                scalar = scale_dict[res]

                quantity = c_resources[res]

                incremental_prob = scalar * quantity
                probability += incremental_prob

            probability = max(min(i_max_prob, probability), i_min_prob)
            # print("Probability of disaster (",
            #       i_name,
            #       ") for country (",
            #       country.name,
            #       ") is ",
            #       probability*100,
            #       "%.",
            #       sep='')

        # TODO finish impl.
        r = random.random()

        # Do we apply event?
        if r <= probability:
            print("Event Occurs: ", i_name)

            # Get impacts
            # [] syntax to {} in case user forgot to use {} in place of [] in excel file.
            i_impacts_list = str.replace(i_impacts_list, "[", "'{")
            i_impacts_list = str.replace(i_impacts_list, "]", "}'")

            # Convert String in the input file into a Python Dictionary
            impact_dict = literal_eval(i_impacts_list)

            for impact in impact_dict:
                country.resources[impact] += country.resources[impact] * impact_dict[impact]

            state.countries[key] = country

            return state

    return state  # TODO: replace with final logic
