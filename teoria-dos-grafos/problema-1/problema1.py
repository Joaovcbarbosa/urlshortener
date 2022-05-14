def DFS(interations, u, v, mark):
    for i in range(len(interations[u])):
        node = interations[u][i]
        if node == v:
            return True
        if mark[node] == 0:
            mark[node] = 1
            if DFS(interations, node, v, mark) == True:
                return True
        
    return False 
 
def mutual(interations, u, v, n):        
    marked = [0 for i in range(n)]
    x = DFS(interations, u, v, marked)
    if x == False:
        return 0
           
    marked = [0 for i in range(n)]
    y = DFS(interations, v, u, marked)
    if y == False:
        return 0
 
    return 1
 
 
def main():
    n, m = input().split(' ')
    n = int(n)
    m = int(m)
    iterations = [[] for i in range(n)] 
    
    for i in range(m):
        u, v = input().split(' ')    
        u = int(u)
        v = int(v)
 
        iterations[u].append(v)
  
    p = input()
    p = int(p)
    x = []
    for i in range(p):
        u, v = input().split(' ')    
        u = int(u)
        v = int(v)
        x.append([u, v])
    
    for i in range(len(x)):
        u = x[i][0]
        v = x[i][1]
        print(mutual(iterations, u, v, n))
 
main()