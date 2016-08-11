from os import listdir

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets

from DLP.settings import MAPS_API_KEY
from dlp.apis.api_weather import generate_weather_image
from dlp.file_manager.file_manager import get_site_url
from dlp.galaxy_comunication.galaxy_comunication import send_kmls, start_tour, \
    exit_tour, fly_to_view, send_empty_kmls
from dlp.kml_manager.kml_generator import create_updates, TMP, \
    LOGISTICCENTER, DROPPOINT, remove_update, create_weather_kml, WEATHER, \
    SLAVE, KMLS_SLAVE_PERS_PATH, SLAVE_UPDATES, create_rotation_kml, create_kml
from dlp.file_manager.file_manager import demo
from dlp.serializers import *
from filters import *
from models import *

'''
Base view
'''


def base(request):
    maps_api_key = MAPS_API_KEY
    return render(request, 'base.html', {'maps_api_key': maps_api_key})


'''
Drone requests to update its position.
'''


@csrf_exempt
def receive_position(request):
    id_trans = request.POST.get('id_transport')
    lat = request.POST.get('lat')
    lng = request.POST.get('lng')
    alt = request.POST.get('alt')
    variables = {
        'id': "Transport{id}".format(id=id_trans),
        'icon': "{url}static/images/galaxy_icons/drone.png".format(
            url=get_site_url()),
        'scale': 1.5,
        'name': "Transport {id}".format(id=id_trans),
        'description': "Drone transporting packet.",
        'lat': lat,
        'lng': lng,
        'alt': alt}
    kml_name = "Transport{id}.kml".format(id=id_trans)
    create_kml("drone_placemark.kml", kml_name, variables, TMP)
    transport = Transport.objects.get(id=id_trans)
    transport.step += 1
    transport.save()
    # server sent event
    return HttpResponse(status=204)


'''
Views to update the Drop Points and Logistic centers in the Liquid Galaxy
'''


@csrf_exempt
def update_droppoints(request):
    remove_update(DROPPOINT)
    send_kmls()
    create_updates(DROPPOINT)
    send_kmls()
    return HttpResponse(status=204)


@csrf_exempt
def update_logistic_centers(request):
    remove_update(LOGISTICCENTER)
    send_kmls()
    create_updates(LOGISTICCENTER)
    send_kmls()
    return HttpResponse(status=204)


'''
Get a Picture of the actual weather

City id get it from the request
'''


@csrf_exempt
def refresh_weather(request):
    city_id = request.GET.get("city")
    image_path = generate_weather_image(city_id)
    kml_name = "Weather.kml"
    if is_inside_folder(kml_name, KMLS_SLAVE_PERS_PATH):
        remove_update(WEATHER)
        create_weather_kml(image_path, kml_name, SLAVE_UPDATES)
    else:
        create_weather_kml(image_path, kml_name, SLAVE)
    return HttpResponse(status=204)


def is_inside_folder(filename, path):
    for f in listdir(path):
        print f, filename
        if f == filename:
            return True
    return False


'''
    Galaxy requests
'''


@never_cache
def make_tour(request):
    city_id = request.GET.get("city")
    create_rotation_kml(city_id)
    return HttpResponse(status=204)


@never_cache
def play_tour(request):
    city_id = request.GET.get("city")
    start_tour(city_id)
    return HttpResponse(status=204)


@never_cache
def stop_tour(request):
    city_id = request.GET.get("city")
    exit_tour(city_id)
    return HttpResponse(status=204)


@never_cache
def fly_to(request):
    city_id = request.GET.get("city")
    fly_to_view(city_id)
    return HttpResponse(status=204)


@never_cache
def refresh_kmls(request):
    city_id = request.GET.get("city")
    send_empty_kmls()
    create_rotation_kml(city_id)
    return HttpResponse(status=204)


'''
    Demo
'''


def run_demo(request):
    demo()
    return HttpResponse(status=204)


'''
API REST ViewSets
'''


class CityViewSet(viewsets.ModelViewSet):
    model = City
    queryset = City.objects.all()
    serializer_class = CitySerializer
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter)
    filter_class = CityFilter
    search_fields = ('^name',)


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
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = TransportFilter


class StyleURLViewSet(viewsets.ModelViewSet):
    model = StyleURL
    queryset = StyleURL.objects.all()
    serializer_class = StyleURLSerializer
    filter_backends = (filters.DjangoFilterBackend,)


class DefinedStyleViewSet(viewsets.ModelViewSet):
    model = DefinedStyle
    queryset = DefinedStyle.objects.all()
    serializer_class = DefinedStyleSerializer
    filter_backends = (filters.DjangoFilterBackend,)
