import copy

def intra_route_swap(instance, routes):
    for route_index in range(len(routes)): # Para cada rota
        lenght_route = len(routes[route_index])
        for point_one_index in range(lenght_route): # Seleciona um ponto da rota
            if point_one_index > 0:
                for point_two_index in range(lenght_route): # Compara ele com todos os outros pontos
                    if point_one_index != point_two_index and point_two_index > 0: # Se o ponto não é o mesmo nem é a garagem
                        aux_point_one = routes[route_index][point_one_index]
                        aux_point_two = routes[route_index][point_two_index]

                        # Executa o SWAP
                        routes[route_index][point_one_index] = aux_point_two
                        routes[route_index][point_two_index] = aux_point_one

                        value_of_new_fo_per_route = instance.calculate_fo_per_route(routes[route_index])

                        if value_of_new_fo_per_route < instance.current_solution_fo_per_route[route_index]: # Se o valor do FO novo é menor que o antigo
                            # Atualiza FO
                            instance.current_solution_fo_per_route[route_index] = value_of_new_fo_per_route
                            instance.current_solution_fo = sum(instance.current_solution_fo_per_route)  
                            instance.current_solution = routes
                            instance.add_best_solution(instance.current_solution_fo, routes)
                            intra_route_swap(instance, routes)
                            break
                        else: # Se não for, reverte o SWAP
                            routes[route_index][point_one_index] = aux_point_one
                            routes[route_index][point_two_index] = aux_point_two
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
                        aux_point_one = routes[route_index][point_one_index]

                        # Executa o shift
                        routes[route_index].remove(aux_point_one)
                        routes[route_index].insert(point_two_index, aux_point_one)

                        value_of_new_fo_per_route = instance.calculate_fo_per_route(routes[route_index])
                        if value_of_new_fo_per_route < instance.current_solution_fo_per_route[route_index]: # Se o valor do FO novo é menor que o antigo
                            # Atualiza FO
                            instance.current_solution_fo_per_route[route_index] = value_of_new_fo_per_route
                            instance.current_solution_fo = sum(instance.current_solution_fo_per_route) 
                            instance.current_solution = routes
                            instance.add_best_solution(instance.current_solution_fo, routes)
                            intra_route_shift(instance, routes)
                            break
                        else: # Se não for, reverte o shift
                            routes[route_index].remove(aux_point_one)
                            routes[route_index].insert(point_one_index, aux_point_one)
                else:
                    continue
            break
     
  
def inter_route_swap(instance, routes):
    for route_one_index in range(len(routes)): # Para cada rota
        for route_one_point_index in range(len(routes[route_one_index])): # Seleciona um ponto
            if route_one_point_index > 0:
                aux_route_one_point = routes[route_one_index][route_one_point_index]
                for route_two_index in range(len(routes)): # Para cada rota, diferente da primeira selecionada
                    if route_one_index != route_two_index:
                        for route_two_point_index in range(len(routes[route_two_index])): # Seleciona um ponto da segunda rota
                            if route_two_point_index > 0:                      
                                aux_route_two_point = routes[route_two_index][route_two_point_index]

                                # Executa o SWAP
                                routes[route_one_index][route_one_point_index] = aux_route_two_point
                                routes[route_two_index][route_two_point_index] = aux_route_one_point

                                # Calcula o valor da nova FO
                                value_of_fo_per_route_old = instance.current_solution_fo_per_route[route_one_index] + instance.current_solution_fo_per_route[route_two_index]
                                value_of_route_one_new_fo_per_route = instance.calculate_fo_per_route(routes[route_one_index]) 
                                value_of_route_two_new_fo_per_route = instance.calculate_fo_per_route(routes[route_two_index])
                                value_of_sum_new_fo_per_route = value_of_route_one_new_fo_per_route + value_of_route_two_new_fo_per_route

                                if value_of_sum_new_fo_per_route < value_of_fo_per_route_old: # Se a nova FO é melhor que a antiga
                                    # Atualiza FO
                                    instance.current_solution_fo_per_route[route_one_index] = value_of_route_one_new_fo_per_route
                                    instance.current_solution_fo_per_route[route_two_index] = value_of_route_two_new_fo_per_route                                    
                                    instance.current_solution_fo = sum(instance.current_solution_fo_per_route)  
                                    instance.current_solution = routes
                                    instance.add_best_solution(instance.current_solution_fo, routes)
                                    inter_route_swap(instance, routes)
                                    break
                                else: # Se não diminuiu a FO, reverte o SWAP
                                    routes[route_one_index][route_one_point_index] = aux_route_one_point
                                    routes[route_two_index][route_two_point_index] = aux_route_two_point              
                        else:
                            continue
                        break
                else:
                    continue
                break


def inter_route_shift(instance, routes):
    for route_one_index in range(len(routes)): # Para cada rota
        for route_one_point_index in range(len(routes[route_one_index])): # Seleciona um ponto
            if route_one_point_index > 0:
                aux_point = routes[route_one_index][route_one_point_index]
                for route_two_index in range(len(routes)): # Seleciona uma rota diferente da primeira selecionada
                    if route_one_index != route_two_index:
                        for route_two_point_index in range(len(routes[route_two_index])): # Seleciona um ponto da segunda rota
                            if route_two_point_index > 0:            

                                # Executa o SHIFT
                                routes[route_one_index].remove(aux_point)
                                routes[route_two_index].insert(route_two_point_index, aux_point)

                                # Calcula o valor da nova FO
                                value_of_fo_per_route_old = instance.current_solution_fo_per_route[route_one_index] + instance.current_solution_fo_per_route[route_two_index]
                                value_of_route_one_new_fo_per_route = instance.calculate_fo_per_route(routes[route_one_index]) 
                                value_of_route_two_new_fo_per_route = instance.calculate_fo_per_route(routes[route_two_index])
                                value_of_sum_new_fo_per_route = value_of_route_one_new_fo_per_route + value_of_route_two_new_fo_per_route
                                
                                if value_of_sum_new_fo_per_route < value_of_fo_per_route_old: # Se a nova FO é melhor que a antiga
                                    # Atualiza FO
                                    instance.current_solution_fo_per_route[route_one_index] = value_of_route_one_new_fo_per_route
                                    instance.current_solution_fo_per_route[route_two_index] = value_of_route_two_new_fo_per_route
                                    instance.current_solution_fo = sum(instance.current_solution_fo_per_route) 
                                    instance.current_solution = routes
                                    instance.add_best_solution(instance.current_solution_fo, routes)
                                    inter_route_shift(instance, routes)                                    
                                    break
                                else: # Se não diminuiu a FO, reverte o SHIFT
                                    routes[route_two_index].remove(aux_point)  
                                    routes[route_one_index].insert(route_one_point_index, aux_point)      
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