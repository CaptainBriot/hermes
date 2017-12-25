class RegistryMeta(type):
    registry = dict()

    def __new__(cls, *args, **kwargs):
        obj = super().__new__(cls, *args, **kwargs)
        cls.registry[obj.model] = obj
        return obj


class First(object, metaclass=RegistryMeta):
    model = '1'


class Second(object, metaclass=RegistryMeta):
    model = '2'


print(RegistryMeta.registry)
print(RegistryMeta.registry['1'])
