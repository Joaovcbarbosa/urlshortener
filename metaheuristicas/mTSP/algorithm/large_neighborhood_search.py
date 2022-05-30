from random import uniform
from math import exp
from copy import deepcopy
from destruction_rebuild import destruction_rebuild

def LNS(instance, T0, SAMax, alpha, betta_min, betta_max) :
    S = deepcopy(instance.current_solution)
    fo_S = instance.current_solution_fo
    S_best = deepcopy(S)
    fo_best = instance.current_solution_fo
    iterations = 0
    T = T0
    while T > 0.0001:
        while iterations < SAMax:
            iterations += 1
            S_new, fo_new = destruction_rebuild(instance, S, fo_S, betta_min, betta_max)           
            delta = fo_new - fo_S

            if delta <= 0:
                S = deepcopy(S_new)
                fo_S = fo_new
                instance.refresh(S, fo_S)
                if fo_new < fo_best:
                    S_best = deepcopy(S_new)
                    fo_best = fo_new
                    instance.add_best_solution(fo_best, S_best)
            else:
                x = uniform(0, 1)
                if x < exp(-delta/T):                    
                    S = deepcopy(S_new)    
                    fo_S = fo_new 
                    instance.refresh(S, fo_S)

                       

        print(T, fo_S, fo_best)
        if fo_best < 445:
            print('a')
        T = T * alpha
        iterations = 0





