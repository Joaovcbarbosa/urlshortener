# Vitor Galioti Martini - 135543

class Grafo:

    # Monta o Grafo
    def __init__(self, quantidade_vertices):
        self.quantidade_vertices = quantidade_vertices
        self.grafo = [[] for i in range(quantidade_vertices)]
        self.vertices_visitados = [0 for i in range(quantidade_vertices)]

    # Adiciona as arestas
    def adicionar_arestas(self, matriz, n, todas_direcoes):
        k = 0  # K representa a posição do vertica dentro do grafo

        # Percorre as linhas e colunas da matriz
        for i in range(n):
            for j in range(n):

                # Se o conteúdo for ".", insere o vértice
                if matriz[i][j] == ".":

                    # Se existir vértice a direita e ele for ".", faz a ligação dos vértices
                    if j != n - 1:
                        if matriz[i][j + 1] == ".":
                            self.grafo[k].append(k + 1)
                            if todas_direcoes == True:
                                self.grafo[k + 1].append(k)

                    # Se existir vértice abaixo e ele for ".", faz a ligação dos vértices
                    if i != n - 1:
                        if matriz[i + 1][j] == ".":
                            self.grafo[k].append(k + n)
                            if todas_direcoes == True:
                                self.grafo[k + n].append(k)

                k += 1

    # Algoritmo de busca em profundidade
    def busca_profundidade(self, todas_direcoes):
        pilha = []
        i = 0
        pilha.append(0)  # adiciona o nó inicial
        while len(pilha) > 0:
            vertice_atual = pilha.pop()

            if vertice_atual == self.quantidade_vertices - 1:
                i += 1
                if todas_direcoes == True:
                    break

            if todas_direcoes == False:
                for vertices in self.grafo[vertice_atual]:
                    pilha.append(vertices)
            else:
                if self.vertices_visitados[vertice_atual] == 0:
                    self.vertices_visitados[vertice_atual] = 1
                    for vertices in self.grafo[vertice_atual]:
                        pilha.append(vertices)

        return i

class Matriz:

    #Monta a matriz com "." e "#"
    def __init__(self, matriz, quantidade_vertices):
        self.matriz = matriz
        for i in range(quantidade_vertices):
            self.matriz.append([])
            linha = input()
            for j in range(quantidade_vertices):
                self.matriz[i].append(linha[j])

quantidade_vertices = int(input())
matriz = []
g1 = Grafo(quantidade_vertices * quantidade_vertices)
m = Matriz(matriz, quantidade_vertices)
g1.adicionar_arestas(m.matriz, quantidade_vertices, False)
i = g1.busca_profundidade(False)

if i != 0:
    print(i)
else:
    g2 = Grafo(quantidade_vertices * quantidade_vertices)
    g2.adicionar_arestas(m.matriz, quantidade_vertices, True)
    i = g2.busca_profundidade(True)
    if i == 0:
        print("INCONCEIVABLE")
    else:
        print("THE GAME IS A LIE")
