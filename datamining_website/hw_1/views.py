from django.shortcuts import render
from models import map_date, utm_data
from django.template import loader
import json
import lshash
import logging
# Create your views here.

# def get_road_data(data):
import decimal, simplejson


class my_lsh(object):
    def __init__(self):
        self.hash_bucket = {}
        self.vector_data = {}
        self.lsh = None
        self.init = False

    @staticmethod
    def get_hash_index(x, y):
        x_range = (362800 - 346000) / 20
        hash_x = int((x - 34600) / 20)
        hash_y = int((y - 3448600) / 20) + 1
        return x_range * hash_x + hash_y

    def lsh_search(self, hash_size):
        with open('roaddata.json', 'r') as f:
            data = json.load(f)

        for road_index in data:
            for point in data[road_index]:
                self.hash_bucket.setdefault(my_lsh.get_hash_index(point[0], point[1]), 0)

        self.lsh = lshash.LSHash(hash_size, len(self.hash_bucket))
        for r in data:
            for p in data[r]:
                self.hash_bucket[my_lsh.get_hash_index(p[0], p[1])] = 1
            self.lsh.index(self.hash_bucket.values(), extra_data=r)
            self.vector_data.setdefault(r, self.hash_bucket.values())
            for d in self.hash_bucket:
                self.hash_bucket[d] = 0
        self.init = True

    def query(self, num):
        ans = self.lsh.query(self.vector_data[num])
        da = []
        for r in ans:
            da.append(r[0][1])
        return da

lsh_method = my_lsh()
lsh_method.lsh_search(10)


def get_all_road():
    data = map_date.objects.all()
    data = list(data)
    roads= {}
    li_index = 1;
    road = []
    for r in data:
        if li_index != r.line_id:
            roads.setdefault(li_index,road)
            road = []
            li_index+=1
        road.append([r.latitude, r.longitude])
    roads.setdefault(li_index,road)
    return  roads

def get_road_by_num(num):
    data = map_date.objects.filter(line_id=num)
    data = list(data)
    road = []
    for point in data:
        road.append([point.latitude, point.longitude])
    return road


class DecimalJSONEncoder(simplejson.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)
        return super(DecimalJSONEncoder, self).default(o)


def index(request):
    with open('mapdata.json', 'r') as f:
        data = json.load(f)

    roads = []
    for re_index in data:
        roads.append(data[re_index])
    road = json.dumps(roads, cls=DecimalJSONEncoder)
    return render(request, "hw_1/index.html", {"road": road})


def get_road(request, line_num, bucket):
    ans = lsh_method.query(line_num)
    roads=[]
    for i in ans:
        roads.append(get_road_by_num(int(i)))
    temp = json.dumps(roads, cls=DecimalJSONEncoder)
    return render(request, "hw_1/index.html", {"road": temp})




