import os
import math

class Instance:
    
    def __init__(self, name, points):
        self.name = name
        self.points = points
        self.matrix = generate_matrix(points)

def generate_matrix(points):
    matrix = []
    for i in range(len(points)): 
        row = [] 
        for j in range(len(points)):
            row.append(math.dist(points[i], points[j])) 
        matrix.append(row)  

    return matrix  

def search_instance(list_of_instance, name):
    for i in range(len(list_of_instance)): 
        if list_of_instance[i].name == name:
            return i

    return -1

def print_instance(list_of_instance, option):
    index = search_instance(list_of_instance, option)
    if index == -1:
        print('File not found.')
        return
    else:
        with open(os.path.dirname(os.path.abspath(__file__)) + '\\results_' + list_of_instance[index].name +'.txt', 'w+') as list_file:

            for i in range(len(list_of_instance[index].points)): 
                list_file.write(str(i+1) + ' ' + str(list_of_instance[index].points[i]) + '\n')

            for row in list_of_instance[index].matrix:                
                list_file.write(str(row))
                list_file.write('\n')

def treat_character(line):
    line = line.replace('\n', '').replace('	', ' ').split(' ')
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
                    name = line[0] + '_' + line[2]
                    i+=1
                else:                    
                    if validation == True:
                        xy.append(float(line[1]))
                        xy.append(float(line[2]))
                        points.append(xy)

            list_of_instance.append(Instance(name, points))
    return list_of_instance
     
list_of_instance = import_instances()

while(True):
    option = input('Filename: ')
    if option == 'exit':
        break
    else:
        print_instance(list_of_instance, option)