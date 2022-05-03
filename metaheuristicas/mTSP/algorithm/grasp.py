from random import sample
import copy

def generate_candidates(instance):
    candidates = copy.deepcopy(instance.points)
    del candidates[0]
    return candidates

def sort_by_fo(e):
  return e['cost']

def create_routes(instance):    
    routes = [[0] for item in range(instance.vehicles_quantity)] # Cria uma lista de listas baseado na quantidade de veículos
    candidates = generate_candidates(instance) # Gera a lista de candidatos

    fo = 0
    RCL = []
    while len(candidates) > 0: # Enquanto houver candidatos
        for candidate in candidates: # Para cada candidato
            for route_index in range(len(routes)): # Para cada rota
                route_length = len(routes[route_index])
                for point_index in range(route_length): # Para cada ponto da rota
                    candidate_index = instance.points.index(candidate) # Seleciona o índice do candidato na lista de pontos

                    # Calcula o custo do candidato
                    cost = instance.matrix[routes[route_index][point_index]][candidate_index]

                    if point_index == route_length - 1:
                        cost += instance.matrix[candidate_index][0] 
                        cost -= instance.matrix[routes[route_index][point_index]][0]                   
                    else:
                        cost += instance.matrix[candidate_index][routes[route_index][point_index + 1]] 
                        cost -= instance.matrix[routes[route_index][point_index]][routes[route_index][point_index + 1]]
                    
                    # Insere os dados na lista
                    element = {}
                    element['cost'] = cost
                    element['candidate'] = candidate
                    element['route_index'] = route_index
                    element['point_index'] = point_index
                    RCL.append(element)
            
        RCL.sort(key=sort_by_fo)     
        best_candidate_values = RCL[0]

        best_candidate_cost = best_candidate_values['cost']
        best_candidate_point = best_candidate_values['candidate']
        best_candidate_point_index = instance.points.index(best_candidate_point)
        best_candidate_route = best_candidate_values['route_index']
        best_candidate_new_index = best_candidate_values['point_index'] + 1
        
        routes[best_candidate_route].insert(best_candidate_new_index, best_candidate_point_index)
        fo += best_candidate_cost
        candidates.remove(best_candidate_point)
        RCL.clear()

    
    instance.add_best_solution(fo, routes)
    instance.print_solutions()
    return routes
    
def GRASP(instance):
    route = create_routes(instance)
    return route

    





