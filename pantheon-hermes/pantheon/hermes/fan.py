import asyncio
import logging
import re

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

    @staticmethod
    def initialize_fan_control():
        args = ''
        for index in pantheon.hermes.gpu.GPU:
            args += ' -a [gpu:{}]/GPUFanControlState=1'.format(index)
        pantheon.hermes.gpu.nvidia.api.settings(args)

    async def update_fans_speed(self):
        LOGGER.info('Updating fans speed')
        setting = pantheon.hermes.gpu.nvidia.api.smi('index', 'temperature.gpu')

        info = {}
        for line in setting.stdout.splitlines():
            line = line.decode('utf-8')
            index, temperature = [int(item.strip()) for item in line.split(',')]
            info[index] = temperature

        LOGGER.debug(info)
        assert len(info) == len(pantheon.hermes.gpu.GPU)

        args = ''
        for index, temperature in info.items():
            gpu = pantheon.hermes.gpu.GPU[index]
            gpu.temperature = temperature
            LOGGER.info('%s temperature is %s', gpu, temperature)
            speed = self.speed_for_temperature(temperature)
            LOGGER.info('Changing %s fan speed to %s', gpu, speed)
            args += ' -a [fan-{}]/GPUTargetFanSpeed={}'.format(index, speed)

        pantheon.hermes.gpu.nvidia.api.settings(args)

    async def __call__(self):
        self.initialize_fan_control()
        while True:
            pantheon.hermes.loop.call_later(0, pantheon.hermes.loop.create_task, self.update_fans_speed())
            await asyncio.sleep(self.rate)
