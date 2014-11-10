from abc import ABCMeta, abstractmethod


class Engine:

    '''
    Base class for commands to run specific to their engines.
    '''
    __metaclass__ = ABCMeta

    @abstractmethod
    def execute(self, policy_dict, device_id, device_udid, *args, **kwargs):
        pass
