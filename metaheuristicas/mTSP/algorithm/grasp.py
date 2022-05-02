from random import sample
import copy

def generate_candidates(instance):
    candidates = copy.deepcopy(instance.points)
    del candidates[0]
    return candidates

def create_routes(instance):    
    routes = [[0] for item in range(instance.vehicles_quantity)] # Cria uma lista de listas baseado na quantidade de veículos
    candidates = generate_candidates(instance)

    fo = []
    for candidate in candidates:
        for route_index in range(len(routes)):
            route_length = len(routes[route_index])
            for point_index in range(route_length):
                candidate_index = instance.points.index(candidate)

                e = (instance.matrix[routes[route_index][point_index]][candidate_index] +
                     (instance.matrix[candidate_index][routes[route_index][point_index + 1]] if point_index + 1 != route_length else 0) -
                     (instance.matrix[routes[route_index][point_index]][routes[route_index][point_index + 1]] if point_index + 1 != route_length else 0))
                fo.append([e, candidate, route_index]) # Selecionar o de menor FO dentro da lista
    
        print(fo) 
    return routes
    
def GRASP(instance):
    route = create_routes(instance)
    return route

    





