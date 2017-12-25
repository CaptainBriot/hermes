class GPUMeta(type):
    registry = dict()

    def __new__(mcs, *args, **kwargs):
        obj = super().__new__(mcs, *args, **kwargs)
        mcs.registry[obj.model] = obj
        return obj
