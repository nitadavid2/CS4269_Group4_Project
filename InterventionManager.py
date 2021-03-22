# Determine whether an event should happen to a country for a given turn.
# If the event does transpire, modify the state appropriately.


def intervention_manager(country, interventions_list):
    """
    Manage the interventions that may/may not occur to a country during a given turn.
    NOTE: This function relies on a file being read in to populate interventions_list.
    :param country: The country that is to be given (or spared) interventions.
    :param interventions_list: A dictionary of possible interventions.
    TODO: Format details
    :return: The country state after any possible interventions are applied.
    """
    c_resources = country.resources

    for intervention in interventions_list:
        # name, type, base probability, min probability, max probability, scaling formula, impacts
        i_name = intervention[0]
        i_type = intervention[1]
        i_base_prob = intervention[2]
        i_min_prob = intervention[3]
        i_max_prob = intervention[4]
        i_scaling_list = intervention[5]
        i_impacts_list = intervention[6]

        # Now determine if this is a natural or deterministic event
        probability = i_base_prob

        if i_type == "deterministic":
            # TODO: Apply scaling
            probability = probability

        continue  # TODO finish impl.

    return -1  # TODO: replace with final logic
