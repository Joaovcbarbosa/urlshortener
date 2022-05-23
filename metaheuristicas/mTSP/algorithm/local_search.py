from copy import deepcopy

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
    instance.current_solution_fo += cost
    instance.current_solution = routes
    instance.add_best_solution(instance.current_solution_fo, routes)

def calculate_cost_swap(instance, routes, route_one_index, route_two_index, point_one_index, point_two_index):
    i = routes[route_one_index][point_one_index]["index"]
    i_front = routes[route_one_index][point_one_index + 1 if point_one_index + 1 < len(routes[route_one_index]) else 0]["index"]
    i_back = routes[route_one_index][point_one_index - 1]["index"]
    j = routes[route_two_index][point_two_index]["index"]
    j_front = routes[route_two_index][point_two_index + 1 if point_two_index + 1 < len(routes[route_two_index]) else 0]["index"]
    j_back = routes[route_two_index][point_two_index - 1]["index"]
    
    if point_one_index + 1 == point_two_index:
        cost = (- instance.matrix[i_back][i]
                - instance.matrix[j][j_front]
                + instance.matrix[i_back][j]
                + instance.matrix[i][j_front])
    else:
        cost = (- instance.matrix[i_back][i]
                - instance.matrix[i][i_front]
                - instance.matrix[j_back][j]
                - instance.matrix[j][j_front]
                + instance.matrix[i_back][j]
                + instance.matrix[j][i_front]
                + instance.matrix[j_back][i]
                + instance.matrix[i][j_front])

    return cost 

def calculate_cost_shift(instance, routes, route_one_index, route_two_index, point_one_index, point_two_index):
    i = routes[route_one_index][point_one_index]["index"]
    i_front = routes[route_one_index][point_one_index + 1 if point_one_index + 1 < len(routes[route_one_index]) else 0]["index"]
    i_back = routes[route_one_index][point_one_index - 1]["index"]
    j_front = routes[route_two_index][point_two_index]["index"]
    j_back = routes[route_two_index][point_two_index - 1]["index"]

    cost = (- instance.matrix[i_back][i]
            - instance.matrix[i][i_front]
            + instance.matrix[i_back][i_front]
            + instance.matrix[j_back][i]
            + instance.matrix[i][j_front]
            - instance.matrix[j_back][j_front])

    return cost

def intra_route_swap(instance, routes):
    for route_index in range(len(routes)): # Para cada rota
        lenght_route = len(routes[route_index])
        for point_one_index in range(lenght_route): # Seleciona um ponto da rota
            if point_one_index > 0:
                for point_two_index in range(lenght_route): # Compara ele com todos os outros pontos
                    if point_one_index < point_two_index and point_two_index > 0: # Se o ponto não é o mesmo nem é a garagem   
                        cost = calculate_cost_swap(instance, routes, route_index, route_index, point_one_index, point_two_index)                        
                        if cost < 0:
                            swap(routes=routes, route_one_index=route_index, route_two_index=route_index, 
                                point_one_index=point_one_index, point_two_index=point_two_index)  
                            update_solution(instance, routes, cost)
                            intra_route_swap(instance, routes)
                            break   
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
                        cost = calculate_cost_shift(instance, routes, route_index, route_index, point_one_index, point_two_index)
                        if cost < 0:
                            shift(routes=routes, route_one_index=route_index, route_two_index=route_index,
                                  insert_index=point_two_index, point_index=point_one_index)
                            update_solution(instance, routes, cost)     
                            intra_route_shift(instance, routes)
                            break                       
                else:
                    continue
            break
     
def inter_route_shift(instance, routes):
    for route_one_index in range(len(routes)): # Para cada rota
        for route_one_point_index in range(len(routes[route_one_index])): # Seleciona um ponto
            if route_one_point_index > 0:
                for route_two_index in range(len(routes)): # Seleciona uma rota diferente da primeira selecionada
                    if route_one_index != route_two_index and len(routes[route_one_index]) > 2: # Deve haver pelo menos 3 pontos na rota
                        for route_two_point_index in range(len(routes[route_two_index])): # Seleciona um ponto da segunda rota
                            if route_two_point_index > 0: 
                                cost = calculate_cost_shift(instance, routes, route_one_index, route_two_index, route_one_point_index, route_two_point_index)
                                if cost < 0:           
                                    shift(routes=routes, route_one_index=route_one_index, route_two_index=route_two_index,
                                        insert_index=route_two_point_index, point_index=route_one_point_index)                               
                                    update_solution(instance, routes, cost)   
                                    inter_route_shift(instance, routes)                                    
                                    break
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
                                cost = calculate_cost_swap(instance, routes, route_one_index, route_two_index, route_one_point_index, route_two_point_index)   

                                if cost < 0:
                                    swap(routes=routes, route_one_index=route_one_index, route_two_index=route_two_index, 
                                        point_one_index=route_one_point_index, point_two_index=route_two_point_index)   
                                    update_solution(instance, routes, cost)                        
                                    inter_route_swap(instance, routes)
                                    break
                        else:
                            continue
                        break
                else:
                    continue
                break

def local_search(instance):     
    routes = deepcopy(instance.current_solution)
    intra_route_swap(instance, routes)
    intra_route_shift(instance, routes)
    inter_route_shift(instance, routes)  
    inter_route_swap(instance, routes)

    return routes