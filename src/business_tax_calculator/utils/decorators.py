# utils/decorators.py

class classproperty(property):
    """A decorator that behaves like @property but works on the class itself."""
    def __get__(self, obj, cls):
        return self.fget(cls)
