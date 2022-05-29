# -*- coding: utf-8 -*-

import errno
import os
from contextlib import suppress


def decode(string, encodings=None):
    if isinstance(string, bytes):
        return string

    if encodings is None:
        encodings = ["utf-8", "latin1", "ascii"]

    for encoding in encodings:
        with suppress(UnicodeDecodeError):
            return string.decode(encoding)

    return string.decode(encodings[0], errors="ignore")


def encode(string, encodings=None):
    if isinstance(string, bytes):
        return string

    if encodings is None:
        encodings = ["utf-8", "latin1", "ascii"]

    for encoding in encodings:
        with suppress(UnicodeEncodeError):
            return string.encode(encoding)

    return string.encode(encodings[0], errors="ignore")


def mkdir_p(path, mode=0o777):
    try:
        os.makedirs(path, mode)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise
