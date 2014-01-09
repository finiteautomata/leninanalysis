class BaseFactory(object):
    def __new__(cls, *args, **kwargs):
        defaults = cls.__dict__.copy()
        defaults.update(kwargs)

        return cls.model(*args, **defaults)
