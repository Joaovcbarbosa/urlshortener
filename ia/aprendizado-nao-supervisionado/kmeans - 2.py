import pandas as pd
from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pyplot as plt

data = pd.read_csv('D31.csv')

X = np.array(data)
kmeans = KMeans(n_clusters=int(max(data['C'])), random_state = 0).fit(X)
plt.scatter(X[:,0], X[:,1],c=kmeans.labels_)
plt.show()


