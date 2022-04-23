import instances
import construction
import local_search

def main():
    list_of_instance = instances.import_instances()
    for instance in list_of_instance:
        routes = construction.create_routes(instance)
        construction.print_routes(instance, routes)
        local_search.local_search(instance, routes)
        construction.print_routes(instance, routes)

main()