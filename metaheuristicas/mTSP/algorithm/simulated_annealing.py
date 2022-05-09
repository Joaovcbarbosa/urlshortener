import random
import math
import copy
import disturbance

def generate_neighbor(instance, S):   
    S_neighbor = disturbance.random_neighbor(S)
    fo_neighbor = instance.calculate_FO(S_neighbor)

    return S_neighbor, fo_neighbor

def SA(instance, T0, SAMax, alpha):
    S = copy.deepcopy(instance.current_solution)
    S_best = copy.deepcopy(S)
    fo_best = instance.current_solution_fo
    iterations = 0
    T = T0
    while T > 0.0001:
        while iterations < SAMax:
            iterations += 1
            S_neighbor, fo_neighbor = generate_neighbor(instance, S) 
            fo_S = instance.calculate_FO(S)
            delta = fo_neighbor - fo_S

            if delta <= 0:
                S = copy.deepcopy(S_neighbor)
                fo_S = fo_neighbor
                if fo_neighbor < fo_best:
                    S_best = copy.deepcopy(S_neighbor)
                    fo_best = fo_neighbor
                    instance.add_best_solution(fo_best, S_best)
            else:
                x = random.uniform(0, 1)
                if x < math.exp(-delta/T):                    
                    S = copy.deepcopy(S_neighbor)    
                    fo_S = fo_neighbor            

        print(T, fo_S, fo_best)
        T = T * alpha
        iterations = 0





