from django.db import models


class GeoSimple(models.Model):
    lat = models.FloatField()
    lng = models.FloatField()

    class Meta:
        abstract = True


class GeoComplex(models.Model):
    lat = models.FloatField()
    lng = models.FloatField()
    alt = models.FloatField()

    class Meta:
        abstract = True
