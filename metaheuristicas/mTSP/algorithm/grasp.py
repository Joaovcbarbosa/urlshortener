import random 
import copy
import local_search

def generate_candidates(instance):
    candidates = copy.deepcopy(instance.points)
    del candidates[0]
    return candidates

def sort_by_fo(e):
  return e['cost']

def get_random_candidate(RCL, RLC_length_in_percentage, alpha):
    RCL.sort(key=sort_by_fo)     
    best_candidate_values = RCL[0]
    best_candidate_cost = best_candidate_values['cost']
    worst_candidate_values = RCL[len(RCL) - 1]
    worst_candidate_cost = worst_candidate_values['cost']
    split_index = int(len(RCL) * RLC_length_in_percentage / 100)
    RCL = RCL[:split_index] # Dimunui o tamanho da lista para apenas (RLC_length_in_percentage)%
    condition = best_candidate_cost + alpha * (worst_candidate_cost - best_candidate_cost)

    for item in RCL:
        if (item['cost'] <= condition) == False:
            RCL.remove(item)

    return random.choice(RCL)
   
def semi_greedy_construction(instance, RLC_length_in_percentage, alpha):    
    routes = [[instance.points[0]] for item in range(instance.vehicles_quantity)] # Cria uma lista de listas baseado na quantidade de veículos
    candidates = generate_candidates(instance) # Gera a lista de candidatos
    fo = 0
    RCL = []
    while len(candidates) > 0: # Enquanto houver candidatos
        for candidate in candidates: # Para cada candidato
            for route_index in range(len(routes)): # Para cada rota
                route_length = len(routes[route_index])
                for point_index in range(route_length): # Para cada ponto da rota
                    candidate_index = candidate['index'] # Seleciona o índice do candidato na lista de pontos

                    cost = instance.matrix[routes[route_index][point_index]['index']][candidate_index] # Custo do ponto até o candidato

                    if point_index == route_length - 1: # Se o ponto selecionado é o último da lista
                        cost += instance.matrix[candidate_index][0] # + Distância do candidato a garagem
                        cost -= instance.matrix[routes[route_index][point_index]['index']][0] # - Distância do ponto corrente a garagem         
                    else:
                        cost += instance.matrix[candidate_index][routes[route_index][point_index + 1]['index']] # + Distância do candidato ao próximo ponto
                        cost -= instance.matrix[routes[route_index][point_index]['index']][routes[route_index][point_index + 1]['index']]# - Distância do ponto corrente ao próximo ponto
                    
                    # Insere os dados na lista
                    candidate_values = {}
                    candidate_values['cost'] = cost
                    candidate_values['candidate'] = candidate
                    candidate_values['route_index'] = route_index
                    candidate_values['point_index'] = point_index
                    RCL.append(candidate_values)
            
        selected_candidate_values = get_random_candidate(RCL, RLC_length_in_percentage, alpha) # Seleciona candidato de forma parcialmente randômica
        selected_candidate = selected_candidate_values['candidate']
        selected_candidate_route_cost = selected_candidate_values['cost']
        selected_candidate_route = selected_candidate_values['route_index']
        selected_candidate_new_index = selected_candidate_values['point_index'] + 1
        fo += selected_candidate_route_cost
        routes[selected_candidate_route].insert(selected_candidate_new_index, selected_candidate) # Adiciona candidato na solução    
           
        candidates.remove(selected_candidate) # Remove da lista de candidatos
        RCL.clear()

    instance.add_best_solution(fo, routes)
    return routes
    
def GRASP(instance, GRASP_max, RLC_length_in_percentage, alpha):
    fo_best = -1
    for iteration in range(GRASP_max):
        S = semi_greedy_construction(instance, RLC_length_in_percentage, alpha)
        S = local_search.local_search(instance, S)

        fo_current = instance.calculate_FO(S)
        if  fo_current < fo_best or fo_best < 0:
            S_best = copy.deepcopy(S)
            fo_best = fo_current
            instance.add_best_solution(fo_best, S_best)

        print(iteration, fo_current, fo_best)

    return S_best

    





