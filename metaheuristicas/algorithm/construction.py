from random import sample
            
def calculate_greedy_function(instance, route):
    gf = instance.matrix[route[0]][route[1]]
    for i in range(len(route)):
        if i > 0 and i < len(route) - 1:
            gf += instance.matrix[route[i]][route[i+1]]
        elif i == len(route) - 1:
            gf += instance.matrix[route[i]][route[0]]
    
    return gf
            
def print_routes(instance, routes):    
    print('=================================================================================================================================================')
    print('instance: ' + instance.name)    
    
    for i in range(len(routes)):
        print('\n')
        print('route ' + str(i+1) + ': ', end = '')
        print(routes[i])
        print('points:', end = ' ')
        for j in range(len(routes[i])):
            print(instance.points[routes[i][j]], end = ' ')
        print('\nfo manually calculated: ' + str(calculate_greedy_function(instance, routes[i])))
        print('fo dynamically calculated: ' + str(instance.greedy_function[i]))
    
    print('fo: ' + str(instance.fo))    

def create_routes(instance):    
    routes = [[0] for item in range(instance.vehicles_quantity)]     
    
    for i in sample(range(len(instance.points)), len(instance.points)):
        if i != 0:
            list_of_new_greedy_function = []
            for j in range(len(routes)):       
                value_of_new_greedy_function = instance.greedy_function[j] + instance.matrix[routes[j][-1]][i] + instance.matrix[routes[j][0]][i] - instance.matrix[routes[j][-1]][0]
                if value_of_new_greedy_function > 0:
                    list_of_new_greedy_function.append(value_of_new_greedy_function)
                    
            route_index = list_of_new_greedy_function.index(min(list_of_new_greedy_function))
            route_greedy_function = min(list_of_new_greedy_function)
            instance.greedy_function[route_index] = route_greedy_function
            routes[route_index].append(i)

    instance.fo = sum(instance.greedy_function)
    return routes
    
