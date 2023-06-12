import random
import math


class City:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance(self, city):
        return math.hypot(self.x - city.x, self.y - city.y)

    def __repr__(self):
        return f"({self.x}, {self.y})"


def read_cities(size):
    cities = []

    with open(f'test_data/cities_{size}.txt', 'r') as file:  # ta3del
        L = file.readlines()
        for line in L:
            x, y = map(float, line.split())
            cities.append(City(x, y))
    return cities


def path_cost(route):
    return sum([city.distance(route[index - 1]) for index, city in enumerate(route)])


class Particle:
    def __init__(self, route, cost=None):
        self.route = route
        self.pbest = route
        self.velocity = []
        # ta3del
        if cost != None:
            self.current_cost = cost
        else:
            self.current_cost = self.path_cost()
        # ta3del
        if cost != None:
            self.pbest_cost = cost
        else:
            self.pbest_cost = self.path_cost()

    def clear_velocity(self):
        self.velocity.clear()

    # update the pbest
    def update_costs_and_pbest(self):
        self.current_cost = self.path_cost()
        if self.current_cost < self.pbest_cost:
            self.pbest = self.route
            self.pbest_cost = self.current_cost

    def path_cost(self):
        return path_cost(self.route)  # hatro7 le satr 29


class PSO:

    def __init__(self, iterations, pop_size, gbest_probability=1.0, pbest_probability=1.0, cities=None):
        self.cities = cities
        self.gbest = None
        self.gcost_iter = []
        self.iterations = iterations
        self.pop_size = pop_size
        self.gbest_probability = gbest_probability
        self.pbest_probability = pbest_probability
        solutions = self.initial_pop()

        # ta3del
        self.particles = []
        for solution in solutions:
            particle = Particle(route=solution)
            self.particles.append(particle)

    # ta3del
    def random_route(self):
        route = list(self.cities)
        random.shuffle(route)
        return route

    def initial_pop(self):
        random_population = []
        for _ in range(self.pop_size - 1):
            random_population.append(self.random_route())

        greedy_population = [self.greedy_route(0)]
        return [*random_population, *greedy_population]

    def greedy_route(self, start_node):
        unvisited = self.cities[:]
        del unvisited[start_node]
        route = [self.cities[start_node]]
        while len(unvisited):
            indx, close_city = min(enumerate(unvisited), key=lambda item: item[1].distance(route[-1]))
            route.append(close_city)
            del unvisited[indx]
        return route

    def run(self):

        self.gbest = min(self.particles, key=lambda p: p.pbest_cost)

        for t in range(self.iterations):
            self.gbest = min(self.particles, key=lambda p: p.pbest_cost)

            if t % 20 == 0:

                x_list, y_list = [], []
                for city in self.gbest.pbest:
                    x_list.append(city.x)
                    y_list.append(city.y)
                x_list.append(pso.gbest.pbest[0].x)
                y_list.append(pso.gbest.pbest[0].y)

            self.gcost_iter.append(self.gbest.pbest_cost)

            # ta3del  *_*    *_*    *_*


            for particle in self.particles:
                particle.clear_velocity()
                temp_velocity = []
                gbest = self.gbest.pbest[:]
                new_route = particle.route[:]


                pbest_swaps = [(i, particle.pbest.index(new_route[i]), self.pbest_probability)
                               for i in range(len(self.cities)) if new_route[i] != particle.pbest[i]]
                temp_velocity.extend(pbest_swaps)


                gbest_swaps = [(i, gbest.index(new_route[i]), self.gbest_probability)
                               for i in range(len(self.cities)) if new_route[i] != gbest[i]]
                temp_velocity.extend(gbest_swaps)


                for swap in temp_velocity:
                    c1 = 2.0
                    c2 = 2.0
                    r1 = random.random()
                    r2 = random.random()
                    vij = swap[2]
                    yij = new_route[swap[1]].y
                    xij = new_route[swap[0]].x
                    vij_updated = vij + (c1 * r1 * yij * xij) + (c2 * r2 * (1 - yij) * xij)
                    particle.velocity.append((swap[0], swap[1], vij_updated))

                # Apply swaps based on velocities
                for swap in particle.velocity:
                    if random.random() <= swap[2]:
                        new_route[swap[0]], new_route[swap[1]] = new_route[swap[1]], new_route[swap[0]]

                particle.route = new_route
                particle.update_costs_and_pbest()


if __name__ == "__main__":
    cities = read_cities(5)  # ta3del
    pso = PSO(100, 50, 0.9, 0.02, cities)
    pso.run()
    print(f'The total cost: {pso.gbest.pbest_cost}')
    print(f'best route: {pso.gbest.pbest}')

    # ta3del
