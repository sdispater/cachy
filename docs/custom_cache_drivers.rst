.. _CustomCacheDrivers:

Custom Cache Drivers
####################

To extend the ``CacheManager`` with a custom driver, you can use the ``extend`` method,
which is used to bind a custom driver resolver to the manager.

For example, to register a new cache driver named "mongo":

.. code-block:: python

    cache.extend('mongo', MongoStore)

On initialization, the ``MongoStore`` class will be passed the driver configuration.

.. note::

    Instead of the class you could also pass a function returning either a ``Store`` instance
    or a ``Repository`` instance.
