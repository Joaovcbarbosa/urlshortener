from random import randint
from random import choice 
from copy import deepcopy
from instances import calculate_cost_remove

def remove_random(instance, S, fo, removed_points):
    route_index = randint(0, len(S) - 1)
    while len(S[route_index]) <= 2:        
        route_index = randint(0, len(S) - 1)

    point_index = randint(1, len(S[route_index]) - 1)
    point = S[route_index][point_index]
    removed_points.append(point["index"])
    cost = calculate_cost_remove(instance, S[route_index], point_index)
    fo += cost     
    S[route_index].remove(point)
   
    return S, fo 

def remove_worst(instance, S, fo, removed_points):
    worst = {
    "route_index": -1,
    "point_index": -1,
    "value": -1,
    "distance": -1
    }

    for route_index in range(len(S)):
        if len(S[route_index]) > 2:
            for point_index in range(1, len(S[route_index])):                   

                cost = calculate_cost_remove(instance, S[route_index], point_index)

                if cost < worst["distance"] or worst["distance"] == -1:
                    worst["route_index"] = route_index
                    worst["point_index"] = point_index 
                    worst["value"] = S[route_index][point_index] 
                    worst["distance"] = cost 

    S[worst["route_index"]].remove(worst["value"])    
    removed_points.append(worst["value"]["index"])
    fo += worst["distance"]
    
    return S, fo 

def sort_by_distance(e):
    return e['distance']

def sort_by_fo(e):
  return e['cost']

def get_min_candidate(RCL):
    RCL.sort(key=sort_by_fo)     
    return RCL[0]
   
def calculate_cost(instance, routes, route_index, point_index, candidate_index, route_length):
    cost = instance.matrix[routes[route_index][point_index]['index']][candidate_index] # Custo do ponto até o candidato

    if point_index == route_length - 1: # Se o ponto selecionado é o último da lista
        cost += instance.matrix[candidate_index][0] # + Distância do candidato a garagem
        cost -= instance.matrix[routes[route_index][point_index]['index']][0] # - Distância do ponto corrente a garagem         
    else:
        cost += instance.matrix[candidate_index][routes[route_index][point_index + 1]['index']] # + Distância do candidato ao próximo ponto
        cost -= instance.matrix[routes[route_index][point_index]['index']][routes[route_index][point_index + 1]['index']]# - Distância do ponto corrente ao próximo ponto
    
    return round(cost, 2)

def candidate_values(cost, candidate, route_index, point_index):
    candidate_values = {}
    candidate_values['cost'] = cost
    candidate_values['candidate'] = candidate
    candidate_values['route_index'] = route_index
    candidate_values['point_index'] = point_index

    return candidate_values

def add_candidate_to_route(selected_candidate_values, routes):
    selected_candidate = selected_candidate_values['candidate']
    selected_candidate_route = selected_candidate_values['route_index']
    selected_candidate_new_index = selected_candidate_values['point_index'] + 1 
    routes[selected_candidate_route].insert(selected_candidate_new_index, selected_candidate) # Adiciona candidato na solução    
           
def greedy_random(instance, routes, fo, list_of_candidates):  
    candidate = choice(list_of_candidates)
    list_of_candidates.remove(candidate)
    candidate = instance.points[candidate]
    RCL = []

    for route_index in range(len(routes)): # Para cada rota
        route_length = len(routes[route_index])
        for point_index in range(route_length): # Para cada ponto da rota
            cost = calculate_cost(instance, routes, route_index, point_index, candidate['index'], route_length)                    
            RCL.append(candidate_values(cost, candidate, route_index, point_index))
        
    selected_candidate_values = get_min_candidate(RCL) # Seleciona candidato de forma parcialmente randômica
    add_candidate_to_route(selected_candidate_values, routes)  
    fo += selected_candidate_values['cost']   
  
    return routes, fo

def greedy_miope(instance, routes, fo, list_of_candidates): 
    RCL = []
    for candidate_index in range(len(list_of_candidates)):   
        candidate = instance.points[list_of_candidates[candidate_index]]        
        for route_index in range(len(routes)): # Para cada rota
            route_length = len(routes[route_index])
            for point_index in range(route_length): # Para cada ponto da rota
                if calculate_cost(instance, routes, route_index, point_index, candidate['index'], route_length) == 0:
                    print('a')
                cost = calculate_cost(instance, routes, route_index, point_index, candidate['index'], route_length)                    
                RCL.append(candidate_values(cost, candidate, route_index, point_index))
        
    selected_candidate_values = get_min_candidate(RCL) 
    list_of_candidates.remove(selected_candidate_values['candidate']['index'])
    add_candidate_to_route(selected_candidate_values, routes)  
    fo += selected_candidate_values['cost']   
  
    return routes, fo

def destruction_rebuild(instance, S, fo, betta_min, betta_max):   

    disturbance_percentage = int((randint(betta_min, betta_max) / 100) * len(instance.points))
    removed_points = []
    for j in range(disturbance_percentage):                         
        option = randint(0, 1) # Sorteia uma das operações        
        if option == 0:
            S, fo = remove_random(instance, S, fo, removed_points) 
        else:
            S, fo = remove_worst(instance, S, fo, removed_points)
        if round(fo, 2) != instance.calculate_FO(S):
            fo = instance.calculate_FO(S)

    for i in range(len(removed_points)):
        option = randint(0, 1) # Sorteia uma das operações        
        if option == 0:
            S, fo = greedy_random(instance, S, fo, removed_points) 
        if option == 1:
            S, fo = greedy_miope(instance, S, fo, removed_points)  
      
    return S, round(fo, 2)
