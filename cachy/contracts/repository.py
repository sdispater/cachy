# -*- coding: utf-8 -*-


class Repository(object):

    def has(self, key):
        """
        Determine if an item exists in the cache.

        :param key: The cache key
        :type key: str

        :rtype: bool
        """
        raise NotImplementedError()

    def get(self, key, default=None):
        """
        Retrieve an item from the cache by key.

        :param key: The cache key
        :type key: str

        :param default: The default value to return
        :type default: mixed

        :rtype: mixed
        """
        raise NotImplementedError()

    def pull(self, key, default=None):
        """
        Retrieve an item from the cache by key and delete ir.

        :param key: The cache key
        :type key: str

        :param default: The default value to return
        :type default: mixed

        :rtype: mixed
        """
        raise NotImplementedError()

    def put(self, key, value, minutes):
        """
        Store an item in the cache.

        :param key: The cache key
        :type key: str

        :param value: The cache value
        :type value: mixed

        :param minutes: The lifetime in minutes of the cached value
        :type minutes: int or datetime
        """
        raise NotImplementedError()

    def add(self, key, value, minutes):
        """
        Store an item in the cache if it does not exist.

        :param key: The cache key
        :type key: str

        :param value: The cache value
        :type value: mixed

        :param minutes: The lifetime in minutes of the cached value
        :type minutes: int or datetime

        :rtype: bool
        """
        raise NotImplementedError()

    def forever(self, key, value):
        """
        Store an item in the cache indefinitely.

        :param key: The cache key
        :type key: str

        :param value: The cache value
        :type value: mixed
        """
        raise NotImplementedError()

    def remember(self, key, minutes, callback):
        """
        Get an item from the cache, or store the default value.

        :param key: The cache key
        :type key: str

        :param minutes: The lifetime in minutes of the cached value
        :type minutes: int or datetime

        :param callback: The default function
        :type callback: callable

        :rtype: mixed
        """
        raise NotImplementedError()

    def remember_forever(self, key, callback):
        """
        Get an item from the cache, or store the default value forever.

        :param key: The cache key
        :type key: str

        :param callback: The default function
        :type callback: callable

        :rtype: mixed
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
