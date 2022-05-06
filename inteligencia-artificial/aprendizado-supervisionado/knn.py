# Vitor Galioti Martini
# 135543
import random
import csv
import math

# Algoritmo KNN
class Dados:

    # Construtor da classe
    def __init__(self, treino, testes):
        self.treino = treino
        self.testes = testes
        self.numero_acertos = 0

    # Algoritmo KNN
    def KNN(self):

        # Percorre os registros de teste
        i = 0
        while i < len(self.testes):
            distancia = []

            # Percorre os treinos
            j = 0
            while j < len(self.treino):

                # Faz o somatório daquele teste com o registro de treino atual
                k = 1
                soma = 0
                while k < 5:
                    soma = soma + (float(self.treino[j][k]) - float(self.testes[i][k]))**2
                    k += 1

                # Adiciona o valor na lista
                distancia.append([math.sqrt(soma), self.treino[j][k], self.treino[j][0]])
                j += 1

            melhores = []
            # Ordena os 3 registros que tiveram o melhor desempenho (K = 3)
            for linha in sorted(distancia, key=lambda x: x[0])[:3]:
                melhores.append(linha[1])

            # Se a classificação do registro teste for igual a classificação encontrada
            if self.testes[i][5] == max(set(melhores), key=melhores.count):
                self.numero_acertos += 1

            i += 1

        # Retorno
        precisao = float("{:.2f}".format(100 * self.numero_acertos / len(self.testes)))
        print("O algoritmo acertou: ", str(self.numero_acertos), " de ", str(len(self.testes)), " testes. Precisão: ", precisao, "%.")


def Importar():
    # Importa arquivo
    arquivo = open("Iris.csv")
    data_set = csv.reader(arquivo)

    # Cria lista com os dados
    lista_data_set = list(data_set)
    lista_data_set.pop(0) # Retirando cabeçalho
    tamanho_data_set = len(lista_data_set)

    # Separa 30% dos dados para testes e 70% para treino
    lista_treino = []
    lista_testes = []

    # Atribui aleatoriamente os registros para treino e teste com base no dataset
    i = 1
    while i < int(tamanho_data_set * 70 / 100):
        index = lista_data_set.index(random.choice(lista_data_set))
        lista_treino.append(lista_data_set[index])
        lista_data_set.pop(index)
        i += 1

    i = 0
    while i <= int(tamanho_data_set * 30 / 100):
        index = lista_data_set.index(random.choice(lista_data_set))
        lista_testes.append(lista_data_set[index])
        lista_data_set.pop(index)
        i += 1

    d = Dados(lista_treino, lista_testes)

    #Executa o algoritmo KNN
    d.KNN()

if __name__ == '__main__':
    Importar()
