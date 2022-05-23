from instances import import_instances
from instances import export_instance
from construction import create_routes
from construction import create_test_routes
from local_search import local_search
from simulated_annealing import SA
from grasp import GRASP 
from iterated_local_search import ILS
from variable_neighborhood_search import VNS
from variable_neighborhood_descent import VND
# from sys import setrecursionlimit

def main():
    # setrecursionlimit(100000000)
    input_string = ('1 -> Local Search\n' +
                    '2 -> SA\n' +
                    '3 -> GRASP \n' +
                    '4 -> ILS\n' +
                    '5 -> VNS\n' +
                    '6 -> VND\n')
    option = input(input_string)
    
    list_of_instance = import_instances()    
    choice = 1 # None # 0
    # export_instance(list_of_instance)
    
    for instance in list_of_instance:
        if option == '1':
            if choice is None:
                create_routes(instance)
            else:
                create_test_routes(instance, choice)
            local_search(instance)      
        if option == '2':
            create_routes(instance)
            SA(instance, 1000000, 100, 0.8)
        if option == '3':
            GRASP(instance, 50, 20, 0.5)   
        if option == '4':
            create_routes(instance)
            ILS(instance, 5, 10, 200)   
        if option == '5':
            create_routes(instance)
            VNS(instance, 5, 100)     
        if option == '6':
            create_routes(instance)
            VND(instance, 4)   
        else:
            exit 
    
    instance.print_solution(False)

main()