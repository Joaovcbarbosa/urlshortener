import sys
 
class Grafo:
 
    def __init__(self, n, m):
        self.n = n
        self.m = m
        self.grafo = self.gerar_grafo(n, m)
 
    def adicionar_aresta(self, u, v):
        self.grafo[u][v] = 1

    def print_grafo(self):
        for linha in self.grafo:
            print(linha)
    
    def gerar_grafo(self, n, m):
        grafo = []

        for i in range(n):         
            linha = []
            for j in range(m):
                linha.append(0)

            grafo.append(linha)  

        return grafo  

    def bpm(self, u, match, visitado): 
        for v in range(self.m): 
            if self.grafo[u][v] and visitado[v] == False:                 
                visitado[v] = True 
                if match[v] == -1 or self.bpm(match[v], match, visitado):
                    match[v] = u
                    return True
        return False
 
    def maxBPM(self):
        match = [-1] * self.m         
        resultado = 0
        for i in range(self.n):             
            visitado = [False] * self.m             
            if self.bpm(i, match, visitado):
                resultado += 1
        return resultado

def main():
    sys.setrecursionlimit(1000000)
    n, m, l = input().split(' ')
    n = int(n)
    m = int(m)
    l = int(l)
    g = Grafo(n, m)
 
    for i in range(l):
        u, v = input().split(' ')    
        u = int(u) 
        v = int(v) 
        g.adicionar_aresta(u, v)    
    
    print(g.maxBPM())
 
main()