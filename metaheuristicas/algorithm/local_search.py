import construction

def intra_route_swap(instance, routes):
    for route_index in range(len(routes)):
        lenght_route = len(routes[route_index])
        for point_one_index in range(lenght_route):
            for point_two_index in range(lenght_route):
                if point_one_index != point_two_index and point_one_index > 0 and point_two_index > 0:
                    aux_point_one = routes[route_index][point_one_index]
                    aux_point_two = routes[route_index][point_two_index]
                    routes[route_index][point_one_index] = aux_point_two
                    routes[route_index][point_two_index] = aux_point_one
                    value_of_new_greedy_function = construction.calculate_greedy_function(instance, routes[route_index])
                    if value_of_new_greedy_function < instance.greedy_function[route_index]:
                        instance.greedy_function[route_index] = value_of_new_greedy_function
                        intra_route_swap(instance, routes)
                        break
                    else:
                        routes[route_index][point_one_index] = aux_point_one
                        routes[route_index][point_two_index] = aux_point_two
            else:
                continue
            break

    instance.fo = sum(instance.greedy_function)  
    
def intra_route_shift(instance, routes):
    for route_index in range(len(routes)):
        lenght_route = len(routes[route_index])
        for point_one_index in range(lenght_route):
            for point_two_index in range(lenght_route):
                if point_one_index != point_two_index and point_one_index > 0 and point_two_index > 0:
                    aux_point_one = routes[route_index][point_one_index]
                    routes[route_index].remove(aux_point_one)
                    routes[route_index].insert(point_two_index, aux_point_one)

                    value_of_new_greedy_function = construction.calculate_greedy_function(instance, routes[route_index])
                    if value_of_new_greedy_function < instance.greedy_function[route_index]:
                        instance.greedy_function[route_index] = value_of_new_greedy_function
                        intra_route_shift(instance, routes)
                        break
                    else:
                        routes[route_index].remove(aux_point_one)
                        routes[route_index].insert(point_one_index, aux_point_one)
            else:
                continue
            break
    
    instance.fo = sum(instance.greedy_function)  
  
def inter_route_swap(instance, routes):
    for route_one_index in range(len(routes)):
        for route_one_point_index in range(len(routes[route_one_index])):
            if route_one_point_index > 0:
                aux_route_one_point = routes[route_one_index][route_one_point_index]
                for route_two_index in range(len(routes)):
                    if route_one_index != route_two_index:
                        for route_two_point_index in range(len(routes[route_two_index])):    
                            if route_two_point_index > 0:                      
                                aux_route_two_point = routes[route_two_index][route_two_point_index]
                                if aux_route_one_point != aux_route_two_point:
                                    routes[route_one_index][route_one_point_index] = aux_route_two_point
                                    routes[route_two_index][route_two_point_index] = aux_route_one_point

                                    value_of_greedy_function_old = instance.greedy_function[route_one_index] + instance.greedy_function[route_two_index]
                                    value_of_route_one_new_greedy_function = construction.calculate_greedy_function(instance, routes[route_one_index]) 
                                    value_of_route_two_new_greedy_function = construction.calculate_greedy_function(instance, routes[route_two_index])
                                    value_of_sum_new_greedy_function = value_of_route_one_new_greedy_function + value_of_route_two_new_greedy_function

                                    if value_of_sum_new_greedy_function < value_of_greedy_function_old:
                                        instance.greedy_function[route_one_index] = value_of_route_one_new_greedy_function
                                        instance.greedy_function[route_two_index] = value_of_route_two_new_greedy_function
                                        inter_route_swap(instance, routes)
                                        break
                                    else:
                                        routes[route_one_index][route_one_point_index] = aux_route_one_point
                                        routes[route_two_index][route_two_point_index] = aux_route_two_point              
                        else:
                            continue
                        break
                else:
                    continue
                break

    instance.fo = sum(instance.greedy_function)  

def inter_route_shift(instance, routes):
    for route_one_index in range(len(routes)):
        for route_one_point_index in range(len(routes[route_one_index])):
            if route_one_point_index > 0:
                aux_point = routes[route_one_index][route_one_point_index]
                for route_two_index in range(len(routes)):
                    if route_one_index != route_two_index:
                        for route_two_point_index in range(len(routes[route_two_index])):    
                            if route_two_point_index > 0:            
                                routes[route_one_index].remove(aux_point)
                                routes[route_two_index].insert(route_two_point_index, aux_point)

                                value_of_greedy_function_old = instance.greedy_function[route_one_index] + instance.greedy_function[route_two_index]
                                value_of_route_one_new_greedy_function = construction.calculate_greedy_function(instance, routes[route_one_index]) 
                                value_of_route_two_new_greedy_function = construction.calculate_greedy_function(instance, routes[route_two_index])
                                value_of_sum_new_greedy_function = value_of_route_one_new_greedy_function + value_of_route_two_new_greedy_function
                                
                                if value_of_sum_new_greedy_function < value_of_greedy_function_old:
                                    instance.greedy_function[route_one_index] = value_of_route_one_new_greedy_function
                                    instance.greedy_function[route_two_index] = value_of_route_two_new_greedy_function
                                    inter_route_shift(instance, routes)
                                    break
                                else:
                                    routes[route_two_index].remove(aux_point)  
                                    routes[route_one_index].insert(route_one_point_index, aux_point)      
                        else:
                            continue
                        break
                else:
                    continue
                break

    instance.fo = sum(instance.greedy_function)  
      
def local_search(instance, routes):
    intra_route_swap(instance, routes)
    intra_route_shift(instance, routes)
    inter_route_swap(instance, routes)
    inter_route_shift(instance, routes)
