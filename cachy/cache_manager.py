# -*- coding: utf-8 -*-

import threading
import types
from .contracts.factory import Factory
from .contracts.store import Store

from .stores import (
    DictStore,
    FileStore,
    RedisStore,
    MemcachedStore
)

from .repository import Repository
from .serializers import (
    Serializer,
    JsonSerializer,
    MsgPackSerializer,
    PickleSerializer
)


class CacheManager(Factory, threading.local):
    """
    A CacheManager is a pool of cache stores.
    """

    _serializers = {
        'json': JsonSerializer(),
        'msgpack': MsgPackSerializer(),
        'pickle': PickleSerializer()
    }

    def __init__(self, config):
        super(CacheManager, self).__init__()

        self._config = config
        self._stores = {}
        self._custom_creators = {}
        self._serializer = self._resolve_serializer(config.get('serializer', 'pickle'))

    def store(self, name=None):
        """
        Get a cache store instance by name.

        :param name: The cache store name
        :type name: str

        :rtype: Repository
        """
        if name is None:
            name = self.get_default_driver()

        self._stores[name] = self._get(name)

        return self._stores[name]

    def driver(self, name=None):
        """
        Get a cache store instance by name.

        :param name: The cache store name
        :type name: str

        :rtype: Repository
        """
        return self.store(name)

    def _get(self, name):
        """
        Attempt to get the store from the local cache.

        :param name: The store name
        :type name: str

        :rtype: Repository
        """
        return self._stores.get(name, self._resolve(name))

    def _resolve(self, name):
        """
        Resolve the given store

        :param name: The store to resolve
        :type name: str

        :rtype: Repository
        """
        config = self._get_config(name)

        if not config:
            raise RuntimeError('Cache store [%s] is not defined.' % name)

        if config['driver'] in self._custom_creators:
            repository = self._call_custom_creator(config)
        else:
            repository = getattr(self, '_create_%s_driver' % config['driver'])(config)

        if 'serializer' in config:
            serializer = self._resolve_serializer(config['serializer'])
        else:
            serializer = self._serializer

        repository.get_store().set_serializer(serializer)

        return repository

    def _call_custom_creator(self, config):
        """
        Call a custom driver creator.

        :param config: The driver configuration
        :type config: dict

        :rtype: Repository
        """
        creator = self._custom_creators[config['driver']](config)

        if isinstance(creator, Store):
            creator = self.repository(creator)

        if not isinstance(creator, Repository):
            raise RuntimeError('Custom creator should return a Repository instance.')

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
        kwargs = {
            'directory': config['path']
        }

        if 'hash_type' in config:
            kwargs['hash_type'] = config['hash_type']

        return self.repository(FileStore(**kwargs))

    def _create_redis_driver(self, config):
        """
        Create an instance of the redis cache driver.

        :param config: The driver configuration
        :type config: dict

        :return: Repository
        """
        return self.repository(RedisStore(**config))

    def _create_memcached_driver(self, config):
        """
        Create an instance of the redis cache driver.

        :param config: The driver configuration
        :type config: dict

        :return: Repository
        """
        return self.repository(MemcachedStore(**config))

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

    def _resolve_serializer(self, serializer):
        """
        Resolve the given serializer.

        :param serializer: The serializer to resolve
        :type serializer: str or Serializer

        :rtype: Serializer
        """
        if isinstance(serializer, Serializer):
            return serializer

        if serializer in self._serializers:
            return self._serializers[serializer]

        raise RuntimeError('Unsupported serializer')

    def register_serializer(self, name, serializer):
        """
        Register a new serializer.

        :param name: The name of the serializer
        :type name: str

        :param serializer: The serializer
        :type serializer: Serializer
        """
        self._serializers[name] = serializer

    def __getattr__(self, item):
        return getattr(self.store(), item)

    def __call__(self, store=None, *args, **kwargs):
        if isinstance(store, (types.FunctionType, types.MethodType)):
            fn = store

            if len(args) > 0:
                store = args[0]
                args = args[1:] if len(args) > 1 else []
            else:
                store = None

            args = (fn,) + args

            return self.store(store)(*args, **kwargs)
        else:
            return self.store(store)(*args, **kwargs)
