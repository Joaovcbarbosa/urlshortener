from random import randint
from random import choice 
from copy import deepcopy
from instances import calculate_cost_remove
from semi_greedy_construction import greedy_random_construction
from semi_greedy_construction import greedy_miope_construction
from semi_greedy_construction import greedy_miope_restrict_construction

class ConstructionWeight:
    weight = [0, 1, 2]

def random_valid_route(routes):
    route_index = randint(0, len(routes) - 1)
    while len(routes[route_index]) <= 2:        
        route_index = randint(0, len(routes) - 1)

    return route_index

def remove_random(instance, routes, fo, removed_points):    
    route_index = random_valid_route(routes)
    point_index = randint(1, len(routes[route_index]) - 1)
    point = routes[route_index][point_index]
    removed_points.append(point["index"])
    cost = calculate_cost_remove(instance, routes[route_index], point_index)
    fo += cost     
    routes[route_index].remove(point)
   
    return routes, fo 

def remove_worst(instance, routes, fo, removed_points):
    worst = {
    "route_index": -1,
    "point_index": -1,
    "value": -1,
    "distance": -1
    }

    for route_index in range(len(routes)):
        if len(routes[route_index]) > 2:
            for point_index in range(1, len(routes[route_index])): 
                cost = calculate_cost_remove(instance, routes[route_index], point_index)
                if cost < worst["distance"] or worst["distance"] == -1:
                    worst["route_index"] = route_index
                    worst["point_index"] = point_index 
                    worst["value"] = routes[route_index][point_index] 
                    worst["distance"] = cost 

    routes[worst["route_index"]].remove(worst["value"])    
    removed_points.append(worst["value"]["index"])
    fo += worst["distance"]
    
    return routes, fo 

def readjust_weight(fo, fo_original, fo_best, option):    
    if fo < fo_original and fo > fo_best:
        ConstructionWeight.weight.append(option)
    if fo < fo_best:
        ConstructionWeight.weight.append(option)
        ConstructionWeight.weight.append(option)

def destruction_rebuild(instance, routes, fo, fo_best, betta_min, betta_max, RLC_length_in_percentage, alpha): 
    fo_original = fo 
    routes_copy = deepcopy(routes)  

    disturbance_percentage = int((randint(betta_min, betta_max) / 100) * len(instance.points))
    removed_points = []
    for j in range(disturbance_percentage):                         
        option = randint(0, 1) # Sorteia uma das operações      
        if option == 0:
            routes_copy, fo = remove_random(instance, routes_copy, fo, removed_points) 
        else:
            routes_copy, fo = remove_worst(instance, routes_copy, fo, removed_points)

    option = choice(ConstructionWeight.weight) # Sorteia uma das operações  
    if option == 0:
        routes_copy, fo = greedy_random_construction(instance, routes_copy, fo, removed_points)  
    if option == 1:
        routes_copy, fo = greedy_miope_construction(instance, routes_copy, fo, removed_points)  
    if option == 2:
        routes_copy, fo = greedy_miope_restrict_construction(instance, routes_copy, fo, removed_points, RLC_length_in_percentage, alpha)    
    
    readjust_weight(fo, fo_original, fo_best, option)
   
    return routes_copy, round(fo, 2)
