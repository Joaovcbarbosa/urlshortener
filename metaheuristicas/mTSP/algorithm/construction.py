from random import sample
            
def calculate_fo_per_route(instance, route):
    fo = 0
    if len(route) > 1:     
        fo = instance.matrix[0][route[1]] # Distância da garagem ao primeiro ponto da rota
        for point_index in range(len(route)): # Para cada ponto
            if point_index > 0 and point_index < len(route) - 1: # Se o index do ponto não for a garagem nem o último ponto
                fo += instance.matrix[route[point_index]][route[point_index + 1]] # Distancia entre o ponto e o próximo ponto
            elif point_index == len(route) - 1: # Se for o último ponto da rota
                fo += instance.matrix[route[point_index]][0] # Distância entre o ponto e a garagem
    
    return fo
            
def print_routes(instance, routes):    
    print('=================================================================================================================================================')
    print('instance: ' + instance.name)    
    
    fo = 0
    for i in range(len(routes)):
        print('\n')
        print('route ' + str(i+1) + ': ', end = '')
        print(routes[i])
        print('points:', end = ' ')
        for j in range(len(routes[i])):
            print(instance.points[routes[i][j]], end = ' ')
        fo_route = calculate_fo_per_route(instance, routes[i])
        fo += fo_route
        print('\nfo manually calculated: ' + str(fo_route))

    print('total fo: ' + str(fo))
        
    
    

def create_routes(instance):    
    routes = [[0] for item in range(instance.vehicles_quantity)] # Cria uma lista de listas baseado na quantidade de veículos
    
    for point_index in sample(range(len(instance.points)), len(instance.points)): # Para cada ponto embaralhado da instância
        if point_index != 0:
            list_of_new_fo_per_route = []
            for route_index in range(len(routes)): # Seleciona uma rota    
                value_of_new_fo_per_route = (instance.fo_per_route[route_index] # FO atual daquela rota
                                             + instance.matrix[routes[route_index][-1]][point_index] # + Distância do último ponto da rota ao ponto atual
                                             + instance.matrix[routes[route_index][0]][point_index] # + Distância da garagem ao ponto atual
                                             - instance.matrix[routes[route_index][-1]][0]) # - Distância do último ponto da rota a garagem
                
                if value_of_new_fo_per_route > 0:
                    list_of_new_fo_per_route.append(value_of_new_fo_per_route) # Adiciona o valor encontrado na lista de FO's de rotas
                    
            route_index = list_of_new_fo_per_route.index(min(list_of_new_fo_per_route)) # Seleciona o index da rota com menor FO
            route_fo_per_route = min(list_of_new_fo_per_route) # Seleciona o valor da FO da rota
            instance.fo_per_route[route_index] = route_fo_per_route # Atualiza o valor da FO da rota
            routes[route_index].append(point_index) # Adiciona ponto a rota

    instance.fo = sum(instance.fo_per_route) # Soma o FO de todas as rotas, formando o FO da solução
    return routes
    
