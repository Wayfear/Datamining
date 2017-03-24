from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^get_road$', views.get_road, name='get_road'),
    url(r'^get_road_by_knn/([0-9]{1,4})/([0-9]{1,2})$', views.get_road_by_knn, name='get_road_by_knn'),

]