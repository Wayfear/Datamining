from django.shortcuts import render
from models import map_date, utm_data
import json
import lshash
from sklearn.neighbors import NearestNeighbors
import numpy as np
import pandas as pd
import decimal, simplejson


class all_road(object):
    def __int__(self):
        self.all_road_data = None

    def load_data(self):
        with open('mapdata.json', 'r') as f:
            data = json.load(f)
        roads = []
        for re_index in data:
            roads.append(data[re_index])
        self.all_road_data = json.dumps(roads, cls=DecimalJSONEncoder)


class DecimalJSONEncoder(simplejson.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)
        return super(DecimalJSONEncoder, self).default(o)

class search_method(object):
    def __init__(self):
        self.vector_data = {}
        self.lsh = None
        self.is_init = False
        self.hash_size = 10
        self.knn_res = None
        self.bucket_length = 0

    @staticmethod
    def get_hash_index(x, y):
        x_range = (362800 - 346000) / 20
        hash_x = int((x - 34600) / 20)
        hash_y = int((y - 3448600) / 20) + 1
        return x_range * hash_x + hash_y

    def init(self):
        with open('roaddata.json', 'r') as f:
            data = json.load(f)
        file_name = "Traj_1000_SH_UTM"
        file_data = pd.read_csv(file_name)
        x_data = file_data['X'].values
        y_data = file_data['Y'].values
        tid = file_data['Tid'].values
        hash_bucket = {}

        x_y = zip(x_data, y_data)
        for x, y in x_y:
            hash_bucket.setdefault(self.get_hash_index(x, y), 0)
        self.bucket_length = len(hash_bucket)
        self.lsh = lshash.LSHash(self.hash_size, len(hash_bucket))
        npX = []
        for r in data:
            for p in data[r]:
                hash_bucket[search_method.get_hash_index(p[0], p[1])] = 1
            self.lsh.index(hash_bucket.values(), extra_data=r)
            self.vector_data.setdefault(r, hash_bucket.values())
            npX.append(hash_bucket.values())
            for d in hash_bucket:
                hash_bucket[d] = 0
        npX = np.array(npX)
        nbrs = NearestNeighbors(n_neighbors=5, algorithm='ball_tree').fit(npX)
        distances, self.knn_res = nbrs.kneighbors(npX)
        self.is_init = True

    def set_hash_size(self, size):
        if self.hash_size == size:
            return None
        self.hash_size = size
        self.lsh = lshash.LSHash(self.hash_size, len(self.bucket_length))
        for da in self.vector_data:
            self.lsh.index(self.vector_data[da], extra_data=da)

    def lsh_query(self, num):
        ans = self.lsh.query(self.vector_data[num])
        da = []
        for r in ans:
            da.append(r[0][1])
        return da

    def knn_query(self, n, index):
        if n > 5:
            n = 5
        return self.knn_res[index][:n]


se_method = search_method()
se_method.init()

allroad = all_road()
allroad.load_data()


def get_road_by_num(num):
    data = map_date.objects.filter(line_id=num)
    data = list(data)
    road = []
    for point in data:
        road.append([point.latitude, point.longitude])
    return road


def index(request):
    return render(request, "hw_1/google_template.html", {"road": allroad.all_road_data})


def get_road_by_lsh(request, line_num, bucket):
    ans = se_method.lsh_query(line_num)
    roads=[]
    for i in ans:
        roads.append(get_road_by_num(int(i)))
        print i
    temp = json.dumps(roads, cls=DecimalJSONEncoder)
    # return render(request, "hw_1/index.html", {"road": allroad.all_road_data, "select_road": temp})
    return temp


def get_road_by_knn(request, line_num, k):
    ans = se_method.knn_query(int(line_num), int(k))
    roads=[]
    for i in ans:
        roads.append(get_road_by_num(int(i)))
        print i
    temp = json.dumps(roads, cls=DecimalJSONEncoder)
    return render(request, "hw_1/index.html", {"road": allroad.all_road_data, "select_road": temp})




