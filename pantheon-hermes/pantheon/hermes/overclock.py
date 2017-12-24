import logging

import pantheon.hermes

LOGGER = logging.getLogger(__name__)


class OverclockControl:
    @staticmethod
    def overclock():
        LOGGER.info('Overclocking GPUs')
        args = ''
        for gpu in pantheon.hermes.gpu.GPUS.values():
            args += ' -a [gpu:{}]/GPUMemoryTransferRateOffset[3]={}'.format(gpu.uid, gpu.mem)
            args += ' -a [gpu:{}]/GPUGraphicsClockOffset[3]={}'.format(gpu.uid, gpu.clock)
        pantheon.hermes.nvidia.settings.settings(args)

    def __call__(self):
        self.overclock()
