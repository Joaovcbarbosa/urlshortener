# Vitor Galioti Martini - 135543
# Dataset: https://www.kaggle.com/fedesoriano/stroke-prediction-dataset
# Inspirado no código original: https://www.kaggle.com/parthshah12001/stroke-prediction-98-90-accuracy

import pandas as pd
import time
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.utils import resample, shuffle
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB


class DataSet:

    # Construtor da classe
    def __init__(self, x_treino, x_teste, y_treino, y_teste):
        self.x_treino = x_treino
        self.x_teste = x_teste
        self.y_treino = y_treino
        self.y_teste = y_teste
        self.algoritmos = []
        self.precisao = []
        self.tempo_execucao = []

    # Executa o algoritmo
    def executar_algoritmo(self, algoritmo):

        # Verifica qual é o algoritmo
        if algoritmo == 'KNN':
            nome_algoritmo = 'K-Nearest Neighbours'
            execucao = KNeighborsClassifier(n_neighbors=5)
        if algoritmo == 'DT':
            nome_algoritmo = 'Decision Tree'
            execucao = DecisionTreeClassifier()
        if algoritmo == 'RF':
            nome_algoritmo = 'Random Forest'
            execucao = RandomForestClassifier()
        if algoritmo == 'NB':
            nome_algoritmo = 'Naive Bayes'
            execucao = GaussianNB()

        # Inicia variáveis
        precisao = 0
        tempo_execucao = 0

        # Executa o algoritmo 100 vezes
        for i in range(100):
            # Recebe o tempo antes da execução
            tempo_inicio = time.time()

            # Executa o algoritmo
            execucao.fit(self.x_treino, self.y_treino)
            predict = execucao.predict(self.x_teste)

            # Soma as precisões e os tempos de execução
            precisao += accuracy_score(self.y_teste, predict) * 100
            tempo_execucao += time.time() - tempo_inicio

        # Printa os dados
        print(nome_algoritmo)
        print("Precisão: " + str(format(precisao / 100, ".4f")) + "%")  # Média das precisões
        print("Tempo de execução: " + str(format(tempo_execucao / 100, ".4f")) + "s")  # Tempo médio das execuções
        print(" ")

        # Guarda os dados obtidos
        self.precisao.append(float(format(precisao / 100, ".4f")))
        self.tempo_execucao.append(float(format(tempo_execucao / 100, ".4f")))
        self.algoritmos.append(algoritmo)

    # Plota os gráficos
    def plotar_graficos(self):

        # Gráfico em barra: algoritmo x precisão
        fig = plt.figure()
        ax = fig.add_axes([0, 0, 1, 1])
        ax.bar(self.algoritmos, self.precisao)
        ax.set_title('Precisão dos algoritmos')
        ax.set_xlabel('Algoritmos')
        ax.set_ylabel('Precisão (%)')
        plt.show()

        # Gráfico em barra: algoritmo x tempo de execução
        fig = plt.figure()
        ax = fig.add_axes([0, 0, 1, 1])
        ax.bar(self.algoritmos, self.tempo_execucao)
        ax.set_title('Tempo de execução dos algoritmos')
        ax.set_xlabel('Algoritmos')
        ax.set_ylabel('Tempo de Execução (s)')
        plt.show()


def trata_dados():
    # Importa dataset
    df = pd.read_csv('healthcare-dataset-stroke-data.csv')

    # Remove valores nulos
    df.dropna(inplace=True)

    # Transforma os dados categóricos em numéricos
    le = LabelEncoder()
    le.fit(df['smoking_status'])
    df['smoking_status'] = le.transform(df['smoking_status'])
    le.fit(df['work_type'])
    df['work_type'] = le.transform(df['work_type'])
    le.fit(df['Residence_type'])
    df['Residence_type'] = le.transform(df['Residence_type'])
    le.fit(df['ever_married'])
    df['ever_married'] = le.transform(df['ever_married'])
    le.fit(df['gender'])
    df['gender'] = le.transform(df['gender'])

    # Remove coluna ID
    df.drop(['id'], axis=1)

    # Como a classe 0 aparece muito mais que a 1, vamos equilibrar reamostrando os dados com o método Upsampling,
    # aumentando os registros da classe 1
    no_stroke = df[df['stroke'] == 0]
    stroke = df[df['stroke'] == 1]
    upsampling = resample(stroke, replace=True, n_samples=no_stroke.shape[0])
    df = pd.concat([no_stroke, upsampling])
    df = shuffle(df)

    x = df.drop(['stroke'], axis=1)
    y = df['stroke']

    # Separa 70% dos dados para treino e o restante para teste
    x_treino, x_teste, y_treino, y_teste = train_test_split(x, y, train_size=0.7, random_state=101)

    # Cria classe
    d = DataSet(x_treino, x_teste, y_treino, y_teste)

    # Executa o algoritmos
    d.executar_algoritmo('KNN')
    d.executar_algoritmo('DT')
    d.executar_algoritmo('RF')
    d.executar_algoritmo('NB')
    d.plotar_graficos()


if __name__ == '__main__':
    trata_dados()
