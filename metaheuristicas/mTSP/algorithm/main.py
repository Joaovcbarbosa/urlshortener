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
            routes = construction.create_routes(instance)
            routes = local_search.local_search(instance, routes)            
        if option == '2':
            routes = construction.create_routes(instance)
            routes = simulated_annealing.SA(instance, routes, 5000000, 1000, 0.8)
        if option == '3':
            routes = grasp.GRASP(instance, 250, 20, 0.5)   
        else:
            exit 
    
    instance.print_solution()

main()