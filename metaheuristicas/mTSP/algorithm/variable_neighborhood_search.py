from variable_neighborhood_descent import VND 
from disturbance import random_neighbor

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

            VND(instance, r=6, print_solution=False)   
            fo_S, S = instance.best_solution()

            if fo_S < fo_best:
                fo_best = fo_S
                k = 1
            else:
                k+=1

        print(i, fo_initial, fo_best)
        fo, S = instance.best_solution()


