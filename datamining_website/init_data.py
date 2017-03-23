import json
import django
import os
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "datamining_website.settings")
django.setup()

from hw_1.models import utm_data,map_date, matrix_date

# data = map_date.objects.filter(line_id=1)
# data = list(data)
# data = map_date.objects.all()
# data = list(data)
# print "test"
# for li in data:
#     print  data

map_date.objects.all().delete()
# utm_data.objects.all().delete()

print map_date.objects.all()

with open('mapdata.json', 'r') as f:
    data = json.load(f)
#
#
for index in data:
    print index
    for point in data[index]:
        d = map_date(line_id=index, latitude=point[0], longitude=point[1])
        d.save()

# with open('roaddata.json', 'r') as f:
#     data = json.load(f)
#
# for index in data:
#     print index
#     for point in data[index]:
#         d = utm_data(line_id=index, latitude=point[0], longitude=point[1])
#         d.save()
