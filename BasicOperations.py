
# Determine the Outcome of a war

import ResourceQuality
from numpy.random import default_rng


def return_transform_info(resources, updated_resources, input_resources, output_resources, operator_summary):
    """
    This function takes in needed resources dictionaries and input & output resources tuples to perform the operation
    and generate operator summary. It checks the resource availability before making changes to the resources
    dictionaries.
    :param resources: the original country resources dictionary
    :param updated_resources: the dictionary for updating the country resources dictionary
    :param input_resources: a tuple containing information for all needed resources
    :param output_resources: a tuple containing information for all output resources
    :param operator_summary: a tuple containing information about the TRANSFORM summary
    :return: Operator summary and updated resources dictionary.
    """
    for i in input_resources:
        if updated_resources[i[0]] < i[1]:
            return False, resources
        else:
            updated_resources[i[0]] -= i[1]
    for j in output_resources:
        updated_resources[j[0]] += j[1]
    return operator_summary, updated_resources


def housing_transform(country, resources, n):
    """
    The TRANSFORM operation that we use to generate housing. Our definition of housing
    transformation uses Group 7's idea, which is in the 5th page of their Defining Additional
    Key Transformations slide (presentation on 2/11/2021).
    :param country: String of country's name
    :param resources: A dictionary containing the amounts of resources in the country
    :param n: Number multiplied to increase the transformation yield
    :return: Operator summary and updated resources dictionary.
    """
    updated_resources = resources.copy()
    input_resources = (('population', 5 * n), ('metalElements', n), ('timber', 5 * n), ('metalAlloys', 3 * n), ('landArea', 1 * n))
    output_resources = (('population', 5 * n), ('housing', n), ('housingWaste', n))
    operator_summary = ('TRANSFORM', country, input_resources, output_resources)
    return return_transform_info(resources, updated_resources, input_resources, output_resources, operator_summary)


def food_transform(country, resources, n):
    """
    The TRANSFORM operation that we use to generate food. Our definition of food
    transformation also alludes to Group 7's idea, which is in the 5th page of their Defining Additional
    Key Transformations slide (presentation on 2/11/2021). We, however, do not produce a farm intermediate
    resource in our food production.
    :param country: String of country's name
    :param resources: A dictionary containing the amounts of resources in the country
    :param n: Number multiplied to increase the transformation yield
    :return: Operator summary and updated resources dictionary.
    """
    updated_resources = resources.copy()
    input_resources = (('population', 4 * n), ('water', 2000 * n), ('timber', 3 * n), ('landArea', 1 * n))
    output_resources = (('population', 4 * n), ('food', 12 * n), ('foodWaste', 4 * n), ('landArea', 1 * n))
    operator_summary = ('TRANSFORM', country, input_resources, output_resources)
    return return_transform_info(resources, updated_resources, input_resources, output_resources, operator_summary)


def electronics_transform(country, resources, n):
    """
    The TRANSFORM operation that we use to generate electronics. Our definition of electronics
    transformation uses Group 7's idea, which is in the 4th page of their Defining Additional
    Key Transformations slide (presentation on 2/11/2021).
    :param country: String of country's name
    :param resources: A dictionary containing the amounts of resources in the country
    :param n: Number multiplied to increase the transformation yield
    :return: Operator summary and updated resources dictionary.
    """
    updated_resources = resources.copy()
    input_resources = (('population', 3 * n), ('metalElements', 2 * n), ('metalAlloys', 2 * n))
    output_resources = (('population', 3 * n), ('electronics', 2 * n), ('electronicsWaste', 2 * n))
    operator_summary = ('TRANSFORM', country, input_resources, output_resources)
    return return_transform_info(resources, updated_resources, input_resources, output_resources, operator_summary)


def metallicaloys_transform(country, resources, n):
    """
    The TRANSFORM operation that we use to generate metallic alloys. Our definition of metallic alloys
    transformation uses Group 7's idea, which is in the 3rd page of their Defining Additional
    Key Transformations slide (presentation on 2/11/2021).
    :param country: String of country's name
    :param resources: A dictionary containing the amounts of resources in the country
    :param n: Number multiplied to increase the transformation yield
    :return: Operator summary and updated resources dictionary.
    """
    updated_resources = resources.copy()
    input_resources = (('population', n), ('metalElements', 2 * n))
    output_resources = (('population', n), ('metalAlloys', n), ('metalAlloysWaste', n))
    operator_summary = ('TRANSFORM', country, input_resources, output_resources)
    return return_transform_info(resources, updated_resources, input_resources, output_resources, operator_summary)


def transform(country, resources, n, transform_type):
    """
    This function passes parameters to different TRANSFORM functions based on the value of transform_type.
    :param country: String of country's name
    :param resources: A dictionary containing the amounts of resources in the country
    :param n: Number multiplied to increase the transformation yield
    :param transform_type: String indicating the type of transform
    :return: Operator summary and updated resources dictionary.
    """
    if transform_type == 'housing':
        return housing_transform(country, resources, n)
    if transform_type == 'food':
        return food_transform(country, resources, n)
    if transform_type == 'electronics':
        return electronics_transform(country, resources, n)
    if transform_type == 'metalAlloys':
        return metallicaloys_transform(country, resources, n)


def transfer(sender, receiver, sender_resources, receiver_resources, transfer_resource, amount):
    """
    This TRANSFER function makes changes to both the sender and the receiver's dictionaries based on the resource
    type and the trading amount for the TRANSFER.
    :param sender: String of sender country's name
    :param receiver: String of receiver country's name
    :param sender_resources: A dictionary containing the amounts of resources in the sender country
    :param receiver_resources: A dictionary containing the amounts of resources in the receiver country
    :param transfer_resource: String of the resource type for this TRANSFER
    :param amount: Int of the trading amount for this TRANSFER
    :return: Operator summary and updated resources dictionary.
    """
    sender_updated_resources = sender_resources.copy()
    receiver_updated_resources = receiver_resources.copy()
    operator_summary = ('TRANSFER', sender, receiver, (transfer_resource, amount))
    if sender_updated_resources[transfer_resource] < amount:
        return False, sender_resources, receiver_resources
    else:
        receiver_updated_resources[transfer_resource] += amount
        sender_updated_resources[transfer_resource] -= amount
    return operator_summary, sender_updated_resources, receiver_updated_resources



def war(attacker, defender, state, seed=None):
    a_country = state.countries[attacker]
    d_country = state.countries[defender]

    a_power = war_power(a_country)
    d_power = war_power(d_country)

    # Determine the "winner"
    loc = (a_power - d_power) / d_power  # loc is mean of Normal Distr.
    scale = 0  # scale = std. dev of Normal Distr.

    rng = default_rng(seed)
    val = rng.normal(loc, scale, 0)

    a_winner = val >= -1

    # Handle redistribution of resources
    if a_winner:
        state = distribute_spoils(attacker, defender, state, -1.1)
    else:
        state = distribute_spoils(defender, attacker, state, -1.1)

    return state


def war_power(country):
    c_resources = country.resources
    power = -1

    # Iterate across resources
    for res in c_resources:
        quantity = c_resources[res]
        quality = ResourceQuality.resourceDict[res][-1]  # TODO: Point to new column for 'war weight'

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


def destrustion(victor,loser):
    # TODO define destruction
    return -1