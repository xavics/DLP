from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from DLP.settings import MAPS_API_KEY
from dlp.apps import get_site_url
from rest_framework import viewsets
from dlp.kml_manager.kml_generator import create_updates, TMP, \
    LOGISTICCENTER, DROPPOINT
from dlp.serializers import *
from models import *
from filters import *
from dlp.kml_manager import kml_generator
import tasks


def base(request):
    maps_api_key = MAPS_API_KEY
    return render(request, 'base.html', {'maps_api_key': maps_api_key})


@csrf_exempt
def receive_position(request):
    id_trans = request.POST.get('id_transport')
    lat = request.POST.get('lat')
    lng = request.POST.get('lng')
    alt = request.POST.get('alt')
    variables = {
        'id': "Transport" + id_trans,
        'icon': get_site_url() + "static/images/galaxy_icons/drone_icon.png",
        'name': "Transport " + id_trans,
        'description': "Drone transporting packet.",
        'lat': lat,
        'lng': lng,
        'alt': alt}
    kml_name = "Transport" + id_trans + ".kml"
    kml_generator.create_kml("drone_placemark.kml", kml_name, variables, TMP)
    transport = Transport.objects.get(id=id_trans)
    transport.step += 1
    transport.save()
    return HttpResponse(status=204)


@csrf_exempt
def update_droppoints(request):
    create_updates(DROPPOINT)
    return HttpResponse(status=204)


@csrf_exempt
def update_logistic_centers(request):
    create_updates(LOGISTICCENTER)
    return HttpResponse(status=204)


'''
API REST ViewSets
'''


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
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = TransportFilter


class StyleURLViewSet(viewsets.ModelViewSet):
    model = StyleURL
    queryset = StyleURL.objects.all()
    serializer_class = StyleURLSerializer
    filter_backends = (filters.DjangoFilterBackend,)

    # def refresh_weather(request):
    #     path_to_kml = generate_weather_image(os.path.dirname(__file__))
    #     try:
    #         return FileResponse(open(path_to_kml, 'rb'))
    #     except IOError:
    #         return HttpResponse(status=201)
