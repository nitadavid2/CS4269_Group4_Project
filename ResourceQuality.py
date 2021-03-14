# ResourceQuality.py
# Evaluate the quality of a resource in a given state.

import math
import ReadResources

resourceDict = ReadResources.getResources()

def getStateQuality(country_resource_dict):
    """
    This is the main function that is called to determine the quality of a country's resources in
    a state. This then calls getResourceQuality() on each resource in that country's state.
    :param country_resource_dict: Dictionary of a country's resources.
    :return: The determined state quality value.
    """
    state_quality = 0
    for key in country_resource_dict:
        state_quality += getResourceQuality(key, country_resource_dict)
    return state_quality


def getResourceQuality(resource, country_resource_dict):
    """
    This determines the quality of a given resource for a country. This determines what type
    of resource is being referenced, obtains (and scales if needed) the resource quantity,
    and then calls the appropriate helper function.
    :param resource: The name of the resource being analyzed.
    :param country_resource_dict: Dictionary of a country's resources.
    :return: The quality value of a given resource in a state for a country.
    """
    # Look up the resource in the dictionary of resources.
    # weight, model, scaling, t1, t2
    data = resourceDict[resource]

    weight = data[0]
    model = data[1]
    scaling = data[2]
    t1 = data[3]
    t2 = data[4]

    # Extract quantity of resource by referencing dictionary of country's resources.
    true_quantity = country_resource_dict[resource]

    # Apply scaling, if applicable and possible
    if scaling is not None:
        # Extract the quantity of scaling resource from country's dictionary of resources.
        scale = country_resource_dict[scaling]

        # Only divide by scaling amount if amount is > 1
        if scale > 1:
            true_quantity = true_quantity / scale

    # Determine what type of model to call, what quantity to pass, and what thresholds/weights to use.
    if model == "rawMaterialModel":
        return rawMaterialsModel(true_quantity, weight, t1, t2)
    elif model == "producedMaterialModel":
        return producedMaterialModel(true_quantity, weight, t1, t2)
    elif model == "wasteModel":
        return wasteModel(true_quantity, weight, t1)
    else:
        # Default return value
        return -1


def rawMaterialsModel(quantity, weight, t1, t2):
    """
    This implements the state quality for raw materials.
    :param quantity: the amount of the resource, scaled if appropriate
    :param weight: the weight value assigned to the resource
    :param t1: the threshold of necessity. Below this amount, additional resources are not that valuable since we don't
    have enough to even do basic transforms. Above this amount, the extra can be exported. This is modeled as a linear
    curve with a slightly steeper slope than below t1.
    :param t2: the threshold of saturation. Above this amount, the market for the resource is saturated so additional
    resources are not that beneficial.
    :return: The quality of the raw resource.
    """
    x0 = min(max(0, quantity), t1)
    x1 = min(max(0, quantity - t1), t2 - t1)
    x2 = max(0, quantity - t2)

    return weight * (0.5 * x0 + 1 * x1 + math.log1p(x2))


def producedMaterialModel(quantity, weight, t1, t2):
    """
    This implements the state quality for produced materials.
    :param quantity: the amount of the resource, scaled if appropriate
    :param weight: the weight value assigned to the resource
    :param t1: the threshold of necessity. Below this amount, additional resources are exponentially valuable since
    the closer to everyone meeting their need, the better the value of each incremental resource is. Above this,
    the growth is linear as demand is met and extra can be exported or sold.
    :param t2: the threshold of saturation. Above this amount, the market for the resource is saturated so additional
    resources are not that beneficial.
    :return: The quality of the produced resource.
    """
    x0 = min(max(0, quantity), t1)
    x1 = min(max(0, quantity - t1), t2 - t1)
    x2 = max(0, quantity - t2)

    return weight * (math.pow(x0, 0.25) + 1 * x1 + math.log1p(x2))


def wasteModel(quantity, weight, t1):
    """
    This implements the state quality for wastes.
    :param quantity: the amount of waste, scaled if appropriate
    :param weight: the weight value assigned to the weight (negative)
    :param t1: the threshold of saturation. Below this, we model the waste as linearly problematic since it can be
    disposed of easily within a country (in a lanfill for example). Once t1 is met, the landfills are full and waste
    must be exported for a higher price. This is modeled as a steeper, linear slope.
    :return: The quality of the waste.
    """
    x0 = min(max(0, quantity), t1)
    x1 = max(0, quantity - t1)

    return weight * (0.5 * x0 + 1 * x1)
