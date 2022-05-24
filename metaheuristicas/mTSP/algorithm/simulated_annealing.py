from random import uniform
from math import exp
from copy import deepcopy
from disturbance import random_neighbor

def SA(instance, T0, SAMax, alpha):
    S = deepcopy(instance.current_solution)
    fo_S = instance.current_solution_fo
    S_best = deepcopy(S)
    fo_best = instance.current_solution_fo
    iterations = 0
    T = T0
    while T > 0.0001:
        while iterations < SAMax:
            iterations += 1
            S_neighbor, fo_neighbor = random_neighbor(instance, S) 
            delta = fo_neighbor - fo_S

            if delta <= 0:
                S = deepcopy(S_neighbor)
                fo_S = fo_neighbor
                instance.refresh(S, fo_S)
                if fo_neighbor < fo_best:
                    S_best = deepcopy(S_neighbor)
                    fo_best = fo_neighbor
                    instance.add_best_solution(fo_best, S_best)
            else:
                x = uniform(0, 1)
                if x < exp(-delta/T):                    
                    S = deepcopy(S_neighbor)    
                    fo_S = fo_neighbor 
                    instance.refresh(S, fo_S)

                       

        print(T, fo_S, fo_best)
        T = T * alpha
        iterations = 0





