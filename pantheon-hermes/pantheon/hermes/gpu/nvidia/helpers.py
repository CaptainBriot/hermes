import logging

from .. import REGISTRY

LOGGER = logging.getLogger(__name__)


def from_dict(info):
    klass = REGISTRY[info['model']]
    gpu = klass(int(info['device_minor']), info['bus_location'])
    LOGGER.info('Initialized %s', gpu)
    return gpu
