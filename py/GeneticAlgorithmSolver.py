from RouteManager import RouteManager
from Route import Route
import numpy as np


class GeneticAlgorithmSolver:
    def __init__(self, cities, population_size=50, mutation_rate=0.2, tournament_size=10, elitism=False):
        self.cities = cities
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.tournament_size = tournament_size
        self.elitism = elitism

    def solve(self, rm):
        rm = self.evolve(rm)
        for i in range(100):
            rm = self.evolve(rm)
        return rm

    def evolve(self, routes):
        j = 0
        while j < self.population_size:
           # print("j:", j)
            k = 0
            route_1 = []
            route_2 = []
            tokens = []
            while k < 2:
                fitness = []
                i = 0
                while i < self.tournament_size:
                    token = np.random.randint(0, self.population_size-1)
                    if token in tokens:
                        continue
                    tokens.append(token)
                    route = routes.get_route(token)
                    fitness.append(route)
                    i += 1
                if k == 0:
                    route_1 = self.tournament(fitness)
                elif k == 1:
                    route_2 = self.tournament(fitness)
                k += 1
            nextRoute = self.crossover(route_1, route_2)
            routes.set_route(j, nextRoute)
            j += 1
        return routes

    def crossover(self, route_1, route_2):
        newMem = Route(self.cities)
        random_1 = np.random.randint(0, route_1.__len__()/2-1)
        random_2 = np.random.randint(9, route_1.__len__() - 1)
        if random_1 > random_2:
            temp = random_2
            random_2 = random_1
            random_1 = temp
        i = 0
        while i < len(self.cities):
            rate = np.random.random()
            if random_1 < i < random_2:
                repeat = i
                city = route_1.get_city(i)
                if not newMem.__contains__(city):
                    newMem.assign_city(int(i), city)
                else:
                    found = False
                    while found is False:
                        repeat += 1
                        if repeat >= len(self.cities):
                            repeat = len(self.cities) - repeat
                        city = route_1.get_city(repeat)
                        if not newMem.__contains__(city):
                            newMem.assign_city(int(i), city)
                            found = True
            else:
                if rate < 0.8:
                    repeat = 0
                    city = None
                    k = 0
                    if i >= random_2:
                        city = route_2.get_city(int(i-random_2))
                    else:
                        city = route_2.get_city(i)
                        k += 1
                    if newMem.__contains__(city):
                        found = False
                        repeat = i
                        if k == 0:
                            while found is False:
                                repeat += 1
                                if repeat >= len(self.cities):
                                    repeat = len(self.cities) - repeat
                                city = route_2.get_city(int(repeat-random_2))
                                if not newMem.__contains__(city):
                                    newMem.assign_city(int(i), city)
                                    found = True
                        elif k == 1:
                            while found is False:
                                repeat += 1
                                if repeat >= len(self.cities):
                                    repeat = len(self.cities) - repeat
                                city = route_2.get_city(repeat)
                                if not newMem.__contains__(city):
                                    newMem.assign_city(int(i+random_1), city)
                                    found = True
                    else:
                        if i >= random_2:
                            newMem.assign_city(int(i-random_2), city)
                        else:
                            newMem.assign_city(int(i), city)
                else:
                    if newMem.__len__() < 2:
                        self.mutate(newMem)
                    i -= 1
            i += 1
        return newMem

    def mutate(self, route):
        changer1 = np.random.randint(0, route.__len__() - 1)
        changer2 = np.random.randint(0, route.__len__() - 1)
        temp1 = route.get_city(changer1)
        temp2 = route.get_city(changer2)
        while temp1 is None or temp2 is None:
            changer1 = np.random.randint(0, route.__len__() - 1)
            changer2 = np.random.randint(0, route.__len__() - 1)
            temp1 = route.get_city(changer1)
            temp2 = route.get_city(changer2)
        route.assign_city(changer1, temp2)
        route.assign_city(changer2, temp1)


    def tournament(self, routes):
        best = None
        i = 0
        while i < len(routes):
            route = routes[i]
            if best is None or route.calc_fitness() > best.calc_fitness():
                best = route
            i += 1
        return best
