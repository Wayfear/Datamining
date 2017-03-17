from django.shortcuts import render
from models import map_date, utm_data
from django.template import loader
import json
# Create your views here.

# def get_road_data(data):
import decimal, simplejson
class DecimalJSONEncoder(simplejson.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)
        return super(DecimalJSONEncoder, self).default(o)


def index(request):
    data = map_date.objects.filter(line_id=1)
    data = list(data)
    road = []
    for point in data:
        road.append([point.latitude, point.longitude])
    temp = json.dumps(road,cls=DecimalJSONEncoder)
    print temp
    # template = loader.get_template('hw_1/index.html')
    return render(request,"hw_1/index.html", {"road": temp})