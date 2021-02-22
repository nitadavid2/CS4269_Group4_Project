import pandas as pd
import ReadInFile


class Country:
    def __init__(self, countryName):
        self.resources = dict
        self.name = countryName

    def state_quality(self):
        return 0

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
