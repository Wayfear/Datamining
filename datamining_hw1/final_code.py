import utm
import lshash
import pandas as pd
import json
from CoordTransform import wgs84togcj02
from sklearn.neighbors import NearestNeighbors
import numpy as np

file_name = "Traj_1000_SH_UTM"

# 一个用于存放数据中被映射到的点的hash值的容器
hash_bucket = {}

# 按路径的序号存放路径的坐标（utm）集合
road_data = {}

# 按路径的序号存放路径的转换后向量
vector_data = {}

# 待设置的hash_size
hash_size = {10,11,12,13,14,15}

# 待查询的序号
search_index = {15, 250, 480, 690, 900}

# 按路径的序号存放路径的坐标（经纬度）集合，结果输出到文件中，给服务器使用
json_data ={}

# utm坐标到hash序号的转换函数
def get_hash_index(x, y):
    x_range = (362800 - 346000) / 20
    hash_x = int((x - 34600) / 20)
    hash_y = int((y - 3448600) / 20) + 1
    return x_range*hash_x+hash_y

# 读取文件
file_data = pd.read_csv(file_name)
x_data = file_data['X'].values
y_data = file_data['Y'].values
tid = file_data['Tid'].values

# 生成用于存放数据中被映射到的点的hash值
x_y = zip(x_data,y_data)
for x, y in x_y:
    hash_bucket.setdefault(get_hash_index(x,y),0)
print len(hash_bucket)

# 数据处理填充坐标（经纬度）集合和坐标（utm）集合
temp = 1
temp_road = []
temp_json = []
for index, point in zip(tid, x_y):
    if index == temp:
        temp_road.append(point)
        tp = utm.to_latlon(point[0], point[1], 51, 'R')
        tp = wgs84togcj02(tp[1],tp[0])
        temp_json.append([tp[1],tp[0]])
    else:
        road_data.setdefault(temp,temp_road)
        json_data.setdefault(temp,temp_json)
        temp_road=[]
        temp_json=[]
        temp+=1
road_data.setdefault(temp,temp_road)
json_data.setdefault(temp, temp_json)


# 生成lsh查询实例
def init_lsh(hash_size, hash_bucket, road_data):
    lsh = lshash.LSHash(hash_size, len(hash_bucket))

    # 将每条路径转化为对应向量，并用于初始化lsh实例
    for r in road_data:
        for p in road_data[r]:
            hash_bucket[get_hash_index(p[0], p[1])] = 1
        lsh.index(hash_bucket.values(), extra_data=r)
        vector_data.setdefault(r, hash_bucket.values())
        for d in hash_bucket:
            hash_bucket[d] = 0
    return lsh, vector_data


# 保存数据到文件
with open('mapdata.json', 'w') as f:
    json.dump(json_data, f)

with open('roaddata.json', 'w') as f:
    json.dump(road_data, f)


# 查询并保存lsh数据
with open('lsh_result.txt', 'w') as f:
    for j in hash_size:
        lsh, vector_data = init_lsh(j, hash_bucket, road_data)
        for i in search_index:
            ans = lsh.query(vector_data[i])
            for a in ans:
                f.write(str(a[0][1])+":\n"+str(road_data[a[0][1]])+"\ndis:"+str(a[1])+"\n")
f.closed()

# 查询并保存knn数据
npX = []
for r in road_data:
    for p in road_data[r]:
        hash_bucket[get_hash_index(p[0], p[1])] = 1
    npX.append(hash_bucket.values())
    for d in hash_bucket:
        hash_bucket[d] = 0
npX = np.array(npX)
nbrs = NearestNeighbors(n_neighbors=5, algorithm='auto').fit(npX)
knn_dis, knn_res = nbrs.kneighbors(npX)

with open('knn_result.txt', 'w') as f:
    for j in knn_res:
        f.write(str(j))
        f.write("\n")

