# -*- coding: utf-8 -*-


def value(val):
    if callable(val):
        return val()

    return val
