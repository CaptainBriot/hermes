class GPUMeta(type):
    registry = dict()

    def __new__(mcs, *args, **kwargs):
        obj = super().__new__(mcs, *args, **kwargs)

        if obj.model is not None:
            mcs.registry[obj.model] = obj

        return obj
