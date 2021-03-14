import ResourceQuality
import BasicOperations
import copy
import math


class Country:
    def __init__(self, countryName, resources, init_state_quality):
        self.name = countryName
        self.resources = resources
        self.init_state_quality = init_state_quality
        self.participation_prob = -1


class State:
    def __init__(self, depth, countries, schedule):
        self.countries = countries
        self.depth = depth
        self.path = schedule
        self.eu = 0

    # Define the notion of '<' for a State, used in PriorityQueue when priority of
    # two states is otherwise equal. We prefer the lower depth in that case
    def __lt__(self, other):
        return self.depth < other.depth

    def findSuccessor(self):
        def successors_for_transform(path, countries, depth):
            for quantity in quantity_choices:
                for transform_type in transform_types:
                    a, b = BasicOperations.transform(country, resources, quantity, transform_type)
                    if a:
                        init_state = countries[country].init_state_quality
                        d_r, par_p = self.country_participation_probability(b, init_state, 0.9, depth+1, 0, 1)
                        p = 1
                        for i in countries:
                            if i != country and countries[i].participation_prob != -1:
                                 p = p * countries[i].participation_prob
                        eu = p * par_p * d_r

                        if eu >= 100000:
                            path_to_update = copy.deepcopy(path)
                            countries_to_update = copy.deepcopy(countries)
                            path_to_update.append(a)
                            countries_to_update[country].resources = b
                            countries_to_update[country].participation_prob = par_p
                            new_state = State(depth + 1, countries_to_update, path_to_update)
                            new_state.eu = eu
                            successor_list.append(new_state)

        def successors_for_transfer(path, countries, depth):
            for quantity in quantity_choices_1:
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
                                    init_state1 = countries[coun].init_state_quality
                                    init_state2 = countries[country].init_state_quality
                                    d_r1, par_p1 = self.country_participation_probability(b2, init_state1, 0.9,
                                                                                          depth + 1, 0, 1)
                                    d_r2, par_p2 = self.country_participation_probability(c2, init_state2, 0.9,
                                                                                          depth + 1, 0, 1)
                                    p = 1
                                    for i in countries:
                                        if i != coun and i != country and countries[i].participation_prob != -1:
                                            p = p * countries[i].participation_prob
                                    eu = p * par_p1 * par_p2 * d_r2

                                    if eu >= 100000:
                                        path_to_update = copy.deepcopy(path)
                                        countries_to_update = copy.deepcopy(countries)
                                        path_to_update.append(a1)
                                        path_to_update.append(a2)
                                        countries_to_update[coun].resources = b2
                                        countries_to_update[country].resources = c2
                                        countries_to_update[coun].participation_prob = par_p1
                                        countries_to_update[country].participation_prob = par_p2
                                        new_state = State(depth + 1, countries_to_update, path_to_update)
                                        new_state.eu = eu
                                        successor_list.append(new_state)

        quantity_choices = (2 ** 0, 2 ** 1, 2 ** 2, 2 ** 3, 2 ** 4, 2 ** 5, 2 ** 6)
        quantity_choices_1 = (1, 10, 100)
        transform_types = ('housing', 'food', 'electronics', 'metalAlloys')
        transfer_unit_prices = [('metalElements', 2100), ('timber', 200), ('metalAlloys', 2200),
                                ('electronics', 4300), ('food', 220), ('water', 2),
                                ('metalAlloysWaste', -53), ('housingWaste', -53),
                                ('electronicsWaste', -53), ('foodWaste', -53)]
        successor_list = list()
        country = 'MyCountry'
        resources = self.countries[country].resources
        successors_for_transform(self.path, self.countries, self.depth)
        successors_for_transfer(self.path, self.countries, self.depth)

        return tuple(successor_list)

    def country_participation_probability(self, resources, init_s, gamma, depth, x_0, k, L=1):
        sq = ResourceQuality.getStateQuality(resources)
        dr = gamma ** depth * (sq - init_s)
        cpp = -1
        if -k * (dr - x_0) < 100:
            cpp = L / (1 + math.exp(-k * (dr - x_0)))
        return dr, cpp
