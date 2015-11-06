.. _Configuration:

Configuration
#############

Cachy provides a unified API for various caching systems.

All you need to get you started is the configuration describing the various cache stores
and passing it to a ``CacheManager`` instance.

.. code-block:: python

    from cachy import CacheManager

    config = {
        'stores': {
            'redis': {
                'driver': 'redis',
                'host': 'localhost',
                'port': 6379,
                'db': 0
            }
        }
    }

    cache = CacheManager(config)

If you have multiple stores configured you can specify which one is the default:

.. code-block:: python

    from cachy import CacheManager

    config = {
        'stores': {
            'redis': {
                'driver': 'redis',
                'host': 'localhost',
                'port': 6379,
                'db': 0
            },
            'memcached': {
                'driver' 'memcached',
                'servers': [
                    '127.0.0.1:11211'
                ]
            }
        }
    }

An example cache configuration is located at `examples/config.py <https://github.com/sdispater/cachy/examples/config.py>`_.

The cache configuration file contains various options, which are documented within the file,
so make sure to read over these options.


.. _Prerequisites:

Cache Prerequisites
===================

Database
--------

When using the ``database`` cache driver, you will need the `Orator ORM <http://orator-orm.com>`_.
You will also need to setup a table to contain the cache items.
You will find an example `SchemaBuilder <http://orator-orm.com/docs/schema_builder.html>`_
declaration for the table below:

.. code-block:: python

    with schema.create('cache') as table:
        table.string('key').unique()
        table.text('value')
        table.integer('expiration')

Memcached
---------

When using the ``memcached`` driver, you will need either the pure-python `python-memcached <https://pypi.python.org/pypi/python-memcached>`_
(`python3-memcached <https://pypi.python.org/pypi/python3-memcached>`_) or the **libmemcached** wrapper, `pylibmc <https://pypi.python.org/pypi/pylibmc>`_.

.. code-block:: python

    {
        'memcached': {
            'driver': 'memcached',
            'servers': [
                '127.0.0.1:11211'
            ]
        }
    }

Redis
-----

You will need the `redis <https://pypi.python.org/pypi/redis>`_ library in order to use the ``redis`` driver.

.. code-block:: python

    {
        'redis': {
            'driver': 'memcached',
            'host': 'localhost',
            'port': 6379,
            'db': 0
        }
    }

File
----

You do not need any extra package to use the ``file`` driver.

.. code-block:: python

    {
        'file': {
            'driver': 'file',
            'path': '/my/cache/directory'
        }
    }

Dict
----

You do not need any extra package to use the ``dict`` driver.

.. code-block:: python

    {
        'dict': {
            'driver': 'dict'
        }
    }


Serialization
=============

By default, Cachy will serialize objects using the ``pickle`` library.
However, this can be changed in the configuration, either globally or at driver level.

The possible values are ``pickle``, ``json``, ``msgpack``.

.. code-block:: python

    config = {
        'default': 'redis',
        'serializer': 'pickle',
        'stores': {
            'redis': {
                'driver': 'redis',
                'serializer': 'json',
                'host': 'localhost',
                'port': 6379,
                'db': 0
            },
            'memcached': {
                'driver' 'memcached',
                'servers': [
                    '127.0.0.1:11211'
                ]
            }
        }
    }

.. warning::

    The serializer you choose will determine which types of objects you can serialize,
    the ``pickle`` serializer being the more permissive.
