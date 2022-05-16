from local_search import local_search
from disturbance import random_neighbor
from random import randint 
from copy import deepcopy

def ILS(instance, betta_min, betta_max, ILS_max):
    local_search(instance)
    best_fo, best_S = instance.best_solution()
    S = deepcopy(best_S)

    for i in range(ILS_max):
        disturbance_percentage = int((randint(betta_min, betta_max) / 100) * len(instance.points))
        for j in range(disturbance_percentage):                         
            S = random_neighbor(S)
            instance.refresh(S, 1)

        local_search(instance)
        S = deepcopy(instance.current_solution)
        S_fo = instance.calculate_FO(S)

        if S_fo < best_fo:
            best_fo = S_fo
            best_S = deepcopy(S)

        best_fo, S = instance.best_solution()
        print(i, S_fo, best_fo)

