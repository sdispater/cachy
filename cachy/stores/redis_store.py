# -*- coding: utf-8 -*-

try:
    from redis import StrictRedis
except ImportError:
    StrictRedis = None

from ..contracts.taggable_store import TaggableStore
from ..redis_tagged_cache import RedisTaggedCache
from ..tag_set import TagSet


class RedisStore(TaggableStore):
    """
    A cache store using the Redis as its backend.
    """

    def __init__(self, host='localhost', port=6379, db=0, password=None,
                 prefix='', redis_class=StrictRedis, **kwargs):
        # Removing potential "driver" key
        kwargs.pop('driver', None)

        self._prefix = prefix
        self._redis = redis_class(host=host, port=port, db=db,
                                  password=password, **kwargs)

    def get(self, key):
        """
        Retrieve an item from the cache by key.

        :param key: The cache key
        :type key: str

        :return: The cache value
        """
        value = self._redis.get(self._prefix + key)

        if value is not None:
            return self.unserialize(value)

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
        value = self.serialize(value)

        minutes = max(1, minutes)

        self._redis.setex(self._prefix + key, minutes * 60, value)

    def increment(self, key, value=1):
        """
        Increment the value of an item in the cache.

        :param key: The cache key
        :type key: str

        :param value: The increment value
        :type value: int

        :rtype: int or bool
        """
        return self._redis.incrby(self._prefix + key, value)

    def decrement(self, key, value=1):
        """
        Decrement the value of an item in the cache.

        :param key: The cache key
        :type key: str

        :param value: The decrement value
        :type value: int

        :rtype: int or bool
        """
        return self._redis.decr(self._prefix + key, value)

    def forever(self, key, value):
        """
        Store an item in the cache indefinitely.

        :param key: The cache key
        :type key: str

        :param value: The value to store
        :type value: mixed
        """
        value = self.serialize(value)

        self._redis.set(self._prefix + key, value)

    def forget(self, key):
        """
        Remove an item from the cache.

        :param key: The cache key
        :type key: str

        :rtype: bool
        """
        return bool(self._redis.delete(self._prefix + key))

    def flush(self):
        """
        Remove all items from the cache.
        """
        return self._redis.flushdb()

    def get_prefix(self):
        """
        Get the cache key prefix.

        :rtype: str
        """
        return self._prefix

    def connection(self):
        return self._redis

    def tags(self, *names):
        """
        Begin executing a new tags operation.

        :param names: The tags
        :type names: tuple

        :rtype: cachy.tagged_cache.TaggedCache
        """
        return RedisTaggedCache(self, TagSet(self, names))
