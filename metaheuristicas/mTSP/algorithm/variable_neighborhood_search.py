from local_search import local_search
from disturbance import random_neighbor
from copy import deepcopy

def VNS(instance, r, VNS_max):
    fo_S, S = instance.best_solution()    
    fo_best = fo_S

    for i in range(VNS_max):
        fo_initial = fo_S
        k = 1
        while k < r:
            for j in range(k):                         
                S, fo_S = random_neighbor(instance, S, fo_S) 
                instance.refresh(S, fo_S)

            local_search(instance)
            fo_S, S = instance.best_solution()

            if fo_S < fo_best:
                fo_best = fo
                k = 1
            else:
                k+=1

        print(i, fo_initial, fo_best)
        fo, S = instance.best_solution()


