import requests
import json
import platform
import os
from uuid import uuid4

class Configure:
    CLIENT_CONFIG = {
        'clientId' : uuid4(),
        'description' : 'Machine: {node}, OS: {system} - Python {version}'.format(node = platform.node(), system = platform.system(), version = platform._sys_version()[1]),
        'name' : platform.node(),
        'ruleName' : 'SDKTEST',
        'onboardingKey' : '7qH8edS+GO9LWJ2MwmxWV4F3er86L4a7/UmMEoCRWzg='
    }   
    BASE_URL = 'http://vault'

    @classmethod
    def register_client(cls):
        request = requests.post(cls.BASE_URL+"/api/v1/sdk-client-accounts", data=cls.CLIENT_CONFIG)

        with open('creds.json', 'w') as outfile:
            json.dump(request.json(), outfile)
    
        request.close()
    
    @classmethod
    def set_config_from_env(cls):
        cls.BASE_URL = os.environ.get('SECRET_SERVER_BASE_URL')
        cls.CLIENT_CONFIG['ruleName'] = os.environ.get('RULE_NAME')
        cls.CLIENT_CONFIG['onboardingKey'] = os.environ.get('RULE_KEY')