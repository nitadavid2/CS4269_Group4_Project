def housing_transform(country, resources, n):
    """
    The TRANSFORM operation that we use to generate housing. Our definition of housing
    transformation uses Group 7's idea, which is in the 5th page of their Defining Additional
    Key Transformations slide (presentation on 2/11/2021).
    :param resources: A dictionary containing the amounts of resources in the country
    :param n: Number multiplied to increase the transformation yield
    :return: The resources dictionary after the transformation.
    """
    updated_resources = resources.copy()
    input_resources = {'population': 5 * n, 'metalElements': n, 'timber': 5 * n, 'metalAlloys': 3 * n}
    output_resources = {'population': 5 * n, 'housing': n, 'housingWaste': n}
    operator_summary = ('TRANSFORM', country, input_resources, output_resources)
    for key in input_resources:
        if updated_resources[key] < input_resources[key]:
            return False, resources
        else:
            updated_resources[key] -= input_resources[key]
    for key in output_resources:
        updated_resources[key] += output_resources[key]
    return operator_summary, updated_resources


def food_transform(resources):
    return resources


def electronics_transform(country, resources, n):
    """
    The TRANSFORM operation that we use to generate electronics. Our definition of electronics
    transformation uses Group 7's idea, which is in the 4th page of their Defining Additional
    Key Transformations slide (presentation on 2/11/2021).
    :param resources: A dictionary containing the amounts of resources in the country
    :param n: Number multiplied to increase the transformation yield
    :return: The resources dictionary after the transformation.
    """
    updated_resources = resources.copy()
    input_resources = {'population': 3 * n, 'metalElements': 2 * n, 'metalAlloys': 2 * n}
    output_resources = {'population': 3 * n, 'electronics': 2 * n, 'electronicsWaste': 2 * n}
    operator_summary = ('TRANSFORM', country, input_resources, output_resources)
    for key in input_resources:
        if updated_resources[key] < input_resources[key]:
            return False, resources
        else:
            updated_resources[key] -= input_resources[key]
    for key in output_resources:
        updated_resources[key] += output_resources[key]
    return operator_summary, updated_resources


def metallicaloys_transform(country, resources, n):
    """
    The TRANSFORM operation that we use to generate metallic alloys. Our definition of metallic alloys
    transformation uses Group 7's idea, which is in the 3rd page of their Defining Additional
    Key Transformations slide (presentation on 2/11/2021).
    :param resources: A dictionary containing the amounts of resources in the country
    :param n: Number multiplied to increase the transformation yield
    :return: The resources dictionary after the transformation.
    """
    updated_resources = resources.copy()
    input_resources = {'population': n, 'metalElements': 2 * n}
    output_resources = {'population': n, 'metalAlloys': n, 'electronicsWaste': n}
    operator_summary = ('TRANSFORM', country, input_resources, output_resources)
    for key in input_resources:
        if updated_resources[key] < input_resources[key]:
            return False, resources
        else:
            updated_resources[key] -= input_resources[key]
    for key in output_resources:
        updated_resources[key] += output_resources[key]
    return operator_summary, updated_resources


def transfer(sender, receiver, sender_resources, receiver_resources, transfer_resources):
    sender_updated_resources = sender_resources.copy()
    receiver_updated_resources = receiver_resources.copy()
    operator_summary = ('TRANSFER', sender, receiver, transfer_resources)
    for key in transfer_resources:
        if sender_updated_resources[key] < transfer_resources[key]:
            return False, sender_resources, receiver_resources
        else:
            receiver_updated_resources[key] += transfer_resources[key]
            sender_updated_resources[key] -= transfer_resources[key]
    return operator_summary, sender_updated_resources, receiver_updated_resources

