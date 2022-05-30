from local_search import local_search
from variable_neighborhood_descent import VND
from disturbance import random_neighbor
from random import randint 

def ILS(instance, betta_min, betta_max, ILS_max, print_solution = True):
    # local_search(instance)
    VND(instance, r=6, print_solution=False)   
    fo, S = instance.best_solution()

    for i in range(ILS_max):
        disturbance_percentage = int((randint(betta_min, betta_max) / 100) * len(instance.points))
        for j in range(disturbance_percentage):                         
            S, fo = random_neighbor(instance, S, fo) 
            instance.refresh(S, fo)

        # local_search(instance)
        VND(instance, r=6, print_solution=False)        
        fo, S = instance.best_solution()

        if print_solution == True:
            print(i, instance.current_solution_fo, fo)