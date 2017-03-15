import utm
import lshash
import pandas as pd
import json
import copy

file_name = "Traj_1000_SH_UTM"

hash_bucket = {}
road_data = {}
vector_data = {}
hash_size = 10
search_index = {15, 250, 480, 690, 900}
json_data ={}


def get_hash_index(x, y):
    x_range = (362800 - 346000) / 20
    hash_x = int((x - 34600) / 20)
    hash_y = int((y - 3448600) / 20) + 1
    return x_range*hash_x+hash_y

file_data = pd.read_csv(file_name)

x_data = file_data['X'].values
y_data = file_data['Y'].values
tid = file_data['Tid'].values

x_y = zip(x_data,y_data)

for x, y in x_y:
    hash_bucket.setdefault(get_hash_index(x,y),0)

print len(hash_bucket)

temp = 1
temp_road = []
temp_json = []
for index, point in zip(tid, x_y):
    if index == temp:
        temp_road.append(point)
        temp_json.append(utm.to_latlon(point[0], point[1], 51, 'R'))
    else:
        road_data.setdefault(temp,temp_road)
        json_data.setdefault(temp,temp_json)
        temp_road=[]
        temp_json=[]
        temp+=1

road_data.setdefault(temp,temp_road)
json_data.setdefault(temp, temp_json)






lsh = lshash.LSHash(hash_size, len(hash_bucket))

for r in road_data:
    for p in road_data[r]:
        hash_bucket[get_hash_index(p[0], p[1])] = 1
    lsh.index(hash_bucket.values(), extra_data=r)
    vector_data.setdefault(r, hash_bucket.values())
    for d in hash_bucket:
        hash_bucket[d] = 0;

with open('data.json', 'w') as f:
    json.dump(json_data, f)

for i in search_index:
    ans = lsh.query(vector_data[i])
    for a in ans:
        print a