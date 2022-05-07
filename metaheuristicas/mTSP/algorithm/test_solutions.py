import instances
import construction
import local_search

def test_local_search():
    instance = instances.generate_test_instance()
    construction.create_test_routes(instance)
    local_search.local_search(instance) 
    assert instance.current_solution_fo == 515.7965443724249

