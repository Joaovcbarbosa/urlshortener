import os
import math

class Instance:    
    def __init__(self, name, points, vehicles_quantity):
        self.name = name
        self.points = points
        self.vehicles_quantity = vehicles_quantity
        self.matrix = generate_matrix(points)
        self.fo_per_route = [0 for item in range(vehicles_quantity)] 
        self.best_fos = []
        self.best_solutions = [] # Guarda as 100 melhores soluções

    def add_best_solution(self, fo, solution):
        if len(self.best_fos) == 100:  # Se a lista está lotada
            worst_value = max(self.best_fos)
            if fo < worst_value: # E o FO encontrado é melhor que o pior FO da lista
                index = self.best_fos.index(worst_value) # Seleciona o index do pior FO
                self.best_fos[index] = fo # Adiciona o FO novo na lista, no lugar do antigo
                self.best_solutions[index] = solution
                self.update_fo_per_route(solution)
        else: # Se a lista ainda não está lotada, insere o FO na lista
            self.best_fos.append(fo)
            self.best_solutions.append(solution)
            self.update_fo_per_route(solution)

    def update_fo_per_route(self, solution): # Atualiza o FO de cada rota
        for route_index in range(len(solution) - 1):
            self.fo_per_route[route_index] = self.calculate_fo_per_route(solution[route_index])

    def best_solution(self):
        best_fo = min(self.best_fos)
        index = self.best_fos.index(best_fo)
        best_solution = self.best_solutions[index]

        return best_fo, best_solution

    def print_solution(self):
        fo, routes = self.best_solution()
        fo_manually = 0
        print('WINNER ROUTE: ')
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
            print('\nfo manually calculated: ' + str(fo_route))

        print('\nfo manually calculated: ' + str(fo_manually))
        print('FO: ' + str(fo))

    def calculate_FO(self, routes):
        fo = 0
        for route in routes: 
            fo += self.calculate_fo_per_route(route)
            
        return fo

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
        
def generate_matrix(points):
    matrix = []
    for i in range(len(points)): # Para cada ponto
        row = [] 
        for j in range(len(points)):
            row.append(math.dist(points[i]['xy'], points[j]['xy'])) # Calcula a distância dele para todos os outros pontos
        matrix.append(row)  

    return matrix  

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

def import_instances():
    walk_dir = os.path.dirname(os.path.abspath(__file__)) + '\instances'
    list_of_instance = []

    for root, subdirs, files in os.walk(walk_dir):        
        for filename in files: # Para cada arquivo de instância           
            instance_file = open(os.path.join(root, filename), 'r')
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

            list_of_instance.append(Instance(name, points, vehicles_quantity))
    return list_of_instance
     