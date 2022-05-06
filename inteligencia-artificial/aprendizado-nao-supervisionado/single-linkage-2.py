import pandas as pd
import sklearn
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pyplot as plt

data = pd.read_csv('D31.csv')

X = np.array(data)
clustering = AgglomerativeClustering(n_clusters=int(max(data['C'])),linkage = 'single').fit(X)
plt.scatter(X[:,0], X[:,1],c=clustering.labels_)
plt.show()




