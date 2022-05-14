class Grafo:
  
    def __init__(self, qtd_vertices):
        self.grafo = [[] for i in range(qtd_vertices)] 
        self.qtd_vertices = qtd_vertices
  
    def BFS(self, u, v):        
        visitados = [False] * (self.qtd_vertices)  
        fila = []
        fila.append(u)
        visitados[u] = True  
        while fila: 
            n = fila.pop(0)
            if n == v:
                return True                
            for i in self.grafo[n]:
                if visitados[i] == False:
                    fila.append(i)
                    visitados[i] = True
        return False
  
def main():
    n, m = input().split(' ')
    n = int(n)
    m = int(m)
    g = Grafo(n)

    for i in range(m):
        u, v = input().split(' ')    
        u = int(u)
        v = int(v)
        g.grafo[u].append(v)

    p = input()
    p = int(p)
    x = []
    for i in range(p):
        u, v = input().split(' ')    
        u = int(u)
        v = int(v)
        if g.BFS(u, v) == True and g.BFS(v, u):
            x.append(1)
        else:
            x.append(0)

    for item in x:
        print(item)
 
main()