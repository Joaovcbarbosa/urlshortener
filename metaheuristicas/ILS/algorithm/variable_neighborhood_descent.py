from local_search import inter_route_swap, inter_route_shift, intra_route_2opt

def VND(instance, ILS_max):
    fo_best = instance.best_solution()[0]
    fo_S = fo_best
    k = 1
    r = 3
    
    while k <= r:        
        if k == 1:                    
            if intra_route_2opt(instance, instance.current_solution) == False:
                return False                          
        if k == 2:                    
            if inter_route_shift(instance, instance.current_solution) == False:
                return False                             
        if k == 3:                     
            if inter_route_swap(instance, instance.current_solution) == False:
                return False                            
               
        fo_S = instance.current_solution_fo

        if fo_S < fo_best:
            fo_best = fo_S
            k = 1
        else:
            k+=1      


