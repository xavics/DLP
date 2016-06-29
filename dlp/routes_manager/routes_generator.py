import math
import geopy
from geopy.distance import VincentyDistance

vertical_speed = 50  # Drone Speed (m/s)
horizontal_speed = 50  # Drone Speed (m/s)
flying_altitude = 400  # Minimum altitude


class Point(object):
    def __init__(self, lat, lng, alt):
        self.lat = lat
        self.lng = lng
        self.alt = alt

    def __str__(self):
        return '{lat} ; {lng} ; {alt}'.format(**self.__dict__)


def calculate_initial_compass_bearing(geo_point_origin, geo_point_destiny):
    if (type(geo_point_origin) != tuple) or (type(geo_point_destiny) != tuple):
        raise TypeError("Only tuples are supported as arguments")

    lat1 = math.radians(geo_point_origin[0])
    lat2 = math.radians(geo_point_destiny[0])

    diff_long = math.radians(geo_point_destiny[1] - geo_point_origin[1])

    x = math.sin(diff_long) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1) * math.cos(lat2) *
                                           math.cos(diff_long))

    initial_bearing = math.atan2(x, y)

    initial_bearing = math.degrees(initial_bearing)
    compass_bearing = (initial_bearing + 360) % 360

    return compass_bearing


def get_drone_steps(origin, destiny):
    geo_point_origin = (origin.lat, origin.lng)
    geo_point_destiny = (destiny.lat, destiny.lng)
    dist = geopy.distance.distance(geo_point_origin, geo_point_destiny) \
        .meters
    total_steps = int(dist // horizontal_speed)
    extra_step = (dist % horizontal_speed) * horizontal_speed
    bearing = \
        calculate_initial_compass_bearing(geo_point_origin, geo_point_destiny)
    actual_point = Point(origin.lat, origin.lng, origin.alt)
    steps = []
    while actual_point.alt != flying_altitude:
        steps.append(
            Point(actual_point.lat, actual_point.lng, actual_point.alt))
        actual_point.alt += vertical_speed
        if actual_point.alt >= flying_altitude:
            actual_point.alt = flying_altitude
            steps.append(
                Point(actual_point.lat, actual_point.lng, actual_point.alt))
    for i in range(total_steps):
        destination = VincentyDistance(meters=horizontal_speed) \
            .destination(geopy.Point(actual_point.lat, actual_point.lng),
                         bearing)
        actual_point.lat = destination.latitude
        actual_point.lng = destination.longitude
        steps.append(
            Point(actual_point.lat, actual_point.lng, actual_point.alt))
    if extra_step:
        destination = VincentyDistance(meters=extra_step) \
            .destination(geopy.Point(actual_point.lat, actual_point.lng),
                         bearing)
        actual_point.lat, actual_point.lng = destination.latitude, destination.longitude
        steps.append(
            Point(actual_point.lat, actual_point.lng, actual_point.alt))
    while actual_point.alt != destiny.alt:
        actual_point.alt -= vertical_speed
        if actual_point.alt <= destiny.alt:
            actual_point.alt = destiny.alt
            steps.append(
                Point(actual_point.lat, actual_point.lng, actual_point.alt))
        else:
            steps.append(
                Point(actual_point.lat, actual_point.lng, actual_point.alt))
    return steps


origin = Point(41.6183169, 0.6218659, 270)
destiny = Point(41.615437, 0.6223383, 180)
