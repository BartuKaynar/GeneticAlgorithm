from RouteManager import RouteManager
from Route import Route
import random
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
                    token = random.randint(0, self.population_size-1)
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
        i = 0
        while i < len(self.cities):
            rate = random.random()
            if i < len(self.cities)/2:
                city = route_1.get_city(int(i+len(self.cities)/4))
                if not newMem.__contains__(city):
                    newMem.assign_city(int(i+len(self.cities)/4), city)
            else:
                if rate < 0.8:
                    repeat = 0
                    city = None
                    k = 0
                    if i >= 3*len(self.cities)/4:
                        city = route_2.get_city(int(i-(3*len(self.cities)/4)))
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
                                city = route_2.get_city(int(repeat-(3*len(self.cities)/4)))
                                if not newMem.__contains__(city):
                                    newMem.assign_city(int(i-(3*len(self.cities)/4)), city)
                                    found = True
                        elif k == 1:
                            while found is False:
                                repeat += 1
                                if repeat >= len(self.cities):
                                    repeat = len(self.cities) - repeat
                                city = route_2.get_city(repeat)
                                if not newMem.__contains__(city):
                                    newMem.assign_city(int(i+len(self.cities)/4), city)
                                    found = True
                    else:
                      #  print(city)
                        if i >= 3*len(self.cities)/4:
                            newMem.assign_city(int(i-(3*len(self.cities)/4)), city)
                        else:
                            newMem.assign_city(int(i+len(self.cities)/4), city)
                       # print("2den aldı")
                else:
                    if newMem.__len__() < 2:
                       # print("mutate")
                        self.mutate(newMem)
                    i -= 1
               # print(newMem)
            i += 1
       # print(newMem)
        return newMem

    def mutate(self, route):
        changer1 = random.randint(0, route.__len__() - 1)
        changer2 = random.randint(0, route.__len__() - 1)
        temp1 = route.get_city(changer1)
        temp2 = route.get_city(changer2)
        while temp1 is None or temp2 is None:
            changer1 = random.randint(0, route.__len__() - 1)
            changer2 = random.randint(0, route.__len__() - 1)
            temp1 = route.get_city(changer1)
            temp2 = route.get_city(changer2)
        route.assign_city(changer1, temp2)
        route.assign_city(changer2, temp1)


    def tournament(self, routes):
        best = None
        i = 0
        while i < len(routes):
            route = routes[i]
            if best is None or routes[i].calc_fitness() > best.calc_fitness():
                best = routes[i]
            i += 1
        return best
