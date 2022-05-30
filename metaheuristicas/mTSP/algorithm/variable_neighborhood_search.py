from local_search import local_search
from variable_neighborhood_descent import VND 
from disturbance import random_neighbor
from copy import deepcopy
from random import randint 

def VNS(instance, betta_min, betta_max, VNS_max):    
    fo_S, S = instance.best_solution()    
    fo_best = fo_S

    for i in range(VNS_max):
        fo_initial = fo_S
        k = 1
        r = int((randint(betta_min, betta_max) / 100) * len(instance.points))   
        while k < r:
            for j in range(k):                         
                S, fo_S = random_neighbor(instance, S, fo_S) 
                instance.refresh(S, fo_S)

            # local_search(instance)
            VND(instance, r=6, print_solution=False)   
            fo_S, S = instance.best_solution()

            if fo_S < fo_best:
                fo_best = fo_S
                k = 1
            else:
                k+=1

        print(i, fo_initial, fo_best)
        fo, S = instance.best_solution()


