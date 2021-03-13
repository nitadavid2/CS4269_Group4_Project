import openpyxl as xl

# constants (enter file path names here)

FILE_PATH_WEIGHTS = "./input_files/Resources.xlsx"
FILE_PATH_INITSTATES = "./input_files/countries.xlsx"


# def getResourceDict():
#     # reads in the resource data
#     weightFrame = xl.load_workbook(FILE_PATH_WEIGHTS, data_only=True).active
#
#     resourcesDictionary = dict()
#     for row in weightFrame['A{}:F{}'.format(weightFrame.min_row + 1, weightFrame.max_row)]:
#         resource = row[0].value
#         data_list = list()
#
#         data = row[1:len(row)]
#
#         for cell in data:
#             data_list.append(cell.value)
#
#         resourcesDictionary[resource] = data_list
#
#     return resourcesDictionary

from ResourceQuality import getStateQuality
from Classes import Country

def getCountryDict():
    # reads in the initial country states
    initStates = xl.load_workbook(FILE_PATH_INITSTATES, data_only=True).active
    #resource_dict = getResourceDict()

    countryDictionary = dict()
    # resource_list = []
    resource_list = [i.value for i in initStates[1] if i.value != 'Country']
    # for i in initStates[1]:
    #     if i.value != 'Country':
    #         resource_list.append(i.value)

    for row in initStates['A{}:N{}'.format(initStates.min_row + 1, initStates.max_row)]:
        country = row[0].value
        data_dict = {}

        data = row[1:len(row)]

        for i in range(len(data)):
            data_dict[resource_list[i]] = data[i].value

        # print(data_list)
        init_state_quality = getStateQuality(data_dict)
        countryDictionary[country] = Country(country, data_dict, init_state_quality)

    return countryDictionary

# a = getCountryDict()['Atlantis']
# print(a.init_state_quality)
