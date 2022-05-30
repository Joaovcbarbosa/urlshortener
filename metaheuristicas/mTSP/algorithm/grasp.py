from local_search import local_search
from variable_neighborhood_descent import VND
from iterated_local_search import ILS 
from semi_greedy_construction import semi_greedy_construction
   
def is_better(instance, fo_best):
    return instance.current_solution_fo < fo_best or fo_best < 0

def GRASP(instance, GRASP_max, RLC_length_in_percentage, alpha):
    fo_best = -1
    for i in range(GRASP_max):
        semi_greedy_construction(instance, RLC_length_in_percentage, alpha)
        # local_search(instance) 
        VND(instance, r=6, print_solution=False) 
        
        if is_better(instance, fo_best):
            fo_best = instance.current_solution_fo

        print(i, instance.current_solution_fo, fo_best)

    





