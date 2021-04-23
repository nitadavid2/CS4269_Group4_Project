import openpyxl as xl
import Parameters

FILE_PATH_WEIGHTS = Parameters.initial_resource_filename


def getResources():
    """
    Read resources information from Resources.xlsx file and pass in all the information to a dictionary.
    :return A dictionary containing information (weights, type, etc.) of each resource
    """
    weightFrame = xl.load_workbook(FILE_PATH_WEIGHTS, data_only=True).active

    resourceDict = dict()
    for row in weightFrame['A{}:J{}'.format(weightFrame.min_row + 1, weightFrame.max_row)]:
        resource = row[0].value
        data_list = list()

        data = row[1:len(row)]

        for cell in data:
            data_list.append(cell.value)

        resourceDict[resource] = data_list

    return resourceDict
