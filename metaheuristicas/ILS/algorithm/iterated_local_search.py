from variable_neighborhood_descent import VND
from local_search import Tempo
from disturbance import random_neighbor
from random import randint 

def ILS(instance, betta_min, betta_max, ILS_max):
    Tempo.tempo_decorrido = 0
    while Tempo.tempo_decorrido < ILS_max:
        if Tempo.tempo_decorrido == 0:
            if VND(instance, ILS_max) == False:
                break  
            fo, S, time = instance.best_solution()

        disturbance_percentage = int((randint(betta_min, betta_max) / 100) * len(instance.points))
        for j in range(disturbance_percentage):                         
            S, fo = random_neighbor(instance, S, fo) 
            instance.refresh(S, fo)

        if VND(instance, ILS_max) == False:
            break  
        fo, S, time = instance.best_solution()

    fo, S, time = instance.best_solution()
    return fo, time 