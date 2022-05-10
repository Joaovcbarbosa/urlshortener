from construction import create_routes
from local_search import local_search
from disturbance import random_neighbor
from copy import deepcopy

def VNS(instance, r, VNS_max, print_result = 1):
    best_fo, best_S = instance.best_solution()
    S = deepcopy(best_S)

    for i in range(VNS_max):
        k = 1
        while k < r:
            for j in range(k):                         
                S = random_neighbor(S)
                instance.refresh(S, 1)

            local_search(instance)
            S = deepcopy(instance.current_solution)
            S_fo = instance.calculate_FO(S)

            if S_fo < best_fo:
                best_fo = S_fo
                best_S = deepcopy(S)
                k = 1
            else:
                k+=1

        best_fo, S = instance.best_solution()
        if print_result == 1:
            print(i, S_fo, best_fo)

