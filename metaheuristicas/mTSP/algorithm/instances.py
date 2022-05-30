import os
from math import dist
from copy import deepcopy
import networkx as nx
import matplotlib.pyplot as plt

class Instance:    
    def __init__(self, name, path, points, vehicles_quantity):
        self.name = name
        self.path = path
        self.points = points
        self.vehicles_quantity = vehicles_quantity
        self.matrix = generate_matrix(points)    
        self.current_solution = []
        self.current_solution_fo = 0 
        self.current_solution_fo_per_route = [0 for item in range(vehicles_quantity)]         
        self.best_fos = []
        self.best_solutions = [] # Guarda as 100 melhores soluções
    
    def add_best_solution(self, fo, solution):
        fo = round(fo, 2)
        if len(self.best_fos) == 100:  # Se a lista está lotada
            worst_value = max(self.best_fos)
            if fo < worst_value: # E o FO encontrado é melhor que o pior FO da lista
                index = self.best_fos.index(worst_value) # Seleciona o index do pior FO
                self.best_fos[index] = fo # Adiciona o FO novo na lista, no lugar do antigo
                self.best_solutions[index] = solution
        else: # Se a lista ainda não está lotada, insere o FO na lista
            self.best_fos.append(fo)
            self.best_solutions.append(solution)

    def best_solution(self):
        best_fo = min(self.best_fos)
        index = self.best_fos.index(best_fo)
        best_solution = self.best_solutions[index]
        return best_fo, best_solution

    def print_solution(self, plot_solution = 0):
        fo, routes = self.best_solution()
        fo_manually = 0
        is_valid = self.is_valid_solution()
       
        if is_valid:
            print('\nThe solution is valid')
        else:
            print('\nTHE SOLUTION IS NOT VALID')

        print('WINNER ROUTE: ')
        print(routes)
        print('\n', end = '')
        for i in range(len(routes)):
            print('\n', end = '')
            print('route ' + str(i+1) + ': ')
            for item in routes[i]:
                print(item['index'], end = ' ')
            print('\n', end = '')
            for item in routes[i]:
                print(item['xy'], end = ' ')
        
            fo_route = self.calculate_fo_per_route(routes[i])
            fo_manually += fo_route
            print('\nfo manually calculated: ' + str(round(fo_route, 2)))

        print('\nfo manually calculated: ' + str(round(fo_manually, 2)))
        print('FO: ' + str(fo))

        if plot_solution == 1:
            self.plot_solution(True)

    def treat_solution(self, solution):
        result = []
        for route in solution:
            del route[0] # Exclui a garagem
            points = []
            for point in route:
                points.append(point['index'] + 1)

            result.append(points)
            points = []

        return result 

    def plot_solution(self, withDepEdges):
        fo, solution = self.best_solution()
        solution = deepcopy(self.treat_solution(solution))
        fIn = open(self.path, 'r')
        matRaw = [ [a for a in b.split('\t')] for b in fIn.read().split('\n') if b != '' ]
        matRaw = matRaw[1:]
        fIn.close()
        baseColors = ['red', 'green', 'blue', 'yellow', 'magenta', 'cyan', 'pink'] #podem add mais cores de rotas
        G=nx.Graph()
        for nNode in matRaw:
            nID = int(nNode[0])
            G.add_node(nID,pos=( float(nNode[1]) , float(nNode[2])), color= 'lightblue' if nID==1 else 'lightgreen')
    
        for rID in range(len(solution)):
            route = solution[rID]
            rColor = baseColors[rID % len(baseColors)]
            if (len(route) > 0):
                if withDepEdges:
                    G.add_edge(1,route[0],  color=rColor)
                    G.add_edge(1,route[-1], color=rColor)
                for i in range(len(route)-1):
                    G.add_edge(route[i], route[i+1], color=rColor)
        positions  = nx.get_node_attributes(G,'pos')
        nodeColors = nx.get_node_attributes(G,'color').values()
        edgeColors = nx.get_edge_attributes(G,'color').values()
        plt.figure(1,figsize=(40,40)) #ajustar: Números maiores -> nós menores (mas a resolução do arquivo de saída aumenta)
        nx.draw(G, positions, edge_color=edgeColors, node_color=nodeColors, with_labels=True)
        plt.savefig("%s.png" % ('solution_' + self.name + '_fo_' + str(float("{0:.4f}".format(fo)))))

    def calculate_FO(self, routes):
        fo = 0
        for route in routes: 
            fo += self.calculate_fo_per_route(route)
            
        return round(fo, 2)

    def calculate_fo_per_route(self, route):
        fo = 0
        if len(route) > 1:     
            first_point_index = route[1]['index']
            fo += self.matrix[0][first_point_index] # Distância da garagem ao primeiro ponto da rota
            for point_index in range(len(route)): # Para cada ponto
                point = route[point_index]['index']
                if point_index > 0 and point_index < len(route) - 1: # Se o index do ponto não for a garagem nem o último ponto                    
                    next_point = route[point_index + 1]['index'] 
                    fo += self.matrix[point][next_point] # Distância entre o ponto e o próximo ponto
                elif point_index == len(route) - 1: # Se for o último ponto da rota
                    fo += self.matrix[point][0] # Distância entre o ponto e a garagem
        
        return fo
    
    def refresh(self, routes, fo = -1):
        if fo == -1:
            self.current_solution_fo = round(sum(self.current_solution_fo_per_route), 2)
        else:        
            self.current_solution_fo = fo
        self.current_solution = deepcopy(routes)

    def is_valid_solution(self):   
        fo, solution = self.best_solution()   
        solution_len = 0     
        points = deepcopy(self.points)

        for route in solution:
            solution_len += len(route) - 1

            # Se todas as rotas tem pelo menos um ponto além da garagem
            if len(route) < 2:
                return False

            for point_index in range(len(route)):
                route_point = route[point_index]
                
                # Se começa na garagem
                if point_index == 0 and route_point != self.points[0]:
                    return False

                if route_point in points:
                    points.remove(route_point)

        # Se todos os pontos foram visitados
        if len(points) > 0:
            return False            
        if solution_len != len(self.points) - 1:
            return False

        return True
                    
def generate_matrix(points):
    matrix = []
    for i in range(len(points)): # Para cada ponto
        row = [] 
        for j in range(len(points)):
            distance = round(dist(points[i]['xy'], points[j]['xy']), 2)
            row.append(distance) # Calcula a distância dele para todos os outros pontos
        matrix.append(row)  

    return matrix  


def calculate_cost_remove(instance, route, point_index):

    i = route[point_index]["index"]
    i_front = route[point_index + 1 if point_index + 1 < len(route) else 0]["index"]
    i_back = route[point_index - 1]["index"]
    
    cost = (- instance.matrix[i_back][i]
            - instance.matrix[i][i_front]
            + instance.matrix[i_back][i_front])

    return round(cost, 2)

def calculate_cost_swap(instance, routes, route_one_index, route_two_index, point_one_index, point_two_index):
    i = routes[route_one_index][point_one_index]["index"]
    i_front = routes[route_one_index][point_one_index + 1 if point_one_index + 1 < len(routes[route_one_index]) else 0]["index"]
    i_back = routes[route_one_index][point_one_index - 1]["index"]
    j = routes[route_two_index][point_two_index]["index"]
    j_front = routes[route_two_index][point_two_index + 1 if point_two_index + 1 < len(routes[route_two_index]) else 0]["index"]
    j_back = routes[route_two_index][point_two_index - 1]["index"]

    if route_one_index == route_two_index and abs(point_one_index - point_two_index) == 1:
        if point_two_index > point_one_index:
            cost = (- instance.matrix[i_back][i]
                    - instance.matrix[j][j_front]
                    + instance.matrix[i_back][j]
                    + instance.matrix[i][j_front])
        else:
            cost = (- instance.matrix[j_back][j]
                    - instance.matrix[i][i_front]
                    + instance.matrix[j_back][i]
                    + instance.matrix[j][i_front])
    else:
        cost = (- instance.matrix[i_back][i]
                - instance.matrix[i][i_front]
                - instance.matrix[j_back][j]
                - instance.matrix[j][j_front]
                + instance.matrix[i_back][j]
                + instance.matrix[j][i_front]
                + instance.matrix[j_back][i]
                + instance.matrix[i][j_front])       
        
    return round(cost, 2)

def calculate_cost_shift(instance, routes, route_one_index, route_two_index, point_one_index, point_two_index):

    intra = 0
    if route_one_index == route_two_index and point_one_index < point_two_index: # Se for intrarota e o ponto i é menor que o j
        intra = 1 # Então adiciona 1 ao ponto, pois ao retirar da posição i, o vetor será rearranjado e j será j - 1
    
    i = routes[route_one_index][point_one_index]["index"]
    i_front = routes[route_one_index][point_one_index + 1 if point_one_index + 1 < len(routes[route_one_index]) else 0]["index"]
    i_back = routes[route_one_index][point_one_index - 1]["index"]
    j = routes[route_two_index][point_two_index + intra if point_two_index + intra < len(routes[route_two_index]) else 0]["index"]
    j_back = routes[route_two_index][point_two_index - 1 + intra]["index"]

    cost = (- instance.matrix[i_back][i]
            - instance.matrix[i][i_front]
            + instance.matrix[i_back][i_front]
            + instance.matrix[j_back][i]
            + instance.matrix[i][j]
            - instance.matrix[j_back][j])


    return round(cost, 2)

def calculate_cost_2opt(instance, routes, route_index, point_one_index, point_two_index):

    i = routes[route_index][point_one_index]["index"]
    i_front = routes[route_index][point_one_index + 1]["index"]
    j = routes[route_index][point_two_index]["index"]
    j_front = routes[route_index][point_two_index + 1]["index"]
    
    cost = (- instance.matrix[i][i_front]
            - instance.matrix[j][j_front]
            + instance.matrix[i][j]
            + instance.matrix[i_front][j_front])

    return round(cost, 2)



def export_instance(list_of_instance): # Exporta a instância para arquivo txt
    for index in range(len(list_of_instance)):        
        with open(os.path.dirname(os.path.abspath(__file__)) + '\\results_' + list_of_instance[index].name +'.txt', 'w+') as list_file:
            list_file.write('vehicles_quantity: ' + str(list_of_instance[index].vehicles_quantity) + '\n') # Quantidade de veículos
            
            for i in range(len(list_of_instance[index].points)): 
                list_file.write(str(list_of_instance[index].points[i]['index']) + ' ' + str(list_of_instance[index].points[i]['xy']) + '\n') # Pontos

            for row in list_of_instance[index].matrix: # Matriz de distância
                list_file.write(str(row))
                list_file.write('\n')
      
def treat_character(line): 
    line = line.replace('\n', '').replace('	', ' ').replace('  ', ' ').split(' ')
    return line[0].isnumeric(), line 

def generate_test_instance():
    instance_file = open('algorithm\instances\set I\mtsp51_3.txt', 'r')
    first_line = True 
    point_index = 0
    points = []  
    for line in instance_file: # Para cada linha do arquivo                
        xy = []  
        validation, line = treat_character(line)
        if first_line == True: # Se for a primeira linha, quarda a qtd de veículos e o nome da instância
            vehicles_quantity = int(line[2])
            name = line[0] + '_' + str(vehicles_quantity)
            first_line = False
        else: # Caso contrário, guarda o index do ponto (para usar na matriz de distância) e o ponto
            if validation == True:                        
                xy.append(float(line[1]))
                xy.append(float(line[2]))
                element = {
                    'index': point_index,
                    'xy': xy
                }
                points.append(element)
                point_index+=1

    return Instance(name, 'algorithm\instances\set I\mtsp51_3.txt', points, vehicles_quantity)

def import_instances():
    walk_dir = os.path.dirname(os.path.abspath(__file__)) + '\instances'
    list_of_instance = []

    for root, subdirs, files in os.walk(walk_dir):        
        for filename in files: # Para cada arquivo de instância   
            instance_file_name = os.path.join(root, filename)  
            instance_file = open(instance_file_name, 'r')
            first_line = True 
            point_index = 0
            points = []  
            for line in instance_file: # Para cada linha do arquivo                
                xy = []  
                validation, line = treat_character(line)
                if first_line == True: # Se for a primeira linha, quarda a qtd de veículos e o nome da instância
                    vehicles_quantity = int(line[2])
                    name = line[0] + '_' + str(vehicles_quantity)
                    first_line = False
                else: # Caso contrário, guarda o index do ponto (para usar na matriz de distância) e o ponto
                    if validation == True:                        
                        xy.append(float(line[1]))
                        xy.append(float(line[2]))
                        element = {
                            'index': point_index,
                            'xy': xy
                        }
                        points.append(element)
                        point_index+=1

            list_of_instance.append(Instance(name, instance_file_name, points, vehicles_quantity))
    return list_of_instance