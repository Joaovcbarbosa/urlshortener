from random import uniform, randint, choice
from copy import deepcopy
from variable_neighborhood_descent import VND

def sort_by_gene(e):
    return e['gene']

def sort_by_fo(e):
    return e['fo']

def calculate_solution(instance, key):  
    S = [[instance.points[0]] for item in range(instance.vehicles_quantity)] # Cria uma lista de listas baseado na quantidade de veículos    
    instance.current_solution_fo_per_route = [0] * instance.vehicles_quantity
    
    for index in range(len(key)):                 
        i = key[index]['index']        
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
        S[route_index].append(instance.points[i]) # Adiciona ponto a rota
    
    fo = round(sum(instance.current_solution_fo_per_route), 2)
    return S, fo 

def generate_key(instance):
    key = []
    for i in range(len(instance.points)):
        value = {
            'gene': uniform(0, 1),
            'index': i
        }
        key.append(value)

    key.pop(0)
    sorted_key = deepcopy(key)
    sorted_key.sort(key=sort_by_gene)
    return key, sorted_key

def create_solutions(instance, p):  
    S = []
    for i in range(p):   
        key, sorted_key = generate_key(instance)
        solution, fo = calculate_solution(instance, sorted_key)
        element = {
            'key': key,
            'sorted_key': sorted_key,
            'fo': fo,
            'solution': solution
        }
        S.append(element)
    return S

def create_elite(S, pe_min, pe_max):
    pe = int((randint(pe_min, pe_max) / 100) * len(S))
    S.sort(key=sort_by_fo)

    split_index = pe
    S_elite = S[:split_index] # Dimunui o tamanho da lista para apenas (RLC_length_in_percentage)%
    S = S[split_index:]
    return S, S_elite

def generate_gene(elite_parent, non_elite_parent, rhoe_min, rhoe_max, pm_min, pm_max, i):
    rhoe = randint(rhoe_min, rhoe_max) / 100
    pm = randint(pm_min, pm_max) / 100

    x = uniform(0, 1)
    if x <= pm:
        value = {
            'gene': x,
            'index': i+1
        }
        return value
    if x <= rhoe:
        return elite_parent['key'][i]
    else:
        return non_elite_parent['key'][i]

def generate_key_crossover(instance, S, S_elite, rhoe_min, rhoe_max, pm_min, pm_max):
    elite_parent = choice(S_elite)
    non_elite_parent = choice(S)

    key = []
    for i in range(len(instance.points) - 1):
        value = generate_gene(elite_parent, non_elite_parent, rhoe_min, rhoe_max, pm_min, pm_max, i)
        key.append(value)

    sorted_key = deepcopy(key)
    sorted_key.sort(key=sort_by_gene)
    return key, sorted_key

def crossover(instance, p, S, S_elite, rhoe_min, rhoe_max, pm_min, pm_max):
    S_new = deepcopy(S_elite)
    for i in range(p - len(S_elite)):   
        key, sorted_key = generate_key_crossover(instance, S, S_elite, rhoe_min, rhoe_max, pm_min, pm_max)
        solution, fo = calculate_solution(instance, sorted_key)
        element = {
            'key': key,
            'sorted_key': sorted_key,
            'fo': fo,
            'solution': solution
        }
        S_new.append(element)

    return S_new

def BRKGA(instance, BRKGAMax, p, pe_min, pe_max, rhoe_min, rhoe_max, pm_min, pm_max):
    # pm_min_original = pm_min
    # pm_max_original = pm_max    
    # rhoe_min_original = rhoe_min
    # rhoe_max_original = rhoe_max

    S = create_solutions(instance, p)
    S, S_elite = create_elite(S, pe_min, pe_max)
    i = 0
    j = 0

    while i < BRKGAMax:
        i += 1
        current_fo = S_elite[0]['fo']

        S = crossover(instance, p, S, S_elite, rhoe_min, rhoe_max, pm_min, pm_max)
        S, S_elite = create_elite(S, pe_min, pe_max)

        instance.add_best_solution(S_elite[0]['fo'], S_elite[0]['solution'])
        VND(instance, r=6, print_solution=False)  
        best_fo, best_solution = instance.best_solution()
        
        print(i, current_fo, best_fo)
        # if current_fo == best_fo:
        #     j+=1

        # if j > 100:
        #     rhoe_min = 70
        #     rhoe_max = 90
        #     j = 0

        # if current_fo != best_fo:
        #     j = 0
        #     rhoe_min = rhoe_min_original
        #     rhoe_max = rhoe_max_original





    
