import copy

def swap(routes, route_one_index, route_two_index, point_one_index, point_two_index):
    point_one = routes[route_one_index][point_one_index]
    point_two = routes[route_two_index][point_two_index]

    routes[route_one_index][point_one_index] = point_two 
    routes[route_two_index][point_two_index] = point_one 

def shift(routes, route_one_index, route_two_index, insert_index, point_index):
    point = routes[route_one_index][point_index]
    routes[route_one_index].remove(point)
    routes[route_two_index].insert(insert_index, point)

def update_solution(instance, routes, route_index_one, route_index_two=-1):
    instance.current_solution_fo_per_route[route_index_one] = instance.calculate_fo_per_route(routes[route_index_one])
    if route_index_two != -1:
        instance.current_solution_fo_per_route[route_index_two] = instance.calculate_fo_per_route(routes[route_index_two])
    instance.current_solution_fo = sum(instance.current_solution_fo_per_route)  
    instance.current_solution = routes
    instance.add_best_solution(instance.current_solution_fo, routes)

def isBetter(instance, routes, route_one_index, route_two_index=-1):
    route_one_fo = instance.calculate_fo_per_route(routes[route_one_index])
    if route_two_index == -1:
        return route_one_fo < instance.current_solution_fo_per_route[route_one_index]
    old_routes_fo = instance.current_solution_fo_per_route[route_one_index] + instance.current_solution_fo_per_route[route_two_index]                            
    route_two_fo = instance.calculate_fo_per_route(routes[route_two_index])
    new_routes_fo = route_one_fo + route_two_fo
    return new_routes_fo < old_routes_fo

def intra_route_swap(instance, routes):
    for route_index in range(len(routes)): # Para cada rota
        lenght_route = len(routes[route_index])
        for point_one_index in range(lenght_route): # Seleciona um ponto da rota
            if point_one_index > 0:
                for point_two_index in range(lenght_route): # Compara ele com todos os outros pontos
                    if point_one_index != point_two_index and point_two_index > 0: # Se o ponto não é o mesmo nem é a garagem                    
                        swap(routes=routes, route_one_index=route_index, route_two_index=route_index, 
                             point_one_index=point_one_index, point_two_index=point_two_index)                        
                        if isBetter(instance, routes, route_index): 
                            update_solution(instance, routes, route_index)
                            intra_route_swap(instance, routes)
                            break
                        else: # Reverte o SWAP                      
                            swap(routes=routes, route_one_index=route_index, route_two_index=route_index, 
                                 point_one_index=point_one_index, point_two_index=point_two_index)
                else:
                    continue
                break
         
def intra_route_shift(instance, routes):
    for route_index in range(len(routes)):  # Para cada rota
        lenght_route = len(routes[route_index])
        for point_one_index in range(lenght_route): # Seleciona um ponto da rota
            if point_one_index > 0:
                for point_two_index in range(lenght_route): # Compara ele com todos os outros pontos
                    if point_one_index != point_two_index and point_two_index > 0: # Se a posição não for a mesma e não for a garagem                       
                        shift(routes=routes, route_one_index=route_index, route_two_index=route_index,
                              insert_index=point_two_index, point_index=point_one_index)
                        if isBetter(instance, routes, route_index): 
                            update_solution(instance, routes, route_index)
                            intra_route_shift(instance, routes)
                            break
                        else: # Reverte o shift
                            shift(routes=routes, route_one_index=route_index, route_two_index=route_index,
                                  insert_index=point_one_index, point_index=point_two_index)
                else:
                    continue
            break
     

def inter_route_shift(instance, routes):
    for route_one_index in range(len(routes)): # Para cada rota
        for route_one_point_index in range(len(routes[route_one_index])): # Seleciona um ponto
            if route_one_point_index > 0:
                for route_two_index in range(len(routes)): # Seleciona uma rota diferente da primeira selecionada
                    if route_one_index != route_two_index:
                        for route_two_point_index in range(len(routes[route_two_index])): # Seleciona um ponto da segunda rota
                            if route_two_point_index > 0:            
                                shift(routes=routes, route_one_index=route_one_index, route_two_index=route_two_index,
                                      insert_index=route_two_point_index, point_index=route_one_point_index)
                                if isBetter(instance, routes, route_one_index, route_two_index): 
                                    update_solution(instance, routes, route_one_index, route_two_index)
                                    inter_route_shift(instance, routes)                                    
                                    break
                                else: # Reverte o SHIFT   
                                    shift(routes=routes, route_one_index=route_two_index, route_two_index=route_one_index,
                                        insert_index=route_one_point_index, point_index=route_two_point_index)
                        else:
                            continue
                        break
                else:
                    continue
                break
            
def inter_route_swap(instance, routes):
    for route_one_index in range(len(routes)): # Para cada rota
        for route_one_point_index in range(len(routes[route_one_index])): # Seleciona um ponto
            if route_one_point_index > 0:
                for route_two_index in range(len(routes)): # Para cada rota, diferente da primeira selecionada
                    if route_one_index != route_two_index:
                        for route_two_point_index in range(len(routes[route_two_index])): # Seleciona um ponto da segunda rota
                            if route_two_point_index > 0: 
                                swap(routes=routes, route_one_index=route_one_index, route_two_index=route_two_index, 
                                     point_one_index=route_one_point_index, point_two_index=route_two_point_index)
                                if isBetter(instance, routes, route_one_index, route_two_index): 
                                    update_solution(instance, routes, route_one_index, route_two_index)
                                    inter_route_swap(instance, routes)
                                    break
                                else: # Reverte o SWAP
                                    swap(routes=routes, route_one_index=route_one_index, route_two_index=route_two_index, 
                                         point_one_index=route_one_point_index, point_two_index=route_two_point_index)
                        else:
                            continue
                        break
                else:
                    continue
                break

def local_search(instance):     
    routes = copy.deepcopy(instance.current_solution)
    inter_route_swap(instance, routes)
    inter_route_shift(instance, routes)  
    intra_route_swap(instance, routes)
    intra_route_shift(instance, routes)

    return routes