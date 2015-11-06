# -*- coding: utf-8 -*-

try:
    from pylibmc import memcache
except ImportError:
    try:
        import memcache
    except ImportError:
        memcache = None

from ..contracts.taggable_store import TaggableStore


class MemcachedStore(TaggableStore):

    def __init__(self, servers, prefix='', **kwargs):
        # Removing potential "driver" key
        kwargs.pop('driver', None)

        self._prefix = prefix
        self._memcache = memcache.Client(servers, **kwargs)

    def get(self, key):
        """
        Retrieve an item from the cache by key.

        :param key: The cache key
        :type key: str

        :return: The cache value
        """
        return self._memcache.get(self._prefix + key)

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
        self._memcache.set(self._prefix + key, value, minutes * 60)

    def add(self, key, val, minutes):
        """
        Store an item in the cache if it does not exist.

        :param key: The cache key
        :type key: str

        :param val: The cache value
        :type val: mixed

        :param minutes: The lifetime in minutes of the cached value
        :type minutes: int

        :rtype: bool
        """
        return self._memcache.add(self._prefix + key, val, minutes * 60)

    def increment(self, key, value=1):
        """
        Increment the value of an item in the cache.

        :param key: The cache key
        :type key: str

        :param value: The increment value
        :type value: int

        :rtype: int or bool
        """
        return self._memcache.incr(self._prefix + key, value)

    def decrement(self, key, value=1):
        """
        Decrement the value of an item in the cache.

        :param key: The cache key
        :type key: str

        :param value: The decrement value
        :type value: int

        :rtype: int or bool
        """
        return self._memcache.decr(self._prefix + key, value)

    def forever(self, key, value):
        """
        Store an item in the cache indefinitely.

        :param key: The cache key
        :type key: str

        :param value: The value
        :type value: mixed
        """
        self.put(key, value, 0)

    def forget(self, key):
        """
        Remove an item from the cache.

        :param key: The cache key
        :type key: str

        :rtype: bool
        """
        return self._memcache.delete(self._prefix + key)

    def flush(self):
        """
        Remove all items from the cache.
        """
        self._memcache.flush_all()

    def get_prefix(self):
        """
        Get the cache key prefix.

        :rtype: str
        """
        return self._prefix
