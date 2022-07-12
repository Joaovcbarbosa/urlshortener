from copy import deepcopy
from instances import calculate_cost_swap, calculate_cost_shift, calculate_cost_2opt
from time import time

class Tempo:
    tempo_decorrido = 0

def swap(route_one, route_two, point_one_index, point_two_index):
    point_one = route_one[point_one_index]
    point_two = route_two[point_two_index]

    route_one[point_one_index] = point_two 
    route_two[point_two_index] = point_one 

def shift(route_one, route_two, insert_index, point_index):
    point = route_one[point_index]
    route_one.remove(point)
    route_two.insert(insert_index, point)

def update_solution(instance, S, cost, time):
    instance.current_solution_fo = round(instance.current_solution_fo + cost, 2)
    instance.current_solution = S
    instance.add_best_solution(instance.current_solution_fo, instance.current_solution, time)

def two_opt(route, i, j): 
    new_route = deepcopy(route)
    new_route = new_route[i:j+1]
    new_route.reverse()
    route[i:j+1] = new_route 

def intra_route_2opt(instance, S, ILS_max):
    tempo_inicio = time()
    for route_index in range(len(S)):  # Para cada rota
        lenght_route = len(S[route_index])
        for i in range(1, lenght_route - 2): # Seleciona um ponto da rota
            j = i + 2
            while j < lenght_route:
                cost = calculate_cost_2opt(instance, S[route_index], i - 1, j - 1)
                if cost < 0:
                    two_opt(S[route_index], i, j - 1)

                    tempo_iter = time()
                    delta = tempo_iter - tempo_inicio
                    Tempo.tempo_decorrido += delta 
                    tempo_inicio = time()   
                    update_solution(instance, S, cost,  Tempo.tempo_decorrido) 
                    if  Tempo.tempo_decorrido > ILS_max:
                        return False
                    return intra_route_2opt(instance, S, ILS_max)
                tempo_iter = time()
                delta = tempo_iter - tempo_inicio
                Tempo.tempo_decorrido += delta 
                tempo_inicio = time()   
                if  Tempo.tempo_decorrido > ILS_max:
                    return False
                j += 1  

def intra_route_swap(instance, S, ILS_max):
    tempo_inicio = time()
    for route_index in range(len(S)): # Para cada rota
        lenght_route = len(S[route_index])
        for i in range(1, lenght_route): # Seleciona um ponto da rota  
            for j in range(1, lenght_route): # Compara ele com todos os outros pontos
                if i < j: # Se o ponto não é o mesmo nem é a garagem   
                    cost = calculate_cost_swap(instance, S[route_index], S[route_index], i, j)                        
                    if cost < 0:
                        swap(S[route_index], S[route_index], i, j)  
                        tempo_iter = time()
                        delta = tempo_iter - tempo_inicio
                        Tempo.tempo_decorrido += delta 
                        tempo_inicio = time()   
                        update_solution(instance, S, cost,  Tempo.tempo_decorrido) 
                        if  Tempo.tempo_decorrido > ILS_max:
                            return False
                        return intra_route_swap(instance, S, ILS_max)
                    tempo_iter = time()
                    delta = tempo_iter - tempo_inicio
                    Tempo.tempo_decorrido += delta 
                    tempo_inicio = time()   
                    if  Tempo.tempo_decorrido > ILS_max:
                        return False

def intra_route_shift(instance, S, ILS_max):
    tempo_inicio = time()
    for route_index in range(len(S)):  # Para cada rota
        lenght_route = len(S[route_index])
        for i in range(1, lenght_route): # Seleciona um ponto da rota
            for j in range(1, lenght_route): # Compara ele com todos os outros pontos
                if i != j: # Se a posição não for a mesma e não for a garagem   
                    cost = calculate_cost_shift(instance, S[route_index], S[route_index], i, j)
                    if cost < 0:
                        shift(S[route_index], S[route_index], j, i)
                        tempo_iter = time()
                        delta = tempo_iter - tempo_inicio
                        Tempo.tempo_decorrido += delta 
                        tempo_inicio = time()   
                        update_solution(instance, S, cost,  Tempo.tempo_decorrido)  
                        if  Tempo.tempo_decorrido > ILS_max:
                            return False  
                        return intra_route_shift(instance, S, ILS_max)
                    tempo_iter = time()
                    delta = tempo_iter - tempo_inicio
                    Tempo.tempo_decorrido += delta 
                    tempo_inicio = time()   
                    if  Tempo.tempo_decorrido > ILS_max:
                        return False  
     
def inter_route_shift(instance, S, ILS_max):
    tempo_inicio = time()  
    for route_one_index in range(len(S)): # Para cada rota
        for i in range(1, len(S[route_one_index])): # Seleciona um ponto
            for route_two_index in range(len(S)): # Seleciona uma rota diferente da primeira selecionada
                if route_one_index != route_two_index and len(S[route_one_index]) > 2: # Deve haver pelo menos 3 pontos na rota
                    for j in range(1, len(S[route_two_index])): # Seleciona um ponto da segunda rota
                        cost = calculate_cost_shift(instance, S[route_one_index], S[route_two_index], i, j)
                        if cost < 0:           
                            shift(S[route_one_index], S[route_two_index], j, i)                               
                            tempo_iter = time()
                            delta = tempo_iter - tempo_inicio
                            Tempo.tempo_decorrido += delta 
                            tempo_inicio = time()   
                            update_solution(instance, S, cost, Tempo.tempo_decorrido)  
                            if  Tempo.tempo_decorrido > ILS_max:
                                return False 
                            return inter_route_shift(instance, S, ILS_max)    
                        tempo_iter = time()
                        delta = tempo_iter - tempo_inicio
                        Tempo.tempo_decorrido += delta 
                        tempo_inicio = time()   
                        if  Tempo.tempo_decorrido > ILS_max:
                            return False   

def inter_route_swap(instance, S, ILS_max):
    tempo_inicio = time()  
    for route_one_index in range(len(S)): # Para cada rota
        for i in range(1, len(S[route_one_index])): # Seleciona um ponto
            for route_two_index in range(len(S)): # Para cada rota, diferente da primeira selecionada
                if route_one_index != route_two_index:
                    for j in range(1, len(S[route_two_index])): # Seleciona um ponto da segunda rota
                        cost = calculate_cost_swap(instance, S[route_one_index], S[route_two_index], i, j)   
                        if cost < 0:
                            swap(S[route_one_index], S[route_two_index], i, j)   
                            tempo_iter = time()
                            delta = tempo_iter - tempo_inicio
                            Tempo.tempo_decorrido += delta 
                            tempo_inicio = time()   
                            update_solution(instance, S, cost, Tempo.tempo_decorrido) 
                            if  Tempo.tempo_decorrido > ILS_max:
                                return False 
                            return inter_route_swap(instance, S, ILS_max)
                        tempo_iter = time()
                        delta = tempo_iter - tempo_inicio
                        Tempo.tempo_decorrido += delta 
                        tempo_inicio = time()   
                        if  Tempo.tempo_decorrido > ILS_max:
                            return False 
                           
def local_search(instance):     
    routes = deepcopy(instance.current_solution)

    intra_route_swap(instance, routes)
    intra_route_shift(instance, routes)
    intra_route_2opt(instance, routes)
    inter_route_shift(instance, routes)  
    inter_route_swap(instance, routes)
    intra_route_2opt(instance, routes)

    return routes