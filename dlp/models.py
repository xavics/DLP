from __future__ import unicode_literals

from django.db import models

from dlp import mixins


class City(mixins.GeoSimple, models.Model):
    name = models.CharField(max_length=100)
    place_id = models.CharField(max_length=100)
    flying_altitude = models.IntegerField(default=400)

    def __unicode__(self):
        return str(self.name)


class StyleURL(models.Model):
    name = models.CharField(max_length=50)
    maps_url = models.CharField(max_length=50)
    earth_url = models.CharField(max_length=50)
    scale = models.FloatField()

    def __unicode__(self):
        return str(self.name)


class DefinedStyle(models.Model):
    name = models.CharField(max_length=50)
    lc = models.ForeignKey(StyleURL, related_name="lc_style")
    dp = models.ForeignKey(StyleURL, related_name="dp_style")


class LogisticCenter(mixins.GeoComplex, models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    description = models.TextField()
    radius = models.FloatField()
    defined_style = models.ForeignKey(DefinedStyle,
                                      related_name='logistic_center')
    city = models.ForeignKey(City, related_name='logistic_centers')

    def __unicode__(self):
        return str(self.name)


class DropPoint(mixins.GeoComplex, models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    logistic_center = models.ForeignKey(LogisticCenter,
                                        related_name='droppoints')

    def __unicode__(self):
        return str(self.name)


class Drone(models.Model):
    class DroneStatus(object):
        DELIVERING = 1
        WAITING = 0
        CHOICES = (
            (DELIVERING, 'Delivering'),
            (WAITING, 'Waiting'),
        )

    model = models.CharField(max_length=50)
    plate = models.CharField(max_length=50)
    status = models.IntegerField(
        default=DroneStatus.WAITING, choices=DroneStatus.CHOICES)
    battery_life = models.PositiveSmallIntegerField(default=100)
    logistic_center = models.ForeignKey(LogisticCenter, related_name='drones')
    style_url = models.ForeignKey(StyleURL)

    def __unicode__(self):
        return str(self.plate)


class Package(models.Model):
    class PackageStatus(object):
        PENDING = 2
        SENDING = 1
        SENT = 0
        CHOICES = (
            (PENDING, 'Pending'),
            (SENDING, 'Sending'),
            (SENT, 'Sent'),
        )

    name = models.CharField(max_length=50)
    drop_point = models.ForeignKey(DropPoint, related_name='packages')
    status = models.IntegerField(
        default=PackageStatus.PENDING, choices=PackageStatus.CHOICES)
    style_url = models.ForeignKey(StyleURL)
    date_delivered = models.DateTimeField(null=True, blank=True)


class Transport(models.Model):
    class TransportStatus(object):
        ACTIVE = 1
        FINISHED = 0
        CHOICES = (
            (ACTIVE, 'Active'),
            (FINISHED, 'Finished'),
        )

    status = models.IntegerField(
        default=TransportStatus.ACTIVE, choices=TransportStatus.CHOICES)
    package = models.ForeignKey(Package, related_name='transport')
    logistic_center = models.ForeignKey(LogisticCenter,
                                        related_name='transports')
    drone = models.ForeignKey(Drone, null=True, related_name='transports')
    step = models.IntegerField(default=0)
    max_steps = models.IntegerField()


class Layouts(models.Model):
    name = models.CharField(max_length=50)
    url = models.CharField(max_length=50)
    size_x = models.FloatField()
    size_y = models.FloatField()
    screen_x = models.FloatField()
    screen_y = models.FloatField()
    overlay_x = models.FloatField()
    overlay_y = models.FloatField()
