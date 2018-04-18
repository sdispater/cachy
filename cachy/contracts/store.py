# -*- coding: utf-8 -*-

from ..serializers import PickleSerializer


class Store(object):
    """
    Abstract class representing a cache store.
    """

    _serializer = PickleSerializer()

    def get(self, key):
        """
        Retrieve an item from the cache by key.

        :param key: The cache key
        :type key: str

        :return: The cache value
        """
        raise NotImplementedError()

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
        raise NotImplementedError()

    def increment(self, key, value=1):
        """
        Increment the value of an item in the cache.

        :param key: The cache key
        :type key: str

        :param value: The increment value
        :type value: int

        :rtype: int or bool
        """
        raise NotImplementedError()

    def decrement(self, key, value=1):
        """
        Decrement the value of an item in the cache.

        :param key: The cache key
        :type key: str

        :param value: The decrement value
        :type value: int

        :rtype: int or bool
        """
        raise NotImplementedError()

    def forever(self, key, value):
        """
        Store an item in the cache indefinitely.

        :param key: The cache key
        :type key: str

        :param value: The value
        :type value: mixed
        """
        raise NotImplementedError()

    def forget(self, key):
        """
        Remove an item from the cache.

        :param key: The cache key
        :type key: str

        :rtype: bool
        """
        raise NotImplementedError()

    def flush(self):
        """
        Remove all items from the cache.
        """
        raise NotImplementedError()

    def get_prefix(self):
        """
        Get the cache key prefix.

        :rtype: str
        """
        raise NotImplementedError()

    def set_serializer(self, serializer):
        """
        Set the serializer.

        :param serializer: The serializer
        :type serializer: cachy.serializers.Serializer

        :rtype: Store
        """
        self._serializer = serializer

        return self

    def unserialize(self, data):
        return self._serializer.unserialize(data)

    def serialize(self, data):
        return self._serializer.serialize(data)
