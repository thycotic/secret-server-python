# -*- coding: utf-8 -*-
import requests
import json

from os import (environ, path, remove)
from platform import (system, _sys_version, node)
from uuid import uuid4
from secret_server.DataProtection import DataProtection


class Config:
    # def __init__(self):

    # These are the arguments required to create a client in Secret Server
    CLIENT_CONFIG = {
        "clientId": uuid4(),
        "description": "Machine: {node}, OS: {system} - Python {version}".format(node=node(), system=system(), version=_sys_version()[1]),
        "name": node(),
        "ruleName": '' or environ.get("SECRET_SERVER_RULE_NAME"),
        "onboardingKey": '' or environ.get("SECRET_SERVER_RULE_KEY")
    }

    BASE_URL = '' or str(environ.get("SECRET_SERVER_BASE_URL")).rstrip("/")

    CREDS_PATH = "creds.json"
    CLIENT_PATH = "client_info.json"
    API_VERSION = "v1"
    SSL_VERIFY = False

    __encrypt = DataProtection().encrypt
    __decrypt = DataProtection().decrypt

    @classmethod
    def register_client(cls):
        if not path.exists(cls.CREDS_PATH):
            resp = requests.post(cls.BASE_URL+"/api/v1/sdk-client-accounts", data=cls.CLIENT_CONFIG, verify=False)
            # The SDK accounts support client credentials grant type. We generate the clientID in our Python client
            # and Secret Server generates the ClientSecret
            creds = {
                "client_id": "sdk-client-"+resp.json()["clientId"],
                "client_secret": resp.json()["clientSecret"],
                "grant_type": "client_credentials"
            }
            # In order to easily consume the credentials by the requests package, we use
            # json.dumps before we encrypt the data
            creds = cls.__encrypt(json.dumps(creds))
            try:
                open(cls.CREDS_PATH, "w").write(creds)
            except IOError as e:
                raise IOError("Couldn't Save credentials: ", e)

            config = {
                "id": resp.json()["id"],
                "endpoint": cls.BASE_URL
            }
            config = cls.__encrypt(json.dumps(config))
            try:
                open(cls.CLIENT_PATH, "w").write(config)
            except IOError as e:
                raise IOError("Couldn't Save client info: ", e)

            resp.close()
            print("Client Registered")
        else:
            print("client already registered")

    @classmethod
    def load_endpoint(cls):
        if path.isfile(cls.CLIENT_PATH):
            cls.endpoint = json.loads(cls.__decrypt(cls.CLIENT_PATH))["endpoint"]
        else:
            cls.endpoint = cls.BASE_URL
        return str(cls.endpoint)

    @classmethod
    def load_credentials(cls):
        if path.isfile(cls.CREDS_PATH):
            cls.creds = json.loads(cls.__decrypt(cls.CREDS_PATH))
        return cls.creds

    @classmethod
    def remove_client(cls, revoke):
        # This method removes the client configuration from disk. There is an optional revoke param which removes the
        # client from secret server as well

        if revoke:
            from secret_server.commands import get_token
            token = get_token()
            client_id = json.loads(cls.__decrypt(cls.CLIENT_PATH))["id"]
            base_url = cls.load_endpoint()
            resp = requests.post(
                "{}/api/v1/sdk-client-accounts/{}/revoke".format(base_url, client_id),
                headers={"Authorization": "bearer {token}".format(token=token)},
                verify=False
            )

            if resp.status_code is not 200:
                print(resp.json()["body"])

            resp.close()
        if path.isfile(cls.CLIENT_PATH):
            remove(cls.CLIENT_PATH)
        cls.endpoint = None
        if path.isfile(cls.CREDS_PATH):
            remove(cls.CREDS_PATH)
        cls.creds = None
        DataProtection.remove_master_key()


