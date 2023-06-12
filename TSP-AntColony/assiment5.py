"ِAsala Ehab 20201020 Assiment 5"""
import numpy as np
import math
import random
import matplotlib.pyplot as plt

class Coordinate:
    x = 0
    y = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_points(self):
        return self.x, self.y


city_name = []
cities = []
"""here to can read the data and work on it
i am read it from the  file as x & y
"""
with open("TSPData.txt", "r") as f:
    for lines in f:
        city_name.append(lines.split("\t")[0])
        cities.append(Coordinate(float(lines.split("\t")[1]), float(lines.split("\t")[2])))

n_cities = len(city_name)
distance = np.full((n_cities, n_cities), 100000, dtype='float64')


"""iam calculate the distance"""
def euclidean_distance():
    for i in range(n_cities):
        for j in range(n_cities):
            if (i != j):
                distance[i][j] = math.sqrt((cities[i].x - cities[j].x) ** 2 + (cities[i].y - cities[j].y) ** 2)
    return distance



D = np.array(euclidean_distance())

# create inverse

# dumpy node to be used
dumyList = D.copy()

etamatrix = np.full((n_cities, n_cities), 100000, dtype='float64')
for i in range(n_cities):
    for j in range(n_cities):
        if (i != j):
            etamatrix[i][j] = 1 / dumyList[i][j]


#max_place = n_cities
path = []
visited = []
tour_len = 0
i = 0
start_node = np.random.randint(0, 29)
while i < n_cities:
    temp = np.array(dumyList[start_node])
    for j in visited:
        temp[j] = 100000000
        """it make the distance so big so that it cannot be choosen"""
    next_node = np.argmin(temp, axis=0)
    if next_node not in visited:
        path.append(next_node)
        visited.append(next_node)
        tour_len = tour_len + temp[next_node]
        i += 1
        start_node = next_node

#print("visited", tour_len)
tau=1/(n_cities*tour_len)


#the pheromones

pheromones=np.full((n_cities, n_cities), tau, dtype='float64')
positions=[]
short_path=[]
t=0
while t<20:
    short_tour=1000000
    initial_pos=0
    ants=[]
    found=[]
    rou=0.5
    alpha = 1
    beta = 2
    probaility=[]
   
      
    i=0
    probability_for_one=[]
    tours=[]
    m=random.randint(1, 29)#m refer to the number of ants
    while i<m:
        node=random.randint(0, 28)#then i create random node to be the initial point
        if node not in found:#so that we will not generate more than one in one city 
            ants.append(cities[node])#to add the node for each ants
            found.append(node)
            
            
            visit=[False]*n_cities
            #inital_point=ants[i].get_points()
            visited_n=0
            ant_tour=0
            
            visit[node]=True
            while visited_n < n_cities:
                mx=-1
                sm=0
                dum=[]
                for c in range(n_cities):
                    if c!=node or visit[c]==False:
                       
                            bast=((pheromones[node][c]**alpha)*(etamatrix[node][c]**beta))#first i will calculate the bast
                            sm+=bast #3ashan a7dar ekmakam el haqsm 3aleh
                            dum.append(bast)
                           
                            
                    else:
                            dum.append(-1000000)
                for d in range(n_cities):
                    probability_for_one.append(dum[d]/sm)#the probalbility for the current node
                pos=0
                for f in range(n_cities):
                    if mx<=probability_for_one[f]:
                        pos=f
                        mx=probability_for_one[f]
                visit[pos]=True
                visited_n+=1
                ant_tour+=distance[node][pos]
            ant_tour+=distance[pos][node]
            tours.append(ant_tour)
            if ant_tour<short_tour:
                short_tour=ant_tour
                initial_pos=node
            i+=1
            found.clear()#for another repeat
    for a in range(n_cities):
        for b in range(n_cities):
            for c in range(len(tours)):
                pheromones[a][b]=((1-rou)* pheromones[a][b])+(1/tours[c]) 
    short_path.append(short_tour)
    positions.append(initial_pos)
    t+=1
    
plt.plot(positions)
plt.title(" positions")
plt.ylabel("initial_positions")
plt.xlabel('Generations')
plt.show()

plt.plot(short_path)
plt.title("short path")
plt.ylabel("tours")
plt.xlabel('Generations')
plt.show()

          
        


