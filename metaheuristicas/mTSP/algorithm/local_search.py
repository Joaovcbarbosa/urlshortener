import copy
from random import randint

def intra_route_swap(routes):
    
    route_index = randint(0, len(routes) - 1)
    point_one_index = randint(1, len(routes[route_index]) - 1)
    point_two_index = point_one_index

    while(point_one_index == point_two_index):
        point_two_index = randint(1, len(routes[route_index]) - 1)

    aux_point_one = routes[route_index][point_one_index]
    aux_point_two = routes[route_index][point_two_index]

    routes[route_index][point_one_index] = aux_point_two
    routes[route_index][point_two_index] = aux_point_one
          
def intra_route_shift(routes):    
    route_index = randint(0, len(routes) - 1)
    point_one_index = randint(1, len(routes[route_index]) - 1)
    point_two_index = point_one_index

    while(point_one_index == point_two_index):
        point_two_index = randint(1, len(routes[route_index]) - 1)

    aux_point_one = routes[route_index][point_one_index]

    routes[route_index].remove(aux_point_one)
    routes[route_index].insert(point_two_index, aux_point_one)

def inter_route_swap(routes):    
    route_one_index = randint(0, len(routes) - 1)
    route_two_index = route_one_index

    while(route_one_index == route_two_index):
        route_two_index = randint(0, len(routes) - 1)

    point_one_index = randint(1, len(routes[route_one_index]) - 1)
    point_two_index = randint(1, len(routes[route_two_index]) - 1)

    aux_point_one = routes[route_one_index][point_one_index]
    aux_point_two = routes[route_two_index][point_two_index]

    routes[route_one_index][point_one_index] = aux_point_two
    routes[route_two_index][point_two_index] = aux_point_one

def inter_route_shift(routes):    
    route_one_index = randint(0, len(routes) - 1)
    route_two_index = route_one_index

    while(route_one_index == route_two_index):
        route_two_index = randint(0, len(routes) - 1)

    point_one_index = randint(1, len(routes[route_one_index]) - 1)
    point_two_index = randint(1, len(routes[route_two_index]) - 1)

    aux_point_one = routes[route_one_index][point_one_index]
    
    routes[route_one_index].remove(aux_point_one)
    routes[route_two_index].insert(point_two_index, aux_point_one)

def random_neighboor(routes):
    
    routes_copy = copy.deepcopy(routes)

    option = randint(0, 3)
    
    if option == 0:
        intra_route_swap(routes_copy)
        
    if option == 1:
        intra_route_shift(routes_copy)
    
    if option == 2:
        inter_route_swap(routes_copy)
    
    if option == 3:
        inter_route_shift(routes_copy)

    return routes_copy