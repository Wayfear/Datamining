from __future__ import unicode_literals

from django.db import models

# Create your models here.


class utm_data(models.Model):
    line_id = models.IntegerField()
    latitude = models.DecimalField(max_digits = 22, decimal_places = 15)
    longitude = models.DecimalField(max_digits = 22, decimal_places = 15)


class map_date(models.Model):
    line_id = models.IntegerField()
    latitude = models.DecimalField(max_digits = 22, decimal_places = 15)
    longitude = models.DecimalField(max_digits = 22, decimal_places = 15)


class matrix_date(models.Model):
    line_id = models.IntegerField()
    latitude = models.IntegerField()
    longitude = models.IntegerField()