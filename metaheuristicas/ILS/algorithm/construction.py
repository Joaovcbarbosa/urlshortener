from random import sample
from copy import deepcopy

def sort_by_distance(e):
    return e['distance']

def create_solution(instance):  
    for k in range(100):  
        S = [[instance.points[0]] for item in range(instance.vehicles_quantity)] # Cria uma lista de listas baseado na quantidade de veículos    
        points = deepcopy(instance.points) # Lista de pontos
        del points[0] # Remove a garagem
        distances = [-1] * len(points) # Lista de distâncias dos pontos a garagem, a partir do ponto 1 (0 é a garagem)

        # Para cada ponto da lista de pontos
        for i in range(len(points)):
            element = {
                        'distance': instance.matrix[0][i + 1] + instance.matrix[i + 1][0], # Distancia a garagem
                        'point': instance.points[i + 1]
                    }
            distances[i] = element
        
        distances.sort(key=sort_by_distance) # Organiza a lista pelas distâncias de forma crescente

        # Para cada rota da solução
        for i in range(len(S)):
            S[i].append(distances[0]['point']) # Adiciona o menor ponto
            instance.current_solution_fo_per_route[i] = round(distances[0]['distance'], 2)
            del distances[0] # Retira o menor ponto da lista
            points.remove(S[i][1]) # Retira o ponto da lista de pontos

        # Para cada ponto embaralhado da instância
        for point in sample(points, len(points)): 
            i = point['index']
            fos = []
            for j in range(len(S)): # Seleciona uma rota   
                last_point = S[j][-1]['index']
                depot = 0            
                value_of_fo = (instance.current_solution_fo_per_route[j] # FO atual daquela rota
                            + instance.matrix[last_point][i] # + Distância do último ponto da rota ao ponto atual
                            + instance.matrix[depot][i] # + Distância da garagem ao ponto atual
                            - instance.matrix[last_point][depot]) # - Distância do último ponto da rota a garagem            
                fos.append(round(value_of_fo, 2)) # Adiciona o valor encontrado na lista de FO's de rotas

            best_fo_value =  min(fos)  # Seleciona o melhor valor de FO
            route_index = fos.index(best_fo_value) # Seleciona o index da rota com menor FO
            instance.current_solution_fo_per_route[route_index] = best_fo_value # Atualiza o valor da FO da rota
            S[route_index].append(point) # Adiciona ponto a rota

        instance.current_solution_fo = round(sum(instance.current_solution_fo_per_route), 2) # Soma o FO de todas as rotas, formando o FO da solução
        instance.current_solution = S
        instance.add_best_solution(instance.current_solution_fo, S)

    instance.current_solution_fo, instance.current_solution = instance.best_solution()
    
    