# ResourceQuality.py
# Evaluate the quality of a resource in a given state.

import math
import ReadResources

# This is the main dictionary of resources and their weights, thresholds, and other relevant info.
resourceDict = ReadResources.getResources()


# getStateQuality:
# This is the main function that is called to determine the quality of a country's resources in
# a state. This then calls getResourceQuality() on each resource in that country's state.
def getStateQuality(country_resource_dict):
    state_quality = 0
    for key in country_resource_dict:
        state_quality += getResourceQuality(key, country_resource_dict)
    return state_quality


# getResourceQuality:
# This determines the quality of a given resource for a country. This determines what type
# of resource is being referenced, obtains (and scales if needed) the resource quantity,
# and then calls the appropriate helper function.
def getResourceQuality(resource, country_resource_dict):
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


# rawMaterialsModel:
# This implements the state quality for raw materials.
def rawMaterialsModel(quantity, weight, t1, t2):
    x0 = min(max(0, quantity), t1)
    x1 = min(max(0, quantity - t1), t2 - t1)
    x2 = max(0, quantity - t2)

    return weight * (0.5 * x0 + 1 * x1 + math.log1p(x2))


# producedMaterialsModel:
# this implements the state quality for produced materials
def producedMaterialModel(quantity, weight, t1, t2):
    x0 = min(max(0, quantity), t1)
    x1 = min(max(0, quantity - t1), t2 - t1)
    x2 = max(0, quantity - t2)

    return weight * (math.pow(x0, 0.25) + 1 * x1 + math.log1p(x2))


# wasteModel:
# This implements the state quality of waste materials.
def wasteModel(quantity, weight, t1):
    x0 = min(max(0, quantity), t1)
    x1 = max(0, quantity - t1)

    return weight * (0.5 * x0 + 1 * x1)
