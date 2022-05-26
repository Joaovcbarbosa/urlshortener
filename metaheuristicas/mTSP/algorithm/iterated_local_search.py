from local_search import local_search
from disturbance import random_neighbor
from random import randint 
from copy import deepcopy

def ILS(instance, betta_min, betta_max, ILS_max):
    local_search(instance)
    fo, S = instance.best_solution()

    for i in range(ILS_max):
        disturbance_percentage = int((randint(betta_min, betta_max) / 100) * len(instance.points))
        for j in range(disturbance_percentage):                         
            S, fo = random_neighbor(instance, S, fo) 
            instance.refresh(S, fo)

        local_search(instance)       
        fo, S = instance.best_solution()
        print(i, instance.current_solution_fo, fo)