import re
import asyncio
import logging

import pantheon.hermes

LOGGER = logging.getLogger(__name__)


class MinMax:
    def __init__(self, min, max):
        self.min = min
        self.max = max


class FanControl:
    def __init__(self, rate=20):
        self.rate = rate
        self.temperature = MinMax(30.0, 70.0)
        self.speed = MinMax(10.0, 100.0)

    def speed_for_temperature(self, temperature):
        if temperature < self.temperature.min:
            return int(self.speed.min)
        elif temperature > self.temperature.max:
            return int(self.speed.max)

        # linear function: y = ax + b
        slope = (float(self.speed.max - self.speed.min) / float(self.temperature.max - self.temperature.min))
        return int((slope * (temperature - self.temperature.max)) + self.speed.max)

    async def update_fans_speed(self):
        LOGGER.info('Updating fans speed')
        setting = pantheon.hermes.nvidia.settings.settings('-q GPUCoreTemp')

        info = {}
        regex = re.compile(".*Attribute 'GPUCoreTemp'.*\[gpu:(?P<uid>\d+)\].*: (?P<temperature>\d+)\..*")
        for line in setting.stdout.splitlines():
            line = str(line)
            search = regex.search(line)
            if search:
                group = search.groupdict()
                info[int(group['uid'])] = int(group['temperature'])

        LOGGER.debug(info)
        assert len(info) == len(pantheon.hermes.gpu.GPUS)

        for uid, temperature in info.items():
            gpu = pantheon.hermes.gpu.GPUS[uid]
            gpu.temperature = temperature
            LOGGER.info('%s temperature is %s', gpu, temperature)
            speed = self.speed_for_temperature(temperature)
            LOGGER.info('Changing %s fan speed to %s', gpu, speed)
            pantheon.hermes.nvidia.settings.settings(
                '-a [gpu:{}]/GPUFanControlState=1 -a [fan-{}]/GPUTargetFanSpeed={}'.format(uid, uid, speed))

    async def __call__(self):
        while True:
            pantheon.hermes.engine.call_later(0, pantheon.hermes.engine.create_task, self.update_fans_speed())
            await asyncio.sleep(self.rate)
