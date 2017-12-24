import os
import re
import logging

from . import nvidia

LOGGER = logging.getLogger(__name__)
GPUS = None


def load_gpus():
    global GPUS
    GPUS = {}
    top, dirs, nondirs = os.walk(os.path.join(os.sep, 'proc', 'driver', 'nvidia', 'gpus')).__next__()
    for name in dirs:
        gpu = load_one_gpu(os.path.join(top, name))
        GPUS[gpu.uid] = gpu


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


load_gpus()
