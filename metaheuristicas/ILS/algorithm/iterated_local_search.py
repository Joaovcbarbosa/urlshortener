from variable_neighborhood_descent import VND
from disturbance import random_neighbor
from random import randint 

class Tempo:
    tempo_decorrido = 0

def ILS(instance, betta_min, betta_max, ILS_max):

    while Tempo.tempo_decorrido < ILS_max:
        if Tempo.tempo_decorrido == 0:
            if VND(instance, ILS_max) == False:
                return 
            fo, S = instance.best_solution()

        disturbance_percentage = int((randint(betta_min, betta_max) / 100) * len(instance.points))
        for j in range(disturbance_percentage):                         
            S, fo = random_neighbor(instance, S, fo) 
            instance.refresh(S, fo)

        VND(instance, ILS_max)        
        fo, S = instance.best_solution()

    print(Tempo.tempo_decorrido)
    return instance.best_solution()[0]