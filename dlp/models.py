from __future__ import unicode_literals

from django.db import models

ACTIVE = 1
DISABLED = 0
STATUS = (
    (ACTIVE, 'Active'),
    (DISABLED, 'Disabled'))

PENDING = 2
SENDING = 1
SENT = 0
STATUS_PACKAGE = (
    (PENDING, 'Pending'),
    (SENDING, 'Sending'),
    (SENT, 'Sent')
)


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
    lat = models.FloatField()
    lng = models.FloatField()
    alt = models.FloatField()
    radius = models.FloatField()
    style_url = models.ForeignKey(StyleURL)
    city = models.ForeignKey(City, related_name='logistic_centers')

    def __unicode__(self):
        return str(self.name)


class DropPoint(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    lat = models.FloatField()
    lng = models.FloatField()
    alt = models.FloatField()
    is_available = models.IntegerField(default=0, choices=STATUS)
    style_url = models.ForeignKey(StyleURL)
    logistic_center = models.ForeignKey(LogisticCenter,
                                        related_name='droppoints')

    def __unicode__(self):
        return str(self.name)


class Drone(models.Model):
    model = models.CharField(max_length=50)
    plate = models.CharField(max_length=50)
    is_transporting = models.IntegerField(default=0, choices=STATUS)
    battery_life = models.PositiveSmallIntegerField(default=100)
    logistic_center = models.ForeignKey(LogisticCenter, related_name='drones')
    style_url = models.ForeignKey(StyleURL)

    def __unicode__(self):
        return str(self.plate)


class Package(models.Model):
    name = models.CharField(max_length=50)
    dropPoint = models.ForeignKey(DropPoint, related_name='packages')
    status = models.IntegerField(default=2, choices=STATUS_PACKAGE)


class Transport(models.Model):
    is_active = models.IntegerField(default=1, choices=STATUS)
    package = models.ForeignKey(Package, related_name='transport')
    drone = models.ForeignKey(Drone, null=True, related_name='transports')
