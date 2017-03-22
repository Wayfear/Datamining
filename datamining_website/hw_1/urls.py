from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^index$', views.index, name='index'),
    url(r'^get_road/([0-9]{1,4})/([0-9]{1,2})$', views.get_road, name='get_road'),
]