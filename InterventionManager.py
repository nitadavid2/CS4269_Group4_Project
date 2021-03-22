import ReadInterventions
# Determine whether an event should happen to a country for a given turn.
# If the event does transpire, modify the state appropriately.


def intervention_manager(country, interventions_list = ReadInterventions.getInterventions()):
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
        continue  # TODO finish impl.

    return -1  # TODO: replace with final logic