# -*- coding: utf-8 -*-

import math
import datetime
from .contracts.repository import Repository as CacheContract
from .helpers import value


class Repository(CacheContract):

    _default = 60

    def __init__(self, store):
        """
        :param store: The underlying cache store
        :type store: Store
        """
        self._store = store

    def has(self, key):
        """
        Determine if an item exists in the cache.

        :param key: The cache key
        :type key: str

        :rtype: bool
        """
        return self.get(key) is not None

    def get(self, key, default=None):
        """
        Retrieve an item from the cache by key.

        :param key: The cache key
        :type key: str

        :param default: The default value to return
        :type default: mixed

        :rtype: mixed
        """
        val = self._store.get(key)

        if val is None:
            return value(default)

        return val

    def pull(self, key, default=None):
        """
        Retrieve an item from the cache by key and delete ir.

        :param key: The cache key
        :type key: str

        :param default: The default value to return
        :type default: mixed

        :rtype: mixed
        """
        val = self.get(key, default)

        self.forget(key)

        return val

    def put(self, key, val, minutes):
        """
        Store an item in the cache.

        :param key: The cache key
        :type key: str

        :param val: The cache value
        :type val: mixed

        :param minutes: The lifetime in minutes of the cached value
        :type minutes: int|datetime
        """
        minutes = self._get_minutes(minutes)

        if minutes is not None:
            self._store.put(key, val, minutes)

    def add(self, key, val, minutes):
        """
        Store an item in the cache if it does not exist.

        :param key: The cache key
        :type key: str

        :param val: The cache value
        :type val: mixed

        :param minutes: The lifetime in minutes of the cached value
        :type minutes: int|datetime

        :rtype: bool
        """
        if hasattr(self._store, 'add'):
            return self._store.add(key, val, self._get_minutes(minutes))

        if not self.has(key):
            self.put(key, val, minutes)

            return True

        return False

    def forever(self, key, val):
        """
        Store an item in the cache indefinitely.

        :param key: The cache key
        :type key: str

        :param val: The cache value
        :type val: mixed
        """
        self._store.forever(key, val)

    def remember(self, key, minutes, callback):
        """
        Get an item from the cache, or store the default value.

        :param key: The cache key
        :type key: str

        :param minutes: The lifetime in minutes of the cached value
        :type minutes: int or datetime

        :param callback: The default function
        :type callback: mixed

        :rtype: mixed
        """
        # If the item exists in the cache we will just return this immediately
        # otherwise we will execute the given callback and cache the result
        # of that execution for the given number of minutes in storage.
        val = self.get(key)
        if val is not None:
            return val

        val = value(callback)

        self.put(key, val, minutes)

        return val

    def remember_forever(self, key, callback):
        """
        Get an item from the cache, or store the default value forever.

        :param key: The cache key
        :type key: str

        :param callback: The default function
        :type callback: mixed

        :rtype: mixed
        """
        # If the item exists in the cache we will just return this immediately
        # otherwise we will execute the given callback and cache the result
        # of that execution forever.
        val = self.get(key)
        if val is not None:
            return val

        val = value(callback)

        self.forever(key, val)

        return val

    def forget(self, key):
        """
        Remove an item from the cache.

        :param key: The cache key
        :type key: str

        :rtype: bool
        """
        success = self._store.forget(key)

        return success

    def get_default_cache_time(self):
        """
        Get the default cache time.

        :rtype: int
        """
        return self._default

    def set_default_cache_time(self, minutes):
        """
        Set the default cache time.

        :param minutes: The default cache time
        :type minutes: int

        :rtype: self
        """
        self._default = minutes

        return self

    def get_store(self):
        """
        Get the cache store implementation.

        :rtype: Store
        """
        return self._store

    def __getitem__(self, item):
        return self.get(item)

    def __setitem__(self, key, val):
        self.put(key, val, self._default)

    def __delitem__(self, key):
        self.forget(key)

    def _get_minutes(self, duration):
        """
        Calculate the number of minutes with the given duration.

        :param duration: The duration
        :type duration: int or datetime

        :rtype: int or None
        """
        if isinstance(duration, datetime.datetime):
            from_now = (duration - datetime.datetime.now()).total_seconds()
            from_now = math.ceil(from_now / 60)

            if from_now > 0:
                return from_now

            return

        return duration

    def __getattr__(self, item):
        try:
            return object.__getattribute__(self, item)
        except AttributeError:
            return getattr(self._store, item)
