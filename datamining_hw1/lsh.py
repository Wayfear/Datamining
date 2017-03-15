import copy
import sys
import utm
import lshash

file_name = "Traj_1000_SH_UTM"
first_line = True

road_num = 1

roads = {}
road = []

max_length = 0
min_length = sys.maxint
max_width = 0
min_width = sys.maxint


def find_range(length, width):
    return


with open(file_name) as file:
    for line in file:
        if first_line:
            first_line = False
            continue
        par = line.split(",")

        if par[0] == str(road_num):
            road.append([float(par[2]), float(par[3])])
        else:
            roads.setdefault(road_num, road)
            road = []
            road_num = int(par[0])
            print(road_num)

roads.setdefault(road_num, road)

print("maxL = " + str(max_length) + "," + "minL = " + str(min_length) + "," +
      "maxW = " + str(max_width) + "," + "minW = " + str(min_width))


hashBarrel = {}


def get_hash_index(list_par):

    return int(list_par[0]/20)*10000000+int(list_par[1]/20)


for r in roads:
    for li in roads[r]:
        hashBarrel.setdefault(get_hash_index(li), 0)
    print(str(len(roads[r])))

print ("Barrel number = " + str(len(hashBarrel)))

lsh = lshash.LSHash(8, len(hashBarrel))

for r in roads:
    for li in roads[r]:
        try:

            hashBarrel[get_hash_index(li)] = 1
        except:
            print("non-existent key")


    lsh.index(hashBarrel.values())
    for da in hashBarrel:
        hashBarrel[da] = 0

print ("finish")
ans = lsh.query(hashBarrel.values())

print ans[0]

print ans[1]

print ans[2]
















