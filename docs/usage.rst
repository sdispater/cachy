.. _Usage:

Usage
#####

As seen in the :ref:`Configuration` section, you first need to create a ``CacheManager``
instance.

Accessing Multiple Cache Stores
===============================

Using the ``CacheManager`` instance, you can access the configured cache stores via the ``store`` method.
The key passed to the store method should correspond to one of the stores listed in the ``stores``
configuration dictionary:

.. code-block:: python

    value = cache.store('redis').get('foo')

    cache.store('memcached').put('foo', 'bar', 10)

.. note::

    If you do not specify a store the default store will be used.

    .. code-block:: python

        value = cache.get('foo')


Retrieving Items From The Cache
===============================

The ``get`` method is used to retrieve items from the cache.
If the item does not exist in the cache, ``None`` will be returned.
If you wish, you can pass a second argument to the ``get`` method specifying the custom default value
you wish to be returned if the item doesn't exist:

.. code-block:: python

    value = cache.get('foo')

    value = cache.get('foo', 'default')

You may even pass a function as the default value.
The result of the function will be returned if the specified item does not exist in the cache.
Passing a function allows you to defer the retrieval of default values from a database or other external service:

.. code-block:: python

    value = cache.get('foo', lambda: db.table('users').get())

Checking For Item Existence
---------------------------

The ``has`` method may be used to determine if an item exists in the cache:

.. code-block:: python

    if cache.has('foo'):
        # ...

Incrementing / Decrementing Values
----------------------------------

The ``increment`` and ``decrement`` methods can be used to adjust the value of integer items in the cache.
Both of these methods optionally accept a second argument indicating the amount
by which to increment or decrement the item's value:

.. code-block:: python

    cache.increment('key')

    cache.increment('key', 3)

    cache.decrement('key')

    cache.decrement('key', 3)

Retrieve or Update
------------------

Sometimes you may wish to retrieve an item from the cache,
but also store a default value if the requested item doesn't exist.
For example, you may wish to retrieve all users from the cache or, if they don't exist,
retrieve them from the database and add them to the cache.
You may do this using the ``remember`` method:

.. code-block:: python

    value = cache.remember('users', 10, lambda: db.table('users').get())

If the item does not exist in the cache,
the function passed to the remember method will be executed and its result will be placed in the cache.

You may also combine the ``remember`` and ``forever`` methods:

.. code-block:: python

    value = cache.remember_forever('users', 10, lambda: db.table('users').get())

.. note::

    Using the ``remember`` method might not be the most practical in some cases,
    that's why you can use the ``CacheManager`` instance like a decorator.

    See :ref:`UsingDecorators`.

Retrieve and Delete
-------------------

If you need to retrieve an item from the cache and then delete it,
you can use the ``pull`` method.
Like the ``get`` method, ``None`` will be returned if the item does not exist in the cache:

.. code-block:: python

    value = cache.pull('key')


Storing Items In The Cache
==========================

You can use the ``put`` method to store items in the cache.
When you place an item in the cache, you will need to specify the number of minutes
for which the value should be cached:

.. code-block:: python

    cache.put('key', 'value', 10)

Instead of passing the number of minutes until the item expires,
you can also pass a ``datetime`` instance representing the expiration time of the cached item:

.. code-block:: python

    expires_at = datetime.now() + timedelta(minutes=10)

    cache.put('key', 'value', expires_at)

The ``add`` method will only add the item to the cache if it does not already exist in the cache store.
The method will return ``True`` if the item is actually added to the cache.
Otherwise, the method will return ``False``:

.. code-block:: python

    cache.add('key', 'value', 10)

The ``forever`` method can be used to store an item in the cache permanently.
These values must be manually removed from the cache using the ``forget`` method:

.. code-block:: python

    cache.forever('key', 'value')


Removing Items From The Cache
=============================

You can remove items from the cache using the ``forget``:

.. code-block:: python

    cache.forget('key')


.. _UsingDecorators:

Using Decorators
================

Instead of using the ``remember`` method, which might not be suitable for functions
with complex logic, you can use the ``CacheManager`` instance as a decorator:

.. code-block:: python

    @cache
    def get_users():
        return db.table('users').get()

This will store the result of the function for the default time of 60 minutes.
The key will automatically be generated based on the function name, its arguments and keyword arguments.

You can also specify a key and the number of minutes the result will be stored in the cache:

.. code-block:: python

    @cache(key='key', minutes=30)
    def get_users():
        return db.table('users').get()

.. warning::

    The ``key`` keyword will only serve as a prefix for the automatically generated key.
    The final cache key will still depend on the arguments and keyword arguments.

You can also specify a store when using the cache manager as a decorator:

.. code-block:: python

    @cache('redis', key='key', minutes=30)
    def get_users():
        return db.table('users').get()
