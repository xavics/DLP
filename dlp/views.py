from django.shortcuts import render
from rest_framework import viewsets
from djng.views.crud import NgCRUDView
import models


def index(request, city=None):
    if city:
        LogisticCenters = models.LogisticCenter.objects.filter(city=city)
    else:
        return welcome(request)
    return render(request, 'static/templates/index.html', {'cities': city})


def welcome(request):
    cities_available = models.City.objects.all()
    return render(request, 'static/templates/welcome.html',
                  {'cities_available': cities_available})


def base(request):
    return render(request, 'base.html')


class LogisticCenter(NgCRUDView):
    model = models.LogisticCenter
    slug_field = 'city'


class Drone(NgCRUDView):
    model = models.Drone


class Droppoint(NgCRUDView):
    model = models.DropPoint


class Package(NgCRUDView):
    model = models.Package


class City(NgCRUDView):
    model = models.City


class Transport(NgCRUDView):
    model = models.Transport
# class DroneViewSet(viewsets.ModelViewSet):
#     queryset = models.Drone.objects.all()
#     context_object_name = 'drone'
