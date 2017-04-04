import utm
import lshash
import pandas as pd
import json
from CoordTransform import wgs84togcj02
from sklearn.neighbors import NearestNeighbors
import numpy as np



class Load_data:
    def __init__(self):
        self.file_name = "Traj_1000_SH_UTM"
        self.hash_bucket = None
        self.utm_data = None
        self.vector_data = None
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
            self.vector_data.setdefault(int(r), self.hash_bucket.values())
            for d in self.hash_bucket:
                self.hash_bucket[d] = 0






