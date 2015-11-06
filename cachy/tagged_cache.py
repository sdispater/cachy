# -*- coding: utf-8 -*-

import hashlib
import datetime
import math
from .contracts.store import Store
from .helpers import value
from .utils import encode


class TaggedCache(Store):
    """

    """
    def __init__(self, store, tags):
        """
        :param store: The cache store implementation
        :type store: cachy.contracts.store.Store

        :param tags: The tag set
        :type tags: cachy.tag_set.TagSet
        """
        self._store = store
        self._tags = tags

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

        :param default: The default value
        :type default: mixed

        :return: The cache value
        """
        val = self._store.get(self.tagged_item_key(key))

        if val is not None:
            return val

        return value(default)

    def put(self, key, value, minutes):
        """
        Store an item in the cache for a given number of minutes.

        :param key: The cache key
        :type key: str

        :param value: The cache value
        :type value: mixed

        :param minutes: The lifetime in minutes of the cached value
        :type minutes: int or datetime
        """
        minutes = self._get_minutes(minutes)

        if minutes is not None:
            return self._store.put(self.tagged_item_key(key), value, minutes)

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
        if not self.has(key):
            self.put(key, val, minutes)

            return True

        return False

    def increment(self, key, value=1):
        """
        Increment the value of an item in the cache.

        :param key: The cache key
        :type key: str

        :param value: The increment value
        :type value: int

        :rtype: int or bool
        """
        self._store.increment(self.tagged_item_key(key), value)

    def decrement(self, key, value=1):
        """
        Decrement the value of an item in the cache.

        :param key: The cache key
        :type key: str

        :param value: The decrement value
        :type value: int

        :rtype: int or bool
        """
        self._store.decrement(self.tagged_item_key(key), value)

    def forever(self, key, value):
        """
        Store an item in the cache indefinitely.

        :param key: The cache key
        :type key: str

        :param value: The value
        :type value: mixed
        """
        self._store.forever(self.tagged_item_key(key), value)

    def forget(self, key):
        """
        Remove an item from the cache.

        :param key: The cache key
        :type key: str

        :rtype: bool
        """
        self._store.forget(self.tagged_item_key(key))

    def flush(self):
        """
        Remove all items from the cache.
        """
        self._tags.reset()

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

    def tagged_item_key(self, key):
        """
        Get a fully qualified key for a tagged item.

        :param key: The cache key
        :type key: str

        :rtype: str
        """
        return '%s:%s' % (hashlib.sha1(encode(self._tags.get_namespace())).hexdigest(), key)

    def get_prefix(self):
        """
        Get the cache key prefix.

        :rtype: str
        """
        return self._store.get_prefix()

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
