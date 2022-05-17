# Vitor Galioti Martini 
# 135543

import sys
class Grafo:
  
    def __init__(self, qtd_vertices):
        self.grafo = [[] for i in range(qtd_vertices)] 
        self.qtd_vertices = qtd_vertices
   
    def adicionar_aresta(self, u, v):
        self.grafo[u].append(v)
        
    def montar_pilha(self, vertice, vertices_visitados, pilha):
        vertices_visitados[vertice] = True
        for i in self.grafo[vertice]:
            if vertices_visitados[i] == False:
                self.montar_pilha(i, vertices_visitados, pilha)
        pilha = pilha.append(vertice)
        
    def grafo_transposto(self):
        g_transposto = Grafo(self.qtd_vertices)  
        for i in range(len(self.grafo)):
            for j in self.grafo[i]:
                g_transposto.adicionar_aresta(j,i)
        return g_transposto

    def CFC(self):          
        pilha = []
        vertices_visitados = [False] * (self.qtd_vertices)

        for i in range(self.qtd_vertices):
            if vertices_visitados[i] == False:
                self.montar_pilha(i, vertices_visitados, pilha)
  
        grafo_transposto = self.grafo_transposto()           
        vertices_visitados = [False] * (self.qtd_vertices)
        cfc = [-1] * (self.qtd_vertices) # Vetor que indica em qual CFC o vértice está
        cfc_index = 0

        while pilha:
            i = pilha.pop()
            if vertices_visitados[i] == False:
                grafo_transposto.DFS(i, vertices_visitados, cfc_index, cfc)
                cfc_index += 1

        return cfc
   
    def DFS(self, vertice, vertices_visitados, cfc_index, cfc):
        vertices_visitados[vertice] = True
        cfc[vertice] = cfc_index
        for i in self.grafo[vertice]:
            if vertices_visitados[i] == False:
                self.DFS(i, vertices_visitados, cfc_index, cfc)
    
def main():   
    sys.setrecursionlimit(1000000)
    n, m = input().split(' ')
    n = int(n)
    m = int(m)
    g = Grafo(n)
 
    for i in range(m):
        u, v = input().split(' ')    
        u = int(u)
        v = int(v)
        g.adicionar_aresta(u, v)
 
    cfc = g.CFC()    
    p = input()
    p = int(p)
    resp = [0] * p

    for i in range(p):
        u, v = input().split(' ')    
        u = int(u)
        v = int(v)
        if cfc[u] == cfc[v]: # Verifica se os vértices estão no mesmo CFC
            resp[i] = 1

    for item in resp:
        print(item)     
                 
main()