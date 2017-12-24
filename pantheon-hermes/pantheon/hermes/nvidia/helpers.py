import logging

from . import gtx

LOGGER = logging.getLogger(__name__)
CATALOG = {gtx.Nvidia1070.model: gtx.Nvidia1070}


def from_dict(info):
    klass = CATALOG[info['model']]
    gpu = klass(int(info['device_minor']), info['bus_location'])
    LOGGER.info('Initialized %s', gpu)
    return gpu
