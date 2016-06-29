import datetime, requests
import simpy


class Drone(object):
    def __init__(self, env, positions, id_transport):
        self.id_transport = id_transport
        self.env = env
        self.positions = positions
        # Start the run process everytime an instance is created.
        self.action = self.env.process(self.run())

    def run(self):
        for position in self.positions:
            alt = position['alt']
            print('Position {0} at {1}; time= {2}'.format(alt, self.env.now, datetime.datetime.now().time()))
            yield self.env.process(self.write_kml(1.0, position))

    def write_kml(self, duration, position):
        print('sending data...')
        requests.post('http://127.0.0.1:8000/receive_position',
                      data={'id_transport': self.id_transport,
                            'lat': position['lat'], 'lng': position['lng'],
                            'alt': position['alt']})
        yield self.env.timeout(duration)


env = simpy.rt.RealtimeEnvironment(initial_time=0, factor=1.5, strict=False)
env2 = simpy.rt.RealtimeEnvironment(initial_time=0, factor=1.5, strict=False)
positions = [{'alt': 30, 'lat': 10, 'lng': 5},
             {'alt': 29, 'lat': 10, 'lng': 5},
             {'alt': 28, 'lat': 10, 'lng': 5},
             {'alt': 27, 'lat': 10, 'lng': 5},
             {'alt': 26, 'lat': 10, 'lng': 5},
             {'alt': 25, 'lat': 10, 'lng': 5},
             {'alt': 24, 'lat': 10, 'lng': 5},
             {'alt': 23, 'lat': 10, 'lng': 5},
             {'alt': 22, 'lat': 10, 'lng': 5},
             {'alt': 21, 'lat': 10, 'lng': 5},
             {'alt': 20, 'lat': 10, 'lng': 5},
             {'alt': 19, 'lat': 10, 'lng': 5},
             {'alt': 18, 'lat': 10, 'lng': 5},
             {'alt': 17, 'lat': 10, 'lng': 5},
             {'alt': 16, 'lat': 10, 'lng': 5},
             {'alt': 15, 'lat': 10, 'lng': 5},
             {'alt': 14, 'lat': 10, 'lng': 5},
             {'alt': 13, 'lat': 10, 'lng': 5},
             {'alt': 12, 'lat': 10, 'lng': 5},
             {'alt': 11, 'lat': 10, 'lng': 5},
             {'alt': 10, 'lat': 10, 'lng': 5},
             {'alt': 9, 'lat': 10, 'lng': 5},
             {'alt': 8, 'lat': 10, 'lng': 5},
             {'alt': 7, 'lat': 10, 'lng': 5},
             {'alt': 6, 'lat': 10, 'lng': 5},
             {'alt': 5, 'lat': 10, 'lng': 5},
             {'alt': 4, 'lat': 10, 'lng': 5},
             {'alt': 3, 'lat': 10, 'lng': 5},
             {'alt': 2, 'lat': 10, 'lng': 5},
             {'alt': 1, 'lat': 10, 'lng': 5},
             {'alt': 0, 'lat': 10, 'lng': 5}]
drone = Drone(env, positions, 25)
env.run(until=drone.action)
drone2 = Drone(env2, positions, 10)
proc2 = env2.process(drone2.action)
env2.run(until=proc2)
