# -*- coding: utf-8 -*-

import os
class Config:
    SDK_CONFIG = {
        'path' : '',
        'url' : '',
        'rule' : '',
        'key' : '',
        'cache_strategy' : 0,
        'cache_age' : 0
    }

    @classmethod
    def get_sdk_file_path(cls):
        sdk_file = os.path.join(cls.SDK_CONFIG['path'], 'tss')
        return os.path.join(cls.SDK_CONFIG['path'], 'tss.exe') if(not os.path.isfile(sdk_file)) else sdk_file

    @classmethod
    def get_strategy(cls):
        strat_dict = ['Never Cache', 'Server Then Cache', 'Cache Then Server', 'Cache Then Server Fallback on Expired Cache']

        if (not isinstance(cls.SDK_CONFIG['cache_strategy'], int) or cls.SDK_CONFIG['cache_strategy'] < 0
                or cls.SDK_CONFIG['cache_strategy'] >= strat_dict.__len__()):
            raise ValueError('Invalid cache strategy. Please look at SDK manual for cache settings information.')

        return strat_dict[cls.SDK_CONFIG['cache_strategy']]

    @classmethod
    def has_valid_path(cls):
        return os.path.isfile(cls.get_sdk_file_path())

    @classmethod
    def has_valid_cache(cls):
        cls.get_strategy()
        if (not isinstance(cls.SDK_CONFIG['cache_age'], int) or
                (cls.SDK_CONFIG['cache_strategy'] > 0 and cls.SDK_CONFIG['cache_age'] <= 0)):
            raise ValueError('Cache age must be a positive integer when trying to set cache')
        return True

    @classmethod
    def set_config_from_env(cls):
        cls.SDK_CONFIG['path'] = os.environ.get('SDK_CLIENT_PATH')
        cls.SDK_CONFIG['url'] = os.environ.get('SECRET_SERVER_URL')
        cls.SDK_CONFIG['rule'] = os.environ.get('SDK_CLIENT_RULE')
        cls.SDK_CONFIG['key'] = os.environ.get('SDK_CLIENT_KEY')