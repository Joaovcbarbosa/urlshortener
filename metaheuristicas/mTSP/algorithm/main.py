import instances
import construction
import local_search
import simulated_annealing
import grasp 

def main():
    option = input('1 -> Local Search\n2 -> SA\n3 -> GRASP\n')
    list_of_instance = instances.import_instances()
    # instances.export_instance(list_of_instance)

    for instance in list_of_instance:
        if option == '1':
            construction.create_routes(instance)
            local_search.local_search(instance)      
        if option == '2':
            construction.create_routes(instance)
            simulated_annealing.SA(instance, 5000000, 1000, 0.8)
        if option == '3':
            grasp.GRASP(instance, 250, 20, 0.5)   
        else:
            exit 
    
    instance.print_solution()

main()