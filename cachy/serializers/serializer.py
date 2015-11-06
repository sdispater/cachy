# -*- coding: utf-8 -*-


class Serializer(object):
    """
    Abstract serializer.
    """

    def serialize(self, data):
        """
        Serialize data.

        :param data: The data to serialize
        :type data: mixed

        :rtype: str
        """
        raise NotImplementedError()

    def unserialize(self, data):
        """
        Unserialize data.

        :param data: The data to unserialize
        :type data: mixed

        :rtype: str
        """
        raise NotImplementedError()
