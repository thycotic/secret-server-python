# -*- coding: utf-8 -*-

from subprocess import Popen, PIPE

from secret_server.config import Config
#from secret_server.sdk_client import SDK_Client

class Commands:
    @classmethod
    def execute(cls, args):
        if Config.has_valid_path():
            p = Popen(' '.join((Config.get_sdk_file_path(),) + args), shell=True, stdout=PIPE, stderr=PIPE)
            stdout, stderr = p.communicate()
            statuscode = p.returncode

            if(statuscode != 0):
                raise ValueError(stdout.decode('utf-8') + " Thycotic SDK configuration is invalid.")
        else:
            raise ValueError('SDK client path is invalid')

        return [stdout.decode('utf-8'), stderr, statuscode]

    @classmethod
    def initialize(cls):
        if Config.SDK_CONFIG['url'] is None:
            raise ValueError('Secret Server URL is not set')

        command = (' -e ', ' -u ', Config.SDK_CONFIG['url'])

        if Config.SDK_CONFIG['rule']:
            command += (' -r ', Config.SDK_CONFIG['rule'])

        if Config.SDK_CONFIG['key']:
            command += (' -k ', Config.SDK_CONFIG['key'])

        return cls.execute(('init',) + command)[0]

    @classmethod
    def get_secret(cls, id, **kwargs):
        if not isinstance(id, int) or id <= 0 :
            raise ValueError('id must be a positive integer')

        command = ('secret -s ', id.__str__())

        if 'field' in kwargs.keys():
            command += (' -ad ',) if(kwargs['field'] == 'all') else (' -f ', kwargs['field'])

        result = cls.execute(command)

        return result[0]

    @classmethod
    def set_cache(cls):
        command = None
        if(Config.has_valid_cache()):
            command = (' cache -s ', Config.SDK_CONFIG['cache_strategy'].__str__())

            if Config.SDK_CONFIG['cache_age'] is not None:
                command += (' -a ', Config.SDK_CONFIG['cache_age'].__str__())
        return cls.execute(command)[0]

    @classmethod
    def clear_cache(cls):
        return cls.execute(('cache', '-b'))[0]

    @classmethod
    def remove(cls):
        return cls.execute(('remove', '-c'))[0]