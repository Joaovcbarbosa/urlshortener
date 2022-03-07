# Vitor Galioti Martini - 135543
# Código ADAPTADO.
# Fonte do original: https://github.com/ashik0007/mlpr1_iris


from sklearn import naive_bayes, svm, neighbors, ensemble
import numpy as np
import pandas as pd

df = pd.read_csv('iris.data.csv')  # Importa dataset
data = np.array(df)

np.random.shuffle(data)  # Embaralha dados
X_train = np.array(data[0:105, 0:4])  # 105 linhas para treino -> 70% de 150
y_train = np.array(data[0:105, 4])
X_test = np.array(data[105:150, 0:4])  # 105 linhas para testes -> 30% de 150
y_test = np.array(data[105:150, 4])

clf = svm.SVC(C=10, kernel='poly') # Define algoritmo MLP

clf.fit(X_train, y_train)  # Treina o algoritmo
esperado = clf.predict(X_test)  # Predição baseado nos treinos
precisao = clf.score(X_test, y_test)  # Calcula precisão

print('Precisão: ', precisao * 100, '%')
print('Saídas: ', y_test)
print('Saídas esperadas: ', esperado)