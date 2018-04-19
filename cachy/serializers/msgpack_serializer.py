# -*- coding: utf-8 -*-

try:
    import msgpack
except ImportError:
    msgpack = None

from .serializer import Serializer


class MsgPackSerializer(Serializer):
    """
    Serializer that uses `msgpack <https://pypi.python.org/pypi/msgpack-python/>`_ representations.

    By default, this serializer does not support serializing custom objects.
    """

    def serialize(self, data):
        """
        Serialize data.

        :param data: The data to serialize
        :type data: mixed

        :rtype: str
        """
        return msgpack.packb(data, use_bin_type=True)

    def unserialize(self, data):
        """
        Unserialize data.

        :param data: The data to unserialize
        :type data: mixed

        :rtype: str
        """
        return msgpack.unpackb(data, encoding='utf-8')
