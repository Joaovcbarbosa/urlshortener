from instances import generate_test_instance
from construction import create_test_routes
from local_search import local_search

def test_local_search():
    instance = generate_test_instance()
    create_test_routes(instance, 0)
    local_search(instance) 
    assert instance.current_solution_fo == 575.84


