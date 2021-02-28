# Evaluate the quality of a resource given some quantity of the resource.
import math


def getResourceQuality(resource, raw_quantity, country, resourceDict):
    # Look up the resource in the dictionary of resources.
    # weight, model, scaling, t1, t2
    data = resourceDict[resource]

    weight = data[0]
    model = data[1]
    scaling = data[2]
    t1 = data[3]
    t2 = data[4]

    # Apply scaling, if applicable
    true_quantity = raw_quantity
    # TODO: Finish this

    # Determine what type of model to call, what quantity to pass, and what thresholds/weights to use.
    if model == "rawMaterialModel":
        return rawMaterialsModel(true_quantity, weight, t1, t2)
    elif model == "producedMaterialModel":
        return producedMaterialModel(true_quantity, weight, t1, t2)
    elif model == "wasteModel":
        return wasteModel(true_quantity, weight, t1)
    else:
        # Placeholder logic
        return -1


def rawMaterialsModel(quantity, weight, t1, t2):
    x0 = min(max(0, quantity), t1)
    x1 = min(max(0, quantity - t1), t2 - t1)
    x2 = max(0, quantity - t2)

    return weight * (0.5 * x0 + 1 * x1 + math.log(x2))


def producedMaterialModel(quantity, weight, t1, t2):
    x0 = min(max(0, quantity), t1)
    x1 = min(max(0, quantity - t1), t2 - t1)
    x2 = max(0, quantity - t2)

    return weight * (math.pow(x0, 0.25) + 1 * x1 + math.log(x2))


def wasteModel(quantity, weight, t1):
    x0 = min(max(0, quantity), t1)
    x1 = max(0, quantity - t1)

    return weight * (0.5 * x0 + 1 * x1)
