from random import sample
          
def create_routes(instance):    
    routes = [[instance.points[0]] for item in range(instance.vehicles_quantity)] # Cria uma lista de listas baseado na quantidade de veículos
    
    for point in sample(instance.points, len(instance.points)): # Para cada ponto embaralhado da instância
        point_index = point['index']
        if point_index != 0: # Se não for a garagem
            list_of_new_fo_per_route = []
            for route_index in range(len(routes)): # Seleciona uma rota   
                last_point_index = routes[route_index][-1]['index']
                first_point_index = 0
                                
                value_of_new_fo_per_route = (instance.fo_per_route[route_index] # FO atual daquela rota
                                             + instance.matrix[last_point_index][point_index] # + Distância do último ponto da rota ao ponto atual
                                             + instance.matrix[first_point_index][point_index] # + Distância da garagem ao ponto atual
                                             - instance.matrix[last_point_index][first_point_index]) # - Distância do último ponto da rota a garagem
                
                list_of_new_fo_per_route.append(value_of_new_fo_per_route) # Adiciona o valor encontrado na lista de FO's de rotas

            best_fo_value =  min(list_of_new_fo_per_route)  # Seleciona o melhor valor de FO
            route_index = list_of_new_fo_per_route.index(best_fo_value) # Seleciona o index da rota com menor FO
            instance.fo_per_route[route_index] = best_fo_value # Atualiza o valor da FO da rota
            routes[route_index].append(point) # Adiciona ponto a rota

    instance.fo = sum(instance.fo_per_route) # Soma o FO de todas as rotas, formando o FO da solução
    return routes
    
