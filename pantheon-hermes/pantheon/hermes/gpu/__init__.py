import logging
import os
import re

from . import meta
from . import gpu

LOGGER = logging.getLogger(__name__)
REGISTRY = meta.GPUMeta.registry  # This is the registry of supported GPUs.

# Modules that need REGISTRY have the be imported after REGISTRY gets defined.
from . import nvidia


def load_gpus():
    gpus = {}
    top, dirs, nondirs = os.walk(os.path.join(os.sep, 'proc', 'driver', 'nvidia', 'gpus')).__next__()
    for name in dirs:
        gpu = load_one_gpu(os.path.join(top, name))
        gpus[gpu.uid] = gpu
    return gpus


def load_one_gpu(path):
    LOGGER.info("Found a Nvidia GPU at '%s'", path)

    with open(os.path.join(path, 'information'), 'r') as information:
        regexes = [re.compile('.*Model:\s*(?P<model>.*)'), re.compile('.*Bus Location:\s*(?P<bus_location>.*)'),
                   re.compile('.*Device Minor:\s*(?P<device_minor>.*)')]
        info = {}

        for line in information.readlines():
            for regex in regexes:
                search = regex.search(line)
                if search:
                    info.update(search.groupdict())

        return nvidia.helpers.from_dict(info)


GPU = load_gpus()

__all__ = ['meta', 'REGISTRY', 'nvidia', 'GPU']
