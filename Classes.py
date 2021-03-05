import pandas as pd
import ReadInFile
import ResourceQuality


class Country:
    def __init__(self, countryName):
        self.name = countryName
        self.resources = ReadInFile.getCountryDict()[self.name]

    def state_quality(self):
        resource_dict = ReadInFile.getResourceDict()
        return ResourceQuality.getStateQuality(self.resources, resource_dict)

    def readCountryResource(self):
        self.resources

    def calc_rawutility(self):
        return 0


class State:
    def __init__(self, depth, countries, schedule):
        self.countries = countries
        self.depth = depth
        self.path = schedule

    def findSuccessor(self, actions):
        return 0

    def discounted_reward(self,country):
        return 0

Atlantis = Country('Atlantis')
print(Atlantis.state_quality())