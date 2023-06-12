"""
Asala Ehab
20201020
Assiment 4"""

import numpy as np
import matplotlib.pyplot as plt

#initialize the position for  particles & velocities
def intialpop(npop, x_min, x_max, v_max, dim): 
    for i in range(dim):
         particles= np.random.uniform(x_min[i], x_max[i], (npop,dim))
         velocities= np.random.uniform((-1*v_max[i]), v_max[i], (npop,dim))
    return particles, velocities


#evaluate the fitness for each particles
#we pass a single particles for it and get its fitness
def fit_evaluation(xi):
  fitness = np.sin(2*xi[0]-(0.5*np.pi)) + 3*np.cos(xi[1]) + (0.5*xi[0])
  return fitness

"""
#to update the local fitness"""
def updatePid(xi, xfitness, pi, particlebestFit):
    if xfitness > particlebestFit:
        pi = xi
    return pi


"""
#to  update the global fitness"""
def updatePgd(pi, particlebestFit, pg, globalbestFit):
    if particlebestFit > globalbestFit:
        pg = pi
        globalbestFit = particlebestFit
    return pg, globalbestFit

"""
#to update the position for  particles & velocities """
def updateVidXid(p_i,p_g,x_i,v_i,c_cog,c_soc,dim):
    r_cog = np.random.random(dim)
    r_soc = np.random.random(dim)
    v_i = np.array(v_i) + (c_cog * np.multiply(r_cog, np.subtract(p_i, x_i))) + (c_soc * np.multiply(r_soc, np.subtract(p_g, x_i)))
    x_i = np.array(x_i) + v_i
    return x_i, v_i

"""
#the basic function that will call all functions""" 
def PSO(numItr,npop,x_max,x_min,v_max,dim,c_cog,c_soc):
    
    prat,velo=intialpop(npop,x_min,x_max,v_max,dim)
    """that will return the particles and velocity"""
    praticle=prat.copy()
    pg = np.zeros(dim)
    globalbestFit = -100000000000
    for f in range(numItr):
        for i in range(npop):
            xfit=fit_evaluation(prat[i])
            praticle[i]=updatePid(prat[i],xfit,praticle[i],fit_evaluation(praticle[i]))
            pg, globalbestFit = updatePgd(praticle[i], fit_evaluation(praticle[i]), pg, globalbestFit)
        pratList=[]
        veloList=[]
        for j in range(npop):
            prat[j], velo[j] = updateVidXid(praticle[j], pg, prat[j], velo[j], c_cog, c_soc, dim)
            pratList.append(prat[j][0])
            veloList.append(velo[j][1])
            
        plt.scatter(pratList, veloList)
        plt.show()
        pratList.clear()
        veloList.clear()
   
    plt.scatter(pg[0], pg[1], color="Red")
    plt.show()

    return pg, globalbestFit

numItr = 200
npop = 50
x_max = [3,1]
x_min = [-2,-2]
v_max = [0.1,0.1]
dim = 2
c_cog = 1.7
c_soc = 1.7
    
for i in range(2):
    pg, globBestFit = PSO(i, npop, x_max, x_min, v_max, dim, c_cog, c_soc)
    print("\nAt Generation ",i+1,"\n")
    print("pg = ", pg, '\n')
    print("globBestFit = ", globBestFit, "\n")

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    