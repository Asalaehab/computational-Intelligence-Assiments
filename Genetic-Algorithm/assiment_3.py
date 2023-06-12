"""
#Asala Ehab Mohmed
#20201020
#Assiment 3
"""
import numpy as np
import random
import matplotlib.pyplot as plt

npop=20

#to initialize population of random variables within a specific range
def create_initial_pop(pop_size,variables_min,variables_max):
   
    number_variables = len(variables_min)
    init_pop = np.random.uniform(variables_min,variables_max,(pop_size,number_variables))
    return init_pop




fit=[]

#optimaztion
"""
to do optimaztion function
"""
def violated_points_fitness(npop,pop):
    for i in range(npop):
        x1=0
        x2=0
        for j in range(2):
            if j == 0:

                x1 = pop[i][j]
            else:

                x2 = pop[i][j]

        z = 8 - (x1 + 0.0317) ** 2 + (x2) ** 2 - abs(x1 + x2 - 1)
        fit.append(z)
        
    return fit

#tournament selection
#at tourment we give it the population and the tournment size it select random individual from it then
#then we select depented on the fitness the best two prarent and return them

"""
tournament selection take three parameters
population>>pop
tournament size>>k
fitness >>f to can choose depend on it
"""
def tournament_selection(pop, k,f):
       parents=random.choices(pop,k=5)
       parents.sort(key=lambda j:f, reverse=True)
       return parents[0],parents[1]



#arithmatic cross_over 
# we implement the two equation that will make the cross for the two real parents
def arithmetic_crossover (two_parents, pcross):
   
    two_children = two_parents

    x = np.random.random()

    if(x <= pcross):
      alpha1 = np.random.random()
      alpha2 = np.random.random()

      two_children[0 , :] = alpha1*two_parents[0 , :]+(1-alpha1)*two_parents[1, :]
      two_children[1 , :] = alpha2*two_parents[0 , :]+(1-alpha2)*two_parents[1 , :]
    return two_children


"""
the mutation function that take the value and 
create the random variable if it is <=pmute
we will do else no
"""
def gaussian_mutate(individual,sigma,pmute,variables_min, variables_max):
    mutated_individual=individual
    if(np.random.random() <= pmute):
          m = np.random.normal(0,sigma)
          mutated_individual = np.array(individual) + m 
    
    return mutated_individual
"""
#the Elitism function that take the fitness>>f and the elitism size>>s
#and return the best fitness to individuals that will remain with us in the new population

""" 
def Elitism(f,s):
    mx=0
    dumpy=f.copy()#to can do change without make effect on the the main fitness
    mx_index=[]
    for i in range(s):
        mx=max(dumpy)
        mx_index.append(dumpy.index(mx))
        dumpy.remove(mx)
    
    return mx_index
"""
the basic function for call
"""
def MainFun(pop_s,length,generations,pc,pmut,eleitizem_size):
    bestFit=[]
    avergFit=[]
    #we call the init_pop and create population
   #to carry the new population
    int_pop=[]
    int_pop=create_initial_pop(pop_s,[-2,2],[2,-2])
    
    #to no if it staisfy the constraints
    for w in range(generations):
        fitN=[]
        agree=[]
        index=[]
        newpop=[] #that always take the new generation of the indviduals 
        
        #the fitness evaluation
        fitN=violated_points_fitness(pop_s,int_pop)
        
        index=Elitism(fitN, eleitizem_size)
        for i in range(eleitizem_size):
            j=index[i]
            newpop.append(int_pop[j])
       
     
        a=eleitizem_size
        
        while(a<=pop_s):
             two_parents=np.array(tournament_selection(int_pop,5,fitN))
            
             individuals=arithmetic_crossover(two_parents,pc)
             for j in range(2):
                 muted_value=gaussian_mutate(individuals[j],0.5,pmut,-2,2)
                 newpop.append(muted_value)
             a+=2   
        for k in range(pop_s):
            int_pop[k]=newpop[k]
    
        #to get the bestfitness
        bestFit.append(max(fitN))
        avergFit.append((sum(fitN))/pop_s)
        
        fitN.clear()
        agree.clear()
        newpop.clear()
        index.clear()
       
    plt.plot(bestFit)
    plt.title("Best Fitness")
    plt.ylabel("High fitness")
    plt.xlabel('Generations')
    plt.show()
    plt.plot(avergFit)
    plt.title("Average Fitness")
    plt.ylabel("Mean of fitness")
    plt.xlabel('Generations')
    plt.show()


"""
to run the code number of times"""
for i in range(10):
    MainFun(20,5,10,0.6,0.05,2)
    
   
    
    







