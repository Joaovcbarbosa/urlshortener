import sys
 
class Grafo:
 
    def __init__(self, qtd_vertices):
        self.qtd_vertices = qtd_vertices 
        self.grafo = [[i for i in range(qtd_vertices)] for i in range(qtd_vertices)] 
        self.tabela = gerar_tabela(qtd_vertices)
 

    def DFS_recursivo(self, u, vertices_visitados):
        vertices_visitados.add(u)
        self.soma_id += u + 1
 
        for v in self.grafo[u]:
            if v not in vertices_visitados:
                self.DFS_recursivo(v, vertices_visitados)
 
    def DFS(self, u, nivel):
        vertices_visitados = set()
        self.DFS_recursivo(u, vertices_visitados, nivel)

    def exchange(self):
        i = 2
        while i <= self.qtd_vertices:
            for j in range(self.qtd_vertices):
                self.DFS(j, i)
                
                
 

def gerar_tabela(n):
    tabela = []

    for i in range(n):         
        linha = []
        j = 0
        flag = 0
        valores = input().split(' ')

        while j < n:
            if i == j:
                linha.append(1)
                flag = 1
            else:
                linha.append(float(valores[j-flag]))
            
            j += 1

        tabela.append(linha)  

    return tabela  
    

def main():
    sys.setrecursionlimit(1000000)
    n = int(input())
    g = Grafo(n)
 
    print(g.grafo)
    print(g.tabela)    
    # g.exchange()
 
main()