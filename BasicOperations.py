def housing_transform(resources, n):
    """
    The TRANSFORM operation that we use to generate housing. Our definition of housing
    transformation uses Group 7's idea, which is in the 5th page of their Defining Additional
    Key Transformations slide (presentation on 2/11/2021).
    :param resources: A dictionary containing the amounts of resources in the country
    :param n: Number multiplied to increase the transformation yield
    :return: The resources dictionary after the transformation.
    """
    if resources['population'] >= 5 * n and resources['metallic elements'] >= 1 * n and \
            resources['timber'] >= 5 * n and resources['metallic alloys'] >= 3 * n:
        resources['population'] -= 5 * n
        resources['metallic elements'] -= 1 * n
        resources['timber'] -= 5 * n
        resources['metallic alloys'] -= 3 * n
        resources['housing'] += 1 * n
        resources['housing wastes'] += 1 * n
    return resources


def food_transform(resources):
    return resources


def electronics_transform(resources, n):
    """
    The TRANSFORM operation that we use to generate electronics. Our definition of electronics
    transformation uses Group 7's idea, which is in the 4th page of their Defining Additional
    Key Transformations slide (presentation on 2/11/2021).
    :param resources: A dictionary containing the amounts of resources in the country
    :param n: Number multiplied to increase the transformation yield
    :return: The resources dictionary after the transformation.
    """
    if resources['population'] >= 3 * n and resources['metallic elements'] >= 2 * n and \
            resources['metallic alloys'] >= 2 * n:
        resources['population'] -= 3 * n
        resources['metallic elements'] -= 2 * n
        resources['metallic alloys'] -= 2 * n
        resources['electronics'] += 2 * n
        resources['electronic wastes'] += 2 * n
    return resources


def metallicaloys_transform(resources, n):
    """
    The TRANSFORM operation that we use to generate metallic alloys. Our definition of metallic alloys
    transformation uses Group 7's idea, which is in the 3rd page of their Defining Additional
    Key Transformations slide (presentation on 2/11/2021).
    :param resources: A dictionary containing the amounts of resources in the country
    :param n: Number multiplied to increase the transformation yield
    :return: The resources dictionary after the transformation.
    """
    if resources['population'] >= 1 * n and resources['metallic elements'] >= 2 * n:
        resources['population'] -= 1 * n
        resources['metallic elements'] -= 2 * n
        resources['metallic alloys'] += 1 * n
        resources['metallic alloy wastes'] += 1 * n
    return resources


def transfer(sender_resources, receiver_resources, amount, resource_name):
    if sender_resources[resource_name] >= amount:
        receiver_resources['resource_name'] += amount
        sender_resources['resource_name'] -= amount
    return sender_resources, receiver_resources

