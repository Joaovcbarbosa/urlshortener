import construction

def intra_route_swap(instance, routes):
    for i in range(len(routes)):
        lenght_route = len(routes[i])
        for j in range(lenght_route):
            for k in range(lenght_route):
                if j != k and j > 0 and k > 0:
                    auxJ = routes[i][j]
                    auxK = routes[i][k]

                    routes[i][j] = auxK
                    routes[i][k] = auxJ

                    new_greedy_function = construction.calculate_greedy_function(instance, routes[i])
                    if new_greedy_function < instance.greedy_function[i]:
                        instance.greedy_function[i] = new_greedy_function
                        break
                    else:
                        routes[i][j] = auxJ
                        routes[i][k] = auxK
                  
                    # value_of_new_greedy_function = (instance.greedy_function[i] - 
                    #                                 instance.matrix[routes[i][j-1]][j] - # (0 if j == 0 else instance.matrix[routes[i][j-1]][j]) - 
                    #                                 (0 if j == lenght_route - 1 else instance.matrix[routes[i][j]][j+1]) - 
                    #                                 (0 if k-1 == j else instance.matrix[routes[i][k-1]][k]) - 
                    #                                 (0 if k == lenght_route - 1 else instance.matrix[routes[i][k]][k+1]) + 
                    #                                 instance.matrix[routes[i][j-1]][k] + 
                    #                                 (0 if j == lenght_route - 1 else instance.matrix[routes[i][k]][j+1]) + 
                    #                                 (instance.matrix[routes[i][k]][j] if k-1 == j else instance.matrix[routes[i][k-1]][j]) + 
                    #                                 (0 if k == lenght_route -1 else instance.matrix[routes[i][j]][k+1]))                
                
                    # if value_of_new_greedy_function < instance.greedy_function[i]:
                    #     aux = routes[i][j]
                    #     routes[i][j] = routes[i][k]
                    #     routes[i][k] = aux
                    #     instance.greedy_function[i] = value_of_new_greedy_function
                    #     break
            else:
                continue
            break
        else:
            continue
    
    instance.fo = sum(instance.greedy_function)  
    
def local_search(instance, routes):
    intra_route_swap(instance, routes)
