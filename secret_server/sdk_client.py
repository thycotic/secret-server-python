# -*- coding: utf-8 -*-

from secret_server.config import Config
#from secret_server.commands import Commands

class SDK_Client:
    singleton = None

    def __new__(cls, *args, **kwargs):
        if not cls.singleton:
            cls.singleton = object.__new__(SDK_Client)
        return cls.singleton

    def __init__(self):
        self.config = Config()
        #self.commands = Commands()

    @classmethod
    def init(cls, **kwargs):
        if kwargs:
            Config.BASE_URL = kwargs['url']
            Config.CLIENT_CONFIG['ruleName'] = kwargs['rule']
            Config.CLIENT_CONFIG['onboardingKey'] = kwargs['key']

        Config.register_client()
        return "Client Registered Successfully"
    
    @classmethod
    def remove(cls):
        Config.remove_client()