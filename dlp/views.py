from django.shortcuts import render
from DLP.settings import MAPS_API_KEY
from rest_framework import viewsets, generics
from djng.views.crud import NgCRUDView
from dlp.serializers import *
from models import *
from filters import *


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
    maps_api_key = MAPS_API_KEY
    return render(request, 'base.html', {'maps_api_key' : maps_api_key})


class CityViewSet(viewsets.ModelViewSet):
    model = City
    queryset = City.objects.all()
    serializer_class = CitySerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = CityFilter


class LogisticCenterViewSet(viewsets.ModelViewSet):
    model = LogisticCenter
    queryset = LogisticCenter.objects.all()
    serializer_class = LogisticCenterSerializer


class DropPointViewSet(viewsets.ModelViewSet):
    model = DropPoint
    queryset = DropPoint.objects.all()
    serializer_class = DropPointSerializer


class DroneViewSet(viewsets.ModelViewSet):
    model = Drone
    queryset = Drone.objects.all()
    serializer_class = DroneSerializer


class PackageViewSet(viewsets.ModelViewSet):
    model = Package
    queryset = Package.objects.all()
    serializer_class = PackageSerializer


class TransportViewSet(viewsets.ModelViewSet):
    model = Transport
    queryset = Transport.objects.all()
    serializer_class = TransportSerializer


class StyleURLViewSet(viewsets.ModelViewSet):
    model = StyleURL
    queryset = StyleURL.objects.all()
    serializer_class = StyleURLSerializer
    filter_backends = (filters.DjangoFilterBackend,)