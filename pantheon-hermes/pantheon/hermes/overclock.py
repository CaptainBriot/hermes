import logging

import pantheon.hermes

LOGGER = logging.getLogger(__name__)


class OverclockControl:
    @staticmethod
    def overclock():
        LOGGER.info('Overclocking GPUs')
        args = ''
        for gpu in pantheon.hermes.gpu.GPU.values():
            args += ' -a [gpu:{}]/GPUMemoryTransferRateOffset[3]={}'.format(gpu.index, gpu.mem)
            args += ' -a [gpu:{}]/GPUGraphicsClockOffset[3]={}'.format(gpu.index, gpu.clock)
        pantheon.hermes.gpu.nvidia.api.settings(args)

    def __call__(self):
        self.overclock()
