import ResourceQuality
import BasicOperations
import copy


class Country:
    def __init__(self, countryName, resources, resource_dict, init_state_quality):
        self.name = countryName
        self.resources = resources
        self.resource_dict = resource_dict
        self.init_state_quality = init_state_quality
        self.discounted_reward = 0
        self.participation_prob = -1

    def state_quality(self):
        return ResourceQuality.getStateQuality(self.resources, self.resource_dict)

    def calc_rawutility(self):
        return 0


class State:
    def __init__(self, depth, countries, schedule):
        self.countries = countries
        self.depth = depth
        self.path = schedule

    def findSuccessor(self):
        def successors_for_transform(path, countries, depth):
            for quantity in quantity_choices:
                for transform_type in transform_types:
                    a, b = BasicOperations.transform(country, resources, quantity, transform_type)
                    if a:
                        path_to_update = copy.deepcopy(path)
                        countries_to_update = copy.deepcopy(countries)
                        path_to_update.append(a)
                        countries_to_update[country].resources = b
                        new_state = State(depth + 1, countries_to_update, path_to_update)
                        new_my_country = new_state.countries[country]
                        new_my_country.discounted_reward = self.discounted_reward(0.9, new_my_country)
                        successor_list.append(new_state)

        def successors_for_transfer(path, countries, depth):
            for quantity in quantity_choices:
                positive_resource_unit_prices = transfer_unit_prices[0:6]
                for desired_resource in positive_resource_unit_prices:
                    other_resources = transfer_unit_prices.copy()
                    other_resources.remove(desired_resource)
                    for coun in countries:
                        if coun != 'MyCountry':
                            for r in other_resources:
                                a1, b1, c1 = BasicOperations.transfer(coun, country, countries[coun].resources,
                                                                      resources, desired_resource[0], quantity)
                                trade_amount = desired_resource[1] * quantity / abs(r[1])
                                if 'Waste' in r[0]:
                                    a2, b2, c2 = BasicOperations.transfer(coun, country, b1,
                                                                          c1, r[0], trade_amount)
                                else:
                                    a2, c2, b2 = BasicOperations.transfer(country, coun, c1,
                                                                          b1, r[0], trade_amount)
                                if a1 and a2:
                                    path_to_update = copy.deepcopy(path)
                                    countries_to_update = copy.deepcopy(countries)
                                    path_to_update.append(a1)
                                    path_to_update.append(a2)
                                    countries_to_update[coun].resources = b2
                                    countries_to_update[country].resources = c2
                                    new_state = State(depth + 1, countries_to_update, path_to_update)
                                    new_my_country = new_state.countries[country]
                                    new_other_country = new_state.countries[coun]
                                    new_my_country.discounted_reward = self.discounted_reward(0.9, new_my_country)
                                    new_other_country.discounted_reward = self.discounted_reward(0.9, new_other_country)
                                    successor_list.append(new_state)

        quantity_choices = [2 ** 0, 2 ** 1, 2 ** 2, 2 ** 3, 2 ** 4, 2 ** 5, 2 ** 6]
        transform_types = ['housing', 'food', 'electronics', 'metalAlloys']
        transfer_unit_prices = [('metalElements', 100), ('timber', 80), ('metalAlloys', 90),
                                ('electronics', 200), ('food', 60), ('water', 20),
                                ('metalAlloysWaste', -100), ('housingWaste', -150),
                                ('electronicsWaste', -200), ('foodWaste', -100)]
        successor_list = list()
        country = 'MyCountry'
        resources = self.countries[country].resources
        successors_for_transform(self.path, self.countries, self.depth)
        successors_for_transfer(self.path, self.countries, self.depth)

        return successor_list

    def undiscounted_reward(self, country):
        return country.state_quality() - country.init_state_quality

    def discounted_reward(self, gamma, country):
        return gamma ** self.depth * self.undiscounted_reward(country)
