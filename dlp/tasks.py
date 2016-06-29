from __future__ import absolute_import

import datetime
import os
import requests

import simpy
from celery.utils.log import get_task_logger

from DLP.celery import app
from DLP.settings import BASE_DIR, SITE_URL
from dlp.kml_manager.kml_generator import create_kml, create_list_test
from dlp.models import Package, LogisticCenter, DropPoint, Drone, Transport
from dlp.routes_manager.routes_generator import get_drone_steps, Point

logger = get_task_logger(__name__)
kml_folder = os.path.join(BASE_DIR + "/dlp/static/kmls/")
send_position_url = SITE_URL + "receive_position"


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
            print('{0}; time= {1}'.format(
                self.env.now, datetime.datetime.now().time()))
            print('sending data...')
            requests.post(send_position_url,
                          data={'id_transport': self.id_transport,
                                'lat': position.lat, 'lng': position.lng,
                                'alt': position.alt})
            yield self.env.timeout(1.0)
        self.positions.reverse()
        yield self.env.timeout(1.0)
        for position in self.positions:
            print('{0}; time= {1}'.format(
                self.env.now, datetime.datetime.now().time()))
            print('sending data...')
            requests.post(send_position_url,
                          data={'id_transport': self.id_transport,
                                'lat': position.lat, 'lng': position.lng,
                                'alt': position.alt})
            yield self.env.timeout(1.0)


@app.task(name="tasks.manage_all_packets")
def manage_all_packets():
    logger.info("Searching for packages pending to send")
    # droppoint = DropPoint.objects.get(id=1)
    # pack = Package(name="pack", dropPoint=droppoint, status=2)
    # pack.save()
    create_list_test("Transport")
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
        create_packet_kml(package)
        drone.is_transporting = 1
        drone.save()
        transport = Transport(package=package, drone=drone)
        transport.save()
        send_package.delay(drone.id, package.id, lc.id, droppoint.id,
                           transport.id)
        break


@app.task()
def send_package(drone_id, package_id, lc_id, droppoint_id, transport_id):
    logger.info("Packet " + str(package_id) + " will be sent by drone " +
                str(drone_id))
    lc = LogisticCenter.objects.get(id=lc_id)
    droppoint = DropPoint.objects.get(id=droppoint_id)
    origin = Point(lc.lat, lc.lng, lc.alt)
    destiny = Point(droppoint.lat, droppoint.lng, droppoint.alt)
    positions = get_drone_steps(origin, destiny)
    env_go = simpy.rt.RealtimeEnvironment(initial_time=0, factor=1.5,
                                          strict=False)
    env_return = simpy.rt.RealtimeEnvironment(initial_time=0, factor=1.5,
                                              strict=False)
    dronetransport_g = DroneTransport(env_go, positions, transport_id)
    env_go.run(until=dronetransport_g.action)
    # positions.reverse()
    # dronetransport_r = DroneTransport(env_return, positions, transport_id)
    # env_return.run(until=dronetransport_r.action)
    final_transport(drone_id, package_id, transport_id)


def final_transport(drone_id, package_id, transport_id):
    package = Package.objects.get(id=package_id)
    package.status = 0
    package.save()
    transport = Transport.objects.get(id=transport_id)
    transport.is_active = 0
    transport.save()
    drone = Drone.objects.get(id=drone_id)
    drone.is_transporting = 0
    drone.save()
    delete_kml(transport_id, package_id)


def delete_kml(transport_id, package_id):
    os.remove(kml_folder + "Transport{}.kml".format(transport_id))
    # os.remove(kml_folder + "package_{}.kml".format(package_id))


def create_packet_kml(package):
    dp = package.dropPoint
    variables = {'icon': SITE_URL + "static/images/galaxy_icons/droppoints/1.png",
                 'name': "Package " + str(package.id),
                 'description': "Droppoint of package.",
                 'lat': dp.lat,
                 'lng': dp.lng,
                 'alt': dp.alt}
    kml_name = "package_" + str(package.id) + ".kml"
    create_kml("drone_placemark.kml", kml_name, variables)
