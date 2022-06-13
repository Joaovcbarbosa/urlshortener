import sys
 
class Grafo:
 
    def __init__(self, qtd_vertices):
        self.qtd_vertices = qtd_vertices 
        self.grafo = [[] for i in range(qtd_vertices)] 
        self.soma_id = 0
 
    def adicionar_aresta(self, u, v):
        self.grafo[u].append(v)
        self.grafo[v].append(u)
 
    def calcular_soma_maior_regiao(self):
        raizes = []
        sum_ids = 0
        max_id = 0
        if len(self.grafo[self.qtd_vertices - 1]) >= 2:
            for v in self.grafo[self.qtd_vertices - 1]:
                self.grafo[v].remove(self.qtd_vertices - 1)
                raizes.append(v)
    
            for u in raizes:
                value = self.DFS(u)
                sum_ids += value
                if value > max_id:
                    max_id = value
 
        return sum_ids - max_id + self.qtd_vertices
 
    def DFS_recursivo(self, u, vertices_visitados):
        vertices_visitados.add(u)
        self.soma_id += u + 1
 
        for v in self.grafo[u]:
            if v not in vertices_visitados:
                self.DFS_recursivo(v, vertices_visitados)
 
    def DFS(self, u):
        vertices_visitados = set()
        self.soma_id = 0
        self.DFS_recursivo(u, vertices_visitados)
 
        return self.soma_id 
 
def main():
    sys.setrecursionlimit(1000000)
    n, m = input().split(' ')
    n = int(n)
    m = int(m)
    g = Grafo(n)
 
    for i in range(m):
        u, v = input().split(' ')    
        u = int(u) - 1
        v = int(v) - 1
        g.adicionar_aresta(u, v)
 
    print(g.calcular_soma_maior_regiao())
    
 
main()