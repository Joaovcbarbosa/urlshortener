# Vitor Galioti Martini
# 135543
import random

# Algoritmo ACO
class Grafo:

    # Construtor do grafo
    def __init__(self, vertices, alpha, beta, rho, tau):
        self.vertices = vertices
        self.caminho = [[] for i in range(self.vertices)]
        self.feromonio = [[] for i in range(self.vertices)]
        self.visitados = [0 for i in range(vertices)]
        self.a = alpha
        self.b = beta
        self.r = rho
        self.t = tau

    # Percorre cada aresta e recebe o valor do usuário
    def adicionar_valor_aresta(self):
        for i in range(self.vertices):
            if i != 0:
                print("Vértice ", i, ": ")
                for j in range(self.vertices):
                    if j != 0:
                        if j != i:
                            mensagem = "Aresta (" + str(i) + " " + str(j) + "), peso: "
                            valor = int(input(mensagem))
                            self.caminho[i].append([j, valor])
                            self.feromonio[i].append([j, self.t])
                        else:
                            self.caminho[i].append([j, 0])
                            self.feromonio[i].append([j, 0])

    # Calcula a probabilidade daquele caminho ser tomado
    def probabilidade(self, vertice_atual, i):
        normalizacao = 0
        for j in range(self.vertices - 1):
            if self.visitados[self.caminho[vertice_atual][j][0]] == 0 or j == vertice_atual:
                normalizacao += (
                            self.feromonio[vertice_atual][j][1] * self.a * self.b * 1 / self.caminho[vertice_atual][j][
                        1])

        return float("{:.2f}".format(((self.feromonio[vertice_atual][i - 1][1] * self.a * self.b * 1 /
                                       self.caminho[vertice_atual][i - 1][1]) / normalizacao)))

    # Caminhar
    def caminhar(self, comeco):
        # Começa do vértice atual
        percurso = [comeco]
        vertice_atual = comeco
        i = 0

        # Seta os visitados para zero
        self.visitados = [0 for i in range(self.vertices)]

        # Enquanto houver vértices
        while i < self.vertices - 1:

            # Reseta variável que recebe o melhor vértice
            Gbest = None

            # Caso o vértice ainda não foi visitado
            if self.visitados[vertice_atual] == 0:
                self.visitados[vertice_atual] = 1

                # Percorre os vértices adjacentes
                for vertices in self.caminho[vertice_atual]:
                    # Caso não seja o vértice atual (pois o vértice A se liga com ele mesmo com peso 0)
                    if self.visitados[vertices[0]] == 0:
                        # Se ainda não tem melhor vértice definido, seta o primeiro encontrado
                        if Gbest is None:
                            Gbest = vertices[0]
                            Fbest = self.probabilidade(vertice_atual, Gbest)
                        else:  # Caso contrário, verifica a probabilidade do vértice analisado ser o melhor, se for, armazena em Gbest
                            if self.probabilidade(vertice_atual, vertices[0]) > Fbest:
                                Gbest = vertices[0]
                                Fbest = self.probabilidade(vertice_atual, vertices[0])

            # Caso não tenha chegado no fim, adiciona o vértice no percurso
            if Gbest is not None:
                vertice_atual = Gbest
                percurso.append(Gbest)

            i += 1

        print("")
        print("Percurso: ", percurso)

    # Atuliza o valor do feromônios
    def atualizar_feromonio(self):
        # Percorre cada feromônio e atualiza seu valor com a formula
        for i in range(self.vertices):
            if i != 0:
                for j in range(self.vertices - 1):
                    if self.caminho[i][j][1] != 0:
                        self.feromonio[i][j][1] = float("{:.2f}".format(
                            (1 - self.r) * self.feromonio[i][j][1] + self.r * 1 / self.caminho[i][j][1]))

    # Exibe o valor dos feromônios
    def exibir_feromonio(self):
        print("")
        print("Feromônio:")
        print('  ', end=' ')
        for i in range(self.vertices):
            if i != 0:
                if i == self.vertices - 1:
                    print(i)
                else:
                    print(i, end='   ')

        for i in range(self.vertices):
            if i != 0:
                print(i, end='  ')
                for j in self.feromonio[i]:
                    print(j[1], end='   ')

                print("")

    # Exibe a qualidade das arestas
    def exibir_qualidade_aresta(self):
        print("")
        print("Qualidade das arestas")
        print('  ', end=' ')

        for i in range(self.vertices):
            if i != 0:
                if i == self.vertices - 1:
                    print(i)
                else:
                    print(i, end='   ')

        for i in range(self.vertices):
            if i != 0:
                print(i, end='  ')
                for j in self.caminho[i]:
                    print(j[1], end='   ')

                print("")

        print("")

    # Executa o algoritmo começando de cada vertice
    def executar(self):
        i = 1
        # Enquanto houver vértices
        while i < self.vertices:
            # Caminha para os vértices vizinhos
            self.caminhar(i)

            # Atualiza os feromônios
            self.atualizar_feromonio()

            # Mostra o feromônio
            self.exibir_feromonio()

            i += 1


def ACO():
    # Recebe as entradas do usuário
    qtd_vertices = int(input("Informe o n° de vértices: "))
    a = float(input("Informe alpha: "))
    b = float(input("Informe beta: "))
    r = float(input("Informe rho: "))
    t = float(input("Informe tau: "))

    # Monta o grafo
    g = Grafo(qtd_vertices + 1, a, b, r, t)

    # Adiciona as arestas
    g.adicionar_valor_aresta()

    # Exibe a qualidade das arestas
    g.exibir_qualidade_aresta()

    # Começa o percurso
    g.executar()


# Função f, recebe a equação do usuário e a resolve com a função eval
def f(funcao, x):
    return eval(funcao)

# Algoritmo PSO
def PSO():
    # Recebe as entradas do usuário:
    funcao = input('f(x) = ')
    w = float(input('w = '))
    c1 = float(input('c1 = '))
    c2 = float(input('c2 = '))
    r1 = float(input('r1 = '))
    r2 = float(input('r2 = '))
    n = int(input('n = '))
    iteracoes = int(input('iteracoes = '))

    # Gera partículas para X e V randomicamente
    x = []
    v = []
    for i in range(n):
        x.append(float("{:.4f}".format((random.uniform(0, 1) - 0.5) * 10)))
        v.append(float("{:.4f}".format(random.uniform(0, 1) - 0.5)))

    # Entradas usadas no exercício teórico:
    # x = [-0.343, 3.956, -1.123, -0.098, 0.039]
    # v = [0.0319, 0.3185, 0.3331, 0.2677, -0.3292]

    # Inicia PBest como uma cópia de X e Gbest como a primeira partícula de X
    Pbest = x
    Gbest = x[0]
    Fbest = float("{:.4f}".format(f(funcao, 0)))

    # Percorre as partículas de X comparando cada uma para chegar no melhor valor de Gbest
    for i in x:
        if f(funcao, i) > Gbest:
            Gbest = i
            Fbest = float("{:.4f}".format(f(funcao, i)))

    # Printa os valores
    print("Local best position: ", Pbest)
    print("Global best fitness: ", Fbest)
    print("Global best position: ", Gbest)
    print(" ")

    # A execução acima foi a primeira interação, agora executa as restantes:
    while iteracoes - 1 > 0:

        # Percorre partículas
        for i in range(n):
            # Define os valores V e X conforme equações vistas em aula
            v[i] = float("{:.4f}".format(w * v[i] + c1 * r1 * (Pbest[i] - x[i]) + c2 * r2 * (Gbest - x[i])))
            x[i] = float("{:.4f}".format(x[i] + v[i]))
            # Redefine PBest caso encontre um valor que o maximize
            if f(funcao, Pbest[i]) < f(funcao, x[i]):
                Pbest = x[i]
            # O mesmo para Gbest
            if f(funcao, Gbest) < f(funcao, x[i]):
                Gbest = x[i]
                Fbest = float("{:.4f}".format(f(funcao, x[i])))

        # Printa os valores
        print("Local best position: ", Pbest)
        print("Global best fitness: ", Fbest)
        print("Global best position: ", Gbest)
        print(" ")

        iteracoes -= 1

# Pergunta ao usuário qual algoritmo ele deseja executar:
opcao = int(input("1 para AOC, 2 para SO e qualquer outro número para sair: "))

# Executa o algoritmo
if opcao == 1:
    ACO()
elif opcao == 2:
    PSO()