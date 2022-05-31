from instances import import_instances, export_instance
from construction import create_solution, create_test_solution
from local_search import local_search
from simulated_annealing import SA
from grasp import GRASP 
from iterated_local_search import ILS
from variable_neighborhood_search import VNS
from variable_neighborhood_descent import VND
from large_neighborhood_search import LNS
from biased_random_key_genetic_algorithm import BRKGA
# from sys import setrecursionlimit

def main():
    # setrecursionlimit(100000000)
    input_string = ('1 -> Local Search\n' +
                    '2 -> SA\n' +
                    '3 -> GRASP \n' +
                    '4 -> ILS\n' +
                    '5 -> VNS\n' +
                    '6 -> VND\n' +
                    '7 -> LNS\n' +
                    '8 -> BRKGA\n')
    option = input(input_string)
    
    list_of_instance = import_instances()    
    choice = None # None, 0, 1, 2
    # export_instance(list_of_instance)
    
    for instance in list_of_instance:
        if choice is None:
            create_solution(instance)
        else:
            create_test_solution(instance, choice)

        if option == '1':            
            local_search(instance)    
        if option == '2':
            SA(instance, T0=1000000, SAMax=200, cooling_rate=0.9)
        if option == '3':
            GRASP(instance, GRASP_max=300, RLC_length_in_percentage=20, alpha=0.3)   
        if option == '4':
            ILS(instance, betta_min=20, betta_max=40, ILS_max=300)   
        if option == '5':
            VNS(instance, betta_min=20, betta_max=40, VNS_max=50)     
        if option == '6':
            VND(instance, r=6)     
        if option == '7':
            LNS(instance, T0=1000000, SAMax=100, cooling_rate=0.9, betta_min=20, betta_max=40, RLC_length_in_percentage=20, alpha=0.3)  
        if option == '8':
            BRKGA(instance, BRKGAMax=2000, p=610, pe_min=10, pe_max=30, rhoe_min=55, rhoe_max=80, pm_min=20, pm_max=40)
        else:
            exit 
    
    instance.print_solution(False)

main()