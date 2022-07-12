from instances import import_instances, export_results
from construction import create_solution
from iterated_local_search import ILS
from sys import setrecursionlimit

def main():
    rounds = 10   
    list_of_instance = import_instances()    
    
    for instance in list_of_instance:
        for j in range(rounds):            
            print('======================== ' + str(j+1) + ' ' + instance.name + ' ========================'  + '\n')
            create_solution(instance) 
            MH = 'ILS'
            result = ILS(instance, betta_min=1, betta_max=10, ILS_max=10) 
            export_results(list_of_instance, MH, j, result)
            instance.reset_solutions()                    

setrecursionlimit(1000000000)
main()