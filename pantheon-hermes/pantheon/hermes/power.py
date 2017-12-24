import logging

import pantheon.hermes

LOGGER = logging.getLogger(__name__)


class PowerControl:
    @staticmethod
    def enable_persistence_mode():
        LOGGER.info('Enabling nvidia smi persistence mode')
        command = pantheon.hermes.command.Command('nvidia-smi -pm 1')
        command()
        command.log_lines()

    @staticmethod
    def set_power_limit():
        for gpu in pantheon.hermes.gpu.GPUS.values():
            LOGGER.info('Setting power limit for %s at %s', gpu, gpu.power)
            command = pantheon.hermes.command.Command('nvidia-smi -i {} -pl {}'.format(gpu.uid, gpu.power))
            command()
            command.log_lines()

    def __call__(self):
        self.enable_persistence_mode()
        self.set_power_limit()
