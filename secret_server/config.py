# -*- coding: utf-8 -*-
import requests
import json
import platform
import os

from uuid import uuid4
from secret_server.data_protection import DataProtection


class Config:
    CLIENT_CONFIG = {
        'clientId' : uuid4(),
        'description' : 'Machine: {node}, OS: {system} - Python {version}'.format(node = platform.node(), system = platform.system(), version = platform._sys_version()[1]),
        'name' : platform.node(),
        'ruleName' : '' or os.environ.get('RULE_NAME'),
        'onboardingKey' : '' or os.environ.get('RULE_KEY')
    }   
    BASE_URL = '' or os.environ.get('SECRET_SERVER_BASE_URL')

    CREDS_PATH = "creds.json"
    CLIENT_PATH = "client_info.json"

    __encrypt = DataProtection().encrypt
    __decrypt = DataProtection().decrypt

    @classmethod
    def register_client(cls):
        if not os.path.exists(cls.CREDS_PATH):
            resp = requests.post(cls.BASE_URL+"/api/v1/sdk-client-accounts", data = cls.CLIENT_CONFIG, verify=False)
            try:
                creds = {
                    "client_id" : "sdk-client-"+resp.json()["clientId"],
                    "client_secret" : resp.json()["clientSecret"],
                    "grant_type" : "client_credentials"
                }
                open(cls.CREDS_PATH , "w").write(cls.__encrypt(creds))
                creds = None
            except IOError as e:
                raise IOError("Couldn't Save credentials: ", e)

            try:
                config = {
                    "id" : resp.json()["id"],
                    "endpoint" : cls.BASE_URL
                }
                open(cls.CLIENT_PATH , "w").write(cls.__encrypt(config))
                config = None
                cls.BASE_URL = cls.__decrypt(cls.CLIENT_PATH)["endpoint"]
            except IOError as e:
                raise IOError("Couldn't Save client info: ", e)

            resp.close()
            print("Client Registered")
        else:
            print("client already registered")
    
    @classmethod
    def remove_client(cls, revoke):
        if os.path.exists(cls.CLIENT_PATH):
            if revoke:
                import secret_server.commands as commands
                token = commands.AccessToken.get_token()

                client_id = cls.__decrypt(cls.CLIENT_PATH)["id"]
                
                resp = requests.post("{base_url}/api/v1/sdk-client-accounts/{id}/revoke".format(base_url=cls.BASE_URL,id=client_id), headers={"Authorization" : "bearer {token}".format(token=token)},verify=False)
                if resp.status_code is 200:
                    print("Client unregistered")
                    os.remove(cls.CLIENT_PATH)
                    os.remove(cls.CREDS_PATH)
                else:
                    print(resp.json()["body"])
                resp.close()
            else:
                os.remove(cls.CLIENT_PATH)
                os.remove(cls.CREDS_PATH)
        else:
            print("Client already unregistered")