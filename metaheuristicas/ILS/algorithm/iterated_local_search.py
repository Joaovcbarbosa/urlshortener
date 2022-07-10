from variable_neighborhood_descent import VND
from disturbance import random_neighbor
from random import randint 
from time import time 

def ILS(instance, betta_min, betta_max, ILS_max):

    tempo_decorrido = 0

    while tempo_decorrido < ILS_max:
        tempo_inicio = time()
        VND(instance)   
        fo, S = instance.best_solution()

        for i in range(ILS_max):
            disturbance_percentage = int((randint(betta_min, betta_max) / 100) * len(instance.points))
            for j in range(disturbance_percentage):                         
                S, fo = random_neighbor(instance, S, fo) 
                instance.refresh(S, fo)

            VND(instance)        
            fo, S = instance.best_solution()

        tempo_iter = time()
        delta = tempo_iter - tempo_inicio
        tempo_decorrido += delta 

    return instance.best_solution()[0]