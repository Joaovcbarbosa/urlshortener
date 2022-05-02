import random
import math
import copy
import construction

def intra_route_swap(route, point_one_index, point_one_value, point_two_index, point_two_value):     
    route[point_one_index] = point_two_value
    route[point_two_index] = point_one_value
              
def intra_route_shift(route, point_one_value, point_two_index):  
    route.remove(point_one_value)
    route.insert(point_two_index, point_one_value)

def inter_route_swap(route_one, route_two, point_one_index, point_one_value, point_two_index, point_two_value):  
    route_one[point_one_index] = point_two_value
    route_two[point_two_index] = point_one_value

def inter_route_shift(route_one, route_two, point_one_value, point_two_index): 
    route_one.remove(point_one_value)
    route_two.insert(point_two_index, point_one_value)

def random_neighbor(routes):    
    routes_copy = copy.deepcopy(routes)
    option = random.randint(0, 3) # Sorteia uma das operações

    # Sorteia uma das rotas que tenha pelo menos dois pontos além da garagem
    route_index = random.randint(0, len(routes) - 1)
    while len(routes[route_index]) <= 2:
        route_index = random.randint(0, len(routes) - 1)

    point_one_index = random.randint(1, len(routes[route_index]) - 1) # Sorteia um ponto da rota selecionada
    point_one_value = routes[route_index][point_one_index]
    
    # Intra rota
    if option <= 1: 
        point_two_index = point_one_index
        while point_two_index == point_one_index:
            point_two_index = random.randint(1, len(routes[route_index]) - 1) # Sorteia um outro ponto, diferente do primeiro     
        point_two_value = routes[route_index][point_two_index]

        if option == 0:
            intra_route_swap(routes_copy[route_index], point_one_index, point_one_value, point_two_index, point_two_value)
            
        if option == 1:
            intra_route_shift(routes_copy[route_index], point_one_value, point_two_index)
    
    # Inter rota
    if option > 1:
        route_two_index = route_index
        while(route_index == route_two_index):
            route_two_index = random.randint(0, len(routes) - 1) # Sorteia uma rota, diferente da primeira

        # Caso a rota 2 sorteada só tenha a garagem, então só é possível fazer o shift
        if len(routes[route_two_index]) <= 1:
            point_two_index = 1
            option = 3
        else:
            point_two_index = random.randint(1, len(routes[route_two_index]) - 1) # Sorteia um ponto da rota 2  
            point_two_value = routes[route_two_index][point_two_index]          

        if option == 2:
            inter_route_swap(routes_copy[route_index], routes_copy[route_two_index], point_one_index, point_one_value, point_two_index, point_two_value)
        
        if option == 3:
            inter_route_shift(routes_copy[route_index], routes_copy[route_two_index], point_one_value, point_two_index)
    
    return routes_copy

def calculate_FO(instance, routes):
    fo = 0
    for route in routes: # Para cada rota   
        if len(route) > 1:     
            fo += instance.matrix[0][route[1]] # Distância da garagem ao primeiro ponto da rota
            for point_index in range(len(route)): # Para cada ponto
                if point_index > 0 and point_index < len(route) - 1: # Se o index do ponto não for a garagem nem o último ponto
                    fo += instance.matrix[route[point_index]][route[point_index+1]] # Distancia entre o ponto e o próximo ponto
                elif point_index == len(route) - 1: # Se for o último ponto da rota
                    fo += instance.matrix[route[point_index]][0] # Distância entre o ponto e a garagem        
    return fo

def SA(instance, S, T0, SAMax, alpha):
    S_best = copy.deepcopy(S)
    fo_best = calculate_FO(instance, S)
    iterations = 0
    T = T0
    while T > 0.0001:
        while iterations < SAMax:
            iterations += 1
            S_neighbor = copy.deepcopy(random_neighbor(S))
            fo_neighbor = calculate_FO(instance, S_neighbor)
            fo_S = calculate_FO(instance, S)
            delta = fo_neighbor - fo_S

            if delta <= 0:
                S = copy.deepcopy(S_neighbor)
                fo_S = fo_neighbor
                if fo_neighbor < fo_best:
                    S_best = copy.deepcopy(S_neighbor)
                    fo_best = fo_neighbor
                    instance.add_best_solution(fo_best, S_best)
            else:
                x = random.uniform(0, 1)
                if x < math.exp(-delta/T):                    
                    S = copy.deepcopy(S_neighbor)    
                    fo_S = fo_neighbor            

        print(T, fo_S, fo_best)
        T = T * alpha
        iterations = 0
    
    instance.print_solutions()
    return S_best

    





