from instances import import_instances, export_results, initiate_results
from construction import create_solution
from simulated_annealing import SA
from grasp import GRASP 
from iterated_local_search import ILS
from variable_neighborhood_search import VNS
from large_neighborhood_search import LNS
from biased_random_key_genetic_algorithm import BRKGA

def main():
    
    list_of_instance = import_instances()  
    
    for instance in list_of_instance:
        initiate_results(instance)
        for i in range(6):
            for j in range(10):
                create_solution(instance)   
                if i == 0:         
                    result = BRKGA(instance, BRKGAMax=1000, p=610, pe_min=10, pe_max=30, rhoe_min=55, rhoe_max=80, pm_min=1, pm_max=7, print_solution = False)    
                    MH = 'BRKGA'        
                if i == 1:
                    result = LNS(instance, T0=10000, SAMax=50, cooling_rate=0.9, betta_min=5, betta_max=30, RLC_length_in_percentage=20, alpha=0.1, print_solution = False)   
                    MH = 'LNS'          
                if i == 2:
                    result = ILS(instance, betta_min=5, betta_max=30, ILS_max=500, print_solution = False)   
                    MH = 'ILS'          
                if i == 3:
                    result = SA(instance, T0=1000000, SAMax=50, cooling_rate=0.7, print_solution = False)   
                    MH = 'SA'          
                if i == 4:
                    result = GRASP(instance, GRASP_max=500, RLC_length_in_percentage=20, alpha_min=1, alpha_max=3, print_solution = False)   
                    MH = 'GRASP'                     
                if i == 5:
                    result = VNS(instance, r=12, VNS_max=500, print_solution = False)   
                    MH = 'VNS' 
                
                export_results(instance, MH, j, result)
                instance.reset_solutions()            

main()