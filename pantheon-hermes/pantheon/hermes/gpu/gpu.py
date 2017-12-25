from . import meta


class BaseGPU(object, metaclass=meta.GPUMeta):
    model = None
    mem = None
    clock = None
    power = None

    def __init__(self, index, bus):
        if self.model is None or self.mem is None or self.clock is None or self.power is None:
            raise RuntimeError('GPU model, mem, clock and power have to be defined')

        self.index = index
        self.bus = bus
        self.temperature = None

    def __str__(self):
        return '{}<{}, index: {}, bus: {}>'.format(self.__class__.__name__, self.model, self.index, self.bus)
