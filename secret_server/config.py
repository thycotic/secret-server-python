# -*- coding: utf-8 -*-

import requests
import json
import platform
import os
from uuid import uuid4


class Config:
    CLIENT_CONFIG = {
        'clientId' : uuid4(),
        'description' : 'Machine: {node}, OS: {system} - Python {version}'.format(node = platform.node(), system = platform.system(), version = platform._sys_version()[1]),
        'name' : platform.node(),
        'ruleName' : '' or os.environ.get('RULE_NAME'),
        'onboardingKey' : '' or os.environ.get('RULE_KEY')
    }   
    BASE_URL = '' or os.environ.get('SECRET_SERVER_BASE_URL')
    
    @classmethod
    def register_client(cls):
        if not os.path.exists("creds.json"):
            resp = requests.post(cls.BASE_URL+"/api/v1/sdk-client-accounts", data = cls.CLIENT_CONFIG)

            creds = {
                "client_id" : "sdk-client-"+resp.json()["clientId"],
                "client_secret" : resp.json()["clientSecret"],
                "grant_type" : "client_credentials"
                }
            with open("creds.json", "w") as outfile:
                json.dump(creds, outfile)

            config = {
                "id" : resp.json()["id"]
            }
            with open("client_info.json", "w") as outfile:
                json.dump(config, outfile)

            resp.close()
            print("Client Registered")
        else:
            print("client already registered")
    
    @classmethod
    def remove_client(cls):
        if os.path.exists("creds.json"):
            os.remove("creds.json")
            json.load()
        else:
            print("Client already unregistered")