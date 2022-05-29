# -*- coding: utf-8 -*-

from functools import partial

from .serializer import Serializer

try:
    import cPickle as pickle  # noqa: N813
except ImportError:
    import pickle

# Serialize pickle dumps using the highest pickle protocol (binary, default
# uses ascii)
dumps = partial(pickle.dumps, protocol=pickle.HIGHEST_PROTOCOL)
loads = pickle.loads


class PickleSerializer(Serializer):
    """
    Serializer that uses the pickle module.
    """

    def serialize(self, data):
        """
        Serialize data.

        :param data: The data to serialize
        :type data: mixed

        :rtype: str
        """
        return dumps(data)

    def unserialize(self, data):
        """
        Unserialize data.

        :param data: The data to unserialize
        :type data: mixed

        :rtype: str
        """
        return loads(data)
