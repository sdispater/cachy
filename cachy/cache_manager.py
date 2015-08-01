# -*- coding: utf-8 -*-

from .contracts.factory import Factory
from .contracts.store import Store

from .stores import (
    DictStore,
    FileStore
)

from .repository import Repository


class CacheManager(Factory):
    """
    A CacheManager is a pool of cache stores
    """

    def __init__(self, config):
        self._config = config
        self._stores = {}
        self._custom_creators = {}

    def store(self, name=None):
        """
        Get a cache store instance by name.

        :param name: The cache store name
        :type name: str

        :rtype: mixed
        """
        if name is None:
            name = self.get_default_driver()

        self._stores[name] = self._get(name)

        return self._stores[name]

    def _get(self, name):
        """
        Attempt to get the store from the local cache.

        :param name: The store name
        :type name: str

        :rtype: mixed
        """
        return self._stores.get(name, self._resolve(name))

    def _resolve(self, name):
        """
        Resolve the given store

        :param name: The store to resolve
        :type name: str

        :rtype: mixed
        """
        config = self._get_config(name)

        if not config:
            raise RuntimeError('Cache store [%s] is not defined.')

        if config['driver'] in self._custom_creators:
            return self._call_custom_creator(config)

        return getattr(self, '_create_%s_driver' % config['driver'])(config)

    def _call_custom_creator(self, config):
        """
        Call a custom driver creator.

        :param config: The driver configuration
        :type config: dict

        :rtype: mixed
        """
        creator = self._custom_creators[config['driver']](config)

        if isinstance(creator, Store):
            return self.repository(creator)

        return creator

    def _create_dict_driver(self, config):
        """
        Create an instance of the dict cache driver.

        :param config: The driver configuration
        :type config: dict

        :rtype: Repository
        """
        return self.repository(DictStore())

    def _create_file_driver(self, config):
        """
        Create an instance of the file cache driver.

        :param config: The driver configuration
        :type config: dict

        :rtype: Repository
        """
        return self.repository(FileStore(config['path']))

    def repository(self, store):
        """
        Create a new cache repository with the given implementation.

        :param store: The cache store implementation instance
        :type store: Store

        :rtype: Repository
        """
        repository = Repository(store)

        return repository

    def _get_prefix(self, config):
        """
        Get the cache prefix.

        :param config: The configuration
        :type config: dict

        :rtype: str
        """
        return config.get('prefix', '')

    def _get_config(self, name):
        """
        Get the cache connection configuration.

        :param name: The cache name
        :type name: str

        :rtype: dict
        """
        return self._config['stores'].get(name)

    def get_default_driver(self):
        """
        Get the default cache driver name.

        :rtype: str

        :raises: RuntimeError
        """
        if 'default' in self._config:
            return self._config['default']

        if len(self._config['stores']) == 1:
            return list(self._config['stores'].keys())[0]

        raise RuntimeError('Missing "default" cache in configuration.')

    def set_default_driver(self, name):
        """
        Set the default cache driver name.

        :param name: The default cache driver name
        :type name: str
        """
        self._config['default'] = name

    def extend(self, driver, store):
        """
        Register a custom driver creator.

        :param driver: The driver
        :type driver: name

        :param store: The store class
        :type store: Store or callable

        :rtype: self
        """
        self._custom_creators[driver] = store

        return self

    def __getattr__(self, item):
        try:
            return object.__getattribute__(self, item)
        except AttributeError:
            return getattr(self.store(), item)
