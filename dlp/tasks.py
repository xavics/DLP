from __future__ import absolute_import
import os
from DLP.celery import app
from dlp.models import Package, LogisticCenter, DropPoint, Drone, Transport
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@app.task
def add(x, y):
    return x + y


@app.task(name="tasks.manage_all_packets")
def manage_all_packets():
    logger.info("Entered to function")
    packages = Package.objects.filter(status=2)
    for package in packages:
        drones_availability(package)

def drones_availability(package):
    droppoint = DropPoint.objects.get(id=package.id)
    lc = LogisticCenter.objects.get(id=droppoint.logistic_center_id)
    for drone_id in lc.drones:
        drone = Drone.objects.get(id=drone_id)
        if drone.is_transporting == 0:
            logger.info("Packet " + package.id + " will be sent by drone " +
                        drone.id)
            package.status = 1
            drone.is_transporting = 1
            transport = Transport(package=package.id, drone=drone.id)
            package.save()
            drone.save()
            transport.save()
            # return "create_kml(transport)"


# def create_kml(transport):



# def get_position_by_time():