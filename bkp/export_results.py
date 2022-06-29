from instances import import_instances, export_results
from iterated_local_search import ILS
from construction import create_solution
from sys import setrecursionlimit

def main():
    setrecursionlimit(1000000000)
    list_of_instance = import_instances()  
    for instance in list_of_instance: 
        for j in range(10):
            print(instance.name + '/ILS/iteration ' + str(j+1))            
            create_solution(instance)        
            result = ILS(instance, betta_min=5, betta_max=30, ILS_max=300, print_solution = False)  
            export_results(list_of_instance, 'ILS', j, result)
            instance.reset_solutions()            

main()