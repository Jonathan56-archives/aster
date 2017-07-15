import datetime as dt


class Logger(object):
    def __init__(self, simulation):
        self.sim = simulation

    def log(self, this, message,
            key='', value=0, level='INFO', location=None):
        self.sim.log.append({
            'level': level,
            'datetime': dt.timedelta(seconds=self.sim.env.now) + self.sim.start,
            'source': this,
            'location': location,
            'message': message,
            'key': key,
            'value': value})


class Monitoring(object):
    def __init__(self, simulation):
        self.sim = simulation
        self.rate = 30 * 24 * 60 * 60

        # Add monitoring process
        self.sim.env.process(self.start())

    def start(self):
        while True:
            # Log status
            self.sim.earth.log()

            # Wait until next monitoring point
            yield self.sim.env.timeout(self.rate)

    def __str__(self):
        return "Monitor"
