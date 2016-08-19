from __future__ import absolute_import

import datetime
import json
import os
import requests

import simpy
from celery.utils.log import get_task_logger

from DLP.celery import app
from DLP.settings import BASE_DIR
from dlp.apis.api_weather import can_fly, ALLOW
from dlp.file_manager.file_manager import get_site_url, \
    get_temperature_availability, has_temperature_availability, \
    get_temperature_restriction
from dlp.galaxy_comunication.galaxy_comunication import send_kmls
from dlp.kml_manager.kml_generator import create_transports_list, \
    create_packages_list, create_delivers
from dlp.models import Package, LogisticCenter, Drone, Transport, StyleURL
from dlp.routes_manager.routes_generator import get_drone_steps, Point

logger = get_task_logger(__name__)
KML_TMP_FOLDER = os.path.join(BASE_DIR + "/dlp/static/kmls/tmp/")
POSITION_URL = get_site_url() + "receive_position"

# Package Stiles id
PENDING_STYLE = 1
SENDING_STYLE = 2
SENT_STYLE = 3


class DroneTransport(object):
    def __init__(self, env, positions, id_transport):
        self.id_transport = id_transport
        self.env = env
        self.positions = positions
        # Start the run process everytime an instance is created.
        self.action = self.env.process(self.run())

    def run(self):
        logger.info(POSITION_URL)
        for position in self.positions:
            yield self.env.process(self.send_data(1.0, position))
        self.positions.reverse()
        yield self.env.timeout(1.0)
        for position in self.positions:
            yield self.env.process(self.send_data(1.0, position))

    def send_data(self, duration, position):
        print('sending data...')
        requests.post(POSITION_URL,
                      data={'id_transport': self.id_transport,
                            'lat': position['lat'], 'lng': position['lng'],
                            'alt': position['alt']})
        yield self.env.timeout(duration)


@app.task(name="tasks.manage_all_packets")
def manage_all_packets():
    logger.info("Searching for packages pending to send")
    create_transports_list()
    create_packages_list()
    create_delivers()
    send_kmls()
    packages = Package.objects.filter(status=Package.PackageStatus.PENDING)
    for package in packages:
        drones_availability(package)


def drones_availability(package):
    droppoint = package.drop_point
    city = droppoint.logistic_center.city
    if not has_temperature_availability(city.name):
        can_fly(city.name, city.lat, city.lng)
    if get_temperature_availability(
            city.name) == ALLOW or get_temperature_restriction() == False:
        lc = LogisticCenter.objects.get(id=droppoint.logistic_center_id)
        drones = Drone.objects.filter(
            logistic_center_id=droppoint.logistic_center_id,
            status=Drone.DroneStatus.WAITING)
        for drone in drones:
            package.status = Package.PackageStatus.SENDING
            package.style_url = StyleURL.objects.get(id=SENDING_STYLE)
            package.save()
            drone.status = Drone.DroneStatus.DELIVERING
            drone.save()
            city = droppoint.logistic_center.city
            origin = Point(lc.lat, lc.lng, lc.alt)
            destiny = Point(droppoint.lat, droppoint.lng, droppoint.alt)
            positions = get_drone_steps(origin, destiny, city)
            json_pos = json.dumps([ob.__dict__ for ob in positions])
            transport = create_transport(package, drone, lc,
                                         len(positions) * 2)
            send_package.delay(drone.id, package.id, transport.id, json_pos)
            break
    else:
        logger.info("Weather inestable in {city}".format(city=city.name))


def create_transport(package, drone, lc, max_steps):
    transport = Transport(package=package, drone=drone, logistic_center=lc,
                          max_steps=max_steps)
    transport.save()
    return transport


@app.task()
def send_package(drone_id, package_id, transport_id, json_pos):
    logger.info("Packet " + str(package_id) + " will be sent by drone " +
                str(drone_id))
    env_go = simpy.rt.RealtimeEnvironment(initial_time=0, factor=1.5,
                                          strict=False)
    positions = json.loads(json_pos)
    dronetransport_g = DroneTransport(env_go, positions, transport_id)
    env_go.run(until=dronetransport_g.action)
    final_transport(drone_id, package_id, transport_id)


def final_transport(drone_id, package_id, transport_id):
    package = Package.objects.get(id=package_id)
    package.status = Package.PackageStatus.SENT
    package.style_url = StyleURL.objects.get(id=SENT_STYLE)
    package.date_delivered = datetime.datetime.now()
    package.save()
    transport = Transport.objects.get(id=transport_id)
    transport.status = Transport.TransportStatus.FINISHED
    transport.save()
    drone = Drone.objects.get(id=drone_id)
    drone.status = Drone.DroneStatus.WAITING
    drone.save()
    delete_kml(transport_id)


def delete_kml(transport_id):
    os.remove(KML_TMP_FOLDER + "Transport{}.kml".format(transport_id))
