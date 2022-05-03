import instances
import construction
import local_search
import simulated_annealing
import grasp 

def main():
    option = input('1 -> Local Search\n2 -> SA\n3 -> GRASP\n')
    list_of_instance = instances.import_instances()
    
    for instance in list_of_instance:
        if option == '1':
            routes = construction.create_routes(instance)
            routes = local_search.local_search(instance, routes)
            construction.print_routes(instance, routes)
        if option == '2':
            routes = construction.create_routes(instance)
            routes = simulated_annealing.SA(instance, routes, 1000000, 200, 0.99)
        if option == '3':
            routes = grasp.GRASP(instance)            
            routes = local_search.local_search(instance, routes)
            construction.print_routes(instance, routes)
        else:
            exit 
        

main()