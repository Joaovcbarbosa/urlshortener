from local_search import local_search
from disturbance import random_neighbor
from copy import deepcopy

def VNS(instance, r, VNS_max):
    fo, S = instance.best_solution()    
    best_fo = fo

    for i in range(VNS_max):
        fo_initial = fo
        k = 1
        while k < r:
            for j in range(k):                         
                S, fo = random_neighbor(instance, S, fo) 
                instance.refresh(S, fo)

            local_search(instance)
            fo, S = instance.best_solution()

            if fo < best_fo:
                best_fo = fo
                k = 1
            else:
                k+=1

        print(i, fo_initial, best_fo)
        fo, S = instance.best_solution()


