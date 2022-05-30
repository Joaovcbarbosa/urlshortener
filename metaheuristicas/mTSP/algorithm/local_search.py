from copy import deepcopy
from instances import calculate_cost_swap
from instances import calculate_cost_shift 
from instances import calculate_cost_2opt 

def swap(routes, route_one_index, route_two_index, point_one_index, point_two_index):
    point_one = routes[route_one_index][point_one_index]
    point_two = routes[route_two_index][point_two_index]

    routes[route_one_index][point_one_index] = point_two 
    routes[route_two_index][point_two_index] = point_one 

def shift(routes, route_one_index, route_two_index, insert_index, point_index):
    point = routes[route_one_index][point_index]
    routes[route_one_index].remove(point)
    routes[route_two_index].insert(insert_index, point)

def update_solution(instance, routes, cost):
    instance.current_solution_fo = round(instance.current_solution_fo + cost, 2)
    instance.current_solution = routes
    instance.add_best_solution(instance.current_solution_fo, instance.current_solution)

def two_opt(route, i, j): 
    new_route = deepcopy(route)
    new_route = new_route[i:j+1]
    new_route.reverse()
    route[i:j+1] = new_route 

def intra_route_2opt(instance, routes):
    for route_index in range(len(routes)):  # Para cada rota
        lenght_route = len(routes[route_index])
        for point_one_index in range(1, lenght_route - 2): # Seleciona um ponto da rota
            point_two_index = point_one_index + 2
            while point_two_index < lenght_route:
                cost = calculate_cost_2opt(instance, routes[route_index], point_one_index - 1, point_two_index - 1)
                if cost < 0:
                    two_opt(routes[route_index], point_one_index, point_two_index - 1)
                    update_solution(instance, routes, cost)     
                    return intra_route_2opt(instance, routes)
                point_two_index += 1  

def intra_route_swap(instance, routes):
    for route_index in range(len(routes)): # Para cada rota
        lenght_route = len(routes[route_index])
        for point_one_index in range(1, lenght_route): # Seleciona um ponto da rota  
            for point_two_index in range(1, lenght_route): # Compara ele com todos os outros pontos
                if point_one_index < point_two_index: # Se o ponto não é o mesmo nem é a garagem   
                    cost = calculate_cost_swap(instance, routes, route_index, route_index, point_one_index, point_two_index)                        
                    if cost < 0:
                        swap(routes=routes, route_one_index=route_index, route_two_index=route_index, 
                            point_one_index=point_one_index, point_two_index=point_two_index)  
                        update_solution(instance, routes, cost)
                        return intra_route_swap(instance, routes)

def intra_route_shift(instance, routes):
    for route_index in range(len(routes)):  # Para cada rota
        lenght_route = len(routes[route_index])
        for point_one_index in range(1, lenght_route): # Seleciona um ponto da rota
            for point_two_index in range(1, lenght_route): # Compara ele com todos os outros pontos
                if point_one_index != point_two_index: # Se a posição não for a mesma e não for a garagem   
                    cost = calculate_cost_shift(instance, routes, route_index, route_index, point_one_index, point_two_index)
                    if cost < 0:
                        shift(routes=routes, route_one_index=route_index, route_two_index=route_index,
                                insert_index=point_two_index, point_index=point_one_index)
                        update_solution(instance, routes, cost)     
                        return intra_route_shift(instance, routes)
     
def inter_route_shift(instance, routes):
    for route_one_index in range(len(routes)): # Para cada rota
        for route_one_point_index in range(1, len(routes[route_one_index])): # Seleciona um ponto
            for route_two_index in range(len(routes)): # Seleciona uma rota diferente da primeira selecionada
                if route_one_index != route_two_index and len(routes[route_one_index]) > 2: # Deve haver pelo menos 3 pontos na rota
                    for route_two_point_index in range(1, len(routes[route_two_index])): # Seleciona um ponto da segunda rota
                        cost = calculate_cost_shift(instance, routes, route_one_index, route_two_index, route_one_point_index, route_two_point_index)
                        if cost < 0:           
                            shift(routes=routes, route_one_index=route_one_index, route_two_index=route_two_index,
                                insert_index=route_two_point_index, point_index=route_one_point_index)                               
                            update_solution(instance, routes, cost)   
                            return inter_route_shift(instance, routes)       

def inter_route_swap(instance, routes):
    for route_one_index in range(len(routes)): # Para cada rota
        for route_one_point_index in range(1, len(routes[route_one_index])): # Seleciona um ponto
            for route_two_index in range(len(routes)): # Para cada rota, diferente da primeira selecionada
                if route_one_index != route_two_index:
                    for route_two_point_index in range(1, len(routes[route_two_index])): # Seleciona um ponto da segunda rota
                        cost = calculate_cost_swap(instance, routes, route_one_index, route_two_index, route_one_point_index, route_two_point_index)   
                        if cost < 0:
                            swap(routes=routes, route_one_index=route_one_index, route_two_index=route_two_index, 
                                point_one_index=route_one_point_index, point_two_index=route_two_point_index)   
                            update_solution(instance, routes, cost) 
                            return inter_route_swap(instance, routes)
                           
def local_search(instance):     
    routes = deepcopy(instance.current_solution)

    intra_route_swap(instance, routes)
    intra_route_shift(instance, routes)
    intra_route_2opt(instance, routes)
    inter_route_shift(instance, routes)  
    inter_route_swap(instance, routes)
    intra_route_2opt(instance, routes)

    return routes