# -*- coding: utf-8 -*-

from secret_server.config import Config
from secret_server.configure import Configure
from secret_server.commands import Commands

class SDK_Client:
    singleton = None

    def __new__(cls, *args, **kwargs):
        if not cls.singleton:
            cls.singleton = object.__new__(SDK_Client)
        return cls.singleton

    def __init__(self):
        self.config = Config()
        self.commands = Commands()

    @classmethod
    def configure(cls, path, url, rule, key):
        Config.SDK_CONFIG['path'] = path
        Config.SDK_CONFIG['url'] = url
        Config.SDK_CONFIG['rule'] = rule
        Config.SDK_CONFIG['key'] = key

    @classmethod
    def configure_from_env(cls):
        Config.set_config_from_env()

    @classmethod
    def set_cache(cls, cache_strategy, cache_age = 0):
        Config.SDK_CONFIG['cache_strategy'] = cache_strategy
        Config.SDK_CONFIG['cache_age'] = cache_age
        return Commands.set_cache()