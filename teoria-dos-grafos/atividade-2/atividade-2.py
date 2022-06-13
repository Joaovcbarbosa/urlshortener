import sys
 
class Grafo:
 
    def __init__(self, qtd_vertices):
        self.qtd_vertices = qtd_vertices 
        self.grafo = [[] for i in range(qtd_vertices)] 
        self.soma_id = 0
 
    def adicionar_aresta(self, u, v):
        self.grafo[u].append(v)
        self.grafo[v].append(u)
 
    def eh_vertice_de_corte(self, u, vertices_visitados, pai):
        vertices_visitados[u] = True
        filho = 0
        for v in self.grafo[u]:
            if vertices_visitados[v] == False :
                pai[v] = u
                filho += 1
                self.eh_vertice_de_corte(v, vertices_visitados, pai)
                if pai[u] == -1 and filho > 1:
                    return True
 
        return False 
 
    def vertice_de_corte(self):
        # vertices_visitados = [False] * (self.qtd_vertices)
        # pai = [-1] * (self.qtd_vertices)
 
        # i = self.qtd_vertices - 1
 
        # if len(self.grafo[i]) >= 2:
        #     return self.calcular_soma_maior_regiao()
 
        # if self.eh_vertice_de_corte(self.qtd_vertices - 1, vertices_visitados, pai) == False:
        #     return i + 1
        
        return self.calcular_soma_maior_regiao()
 
    def calcular_soma_maior_regiao(self):
        raizes = []
        sum_ids = 0
        max_id = 0
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
 
    print(g.vertice_de_corte())
    
 
main()