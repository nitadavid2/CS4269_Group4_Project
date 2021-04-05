import openpyxl as xl
from ResourceQuality import getStateQuality
from Classes import Country

FILE_PATH_INITSTATES = "./input_files/countries.xlsx"


def getCountryDict(FILE_PATH_INITSTATES):
    """
    Read countries information from countries.xlsx file, create country object for every country in the list, and pass
    in all the information to a dictionary.
     :return A dictionary containing all country objects
     """
    initStates = xl.load_workbook(FILE_PATH_INITSTATES, data_only=True).active

    countryDictionary = dict()
    resource_list = [i.value for i in initStates[1] if i.value != 'Country']

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
