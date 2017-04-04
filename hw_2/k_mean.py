from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples, silhouette_score
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import pandas as pd
import json
import math

range_n_clusters = [2, 3, 4, 5, 6]

k = int(math.sqrt(1000/2))
print k

class Load_data:
    def __init__(self):
        self.file_name = "Traj_1000_SH_UTM"
        self.hash_bucket = None
        self.utm_data = None
        self.vector_data = []
        self.lon_lat_data = None

    @staticmethod
    def get_hash_index(x, y):
        x_range = (362800 - 346000) / 20
        hash_x = int((x - 34600) / 20)
        hash_y = int((y - 3448600) / 20) + 1
        return x_range*hash_x+hash_y

    def init(self):
        with open('roaddata.json', 'r') as utm_f:
            self.utm_data = json.load(utm_f)
        with open('mapdata.json', 'r') as lon_lat_f:
            self.lon_lat_data = json.load(lon_lat_f)

        file_data = pd.read_csv(self.file_name)
        x_data = file_data['X'].values
        y_data = file_data['Y'].values

        self.hash_bucket = {}
        x_y = zip(x_data, y_data)
        for x, y in x_y:
            self.hash_bucket.setdefault(Load_data.get_hash_index(x, y), 0)

        print len(self.hash_bucket)

        for r in self.utm_data:
            for p in self.utm_data[r]:
                self.hash_bucket[Load_data.get_hash_index(p[0], p[1])] = 1
            self.vector_data.append(self.hash_bucket.values())
            for d in self.hash_bucket:
                self.hash_bucket[d] = 0

file_data = Load_data()
file_data.init()
X = np.array(file_data.vector_data)
# for i in range(500,10000,1000):
#     pca = PCA(n_components=i)
#     pca.fit(X)
#     print str(i)+": "+ str(pca.explained_variance_ratio_)
pca = PCA(n_components=100)
X = pca.fit_transform(X)
print str(600)+": "+ str(pca.explained_variance_ratio_)

for clusters in range(k-5,k+10):
    kmeans = KMeans(n_clusters=clusters, random_state=0)
    cluster_labels = kmeans.fit_predict(X)
    silhouette_avg = silhouette_score(X, cluster_labels)
    print cluster_labels
    print str(clusters)+":"+str(silhouette_avg)
    # sample_silhouette_values = silhouette_samples(X, cluster_labels)
    # i = 0
    # print sample_silhouette_values







