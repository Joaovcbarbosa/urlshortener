from threading import local
import instances
import construction
import local_search
import simulated_annealing

def main():
    list_of_instance = instances.import_instances()
    for instance in list_of_instance:
        routes = construction.create_routes(instance)
        routes = simulated_annealing.SA(instance, routes, 5000000, 1000, 0.8)
        # local_search.local_search(instance, routes)
        # construction.print_routes(instance, routes)

main()