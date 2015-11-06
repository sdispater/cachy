# -*- coding: utf-8 -*-

import sys
import os
import errno

PY2 = sys.version_info[0] == 2
PY3K = sys.version_info[0] >= 3
PY33 = sys.version_info >= (3, 3)

if PY2:
    import imp

    long = long
    unicode = unicode
    basestring = basestring
else:
    long = int
    unicode = str
    basestring = str


def decode(string, encodings=None):
    if not PY2 and not isinstance(string, bytes):
        return string

    if encodings is None:
        encodings = ['utf-8', 'latin1', 'ascii']

    for encoding in encodings:
        try:
            return string.decode(encoding)
        except UnicodeDecodeError:
            pass

    return string.decode(encodings[0], errors='ignore')


def encode(string, encodings=None):
    if isinstance(string, bytes) or PY2 and isinstance(string, unicode):
        return string

    if encodings is None:
        encodings = ['utf-8', 'latin1', 'ascii']

    for encoding in encodings:
        try:
            return string.encode(encoding)
        except UnicodeDecodeError:
            pass

    return string.encode(encodings[0], errors='ignore')


def mkdir_p(path, mode=0o777):
    try:
        os.makedirs(path, mode)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise
