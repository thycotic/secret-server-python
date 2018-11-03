# -*- coding: utf-8 -*-
from secret_server.config import Config

class CacheClient:
    def __init__(self):


# @property
# def cache_settings(self):
#     settings = {
#         "Minutes": self.minutes,
#         "Strategy": self.strategy
#     }
#     return settings
#
#
#     def enum(*args):
#         enums = dict(zip(args, range(len(args))))
#         return type('Enum', (), enums)
#
#     self.cache_strategy = enum("Never", "ServerThenCache", "CacheThenServer", "CacheThenServerAllowExpired")
#     self.minutes = 0
#     self.strategy = self.cache_strategy