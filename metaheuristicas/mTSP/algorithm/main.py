import instances
import construction
import simulated_annealing

def main():
    list_of_instance = instances.import_instances()
    for instance in list_of_instance:
        routes = construction.create_routes(instance)
        # construction.print_routes(instance, routes)
        simulated_annealing.SA(instance, routes, 5000000, 1000, 0.9999)
        # construction.print_routes(instance, routes)

main()