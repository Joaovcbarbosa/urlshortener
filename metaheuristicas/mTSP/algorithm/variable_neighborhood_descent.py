from construction import create_routes
from local_search import inter_route_swap, inter_route_shift, intra_route_shift, intra_route_swap
from disturbance import random_neighbor
from copy import deepcopy

def VND(instance, r):
    best_fo, best_S = instance.best_solution()
    fo = best_fo
    k = 1
    
    while k <= r:        
        fo_initial = fo
        if k >= 1:                    
            intra_route_swap(instance, instance.current_solution)        
        if k >= 2:                    
            intra_route_shift(instance, instance.current_solution)       
        if k >= 3:                    
            inter_route_shift(instance, instance.current_solution)       
        if k == 4:                    
            inter_route_swap(instance, instance.current_solution)

        fo = instance.current_solution_fo

        if fo < best_fo:
            best_fo = fo
            k = 1
        else:
            k+=1
        
        print(fo_initial, best_fo)


