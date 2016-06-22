class Drone(object):
    def __init__(self, env, positions):
        self.env = env
        self.positions = positions
        # Start the run process everytime an instance is created.
        self.action = env.process(self.run())

    def run(self):
        for position in self.positions:
            print('Position %d at %d' % position.alt, self.env.now)
            # We yield the process that process() returns
            # to wait for it to finish
            yield self.env.process(self.write_kml(1))

    def write_kml(self, position):
        print('writing...')


import simpy
env = simpy.rt.RealtimeEnvironment(initial_time=0, factor=1.0, strict=False)
positions = [{alt: 15, lat: 10, lng: 5}, {alt: 12, lat: 10, lng: 5}, {alt: 9, lat: 10, lng: 5}]
drone = Drone(env, positions)
drone2 = Drone(env, positions)
drone3 = Drone(env, positions)
drone4 = Drone(env, positions)
drone5 = Drone(env, positions)
drone6 = Drone(env, positions)
drone7 = Drone(env, positions)
drone8 = Drone(env, positions)
drone9 = Drone(env, positions)
drone10 = Drone(env, positions)
drone11 = Drone(env, positions)
drone12 = Drone(env, positions)
drone13 = Drone(env, positions)
drone14 = Drone(env, positions)
drone15 = Drone(env, positions)
drone16 = Drone(env, positions)
drone17 = Drone(env, positions)
drone18 = Drone(env, positions)
drone19 = Drone(env, positions)
drone20 = Drone(env, positions)
