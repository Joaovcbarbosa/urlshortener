from construction import create_routes
from local_search import inter_route_swap, inter_route_shift, intra_route_shift, intra_route_swap
from disturbance import random_neighbor
from copy import deepcopy

def VND(instance, r):
    best_fo, best_S = instance.best_solution()
    k = 1
    while k <= r:
        S = deepcopy(instance.current_solution)
        if k >= 1:                    
            intra_route_swap(instance, S)        
        if k >= 2:                    
            intra_route_shift(instance, S)       
        if k >= 3:                    
            inter_route_shift(instance, S)       
        if k == 4:                    
            inter_route_swap(instance, S)

        S = deepcopy(instance.current_solution)
        S_fo = instance.calculate_FO(S)

        if S_fo < best_fo:
            best_fo = S_fo
            k = 1
        else:
            k+=1
        
        print(S_fo, best_fo)


