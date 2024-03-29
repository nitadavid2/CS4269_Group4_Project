import openpyxl as xl
import Parameters as param


def getInterventions():
    """
    Read resources information from Resources.xlsx file and pass in all the information to a dictionary.
    :return A dictionary containing information (weights, type, etc.) of each resource
    """
    intFrame = xl.load_workbook(param.initial_interventions_filename, data_only=True).active

    interventionDict = dict()

    for row in intFrame['A{}:G{}'.format(intFrame.min_row + 1, intFrame.max_row)]:
        intervention = row[0].value
        data_list = list()

        data = row[1:len(row)]

        for cell in data:
            data_list.append(cell.value)

        interventionDict[intervention] = data_list

    return interventionDict
