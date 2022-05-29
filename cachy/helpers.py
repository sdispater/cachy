def value(val):
    if callable(val):
        return val()

    return val
