import local_search
import random
import math

def calculate_FO(instance, routes):
    fo = 0
    for route in routes:
        fo += instance.matrix[route[0]][route[1]]
        for i in range(len(route)):
            if i > 0 and i < len(route) - 1:
                fo += instance.matrix[route[i]][route[i+1]]
            elif i == len(route) - 1:
                fo += instance.matrix[route[i]][route[0]]
    
    return fo

def SA(instance, S, T0, SAMax, alpha):
    iterations = 0
    T = T0
    FO_test = calculate_FO(instance, S)
    while T > 0.0001:
        while(iterations < SAMax):
            iterations += 1
            S_neighboor = local_search.random_neighboor(S)
            delta = calculate_FO(instance, S_neighboor) - calculate_FO(instance, S)

            if delta <= 0:
                S = S_neighboor
            else:
                x = random.uniform(0, 1)
                if x > math.exp(-delta/T):                    
                    S = S_neighboor
                
            if(calculate_FO(instance, S) < FO_test):
                S_best = S
                FO_test = calculate_FO(instance, S)

        print(calculate_FO(instance, S), calculate_FO(instance, S_best))
        T = alpha * T
        iterations = 0

    print(S_best)

    





