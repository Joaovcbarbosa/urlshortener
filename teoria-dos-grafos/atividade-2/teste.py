class Grafo:
 
    def __init__(self, qtd_vertices):
        self.qtd_vertices = qtd_vertices 
        self.grafo = [[] for i in range(qtd_vertices)] 
   
def main():
    n, m = input().split(' ')
    n = int(n)
    m = int(m)
    g = Grafo(n)
 
    for i in range(m):
        u, v = input().split(' ')    
        u = int(u) - 1
        v = int(v) - 1
        g.grafo[u].append(v)
        g.grafo[v].append(u)
    
main()