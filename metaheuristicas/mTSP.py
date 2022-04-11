import os

class Instance:
    
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y

def import_instances():
    walk_dir = os.path.dirname(os.path.abspath(__file__)) + '\instances'

    list_of_instance = []

    for root, subdirs, files in os.walk(walk_dir):
        
        for filename in files:
            instance_file = open(os.path.join(root, filename), 'r')
            i = 0
            x = []       
            y = [] 
            for linha in instance_file: 
                if i == 0:
                    name = linha.replace('\n', '').split(' ')[0] + '_' +linha.replace('\n', '').split(' ')[2]
                    i+=1
                else:
                    if linha != '\n':
                        x.append(linha.replace('\n', '').split(' ')[1])
                        y.append(linha.replace('\n', '').split(' ')[2])

            list_of_instance.append(Instance(name, x, y))

    return list_of_instance
     
list_of_instance = import_instances()
for item in list_of_instance:
    print(item.name)
    print('x: ')
    print(item.x)
    print('y: ')
    print(item.y)
    print('\n')
    