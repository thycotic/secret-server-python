# -*- coding: utf-8 -*-

from secret_server.config import Config
from secret_server.commands import AccessToken
from secret_server.commands import Secret

class SDK_Client:
    __singleton = None

    def __new__(cls, *args, **kwargs):
        if not cls.__singleton:
            cls.__singleton = object.__new__(SDK_Client)
        return cls.__singleton

    def __init__(self):
        #self.commands = Commands()
        self.token = AccessToken.get_token

    @classmethod
    def configure(cls, **kwargs):
        if kwargs:
            Config.BASE_URL = kwargs['url']
            Config.CLIENT_CONFIG['ruleName'] = kwargs['rule']
            Config.CLIENT_CONFIG['onboardingKey'] = kwargs['key']

        Config.register_client()
        return "Client Registered Successfully"
    
    @classmethod
    def remove(cls):
        Config.remove_client()
    
    @classmethod
    def token(cls):
        
