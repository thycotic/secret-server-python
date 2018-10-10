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
    __creds_path = "creds.json"
    __client_path = "client_info.json"

    @classmethod
    def register_client(cls):
        if not os.path.exists(cls.__creds_path):
            resp = requests.post(cls.BASE_URL+"/api/v1/sdk-client-accounts", data = cls.CLIENT_CONFIG)

            creds = {
                "client_id" : "sdk-client-"+resp.json()["clientId"],
                "client_secret" : resp.json()["clientSecret"],
                "grant_type" : "client_credentials"
                }
            with open(cls.__creds_path, "w") as outfile:
                json.dump(creds, outfile)

            config = {
                "id" : resp.json()["id"]
            }
            with open(cls.__client_path, "w") as outfile:
                json.dump(config, outfile)

            resp.close()
            print("Client Registered")
        else:
            print("client already registered")
    
    @classmethod
    def remove_client(cls):
        if os.path.exists(cls.__client_path):
            ### I initially had this in here, but realized it requires certain permissions and requires some code change to implement it without 
            ### relying on the config class for initialization. We need to think about how to better implement it

            # import secret_server.commands as commands
            # token = commands.AccessToken.get_token()

            # with open(cls.__client_path) as outfile:
            #     client_id = json.load(outfile)["id"]
            
            # resp = requests.post("{base_url}/api/v1/sdk-client-accounts/{id}/revoke".format(base_url=cls.BASE_URL,id=client_id), headers={"Authorization" : "bearer {token}".format(token=token)})
            # if resp.status_code is 200:
            #     print("Client unregistered")
            #     os.remove(cls.__client_path)
            #     os.remove(cls.__creds_path)
            # resp.close()
            os.remove(cls.__client_path)
            os.remove(cls.__creds_path)
        else:
            print("Client already unregistered")