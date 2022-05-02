import os
import math
import construction

class Instance:    
    def __init__(self, name, points, vehicles_quantity):
        self.name = name
        self.points = points
        self.vehicles_quantity = vehicles_quantity
        self.matrix = generate_matrix(points)
        self.fo_per_route = [0 for item in range(vehicles_quantity)] 
        self.best_fos = []
        self.best_solutions = []

    def add_best_solution(self, fo, solution):
        if len(self.best_fos) == 100:
            worst_value = max(self.best_fos)
            if fo < worst_value:
                index = self.best_fos.index(worst_value)
                self.best_fos[index] = fo
                self.best_solutions[index] = solution
                self.calculate_fo_per_route(solution)
        else:
            self.best_fos.append(fo)
            self.best_solutions.append(solution)
            self.calculate_fo_per_route(solution)

    def calculate_fo_per_route(self, solution):
        for route_index in range(len(solution) - 1):
            self.fo_per_route[route_index] = construction.calculate_fo_per_route(self, solution[route_index])

    def best_solution(self):
        best_fo = min(self.best_fos)
        index = self.best_fos.index(best_fo)
        best_solution = self.best_solutions[index]

        return best_fo, best_solution

    def all_solutions(self):
        return self.best_solutions

    def print_solutions(self):
        print('BEST SOLUTIONS:')
        for index in range(len(self.best_solutions)):
            print(str(index + 1) + ' -> ', end = '')
            print(self.best_solutions[index])

        print('================================================================================')

        fo, route = self.best_solution()
        print('WINNER:')                    
        print('ROUTES: ' + str(route))
        print('FO: ' + str(fo))

def generate_matrix(points):
    matrix = []
    for i in range(len(points)): 
        row = [] 
        for j in range(len(points)):
            row.append(math.dist(points[i], points[j])) 
        matrix.append(row)  

    return matrix  

def print_instance(list_of_instance):
    for index in range(len(list_of_instance)):        
        with open(os.path.dirname(os.path.abspath(__file__)) + '\\results_' + list_of_instance[index].name +'.txt', 'w+') as list_file:
            list_file.write('vehicles_quantity: ' + str(list_of_instance[index].vehicles_quantity) + '\n')
            
            for i in range(len(list_of_instance[index].points)): 
                list_file.write(str(i+1) + ' ' + str(list_of_instance[index].points[i]) + '\n')

            for row in list_of_instance[index].matrix:                
                list_file.write(str(row))
                list_file.write('\n')

def treat_character(line):
    line = line.replace('\n', '').replace('	', ' ').replace('  ', ' ').split(' ')
    return line[0].isnumeric(), line 

def import_instances():
    walk_dir = os.path.dirname(os.path.abspath(__file__)) + '\instances'
    list_of_instance = []

    for root, subdirs, files in os.walk(walk_dir):        
        for filename in files:            
            instance_file = open(os.path.join(root, filename), 'r')
            i = 0
            points = []   
            for line in instance_file: 
                xy = []  
                validation, line = treat_character(line)
                if i == 0:
                    vehicles_quantity = int(line[2])
                    name = line[0] + '_' + str(vehicles_quantity)
                    i+=1
                else:                    
                    if validation == True:
                        xy.append(float(line[1]))
                        xy.append(float(line[2]))
                        points.append(xy)

            list_of_instance.append(Instance(name, points, vehicles_quantity))
    return list_of_instance
     