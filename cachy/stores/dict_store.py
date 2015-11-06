# -*- coding: utf-8 -*-

import time
import math
from ..contracts.taggable_store import TaggableStore


class DictStore(TaggableStore):
    """
    A cache store using a dictionary as its backend.
    """

    def __init__(self):
        self._storage = {}

    def get(self, key):
        """
        Retrieve an item from the cache by key.

        :param key: The cache key
        :type key: str

        :return: The cache value
        """
        return self._get_payload(key)[0]

    def _get_payload(self, key):
        """
        Retrieve an item and expiry time from the cache by key.

        :param key: The cache key
        :type key: str

        :rtype: dict
        """
        payload = self._storage.get(key)

        # If the key does not exist, we return nothing
        if not payload:
            return (None, None)

        expire = payload[0]

        # If the current time is greater than expiration timestamps we will delete
        # the entry
        if round(time.time()) >= expire:
            self.forget(key)

            return (None, None)

        data = payload[1]

        # Next, we'll extract the number of minutes that are remaining for a cache
        # so that we can properly retain the time for things like the increment
        # operation that may be performed on the cache. We'll round this out.
        time_ = math.ceil((expire - round(time.time())) / 60.)

        return (data, time_)

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
        self._storage[key] = (self._expiration(minutes), value)

    def increment(self, key, value=1):
        """
        Increment the value of an item in the cache.

        :param key: The cache key
        :type key: str

        :param value: The increment value
        :type value: int

        :rtype: int or bool
        """
        data, time_ = self._get_payload(key)

        integer = int(data) + value

        self.put(key, integer, int(time_))

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
        if key in self._storage:
            del self._storage[key]

            return True

        return False

    def flush(self):
        """
        Remove all items from the cache.
        """
        self._storage = {}

    def _expiration(self, minutes):
        """
        Get the expiration time based on the given minutes.

        :param minutes: The minutes
        :type minutes: int

        :rtype: int
        """
        if minutes == 0:
            return 9999999999

        return round(time.time()) + (minutes * 60)

    def get_prefix(self):
        """
        Get the cache key prefix.

        :rtype: str
        """
        return ''
