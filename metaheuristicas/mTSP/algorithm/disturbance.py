from random import randint
from copy import deepcopy

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

def random_route(routes):
    # Sorteia uma das rotas que tenha pelo menos dois pontos além da garagem
    route_index = randint(0, len(routes) - 1)
    while len(routes[route_index]) <= 2:
        route_index = randint(0, len(routes) - 1)
    return route_index

def random_route_two(routes, route_one_index):    
    route_two_index = route_one_index
    while(route_one_index == route_two_index):
        route_two_index = randint(0, len(routes) - 1) # Sorteia uma rota, diferente da primeira
    return route_two_index

def random_point(point_one_index, routes, route_index):
    point_two_index = point_one_index
    while point_two_index == point_one_index:
        point_two_index = randint(1, len(routes[route_index]) - 1) # Sorteia um outro ponto, diferente do primeiro     
    point_two_value = routes[route_index][point_two_index]
    return point_two_index, point_two_value

def inter_route_shift_is_valid(routes, route_index):
    return len(routes[route_index]) > 2

def random_neighbor(routes):    
    routes_copy = deepcopy(routes)
    route_one_index = random_route(routes)
    point_one_index = randint(1, len(routes[route_one_index]) - 1) # Sorteia um ponto da rota selecionada
    point_one_value = routes[route_one_index][point_one_index]    
    option = randint(0, 3) # Sorteia uma das operações

    # Intra rota
    if option <= 1: 
        point_two_index, point_two_value = random_point(point_one_index, routes, route_one_index)  
        if option == 0:
            intra_route_swap(routes_copy[route_one_index], point_one_index, point_one_value, point_two_index, point_two_value)
            
        if option == 1:
            intra_route_shift(routes_copy[route_one_index], point_one_value, point_two_index)

    # Inter rota
    if option > 1:
        route_two_index = random_route_two(routes, route_one_index) 
        point_two_index = randint(1, len(routes[route_two_index]) - 1) # Sorteia um ponto da rota 2  
        point_two_value = routes[route_two_index][point_two_index]  
        
        if inter_route_shift_is_valid(routes, route_one_index) == False:
            option = 2        

        if option == 2:
            inter_route_swap(routes_copy[route_one_index], routes_copy[route_two_index], point_one_index, point_one_value, point_two_index, point_two_value)
        
        if option == 3:
            inter_route_shift(routes_copy[route_one_index], routes_copy[route_two_index], point_one_value, point_two_index)
        
    return routes_copy
