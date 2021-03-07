import copy

def return_transform_info(resources, updated_resources, input_resources, output_resources, operator_summary):
    for key in input_resources:
        if updated_resources[key] < input_resources[key]:
            return False, resources
        else:
            updated_resources[key] -= input_resources[key]
    for key in output_resources:
        updated_resources[key] += output_resources[key]
    return operator_summary, updated_resources


def housing_transform(country, resources, n):
    """
    The TRANSFORM operation that we use to generate housing. Our definition of housing
    transformation uses Group 7's idea, which is in the 5th page of their Defining Additional
    Key Transformations slide (presentation on 2/11/2021).
    :param resources: A dictionary containing the amounts of resources in the country
    :param n: Number multiplied to increase the transformation yield
    :return: The resources dictionary after the transformation.
    """
    updated_resources = copy.deepcopy(resources)
    input_resources = {'population': 5 * n, 'metalElements': n, 'timber': 5 * n, 'metalAlloys': 3 * n, 'landArea': 1 * n}
    output_resources = {'population': 5 * n, 'housing': n, 'housingWaste': n}
    operator_summary = ('TRANSFORM', country, input_resources, output_resources)
    return return_transform_info(resources, updated_resources, input_resources, output_resources, operator_summary)


def food_transform(country, resources, n):
    """
    The TRANSFORM operation that we use to generate food. Our definition of food
    transformation also alludes to Group 7's idea, which is in the 5th page of their Defining Additional
    Key Transformations slide (presentation on 2/11/2021). We, however, do not produce a farm intermediate
    resource in our food production.
    :param resources: A dictionary containing the amounts of resources in the country
    :param n: Number multiplied to increase the transformation yield
    :return: The resources dictionary after the transformation.
    """
    updated_resources = resources.copy()
    input_resources = {'population': 4 * n, 'water': 2 * n, 'timber': 3 * n, 'landArea': 1 * n}
    output_resources = {'population': 4 * n, 'food': 12 * n, 'foodWaste': 4 * n, 'landArea': 1 * n}
    operator_summary = ('TRANSFORM', country, input_resources, output_resources)
    return return_transform_info(resources, updated_resources, input_resources, output_resources, operator_summary)


def electronics_transform(country, resources, n):
    """
    The TRANSFORM operation that we use to generate electronics. Our definition of electronics
    transformation uses Group 7's idea, which is in the 4th page of their Defining Additional
    Key Transformations slide (presentation on 2/11/2021).
    :param resources: A dictionary containing the amounts of resources in the country
    :param n: Number multiplied to increase the transformation yield
    :return: The resources dictionary after the transformation.
    """
    updated_resources = copy.deepcopy(resources)
    input_resources = {'population': 3 * n, 'metalElements': 2 * n, 'metalAlloys': 2 * n}
    output_resources = {'population': 3 * n, 'electronics': 2 * n, 'electronicsWaste': 2 * n}
    operator_summary = ('TRANSFORM', country, input_resources, output_resources)
    return return_transform_info(resources, updated_resources, input_resources, output_resources, operator_summary)


def metallicaloys_transform(country, resources, n):
    """
    The TRANSFORM operation that we use to generate metallic alloys. Our definition of metallic alloys
    transformation uses Group 7's idea, which is in the 3rd page of their Defining Additional
    Key Transformations slide (presentation on 2/11/2021).
    :param resources: A dictionary containing the amounts of resources in the country
    :param n: Number multiplied to increase the transformation yield
    :return: The resources dictionary after the transformation.
    """
    updated_resources = copy.deepcopy(resources)
    input_resources = {'population': n, 'metalElements': 2 * n}
    output_resources = {'population': n, 'metalAlloys': n, 'metalAlloysWaste': n}
    operator_summary = ('TRANSFORM', country, input_resources, output_resources)
    return return_transform_info(resources, updated_resources, input_resources, output_resources, operator_summary)


def transform(country, resources, n, transform_type):
    if transform_type == 'housing':
        return housing_transform(country, resources, n)
    if transform_type == 'food':
        return food_transform(country, resources, n)
    if transform_type == 'electronics':
        return electronics_transform(country, resources, n)
    if transform_type == 'metalAlloys':
        return metallicaloys_transform(country, resources, n)


def transfer(sender, receiver, sender_resources, receiver_resources, transfer_resource, amount):
    sender_updated_resources = copy.deepcopy(sender_resources)
    receiver_updated_resources = copy.deepcopy(receiver_resources)
    operator_summary = ('TRANSFER', sender, receiver, {transfer_resource: amount})
    if sender_updated_resources[transfer_resource] < amount:
        return False, sender_resources, receiver_resources
    else:
        receiver_updated_resources[transfer_resource] += amount
        sender_updated_resources[transfer_resource] -= amount
    return operator_summary, sender_updated_resources, receiver_updated_resources

