from __future__ import absolute_import

import datetime
import os
import requests
import json
import simpy
from celery.utils.log import get_task_logger

from DLP.celery import app
from DLP.settings import BASE_DIR
from dlp.apps import get_site_url
from dlp.galaxy_comunication.galaxy_comunication import send_kmls
from dlp.kml_manager.kml_generator import create_kml, create_transports_list, \
    create_packages_list
from dlp.models import Package, LogisticCenter, DropPoint, Drone, Transport
from dlp.routes_manager.routes_generator import get_drone_steps, Point

logger = get_task_logger(__name__)
kml_tmp_folder = os.path.join(BASE_DIR + "/dlp/static/kmls/tmp/")
send_position_url = get_site_url() + "receive_position"


class DroneTransport(object):
    def __init__(self, env, positions, id_transport):
        self.id_transport = id_transport
        self.env = env
        self.positions = positions
        # Start the run process everytime an instance is created.
        self.action = self.env.process(self.run())

    def run(self):
        logger.info(send_position_url)
        for position in self.positions:
            yield self.env.process(self.send_data(1.0, position))
        self.positions.reverse()
        yield self.env.timeout(1.0)
        for position in self.positions:
            yield self.env.process(self.send_data(1.0, position))

    def send_data(self, duration, position):
        print('sending data...')
        requests.post(send_position_url,
                      data={'id_transport': self.id_transport,
                            'lat': position['lat'], 'lng': position['lng'],
                            'alt': position['alt']})
        yield self.env.timeout(duration)


@app.task(name="tasks.manage_all_packets")
def manage_all_packets():
    logger.info("Searching for packages pending to send")
    create_transports_list()
    create_packages_list()
    send_kmls()
    packages = Package.objects.filter(status=2)
    for package in packages:
        drones_availability(package)


def drones_availability(package):
    droppoint = package.dropPoint
    lc = LogisticCenter.objects.get(id=droppoint.logistic_center_id)
    drones = Drone.objects.filter(
        logistic_center_id=droppoint.logistic_center_id, is_transporting=0)
    for drone in drones:
        package.status = 1
        package.save()
        # create_packet_kml(package)
        drone.is_transporting = 1
        drone.save()
        origin = Point(lc.lat, lc.lng, lc.alt)
        destiny = Point(droppoint.lat, droppoint.lng, droppoint.alt)
        positions = get_drone_steps(origin, destiny)
        json_pos = json.dumps([ob.__dict__ for ob in positions])
        transport = create_transport(package, drone, lc, len(positions) * 2)
        send_package.delay(drone.id, package.id, transport.id, json_pos)
        break


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
    package.status = 0
    package.date_delivered = datetime.datetime.now()
    package.save()
    transport = Transport.objects.get(id=transport_id)
    transport.is_active = 0
    transport.save()
    drone = Drone.objects.get(id=drone_id)
    drone.is_transporting = 0
    drone.save()
    delete_kml(transport_id, package_id)


def delete_kml(transport_id, package_id):
    os.remove(kml_tmp_folder + "Transport{}.kml".format(transport_id))
