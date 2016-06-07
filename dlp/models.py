from __future__ import unicode_literals

from django.db import models

ACTIVE = 1
DISABLED = 0
STATUS = (
    (ACTIVE, 'Active'),
    (DISABLED, 'Disabled'))


class City(models.Model):
    name = models.CharField(max_length=100)
    lat = models.FloatField(default='0')
    lng = models.FloatField(default='0')

    def __unicode__(self):
        return str(self.name)


class StyleURL(models.Model):
    name = models.CharField(max_length=50)
    href = models.URLField()
    scale = models.FloatField()

    def __unicode__(self):
        return str(self.name)


class LogisticCenter(models.Model):
    name = models.CharField(max_length=50, null=True)
    address = models.CharField(max_length=50)
    description = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    altitude = models.FloatField()
    radius = models.FloatField()
    # is_available = models.BooleanField(default=True)
    style_url = models.ForeignKey(StyleURL)
    # drop_points = models.ManyToManyField(DropPoint)
    city = models.ForeignKey(City, related_name='logisticcenter')

    def __unicode__(self):
        return str(self.name)


class DropPoint(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    altitude = models.FloatField()
    is_available = models.IntegerField(default=0, choices=STATUS)
    style_url = models.ForeignKey(StyleURL)
    logistic_center = models.ForeignKey(LogisticCenter,
                                        related_name='dropoint')

    def __unicode__(self):
        return str(self.name)


class Drone(models.Model):
    model = models.CharField(max_length=50)
    plate = models.CharField(max_length=50)
    # altitude = models.FloatField(default=50)
    is_transporting = models.IntegerField(default=0, choices=STATUS)
    battery_life = models.PositiveSmallIntegerField(default=100)
    logistic_center = models.ForeignKey(LogisticCenter, related_name='drone')
    style_url = models.ForeignKey(StyleURL)

    def __unicode__(self):
        return str(self.name + '-' + self.plate)


class Package(models.Model):
    name = models.CharField(max_length=50)
    dropPoint = models.ForeignKey(DropPoint, related_name='package')
    logistic_center = models.ForeignKey(LogisticCenter, related_name='package')


class Transport(models.Model):
    is_active = models.IntegerField(default=0, choices=STATUS)
    package = models.ForeignKey(Package, related_name='transport')
    drone = models.ForeignKey(Drone, null=True, related_name='transport')
