# -*- coding: utf-8 -*-

import os
import time
import math
import hashlib
from ..contracts.store import Store
from ..utils import mkdir_p, encode


class FileStore(Store):
    """
    A cache store using the filesystem as its backend.
    """

    _HASHES = {
        'md5': (hashlib.md5, 2),
        'sha1': (hashlib.sha1, 4),
        'sha256': (hashlib.sha256, 8)
    }

    def __init__(self, directory, hash_type='sha256'):
        """
        :param directory: The cache directory
        :type directory: str
        """
        self._directory = directory

        if hash_type not in self._HASHES:
            raise ValueError('hash_type "{}" is not valid.'.format(hash_type))

        self._hash_type = hash_type

    def get(self, key):
        """
        Retrieve an item from the cache by key.

        :param key: The cache key
        :type key: str

        :return: The cache value
        """
        return self._get_payload(key).get('data')

    def _get_payload(self, key):
        """
        Retrieve an item and expiry time from the cache by key.

        :param key: The cache key
        :type key: str

        :rtype: dict
        """
        path = self._path(key)

        # If the file doesn't exists, we obviously can't return the cache so we will
        # just return null. Otherwise, we'll get the contents of the file and get
        # the expiration UNIX timestamps from the start of the file's contents.
        if not os.path.exists(path):
            return {'data': None, 'time': None}

        with open(path, 'rb') as fh:
            contents = fh.read()

        expire = int(contents[:10])

        # If the current time is greater than expiration timestamps we will delete
        # the file and return null. This helps clean up the old files and keeps
        # this directory much cleaner for us as old files aren't hanging out.
        if round(time.time()) >= expire:
            self.forget(key)

            return {'data': None, 'time': None}

        data = self.unserialize(contents[10:])

        # Next, we'll extract the number of minutes that are remaining for a cache
        # so that we can properly retain the time for things like the increment
        # operation that may be performed on the cache. We'll round this out.
        time_ = math.ceil((expire - round(time.time())) / 60.)

        return {'data': data, 'time': time_}

    def put(self, key, value, minutes):
        """
        Store an item in the cache for a given number of minutes.

        :param key: The cache key
        :type key: str

        :param value: The cache value
        :type value: mixed

        :param minutes: The lifetime in minutes of the cached value
        :type minutes: int
        """
        value = encode(str(self._expiration(minutes))) + encode(self.serialize(value))

        path = self._path(key)
        self._create_cache_directory(path)

        with open(path, 'wb') as fh:
            fh.write(value)

    def _create_cache_directory(self, path):
        """
        Create the file cache directory if necessary

        :param path: The cache path
        :type path: str
        """
        mkdir_p(os.path.dirname(path))

    def increment(self, key, value=1):
        """
        Increment the value of an item in the cache.

        :param key: The cache key
        :type key: str

        :param value: The increment value
        :type value: int

        :rtype: int or bool
        """
        raw = self._get_payload(key)

        integer = int(raw['data']) + value

        self.put(key, integer, int(raw['time']))

        return integer

    def decrement(self, key, value=1):
        """
        Decrement the value of an item in the cache.

        :param key: The cache key
        :type key: str

        :param value: The decrement value
        :type value: int

        :rtype: int or bool
        """
        return self.increment(key, value * -1)

    def forever(self, key, value):
        """
        Store an item in the cache indefinitely.

        :param key: The cache key
        :type key: str

        :param value: The increment value
        :type value: int
        """
        self.put(key, value, 0)

    def forget(self, key):
        """
        Remove an item from the cache.

        :param key: The cache key
        :type key: str

        :rtype: bool
        """
        path = self._path(key)

        if os.path.exists(path):
            os.remove(path)

            return True

        return False

    def flush(self):
        """
        Remove all items from the cache.
        """
        if os.path.isdir(self._directory):
            for root, dirs, files in os.walk(self._directory, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))

                for name in dirs:
                    os.rmdir(os.path.join(root, name))

    def _path(self, key):
        """
        Get the full path for the given cache key.

        :param key: The cache key
        :type key: str

        :rtype: str
        """
        hash_type, parts_count = self._HASHES[self._hash_type]
        h = hash_type(encode(key)).hexdigest()

        parts = [h[i:i+2] for i in range(0, len(h), 2)][:parts_count]

        return os.path.join(self._directory, os.path.sep.join(parts), h)

    def _expiration(self, minutes):
        """
        Get the expiration time based on the given minutes.

        :param minutes: The minutes
        :type minutes: int

        :rtype: int
        """
        if minutes == 0:
            return 9999999999

        return int(round(time.time()) + (minutes * 60))

    def get_prefix(self):
        """
        Get the cache key prefix.

        :rtype: str
        """
        return ''
        return ''
