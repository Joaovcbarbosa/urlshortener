import os
import math

class Instance:
    
    def __init__(self, name, points, vehicles_quantity):
        self.name = name
        self.points = points
        self.vehicles_quantity = vehicles_quantity
        self.matrix = generate_matrix(points)

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
            list_file.write('vehicles_quantity: ' + list_of_instance[index].vehicles_quantity + '\n')
            
            for i in range(len(list_of_instance[index].points)): 
                list_file.write(str(i+1) + ' ' + str(list_of_instance[index].points[i]) + '\n')

            for row in list_of_instance[index].matrix:                
                list_file.write(str(row))
                list_file.write('\n')

def create_routes(list_of_instance):
    for index in range(len(list_of_instance)):   
        routes = []     
        for i in range(int(list_of_instance[index].vehicles_quantity)):
            route = [1, 2, 3]
            routes.append(route)


    print(routes)

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
                    vehicles_quantity = line[2]
                    name = line[0] + '_' + vehicles_quantity
                    i+=1
                else:                    
                    if validation == True:
                        xy.append(float(line[1]))
                        xy.append(float(line[2]))
                        points.append(xy)

            list_of_instance.append(Instance(name, points, vehicles_quantity))
    return list_of_instance
     
list_of_instance = import_instances()
print_instance(list_of_instance)
create_routes(list_of_instance)