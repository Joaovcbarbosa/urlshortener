from pickle import TRUE
import random
import math
import copy

def intra_route_swap(route, point_one_index, point_one_value, point_two_index, point_two_value):     
    route[point_one_index] = point_two_value    
    route[point_two_index] = point_one_value
    
    # point_b = route[route_index][point_one_index]['index']
    # point_a = route[route_index][point_one_index - 1]['index']
    # point_c = route[route_index][point_one_index + 1]['index'] if point_one_index + 1 < len(route[route_index]) else 0

    # point_e = route[route_index][point_two_index]['index']
    # point_d = route[route_index][point_two_index - 1]['index']
    # point_f = route[route_index][point_two_index + 1]['index'] if point_one_index + 1 < len(route[route_index]) else 0

    # cost = (instance.matrix[point_b][point_d] +
    #         instance.matrix[point_b][point_f] -
    #         instance.matrix[point_d][point_e] -
    #         instance.matrix[point_d][point_f] +
    #         instance.matrix[point_a][point_e] +
    #         instance.matrix[point_e][point_c] -
    #         instance.matrix[point_a][point_b] -
    #         instance.matrix[point_b][point_c])
    
    # instance.fo += cost                    
              
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

def SA(instance, T0, SAMax, alpha):
    S = copy.deepcopy(instance.current_solution)
    S_best = copy.deepcopy(S)
    fo_best = instance.current_solution_fo
    iterations = 0
    T = T0
    while T > 0.0001:
        while iterations < SAMax:
            iterations += 1
            S_neighbor = random_neighbor(S)
            fo_neighbor = instance.calculate_FO(S_neighbor)
            fo_S = instance.calculate_FO(S)
            delta = fo_neighbor - fo_S

            if delta <= 0:
                S = copy.deepcopy(S_neighbor)
                fo_S = fo_neighbor
                if fo_neighbor < fo_best:
                    S_best = copy.deepcopy(S_neighbor)
                    fo_best = fo_neighbor
                    instance.add_best_solution(fo_best, S_best)
                    instance.refresh(solution = S_best, calculate_fo_per_route = 1)
            else:
                x = random.uniform(0, 1)
                if x < math.exp(-delta/T):                    
                    S = copy.deepcopy(S_neighbor)    
                    fo_S = fo_neighbor            

        print(T, fo_S, fo_best)
        T = T * alpha
        iterations = 0





