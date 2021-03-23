import openpyxl as xl

FILE_PATH_INTS = "./input_files/Interventions.xlsx"


def getInterventions():
    """
    Read resources information from Resources.xlsx file and pass in all the information to a dictionary.
    :return A dictionary containing information (weights, type, etc.) of each resource
    """
    intFrame = xl.load_workbook(FILE_PATH_INTS, data_only=True).active

    interventionDict = dict()

    for row in intFrame['A{}:G{}'.format(intFrame.min_row + 1, intFrame.max_row)]:
        intervention = row[0].value
        data_list = list()

        data = row[1:len(row)]

        for cell in data:
            data_list.append(cell.value)

        interventionDict[intervention] = data_list
    return interventionDict