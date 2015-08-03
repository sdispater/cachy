# -*- coding: utf-8 -*-

try:
    import msgpack
except ImportError:
    msgpack = None

from .serializer import Serializer


class MsgPackSerializer(Serializer):
    """
    Serializer that uses msgpack representations.
    """

    def serialize(self, data):
        """
        Serialize data.

        :param data: The data to serialize
        :type data: mixed

        :rtype: str
        """
        return msgpack.packb(data)

    def unserialize(self, data):
        """
        Unserialize data.

        :param data: The data to unserialize
        :type data: mixed

        :rtype: str
        """
        return msgpack.unpackb(data)
