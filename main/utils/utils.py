
def override(method):
    def wrapper(*args, **kwargs):
        # Check if the method exists in the superclass
        if not any(method.__name__ in supercls.__dict__ for supercls in args[0].__class__.__bases__):
            raise TypeError(f"{method.__name__} does not override any method in the base class")
        return method(*args, **kwargs)
    return wrapper