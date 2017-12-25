import asyncio

from . import command
from . import fan
from . import gpu
from . import overclock
from . import power
from .version import __version__

DISPLAY = 999
loop = asyncio.get_event_loop()

__all__ = ['__version__', 'fan', 'loop', 'command', 'gpu', 'DISPLAY', 'power']
